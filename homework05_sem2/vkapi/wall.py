import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import Session, config
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:

    s = Session("https://api.vk.com/method")
    v = config.VK_CONFIG["version"]
    all_posts = []
    params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": count,
        "max_count": max_count,
        "filter": filter,
        "extended": extended,
        "fields": fields,
    }
    for i in range(0, count, 100):
        cur_code = f"""
                            return API.wall.get ({{
                            "owner_id": "{owner_id}",
                            "domain": "{domain}",
                            "offset": {0},
                            "count": "1",
                            "filter": "{filter}",
                            "extended": "0",
                            "fields": ""
                }});
                """
        data = {
            "code": cur_code,
            "access_token": VK_CONFIG["access_token"],
            "v": VK_CONFIG["version"],
        }
        cur_response = s.post("execute", data=data)
        for post in cur_response["response"]["items"]:
            all_posts.append(post)
        time.sleep(2)
    return json_normalize(all_posts)


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    s = Session("https://api.vk.com/method")
    v = config.VK_CONFIG["version"]

    code_template = f"""
                    return API.wall.get ({{
                    "owner_id": "{owner_id}",
                    "domain": "{domain}",
                    "offset": {0},
                    "count": "1",
                    "filter": "{filter}",
                    "extended": "0",
                    "fields": ""
        }});
        """

    data = {
        "code": code_template,
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
    }
    response = s.post("execute", data=data)
    actual_response = get_posts_2500(owner_id=owner_id, domain=domain, count=count, filter=filter)
    time.sleep(2)
    return actual_response


# print(get_wall_execute(domain="zatask", count=1000))
