import pytest
from fastapi.testclient import TestClient
import os
from datetime import datetime
import json

def test_get_printers(test_client):
    response = test_client.get("/api/printers")
    assert response.status_code == 200
    printers = response.json()
    assert isinstance(printers, dict)
    assert len(printers) > 0
    # Проверяем структуру данных принтера
    for printer_id, printer_data in printers.items():
        assert isinstance(printer_id, str)
        assert all(key in printer_data for key in ['name', 'web_name', 'x', 'y', 'w', 'h', 'd_x', 'd_y'])

def test_convert_gerber_success(test_client, test_storage_dir, sample_gerber_file, sample_drill_file):
    # Подготавливаем файлы для отправки
    with open(sample_gerber_file, 'rb') as gerber, open(sample_drill_file, 'rb') as drill:
        files = {
            'gerber_file': ('test.gbr', gerber, 'application/octet-stream'),
            'drill_file': ('test.drl', drill, 'application/octet-stream')
        }
        data = {
            'printer_id': '0',
            'flip_horizontal': 'false',
            'flip_vertical': 'false'
        }
        response = test_client.post("/api/convert", files=files, data=data)
    
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
    assert len(response.content) > 0  # проверяем, что PNG не пустой
    
    # Проверяем, что файлы сохранены в storage
    today = datetime.now().strftime("%Y%m%d")
    storage_dir = os.path.join(test_storage_dir, today)
    print(f"\nTest storage directory: {test_storage_dir}")
    print(f"Storage directory for today: {storage_dir}")
    print(f"Current directory: {os.getcwd()}")
    assert os.path.exists(storage_dir)
    
    # Проверяем наличие файлов в директории
    files = os.listdir(storage_dir)
    print(f"Files in storage directory: {files}")
    assert len(files) == 2  # только .gbr и .drl файлы
    assert any(f.endswith('.gbr') for f in files)
    assert any(f.endswith('.drl') for f in files)

def test_convert_gerber_invalid_files(test_client, test_storage_dir):
    # Тест с пустыми файлами
    files = {
        'gerber_file': ('test.gbr', b'', 'application/octet-stream'),
        'drill_file': ('test.drl', b'', 'application/octet-stream')
    }
    data = {
        'printer_id': '0',
        'flip_horizontal': 'false',
        'flip_vertical': 'false'
    }
    response = test_client.post("/api/convert", files=files, data=data)
    
    assert response.status_code == 500
    assert 'error' in response.json()

def test_convert_gerber_missing_files(test_client):
    response = test_client.post("/api/convert", files={}, data={
        'printer_id': '0',
        'flip_horizontal': 'false',
        'flip_vertical': 'false'
    })
    assert response.status_code == 422  # Validation error

def test_convert_gerber_invalid_printer_id(test_client, sample_gerber_file, sample_drill_file):
    with open(sample_gerber_file, 'rb') as gerber, open(sample_drill_file, 'rb') as drill:
        files = {
            'gerber_file': ('test.gbr', gerber, 'application/octet-stream'),
            'drill_file': ('test.drl', drill, 'application/octet-stream')
        }
        data = {
            'printer_id': 'invalid_id',
            'flip_horizontal': 'false',
            'flip_vertical': 'false'
        }
        response = test_client.post("/api/convert", files=files, data=data)
    
    assert response.status_code == 500
    assert 'error' in response.json() 