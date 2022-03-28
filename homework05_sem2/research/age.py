import datetime as dt
import statistics
import typing as tp
from datetime import datetime
from webbrowser import get

import pandas as pd
from vkapi.config import VK_CONFIG
from vkapi.friends import FriendsResponse, get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    birth_dates = []
    ages = []
    friends_list: FriendsResponse = get_friends(user_id, fields=["bdate"])
    num_friends = friends_list.count
    friends_data = friends_list.items
    for i in range(num_friends):
        date = friends_data[i]["bdate"]
        if date:
            if len(date) > 5:
                birth_dates.append(date)
    if not birth_dates:
        return None
    for j in range(len(birth_dates)):
        birth_dates[j] = datetime.strptime(birth_dates[j], "%d.%m.%Y")

    today = datetime.today()
    for date in birth_dates:
        one_or_zero = (today.month, today.day) < (date.month, date.day)
        ages.append(today.year - date.year - int(one_or_zero))
    median = statistics.median(ages)
    return median


# print(age_predict(169132840))
