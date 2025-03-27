import string
import random
from datetime import datetime
from zoneinfo import ZoneInfo

def timestamp_to_hms_format(timestamp, timezone_offset):
    tz = ZoneInfo(f"Etc/GMT{'+' if timezone_offset <= 0 else '-'}{abs(timezone_offset) // 3600}")
    dt = datetime.fromtimestamp(timestamp, tz)
    return dt.strftime('%H:%M:%S')
def wind_direction(degrees):
    directions = [
        "North", "Northeast", "East", "Southeast",
        "South", "Southwest", "West", "Northwest"
    ]
    sector_size = 360 / len(directions)
    sector_index = int((degrees + sector_size / 2) % 360 // sector_size)
    return directions[sector_index]
def hpa_to_mmhg(hpa):
    return int(hpa * 0.750062)
def generate_code():
    letter = random.choice(string.ascii_uppercase)
    digits = ''.join(random.choices(string.digits, k=5))
    return letter + digits


def generate_short_code(length: int = 6, letters_first: bool = True) -> str:
    """
    Генерирует случайный код из букв и цифр

    Args:
        length: Общая длина кода (по умолчанию 6)
        letters_first: Если True - сначала буквы, потом цифры (по умолчанию True)
                      Если False - полностью случайный порядок

    Returns:
        Строка с случайным кодом (5 букв + 1 цифра по умолчанию)
    """
    if letters_first:
        # 5 букв + 1 цифра (по умолчанию)
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(length - 1))
        digit = random.choice(string.digits)
        return letters + digit
    else:
        # Полностью случайный порядок символов
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))


def generate_unique_code(prefix: str = "", suffix: str = "") -> str:
    """
    Генерирует уникальный код с возможными префиксом и суффиксом

    Args:
        prefix: Префикс кода (по умолчанию "")
        suffix: Суффикс кода (по умолчанию "")

    Returns:
        Строка формата "префикс + 6 символов + суффикс"
    """
    code = generate_short_code()
    return f"{prefix}{code}{suffix}"
