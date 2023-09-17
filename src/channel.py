import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.channel_url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self.fill_channel_data()
    def print_info(self):
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def fill_channel_data(self):
        response = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel = response['items'][0]
        self.title = channel['snippet']['title']
        self.description = channel['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(channel['statistics']['subscriberCount'])
        self.video_count = int(channel['statistics']['videoCount'])
        self.view_count = int(channel['statistics']['viewCount'])

    def to_json(self, file_path):
        data = {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'channel_url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    @property
    def channel_id(self):
        return self._channel_id
