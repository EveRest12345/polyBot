import datetime
import http
from collections import namedtuple
from logging import getLogger
from typing import Optional

import xmltodict
import requests


logger = getLogger(__name__)


Rate = namedtuple('Rate', 'name,rate')


def str_to_float(item: str) -> float:
    item = item.replace(',', '.')
    return float(item)


class CentralBankError(Exception):
    """ Ошибка при запросе API ЦБ
    """


def get_rate() -> Optional[Rate]:
    # URL запроса
    get_curl = "http://www.cbr.ru/scripts/XML_daily.asp"
    # Формат даты: день/месяц/год
    date_format = "%d/%m/%Y"

    # Дата запроса
    today = datetime.datetime.today()
    params = {
        "date_req": today.strftime(date_format),
    }
    r = requests.get(get_curl, params=params)
    if r.status_code != http.HTTPStatus.OK:
        raise CentralBankError('bad status code')

    resp = r.text

    try:
        data = xmltodict.parse(resp)
    except xmltodict.expat.error:
        logger.exception('status_code = %s\n%s\n----', r.status_code, resp)
        raise CentralBankError('bad xml')

    # Ищем по @ID
    section_id = 'R01235'

    try:
        for item in data['ValCurs']['Valute']:
            if item['@ID'] == section_id:
                r = Rate(
                    name=item['CharCode'],
                    rate=str_to_float(item['Value']),
                )
                return r
    except (KeyError, TypeError, ValueError):
        logger.exception('json traversal error')
        raise CentralBankError('json traversal error')
    return None
