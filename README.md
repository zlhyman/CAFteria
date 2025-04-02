# CAFteria ☕

A stylish, coffee-themed converter that transforms .caf (Core Audio Format) files into .mp3 format.

## Features

- Coffee-themed interface
- Drag-and-drop file upload
- Coffee cup loading animation
- Direct save to Downloads folder
- Preserves original file names (or tries - struggles a bit with Chinese characters)

## Prerequisites

- Python 3.6 or higher
- FFmpeg installed on your system

## Installation

1. Install FFmpeg:
   ```bash
   # On macOS
   brew install ffmpeg
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

1. Run the Flask app:
   ```bash
   python3 app.py
   ```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

3. Drag your .caf files into the interface or click to select them

4. Click "Convert to MP3"

5. Find your converted files in your Downloads folder!

## Development

Built with:
- Flask
- FFmpeg-python
- HTML5/CSS3
- Vanilla JavaScript

## License

MIT License 
