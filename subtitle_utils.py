import streamlit as st
import os
import subprocess
import tempfile
import time
import json
from datetime import timedelta
import torch
from transformers import pipeline

# Initialize the transcription model at startup
@st.cache_resource
def load_whisper_model(language="en"):
    """Load the Whisper model using HuggingFace transformers."""
    try:
        # For faster inference on CPU, use tiny model
        model_name = "openai/whisper-tiny"
        
        # If CUDA is available, we can use a slightly larger model
        if torch.cuda.is_available():
            model_name = "openai/whisper-base"
            st.info("CUDA detected: Using whisper-base model")
        else:
            st.info("Using whisper-tiny model (CPU mode)")
        
        pipe = pipeline(
            "automatic-speech-recognition", 
            model=model_name,
            chunk_length_s=30,
            return_timestamps=True,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        return pipe
    except Exception as e:
        st.error(f"Error loading Whisper model: {str(e)}")
        return None

def extract_audio(video_path, output_dir):
    """Extract audio from a video file using FFmpeg."""
    try:
        # Create a filename for the audio file
        audio_filename = os.path.splitext(os.path.basename(video_path))[0] + ".wav"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # FFmpeg command to extract audio
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # PCM 16-bit LE format
            "-ar", "16000",  # 16kHz sampling rate (optimal for speech recognition)
            "-ac", "1",  # Mono channel
            audio_path
        ]
        
        # Execute command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True, errors='replace')
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            st.error(f"Error extracting audio: {stderr}")
            return None
        
        return audio_path
    except Exception as e:
        st.error(f"Error in audio extraction: {str(e)}")
        return None

def format_timestamp(seconds):
    """Format seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def create_srt_file(transcription, output_dir, base_filename):
    """Create an SRT subtitle file from transcription data."""
    try:
        # Use transcription chunks from Whisper
        chunks = transcription["chunks"] if "chunks" in transcription else []
        
        # If no chunks are available, try alternative format
        if not chunks and "segments" in transcription:
            chunks = transcription["segments"]
        
        # Last resort - format from simple texts with timestamps
        if not chunks and isinstance(transcription, list):
            chunks = transcription
        
        srt_filename = f"{base_filename}.srt"
        srt_path = os.path.join(output_dir, srt_filename)
        
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(chunks, 1):
                # Extract start and end times
                if isinstance(segment, dict) and "timestamp" in segment:
                    # Format for whisper transformers output
                    start_time = segment["timestamp"][0]
                    end_time = segment["timestamp"][1]
                    text = segment["text"]
                elif isinstance(segment, dict) and "start" in segment and "end" in segment:
                    # Format for custom segments
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]
                else:
                    # Default format as fallback
                    start_time = 0
                    end_time = 0
                    text = str(segment)
                
                # Write SRT entries
                f.write(f"{i}\n")
                f.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
                f.write(f"{text.strip()}\n\n")
        
        return srt_path
    except Exception as e:
        st.error(f"Error creating SRT file: {str(e)}")
        return None

def embed_subtitles(video_path, srt_path, output_dir, format_type):
    """Embed SRT subtitles into a video using FFmpeg."""
    try:
        # Create output filename
        output_filename = os.path.splitext(os.path.basename(video_path))[0] + "_subtitled." + format_type.lower()
        output_path = os.path.join(output_dir, output_filename)
        
        # Log paths for debugging
        st.info(f"Video path: {video_path}")
        st.info(f"SRT path: {srt_path}")
        st.info(f"Output path: {output_path}")
        
        # Write a temporary script file to handle path issues
        # This avoids problems with special characters in paths
        script_content = f"""
        file '{video_path.replace("'", "'\\''")}' 
        """
        script_path = os.path.join(output_dir, "subtitle_script.txt")
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Method 1: Try with different approach for Windows to handle the paths
        if os.name == 'nt':  # Windows
            # Use the hardburn approach
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"subtitles='{srt_path.replace('\\', '/').replace(':', '\\:')}'",
                "-c:a", "copy",
                output_path
            ]
        else:  # Linux/Mac
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=3'",
                "-c:a", "copy",
                output_path
            ]
        
        # Log command for debugging
        st.info(f"FFmpeg command: {' '.join(cmd)}")
        
        # Execute command
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True, errors='replace')
        stdout, stderr = process.communicate()
        
        # If the first method fails, try method 2 with temporary files
        if process.returncode != 0:
            st.warning("First embedding method failed, trying alternative approach...")
            
            # Create temporary files with simple names
            temp_video = os.path.join(output_dir, "temp_video.mp4")
            temp_srt = os.path.join(output_dir, "temp_subs.srt")
            temp_output = os.path.join(output_dir, "temp_output.mp4")
            
            # Copy the files to simpler names
            import shutil
            shutil.copy2(video_path, temp_video)
            shutil.copy2(srt_path, temp_srt)
            
            # Try the command with simple filenames
            cmd2 = [
                "ffmpeg", "-y",
                "-i", temp_video,
                "-vf", f"subtitles={temp_srt}",
                "-c:a", "copy",
                temp_output
            ]
            
            st.info(f"Trying alternative command: {' '.join(cmd2)}")
            
            process = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   text=True, errors='replace')
            stdout, stderr = process.communicate()
            
            # If successful, copy the output file back
            if process.returncode == 0 and os.path.exists(temp_output):
                shutil.copy2(temp_output, output_path)
            else:
                st.error(f"Alternative method also failed: {stderr}")
                return None
        
        # Verify the output file exists
        if not os.path.exists(output_path):
            st.error("Output subtitled video file was not created")
            return None
            
        return output_path
    except Exception as e:
        st.error(f"Error embedding subtitles: {str(e)}")
        return None

def transcribe_audio(audio_path, language="en"):
    """Transcribe audio using Whisper model."""
    try:
        # Load the model
        pipe = load_whisper_model(language)
        
        if not pipe:
            st.error("Failed to load transcription model. Using mock data instead.")
            # Return mock data as a fallback
            return mock_transcription(language)
        
        st.info("Transcribing audio with Whisper model...")
        
        # Set language-specific parameters
        task = "transcribe" 
        if language == "es":
            # For Spanish, be explicit about the language
            result = pipe(audio_path, generate_kwargs={"language": "es", "task": task})
        else:
            # For English, let the model detect
            result = pipe(audio_path, generate_kwargs={"task": task})
        
        # Process the result to get chunks with timestamps
        return process_whisper_result(result)
        
    except Exception as e:
        st.error(f"Error in transcription: {str(e)}")
        st.info("Using mock transcription data as fallback.")
        return mock_transcription(language)
        
def process_whisper_result(result):
    """Process the Whisper transcription output to get chunks with timestamps."""
    chunks = []
    
    # Check if the result has chunks with timestamps
    if "chunks" in result:
        return result
    
    # If we have timestamps format
    if "time_precision" in result and hasattr(result, "get") and result.get("timestamped_text"):
        for item in result["timestamped_text"]:
            chunks.append({
                "text": item["text"],
                "timestamp": [item.get("start", 0), item.get("end", 0)]
            })
        return {"chunks": chunks}
        
    # Convert from a raw text with timestamps
    if hasattr(result, "get") and result.get("text"):
        text = result["text"]
        chunks.append({
            "text": text,
            "timestamp": [0, 30]  # Default 30 seconds for the whole text
        })
        
    # If we have chunks format
    if isinstance(result, list) and len(result) > 0 and "timestamp" in result[0]:
        return {"chunks": result}
    
    # If we only have text, create a simple chunk
    if isinstance(result, str) or (hasattr(result, "get") and result.get("text")):
        text = result if isinstance(result, str) else result.get("text", "")
        chunks.append({
            "text": text,
            "timestamp": [0, 30]  # Default 30 seconds for the whole text
        })
        
    return {"chunks": chunks}

def mock_transcription(language="en"):
    """Create a mock transcription when the real model fails."""
    if language == "en":
        mock_chunks = [
            {"text": "This is a sample subtitle in English.", "timestamp": [0.0, 2.5]},
            {"text": "It will be replaced with actual transcription.", "timestamp": [3.0, 5.5]},
            {"text": "When the Whisper model is working correctly.", "timestamp": [6.0, 9.0]}
        ]
    else:  # Spanish
        mock_chunks = [
            {"text": "Este es un subtítulo de ejemplo en Español.", "timestamp": [0.0, 2.5]},
            {"text": "Será reemplazado con transcripción real.", "timestamp": [3.0, 5.5]},
            {"text": "Cuando el modelo Whisper esté funcionando correctamente.", "timestamp": [6.0, 9.0]}
        ]
    
    return {"chunks": mock_chunks}