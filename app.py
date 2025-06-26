from flask import Flask, send_file, request
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h2>YouTube to MP3</h2>
    <p>To download a YouTube video as MP3, prefix the link like this:</p>
    <pre>http://localhost:5000/https://www.youtube.com/watch?v=dQw4w9WgXcQ</pre>
    """

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/<path:video_url>")
def download(video_url):
    if not video_url.startswith("http"):
        video_url = "https://" + video_url

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": False,
            "verbose": True,
            "nopart": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)

            # Find the .mp3 file in the temp directory
            for file in os.listdir(tmpdir):
                if file.lower().endswith(".mp3"):
                    mp3_path = os.path.join(tmpdir, file)
                    return send_file(mp3_path, as_attachment=True)

            return "<h3>MP3 file not found after download.</h3>", 500

        except Exception as e:
            return f"<h3>Download failed:</h3><pre>{str(e)}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
