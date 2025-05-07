import os
import pytest
from fastapi.testclient import TestClient
import tempfile
import shutil
from datetime import datetime
from app.main import app, gerber2png

@pytest.fixture
def test_storage_dir():
    # Создаем временную директорию для тестов
    temp_dir = tempfile.mkdtemp()
    # Создаем директорию для текущей даты
    today = datetime.now().strftime("%Y%m%d")
    date_dir = os.path.join(temp_dir, today)
    os.makedirs(date_dir)
    # Сохраняем старую директорию
    old_storage_dir = gerber2png.storage_dir
    # Устанавливаем новую директорию
    gerber2png.storage_dir = temp_dir
    yield temp_dir
    # Восстанавливаем старую директорию
    gerber2png.storage_dir = old_storage_dir
    # Очищаем после тестов
    shutil.rmtree(temp_dir)

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def sample_gerber_file():
    content = """G04 Layer: BoardOutline*
G04 EasyEDA v6.5.34, 2023-03-19 14:30:22*
G04 Gerber Generator version 0.2*
G04 Scale: 100 percent, Rotated: No, Reflected: No *
G04 Dimensions in millimeters *
G04 leading zeros omitted , absolute positions ,3 integer and 3 decimal *
%FSLAX33Y33*%
%MOMM*%
%ADD10C,0.2540*%
D10*
X0Y0D02*
X100000Y0D01*
X100000Y100000D01*
X0Y100000D01*
X0Y0D01*
M02*"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.gbr', delete=False) as f:
        f.write(content)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def sample_drill_file():
    content = """M48
METRIC,TZ
T1C1.000
%
G90
G05
T1
X1000Y1000
X2000Y2000
T0
M30"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.drl', delete=False) as f:
        f.write(content)
    yield f.name
    os.unlink(f.name) 