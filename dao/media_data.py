import os


class MediaData:
    media_storage_root = os.path.join('static', 'resources', 'media')

    @staticmethod
    def full_path(sub_path: str) -> str:
        return os.path.join(MediaData.media_storage_root, sub_path)

    @staticmethod
    def save(request_file, sub_path: str):
        request_file.save(MediaData.full_path(sub_path))

    @staticmethod
    def media_file_exists(sub_path: str) -> bool:
        return os.path.exists(MediaData.full_path(sub_path))
