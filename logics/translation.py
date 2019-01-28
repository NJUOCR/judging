DICTIONARY = {
    "_id": "_id",
    "名称": "name",
    "证据链条": "firstLevelItems",
    "查证事项": "secondLevelItems",
    "概要": "outlines",
    "内容": "contents",
    "印证证据": "thirdLevelItems",
    "类型": "type",
    "路径": 'path',
    "描述": 'description',
    "目录": 'headers',
    "起始页": 'start'
}


def translate_key(name: str, to: str):
    assert to in ('en', 'zh')

    if to == "en":
        return DICTIONARY[name] if name in DICTIONARY else name
    else:
        for k, v in DICTIONARY.items():
            if v == name:
                return k
        return name


def translate_json(obj: dict or list, to: str):
    assert to in ('en', 'zh')

    if isinstance(obj, dict):
        cp = {}
        for k, v in obj.items():
            cp[translate_key(k, to)] = translate_json(v, to)
        return cp
    elif isinstance(obj, list):
        return list(map(lambda _j: translate_json(_j, to), obj))
    else:
        return obj
