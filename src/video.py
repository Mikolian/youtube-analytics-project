import os

from googleapiclient.discovery import build


class InfoFromAPI(Exception):
    def __init__(self):
        self.message = "Несуществующий id видео"


class MixinApi:
    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class Video(MixinApi):
    """
    Инициализация реальными данными следующих атрибутов экземпляра класса Video:
    id видео,
    название видео,
    ссылка на видео,
    количество просмотров,
    количество лайков
"""

    def __init__(self, id_video=None):
        """Инициализируем по id_video"""
        self.id_video = id_video
        try:
            self.fill_channel_data()
        except InfoFromAPI as m:
            print(m.message)
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """Реализуем метод согласно заданию """
        return f"{self.title}"

    def fill_channel_data(self):
        """Подтягиваем недостающие данные из API"""
        response = self.get_service().videos().list(id=self.id_video, part='statistics, snippet').execute()
        if response['pageInfo']['totalResults'] != 0:
            video = response['items'][0]
            self.title = video['snippet']['title']
            self.url_video = f"http://www.youtube.com/watch?v={self.id_video}"
            self.like_count = int(video['statistics']['likeCount'])
            self.view_count = int(video['statistics']['viewCount'])
        else:
            raise InfoFromAPI



class PLVideo(Video):
    """который инициализируется 'id видео' и 'id плейлиста'"""

    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
        self.title_video = None
        self.name_video()

    def name_video(self):
        playlist_videos = self.get_service().playlistItems().list(
            part='snippet',
            playlistId=self.id_playlist,
            videoId=self.id_video
        ).execute()
        video = playlist_videos['items'][0]
        self.title_video = video['snippet']['title']