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
            'nopart': True,  # Disable use of .part files (temp download files)
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        except Exception as e:
            return f"Download failed: {str(e)}", 500

        return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
# To run this app, you need to have Flask and yt-dlp installed.