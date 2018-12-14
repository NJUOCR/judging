from abc import abstractmethod
from typing import Tuple, List
from werkzeug.datastructures import FileStorage
from dao.media_data import MediaData


class MediaResource:
    video_list = ['avi', 'asf', 'asx', 'rm', 'rmvb', 'mpg', 'mpeg', 'mpe', '3gp', 'mov', 'mp4', 'm4v', 'dat', 'mkv',
                  'flv', 'vob']
    audio_list = ['mp3', 'aac', 'wav', 'wma', 'cda', 'flac', 'm4a', 'mid', 'mka', 'mp2', 'mpa', 'mpc', 'ape', 'ofr',
                  'ogg', 'ra', 'wv', 'tta', 'ac3', 'dts']
    image_list = ['jpg', 'bmp', 'eps', 'gif', 'mif', 'miff', 'png', 'tif', 'tiff', 'svg', 'wmf', 'jpe', 'jpeg', 'dib',
                  'ico', 'tga', 'cut', 'pic']

    def __init__(self, name: str, sub_dir: str, description: str, file_bundles: List[Tuple[str, FileStorage]]):
        self.name = name
        self.sub_dir = sub_dir  # 以子路径作为id，因为名称和描述都可以被编辑修改
        self.description = description
        self.file_bundles = file_bundles

    @staticmethod
    def instance(name: str, sub_path: str, description: str, file_bundles: List[Tuple[str, FileStorage]]):
        if len(file_bundles) == 0:
            return None
        elif len(file_bundles) == 1:
            file_type, _ = file_bundles[0]
            if file_type in MediaResource.video_list:
                return VideoResource(name, sub_path, description, file_bundles)
            elif file_type in MediaResource.audio_list:
                return AudioResource(name, sub_path, description, file_bundles)
            elif file_type in MediaResource.image_list:
                return ImageResource(name, sub_path, description, file_bundles)
            else:
                return OtherResource(name, sub_path, description, file_bundles)
        else:
            # 如果传入多个文件，则过滤掉不是图片的那些
            return ImageResource(name, sub_path, description, list(
                filter(lambda bundle: bundle[0] in MediaResource.image_list, file_bundles)
            ))

    def make_data_structure(self):
        return {
            '名称': self.name,
            '描述': self.description,
            '路径': self.sub_dir,
            '类型': self.get_file_type()
        }

    @abstractmethod
    def get_file_type(self) -> str:
        """
        Override by sub class
        :return: 'image' | 'audio' | 'video' | 'other'
        """
        pass

    def file_exists(self):
        return MediaData.media_exists(self.sub_dir)

    def save(self) -> dict:
        MediaData.save(self.file_bundles, self.sub_dir)
        return self.make_data_structure()


class ImageResource(MediaResource):

    def get_file_type(self) -> str:
        return 'image'

    def __init__(self, *args):
        MediaResource.__init__(self, *args)


class VideoResource(MediaResource):

    def get_file_type(self) -> str:
        return 'video'

    def __init__(self, *args):
        MediaResource.__init__(self, *args)


class AudioResource(MediaResource):

    def get_file_type(self) -> str:
        return 'audio'

    def __init__(self, *args):
        MediaResource.__init__(self, *args)


class OtherResource(MediaResource):

    def get_file_type(self):
        return 'other'

    def __init__(self, *args):
        MediaResource.__init__(self, *args)
