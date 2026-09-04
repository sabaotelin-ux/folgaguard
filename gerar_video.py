import subprocess
import os

def render_vertical_clip(input_image="asset.jpg", output_video="output_916.mp4", duration=5):
    if not os.path.exists(input_image):
        return {"error": f"Arquivo base {input_image} não encontrado."}
    
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", input_image,
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-t", str(duration), "-shortest", "-c:v", "libx264", "-c:a", "aac",
        output_video
    ]
    
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode == 0:
        return {"success": True, "output": output_video}
    else:
        return {"success": False, "error": process.stderr.decode()[-200:]}
