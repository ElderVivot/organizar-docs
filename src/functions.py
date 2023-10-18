import os
import sys
import unicodedata
import re
import datetime
from typing import Dict, List, Any


def getDateTimeNowInFormatStr():
    dateTimeObj = datetime.datetime.now()
    return dateTimeObj.strftime("%Y_%m_%d_%H_%M")


def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
    palavraTratada = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com valores corretos
    return re.sub('[^a-zA-Z0-9.!+:><=)?$(/*,\-_ \\\]', '', palavraTratada)


def minimalizeSpaces(text):
    _result = text
    while ("  " in _result):
        _result = _result.replace("  ", " ")
    _result = _result.strip()
    return _result


def treatTextField(value):
    try:
        if value is None:
            return ""
        value = str(value)
        return minimalizeSpaces(removerAcentosECaracteresEspeciais(value.strip().upper()))
    except Exception:
        return ""
