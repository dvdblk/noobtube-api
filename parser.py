from pprint import pprint as pp

import youtube_dl


URL = "https://www.youtube.com/watch?v="
ITAG_VALUE = [22, 43, 18, 36]


def video_info(id):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            "{url}{id}".format(url=URL, id=id),
            download=False # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    return video

def get_url(video):
    acceptable_formats = {int(quality["format_id"]): quality["url"]
                          for quality in video['formats'] if int(quality["format_id"]) in ITAG_VALUE}
    return acceptable_formats

def get_best_quality(acceptable_formats):
    return next(acceptable_formats[priority] for priority in ITAG_VALUE
                if priority in acceptable_formats.keys())
