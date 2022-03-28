import dataclasses
import math
import time
import typing as tp

from vkapi import Session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int,
    count: int = 5000,
    offset: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    args = ["id", "deactivated"]
    if fields:
        for field in fields:
            args.append(field)
    params = {
        "access_token": VK_CONFIG["access_token"],
        "fields": args,
        "user_id": user_id,
        "v": VK_CONFIG["version"],
        "offset": offset,
        "count": count,
    }
    s = Session("https://api.vk.com/method")
    data = s.get("friends.get", params=params)
    items = data["response"]["items"]
    count = data["response"]["count"]
    returns = []
    deactivated = 0
    new_args = []
    for arg in args:
        if arg != "deactivated":
            new_args.append(arg)
    for i in range(count):
        to_add = {}
        if "deactivated" in items[i].keys():
            deactivated += 1
        else:
            for field in new_args:
                if field in items[i]:
                    to_add[field] = items[i][field]
                else:
                    to_add[field] = None
            returns.append(to_add)

    return FriendsResponse(count - deactivated, returns)


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    s = Session("https://api.vk.com/method")
    all_mutual = []
    if target_uids:
        try:
            for i in range(((len(target_uids) - 1) // 100) + 1):
                mutual_friends = s.get(
                    "friends.getMutual",
                    params={
                        "access_token": VK_CONFIG["access_token"],
                        "sourse_uid": source_uid,
                        "target_uids": ",".join(list(map(str, target_uids))),
                        "v": VK_CONFIG["version"],
                        "order": order,
                        "offset": i * 100,
                        "count": 100,
                    },
                )
                for friend in mutual_friends["response"]:
                    all_mutual.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
        except:
            pass
        time.sleep(1)
        return all_mutual

    try:
        mutual_friends = s.get(
            "friends.getMutual",
            params={
                "access_token": VK_CONFIG["access_token"],
                "sourse_uid": source_uid,
                "target_uid": target_uid,
                "v": VK_CONFIG["version"],
                "order": order,
            },
        )
        for friend in mutual_friends["response"]:
            all_mutual.append(friend)
    except:
        pass
    return all_mutual


# if __name__ == "__main__":
#     friends = []
#     friends_temp = get_friends(448281460).items
#     print(len(friends_temp))
#     for friend in friends_temp:
#        friends.append(friend["id"])
#     print(friends)
#     a = get_mutual(source_uid=448281460, target_uids=friends)
#     print(a)
# f = get_friends(448281460)
# print(f)
