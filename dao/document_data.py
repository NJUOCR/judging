import os
import re
import shutil
from typing import List, Tuple
import random as rd
import fitz
from fitz import Document
from werkzeug.datastructures import FileStorage

parent_dir = 'static/resources/documents/'

checkXO = r"/Type(?= */XObject)"
checkIM = r"/Subtype(?= */Image)"


def save_transform_pdf(case_id: str, pdf_file: FileStorage, ):
    case_dir_path = __case_dir_path(case_id)
    os.makedirs(case_dir_path, exist_ok=True)
    # pdf_path = "%s%08d.pdf" % (parent_dir, 4727909)
    pdf_path = "%s%08d.pdf" % (parent_dir, rd.randint(0, 1e7))
    pdf_file.save(pdf_path)
    pdf = fitz.open(pdf_path)
    refs_size = pdf._getXrefLength()
    img_cnt = 0
    # 遍历每一个对象
    for i in range(1, refs_size):
        # 定义对象字符串
        text = pdf._getXrefString(i)
        is_object = re.search(checkXO, text)
        # 使用正则表达式查看是否是图片
        is_img = re.search(checkIM, text)
        # 如果不是对象也不是图片，则continue
        if not is_object or not is_img:
            continue

        img_cnt += 1
        path = '%s%08d.png' % (case_dir_path, img_cnt)
        # 根据索引生成图像
        pix = fitz.Pixmap(pdf, i)
        if pix.n < 5:
            pix.writePNG(path)
        # 否则先转换CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(path)
        # 释放资源
        pix = None


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
