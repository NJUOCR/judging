import os
import shutil
from typing import Tuple, List
from werkzeug.datastructures import FileStorage


class MediaData:
    media_storage_root = '/'.join(['static', 'resources', 'media'])

    @staticmethod
    def full_path(sub_dir: str) -> str:
        return '/'.join([MediaData.media_storage_root, sub_dir])

    @staticmethod
    def save(file_bundles: List[Tuple[str, FileStorage]], sub_dir: str):
        os.makedirs(MediaData.full_path(sub_dir), exist_ok=True)
        for filename, file in file_bundles:
            file.save('/'.join([MediaData.full_path(sub_dir), filename]))

    @staticmethod
    def media_exists(sub_dir: str) -> bool:
        return os.path.isdir(MediaData.full_path(sub_dir)) and len(os.listdir(MediaData.full_path(sub_dir))) > 0

    @staticmethod
    def remove_media(sub_dir: str):
        return shutil.rmtree(sub_dir, ignore_errors=True)
