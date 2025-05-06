# Gerber to PNG Converter

Web application for converting Gerber files to PNG format.

## Requirements

- Docker
- Docker Compose

## Installation and launch

1. Clone the repository:
```bash
git clone <repository-url>
cd gerber2png-online
```

2. Launch the application using Docker Compose:
```bash
docker-compose up --build
```

3. Open your browser and go to:
```
http://localhost:3000
```

## Usage

1. Upload Gerber file (.gbr)
2. Upload Drill file (.drl)
3. Select printer from the list
4. Click "Convert" button
5. Download the resulting PNG file

## Project structure

- `backend/` - Python FastAPI backend
- `frontend/` - React TypeScript frontend
- `docker-compose.yml` - Docker Compose configuration 