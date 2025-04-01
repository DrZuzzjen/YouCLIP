import streamlit as st
import subprocess
import os

def format_time(seconds):
    """Format seconds to HH:MM:SS or MM:SS."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes):02d}:{int(seconds):02d}"

def format_ffmpeg_time(seconds):
    """Format seconds to HH:MM:SS for FFmpeg."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def clip_video(input_path, output_path, start_time, end_time, format_type, quality):
    """Clip a video using FFmpeg."""
    try:
        # Validate that input file exists
        if not os.path.exists(input_path):
            st.error(f"Input file does not exist: {input_path}")
            return False
            
        # Log paths for debugging
        st.write(f"Input path: {input_path}")
        st.write(f"Output path: {output_path}")
            
        # Quality settings with fixed even dimensions
        quality_settings = {
            "High": {"video_bitrate": "2M", "audio_bitrate": "192k", "scale": "720"},  # Will force height to 720
            "Medium": {"video_bitrate": "1M", "audio_bitrate": "128k", "scale": "480"},  # Will force height to 480
            "Low": {"video_bitrate": "500k", "audio_bitrate": "96k", "scale": "360"}   # Will force height to 360
        }
        
        # Format settings
        format_settings = {
            "MP4": {"format": "mp4", "vcodec": "libx264", "acodec": "aac"},
            "WebM": {"format": "webm", "vcodec": "libvpx-vp9", "acodec": "libopus"},
            "MKV": {"format": "matroska", "vcodec": "libx264", "acodec": "aac"}
        }
        
        q_settings = quality_settings[quality]
        f_settings = format_settings[format_type]
        
        # Create a scale filter that ensures both dimensions are even
        # Use 'scale' as height and calculate width to maintain aspect ratio,
        # then use the 'scale=trunc(iw/2)*2:trunc(ih/2)*2' filter to ensure even dimensions
        scale_filter = f"scale=-2:{q_settings['scale']},scale=trunc(iw/2)*2:trunc(ih/2)*2"
        
        # Construct ffmpeg command with the modified scale filter
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-ss", start_time,
            "-to", end_time,
            "-vf", scale_filter,
            "-b:v", q_settings["video_bitrate"],
            "-b:a", q_settings["audio_bitrate"],
            "-c:v", f_settings["vcodec"],
            "-c:a", f_settings["acodec"],
            "-f", f_settings["format"],
            "-movflags", "+faststart",  # For better streaming compatibility
            output_path
        ]
        
        # Log the command for debugging
        st.write(f"FFmpeg command: {' '.join(cmd)}")
        
        # Execute command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                  text=True, errors='replace')
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            st.error(f"Error clipping video: {stderr}")
            return False
        
        # Verify output file was created
        if not os.path.exists(output_path):
            st.error("Output file was not created")
            return False
            
        st.success(f"Output file created: {output_path}")
        return True
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")
        return False