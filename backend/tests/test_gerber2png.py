import pytest
import os
from app.gerber2png import Gerber2Png
import tempfile

def test_gerber2png_initialization():
    g2p = Gerber2Png()
    assert g2p is not None
    assert hasattr(g2p, 'logger')
    assert hasattr(g2p, 'printers')
    assert len(g2p.printers) > 0

def test_get_printers():
    g2p = Gerber2Png()
    printers = g2p.get_printers()
    assert isinstance(printers, dict)
    assert len(printers) > 0
    # Проверяем структуру данных принтера
    for printer_id, printer_data in printers.items():
        assert isinstance(printer_id, str)
        assert all(key in printer_data for key in ['name', 'web_name', 'x', 'y', 'w', 'h', 'd_x', 'd_y'])

def test_convert_success(sample_gerber_file, sample_drill_file):
    g2p = Gerber2Png()
    
    # Создаем временный файл для выходного PNG
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_output:
        output_file = temp_output.name
    
    try:
        # Выполняем конвертацию
        result = g2p.convert(
            printer_id="0",
            gerber_file=sample_gerber_file,
            drill_file=sample_drill_file,
            output_file=output_file
        )
        
        # Проверяем результат
        assert result is True
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    finally:
        # Очищаем временный файл
        if os.path.exists(output_file):
            os.unlink(output_file)

def test_convert_invalid_printer_id(sample_gerber_file, sample_drill_file):
    g2p = Gerber2Png()
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_output:
        with pytest.raises(Exception):
            g2p.convert(
                printer_id="invalid_id",
                gerber_file=sample_gerber_file,
                drill_file=sample_drill_file,
                output_file=temp_output.name
            )

def test_convert_missing_files():
    g2p = Gerber2Png()
    with tempfile.NamedTemporaryFile(suffix='.png') as temp_output:
        with pytest.raises(FileNotFoundError):
            g2p.convert(
                printer_id="0",
                gerber_file="nonexistent.gbr",
                drill_file="nonexistent.drl",
                output_file=temp_output.name
            )

def test_convert_with_flipping(sample_gerber_file, sample_drill_file):
    g2p = Gerber2Png()
    
    # Тестируем различные комбинации отражений
    flip_combinations = [
        (True, False),
        (False, True),
        (True, True)
    ]
    
    for flip_h, flip_v in flip_combinations:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_output:
            output_file = temp_output.name
            
        try:
            result = g2p.convert(
                printer_id="0",
                gerber_file=sample_gerber_file,
                drill_file=sample_drill_file,
                output_file=output_file,
                flip_horizontal=flip_h,
                flip_vertical=flip_v
            )
            
            assert result is True
            assert os.path.exists(output_file)
            assert os.path.getsize(output_file) > 0
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file) 