import os
import random as rd
import re
import shutil
import time
from multiprocessing import Queue, Process
from typing import List, Tuple

import fitz
from fitz import Document
from werkzeug.datastructures import FileStorage

parent_dir = 'static/resources/documents/'

checkXO = r"/Type(?= */XObject)"
checkIM = r"/Subtype(?= */Image)"


def render(q: Queue):
    __pdf_path = None
    __pdf_doc = None
    while not q.empty():
        pdf_path, xref, save_to = q.get()
        if __pdf_path == pdf_path:
            pdf_doc = __pdf_doc
        else:
            print('Worker Read')
            pdf_doc = Document(pdf_path)
            __pdf_path = pdf_path
            __pdf_doc = pdf_doc

        pix = fitz.Pixmap(pdf_doc, xref)
        if pix.n < 5:
            pix.writePNG(save_to)
        # 否则先转换CMYK
        else:
            fitz.Pixmap(fitz.csRGB, pix).writePNG(save_to)


def save_transform_pdf(case_id: str, pdf_file: FileStorage, ):
    __init_time = time.time()
    __total_rendering_time = 0

    case_dir_path = __case_dir_path(case_id)
    os.makedirs(case_dir_path, exist_ok=True)
    pdf_path = "%s%08d.pdf" % (parent_dir, rd.randint(0, 1e7))
    pdf_file.save(pdf_path)
    pdf = Document(pdf_path)
    refs_size = pdf._getXrefLength()
    img_cnt = 0
    q = Queue()
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
        q.put((pdf_path, i, path))

    procs = [Process(target=render, name="P%d" % _pi, args=(q,)) for _pi in range(64)]
    for proc in procs:
        print('start', proc.name)
        proc.start()
    for proc in procs:
        proc.join()

    print("total time: %.4f" % (time.time()-__init_time))


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
