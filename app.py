from flask import Flask, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h2>YouTube to MP3</h2>
    <p>Prefix any YouTube URL like this:</p>
    <code>https://yourproject.railway.app/https://www.youtube.com/watch?v=abc123</code>
    '''

@app.route('/<path:video_url>')
def download(video_url):
    if not video_url.startswith('http'):
        video_url = 'https://' + video_url

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'nopart': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)

                # Find the actual .mp3 file created in tmpdir
                for file in os.listdir(tmpdir):
                    if file.endswith('.mp3'):
                        return send_file(os.path.join(tmpdir, file), as_attachment=True)

                return "MP3 file not found after download.", 500

        except Exception as e:
            return f"<h3>Download failed:</h3><pre>{str(e)}</pre>", 500

if __name__ == '__main__':
    app.run(debug=True)
# To run this app, you need to have Flask and yt-dlp installed.