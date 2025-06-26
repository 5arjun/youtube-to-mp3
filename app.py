from flask import Flask, send_file, request
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h2>YouTube to MP3</h2>
    <p>To download, paste a YouTube URL after the slash like this:</p>
    <pre>http://localhost:5000/https://www.youtube.com/watch?v=dQw4w9WgXcQ</pre>
    """

@app.route("/mp3")
def download():
    video_url = request.args.get("url")
    if not video_url or not video_url.startswith("http"):
        return "Invalid or missing URL", 400

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": False,  # Show logs in terminal
            "verbose": True,
            "nopart": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)

            # List all files in the temp directory for debugging
            print("Files created by yt-dlp:")
            for file in os.listdir(tmpdir):
                print(" -", file)

            # Look for the .mp3 file
            for file in os.listdir(tmpdir):
                if file.lower().endswith(".mp3"):
                    return send_file(os.path.join(tmpdir, file), as_attachment=True)

            return "<h3>MP3 file not found after download.</h3>", 500

        except Exception as e:
            return f"<h3>Download failed:</h3><pre>{str(e)}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
