import os
import tempfile
import hashlib
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from .gerber2png import Gerber2Png
import uvicorn

# Storage base directory
STORAGE_BASE_DIR = os.environ.get("STORAGE_DIR", "storage")
gerber2png = Gerber2Png(storage_dir=STORAGE_BASE_DIR)

PORT = os.getenv("PORT", 8000)
if not os.path.exists(STORAGE_BASE_DIR):
    os.makedirs(STORAGE_BASE_DIR)

def generate_filename(content: bytes) -> str:
    """
    Generates a filename based on the date, time, and content hash
    """
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    content_hash = hashlib.md5(content).hexdigest()[:8]
    
    # Create a directory for the current date if it doesn't exist
    date_dir = os.path.join(gerber2png.storage_dir, date_str)
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    
    return os.path.join(date_dir, f"{date_str}_{time_str}_{content_hash}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/convert")
async def convert_gerber(
    printer_id: str = Form(0),
    gerber_file: UploadFile = File(...),
    drill_file: UploadFile = File(...),
    flip_horizontal: bool = Form(False),
    flip_vertical: bool = Form(False)
):
    """
    Convert Gerber to PNG
    """
    try:
        # Read file contents
        gerber_content = await gerber_file.read()
        drill_content = await drill_file.read()
        
        # Generate base filename
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        content_hash = hashlib.md5(gerber_content + drill_content).hexdigest()[:8]
        
        # Create a directory for the current date if it doesn't exist
        date_dir = os.path.join(gerber2png.storage_dir, date_str)
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)
        
        # Save original files
        base_filename = os.path.join(date_dir, f"{date_str}_{time_str}_{content_hash}")
        gerber_save_path = f"{base_filename}.gbr"
        drill_save_path = f"{base_filename}.drl"
        with open(gerber_save_path, 'wb') as f:
            f.write(gerber_content)
        with open(drill_save_path, 'wb') as f:
            f.write(drill_content)

        # Convert to PNG using temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_output:
            output_file = temp_output.name
            
        gerber2png.logger.debug(f"Printer ID: {printer_id}")
        gerber2png.logger.debug(f"Gerber file: {gerber_save_path}")
        gerber2png.logger.debug(f"Drill file: {drill_save_path}")
        gerber2png.logger.debug(f"Output file: {output_file}")
        gerber2png.logger.debug(f"Flip horizontal: {flip_horizontal}")
        gerber2png.logger.debug(f"Flip vertical: {flip_vertical}")
        gerber2png.convert(
            printer_id=printer_id,
            gerber_file=gerber_save_path,
            drill_file=drill_save_path,
            output_file=output_file,
            flip_horizontal=flip_horizontal,
            flip_vertical=flip_vertical
        )
        
        if not os.path.exists(output_file):
            gerber2png.logger.error(f"Output file does not exist: {output_file}")
            return JSONResponse(
                content={"error": "Output file does not exist"},
                status_code=500
            )
        
        with open(output_file, 'rb') as f:
            png_content = f.read()
        
        # Delete only temporary PNG file
        os.unlink(output_file)

        return Response(
            content=png_content,
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=converted.png"
            }
        )
    except Exception as e:
        gerber2png.logger.error(f"Error during conversion: {str(e)}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/api/printers")
async def get_printers():
    """
    Get a list of available printers
    """
    return gerber2png.get_printers()

def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()