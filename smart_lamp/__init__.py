from commands import COMMAND_RED, COMMAND_YELLOW, COMMAND_GREEN, COMMAND_BLUE, COMMAND_OFF, COMMAND_ON

DEFAULT_SETTING_LIGHT = {
    "brightness": 0,
    "temperature": 0
}

DEFAULT_SETTING_RGB = {
    "red": 0,
    "green": 0,
    "blue": 0
}

DEFAULT_SETTING = {
    "fito": 0,
    "light": {**DEFAULT_SETTING_LIGHT},
    "rgb": {**DEFAULT_SETTING_RGB}
}

RGB_SETTING_BY_COMMAND = {
    COMMAND_RED: {**DEFAULT_SETTING_RGB, "red": 255},
    COMMAND_YELLOW: {**DEFAULT_SETTING_RGB, "red": 255, "green": 255},
    COMMAND_GREEN: {**DEFAULT_SETTING_RGB, "green": 255},
    COMMAND_BLUE: {**DEFAULT_SETTING_RGB, "blue": 255},
}

LIGHT_SETTING_BY_COMMAND = {
    COMMAND_ON: {**DEFAULT_SETTING_LIGHT, "brightness": 100},
    COMMAND_OFF: {**DEFAULT_SETTING_LIGHT, "brightness": 0},
}


def get_rgb_setting_by_command(command: str) -> dict:
    """
    Получить конфигурацию для установки цвета

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    dict
        конфигурация цвета
    """

    return RGB_SETTING_BY_COMMAND[command]


def get_light_setting_by_command(command: str) -> dict:
    """
    Получить конфигурацию для включения/выключения

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    dict
        конфигурация светимости
    """

    return LIGHT_SETTING_BY_COMMAND[command]


__all__ = ['get_rgb_setting_by_command', 'get_light_setting_by_command', 'DEFAULT_SETTING']
