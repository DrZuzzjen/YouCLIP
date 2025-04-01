# YouClip - YouTube Video Clipper

YouClip is a beautiful Streamlit application that allows users to create custom clips from YouTube videos. With YouClip, you can easily select a portion of any YouTube video, customize its format and quality, and download it for personal use.

## Features

- **YouTube Video Processing**: Input any YouTube URL and get instant video information
- **Custom Clipping**: Set precise start and end times for your clips
- **Multiple Formats**: Choose from MP4, WebM, and MKV formats
- **Quality Options**: Select from Low (360p), Medium (480p), or High (720p) quality
- **Beautiful UI**: Enjoy a modern, intuitive interface with smooth animations
- **Instant Preview**: Preview your clip before downloading (for clips under 50MB)
- **Fast Processing**: Efficient backend for quick video processing
- **Multiple Download Methods**: Fallback methods if primary method fails

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg installed on your system

### Setup 

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youclip.git
   cd youclip
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Make sure FFmpeg is installed:
   - For Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - For macOS: `brew install ffmpeg`
   - For Ubuntu/Debian: `sudo apt install ffmpeg`

### Running the App

Start the Streamlit app:
```
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Project Structure

- `app.py`: Main Streamlit application
- `youtube_utils.py`: YouTube video fetching and downloading utilities
- `ffmpeg_utils.py`: Video clipping and format conversion
- `ui_components.py`: UI styling and components
- `requirements.txt`: Required Python packages

## Usage

1. Enter a valid YouTube video URL in the input field
2. The video information will be displayed with a thumbnail
3. Set the start and end times for your clip using the minute/second inputs
4. Select your preferred video format (MP4, WebM, or MKV)
5. Choose the quality level (Low, Medium, High)
6. Click "Generate Clip" to process your video
7. Once processing is complete, download your clip using the provided button

## Troubleshooting

- If you encounter a "HTTP Error 403: Forbidden" message, the app will automatically try an alternative download method
- If FFmpeg shows errors about dimensions, the app uses special scaling to ensure compatibility
- For very long videos, it's recommended to create shorter clips (under 5 minutes) for better performance

## Legal Disclaimer

This tool is intended for personal use only. Always respect copyright laws and YouTube's Terms of Service when using this application.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.