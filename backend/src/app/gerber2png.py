#!/usr/bin/env python
"""
gerber2png.py

The script is designed to convert Gerber files from KiCad to PNG,
for further lighting of PCB on photopolymer printer.

Author: Sergey Poterianski
"""

import os
import sys
import json
import loguru
from decimal import Decimal
from pygerber.gerberx3.api.v2 import ColorScheme, GerberFile, PixelFormatEnum
from pygerber.common.rgba import RGBA
from PIL import Image, ImageDraw


class Gerber2Png:
    def __init__(self, storage_dir="storage"):
        self.logger = loguru.logger
        self.logger.remove()
        self.logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} {level}: {message}", 
                        level=os.getenv("LOG_LEVEL", "INFO"))
        self.printers = self.load_printers('printers.json')
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def load_printers(self, printers_filename):
        """
        Load printer parameters from a JSON file.
        """
        try:
            with open(printers_filename, 'r', encoding='utf-8') as f:
                printers = json.load(f)
            
            prn = {}
            for printer in printers:
                id = str(printer['id'])
                web_name = f"{printer['name']} res: {printer['resolution']['x']}x{printer['resolution']['y']} "
                web_name += f"size: {round(printer['size']['w'],2)}x{round(printer['size']['h'],2)}"
                prn[id] = {
                    'name': printer['name'],
                    'web_name': web_name,
                    'x': printer['resolution']['x'],
                    'y': printer['resolution']['y'],
                    'w': printer['size']['w'],
                    'h': printer['size']['h'],
                    'd_x': Decimal(printer['resolution']['x'] / printer['size']['w']),
                    'd_y': Decimal(printer['resolution']['y'] / printer['size']['h'])
                }
            return prn

        except FileNotFoundError:
            self.logger.error(f"File {printers_filename} not found.")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from {printers_filename}.")
            return None

    def get_printers(self):
        """
        Return list of available printers.
        """
        return self.printers
        
    def get_printer(self, printer_id):
        """
        Get printer parameters by ID.
        """
        return self.printers[str(printer_id)]

    def parse_drl_file(self, drl_file_path):
        """
        Parse a DRL file and extract hole coordinates and diameters.
        """
        holes = []
        tools = {}
        current_tool = None
        in_header = True

        with open(drl_file_path, 'r', encoding='utf-8') as drl_file:
            for line in drl_file:
                line = line.strip()
                if line.startswith('T') and 'C' in line and line[1].isdigit():
                    tool_id = line.split('C')[0]
                    diameter = Decimal(line.split('C')[1])
                    tools[tool_id] = diameter
                elif line == '%':
                    in_header = False
                elif not in_header:
                    if line.startswith('T'):
                        current_tool = line
                    elif line.startswith('X') and 'Y' in line:
                        x_str, y_str = line[1:].split('Y')
                        x = Decimal(x_str)
                        y = Decimal(y_str)
                        diameter = tools.get(current_tool, Decimal("0.5"))
                        holes.append((x, y, diameter))
        return holes

    def convert(self, printer_id, gerber_file, drill_file, output_file, flip_horizontal=False, flip_vertical=False):
        """
        Convert a Gerber file to PNG format and overlay drill holes from a DRL file.
        """
        self.logger.debug(f"Converting Gerber file to PNG for printer ID: {printer_id}")
        printer = self.get_printer(printer_id)
        self.logger.debug(f"Printer: {printer}")
        dpmm = 100
        bw = ColorScheme(
            background_color=RGBA.from_hex("#000000"),
            clear_color=RGBA.from_hex("#000000"),
            solid_color=RGBA.from_hex("#FFFFFF"),
            clear_region_color=RGBA.from_hex("#000000"),
            solid_region_color=RGBA.from_hex("#FFFFFF"),
        )

        self.logger.debug("Start conversion of Gerber file to PNG")
        self.logger.debug(f"Printer: {printer['name']}")

        # Parse Gerber file
        gb = GerberFile.from_file(gerber_file)
        parsed_file = gb.parse()
        board_info = parsed_file.get_info()

        board_min_x = float(board_info.min_x_mm)
        board_max_y = float(board_info.max_y_mm)

        # Render the Gerber file to PNG
        parsed_file.render_raster(
            output_file,
            dpmm=dpmm,
            color_scheme=bw,
            pixel_format=PixelFormatEnum.RGB
        )

        # Load the rendered PNG
        img = Image.open(output_file)
        draw = ImageDraw.Draw(img)

        # Parse the DRL file and draw holes
        holes = self.parse_drl_file(drill_file)

        for x, y, diameter in holes:
            x_px = int(float(x) * dpmm - board_min_x * dpmm)
            y_px = abs(int(float(y) * dpmm - board_max_y * dpmm))
            radius_px = int((float(diameter) / 2) * dpmm)

            draw.ellipse(
                [x_px - radius_px, y_px - radius_px, x_px + radius_px, y_px + radius_px],
                fill='black', outline='black'
            )

        # Scale the image to the required resolution
        w = int(parsed_file.get_info().width_mm * printer['d_x'])
        h = int(parsed_file.get_info().height_mm * printer['d_y'])

        if flip_horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if flip_vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_resized = img.resize((w, h), Image.Resampling.LANCZOS)

        img_resized.save(output_file)
        self.logger.debug(f"Done: image saved to: {output_file}")
        return True

