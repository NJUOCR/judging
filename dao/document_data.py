import os
import shutil
from typing import List, Tuple

from werkzeug.datastructures import FileStorage

parent_dir = 'static/resources/documents/'


def __case_dir_path(case_id):
    return parent_dir + case_id + '/'


def exists(case_id: str):
    return os.path.isdir(__case_dir_path(case_id))


def save_document(case_id: str, files: List[Tuple[FileStorage, str]]) -> List[str]:
    """

    :param case_id:
    :param files: [(file, suffix), ...]
    :return:
    """
    case_dir_path = __case_dir_path(case_id)
    if exists(case_id):
        shutil.rmtree(case_dir_path)

    os.makedirs(case_dir_path, exist_ok=True)
    paths = []
    for index, (file, suffix) in enumerate(files):
        path = '%s%08d.%s' % (case_dir_path, index, suffix)
        file.save(path)
        paths.append(path)
    return paths


def get_document_paths(case_id: str):
    case_dir_path = __case_dir_path(case_id)
    return list(
        map(
            lambda img: case_dir_path + img,
            sorted(os.listdir(case_dir_path))
        )
    ) if os.path.isdir(case_dir_path) else []
