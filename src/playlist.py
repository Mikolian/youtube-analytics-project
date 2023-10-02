import isodate as isodate
import datetime

from video import MixinApi


class MixinVideo:
    """Миксин на получение информации о видео из API"""
    def set_information(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.id_play_list,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response


class PlayList(MixinApi, MixinVideo):
    """
    инициализируется id плейлиста и имеет следующие публичные атрибуты:
    название плейлиста
    ссылку на плейлист
    """
    def __init__(self, id_play_list):
        self.id_play_list = id_play_list
        self.title = None
        self.url = None
        self.fill_info_from_api()
        self._total_duration = None

    @property
    def total_duration(self):
        """total_duration возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        if self._total_duration is None:
            self._total_duration = self.set_duration()
        return self._total_duration

    def set_duration(self):
        """Узнаем суммарную длительность плейлиста"""
        video_response = self.set_information()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def fill_info_from_api(self):
        """Подтягиваем недостающие данные из API"""
        response = self.get_service().playlists().list(id=self.id_play_list,
                                                       part='snippet,contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video = response['items'][0]
        self.title = video['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.id_play_list}"
        self.set_duration()

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        video_response = self.set_information()
        best_video = 0
        video_id = ''
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > best_video:
                best_video = int(video['statistics']['likeCount'])
                video_id = video['id']
        return f"https://youtu.be/{video_id}"