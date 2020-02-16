import re
import youtube_dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'logger': MyLogger(),
            'outtmpl': '%(title)s.%(ext)s'
            }

ydl_opts_audio_only = {'format': 'bestaudio/best',
                       'postprocessors': [{
                           'key': 'FFmpegExtractAudio',
                           'preferredcodec': 'mp3',
                           'preferredquality': '192',
                       }],
                       'logger': MyLogger(),
                       'outtmpl': '%(title)s.%(ext)s'
                       }

def download(link, only_audio):
    try:
        if only_audio:
            opts = ydl_opts_audio_only
        else:
            opts = ydl_opts
        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([link])
    except youtube_dl.utils.DownloadError as e:
        print(e)

def get_filename(link, only_audio):
    try:
        if only_audio:
            opts = ydl_opts_audio_only
        else:
            opts = ydl_opts

        with youtube_dl.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(link, download=False)
            filename = ydl.prepare_filename(info)
            if only_audio:
                filename = re.sub(r'\.[^.]+$', '.mp3', filename)
            return filename
    except youtube_dl.utils.DownloadError as e:
        print(e)

