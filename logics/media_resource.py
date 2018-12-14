from abc import abstractmethod

from dao.media_data import MediaData


class MediaResource:

    def __init__(self, name: str, sub_path: str, description: str, file):
        self.name = name
        self.sub_path = sub_path  # 以子路径作为id，因为名称和描述都可以被编辑修改
        self.description = description
        self.request_file = file

    def make_data_structure(self):
        return {
            '名称': self.name,
            '描述': self.description,
            '路径': self.sub_path,
            '类型': self.get_file_type()
        }

    @abstractmethod
    def get_file_type(self) -> str:
        # todo @熊 实现子类的抽象方法
        """
        Override this in child classes
        :return: 'file' | 'image' | 'audio' | 'video'
        """

    def file_exists(self):
        return MediaData.media_file_exists(self.sub_path)

    def save(self) -> dict:
        MediaData.save(self.request_file, self.sub_path)
        return self.make_data_structure()


class ImageResource(MediaResource):

    def get_file_type(self) -> str:
        pass

    def __init__(self, *args):
        MediaResource.__init__(self, *args)


class VideoResource(MediaResource):

    def get_file_type(self) -> str:
        pass

    def __init__(self, *args):
        MediaResource.__init__(self, *args)


class AudioResource(MediaResource):

    def get_file_type(self) -> str:
        pass

    def __init__(self, *args):
        MediaResource.__init__(self, *args)
