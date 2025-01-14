import subprocess
import platform

rtmp_url = 'rtmp://a.rtmp.youtube.com/live2/77f4-a1uu-cgx3-0zbc-99cf'

os_type = platform.system()

if os_type != "Linux":
    raise EnvironmentError("This script is configured for Linux (Ubuntu).")

ffmpeg_command = [
    'ffmpeg',
    '-re',                                   # Read input at native frame rate
    '-f', 'pipewire',                        # Use PipeWire for screen capture on Wayland
    '-i', '0',                               # Default PipeWire source
    '-f', 'lavfi',
    '-i', 'anullsrc',                        # Add silent audio source
    '-c:v', 'libx264',                       # Video codec
    '-preset', 'veryfast',                   # Encoding preset
    '-b:v', '2500k',                         # Set video bitrate to 2500 Kbps
    '-maxrate', '2500k',                     # Max video bitrate
    '-bufsize', '5000k',                     # Buffer size for rate control
    '-pix_fmt', 'yuv420p',                   # Pixel format
    '-g', '60',                              # Keyframe interval
    '-c:a', 'aac',                           # Audio codec
    '-b:a', '128k',                          # Set audio bitrate to 128 Kbps
    '-f', 'flv',                             # Output format
    rtmp_url                                 # YouTube RTMP URL
]

print("Streaming your screen. Press Ctrl+C to stop.")

process = subprocess.Popen(ffmpeg_command)

try:
    process.wait()
except KeyboardInterrupt:
    print("Stopping the stream...")
    process.terminate()
    process.wait()
    
