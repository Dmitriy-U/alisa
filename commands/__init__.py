COMMAND_ON = "on"
COMMAND_OFF = "off"
COMMAND_INFO = "info"
COMMAND_RED = "red"
COMMAND_YELLOW = "yellow"
COMMAND_GREEN = "green"
COMMAND_BLUE = "blue"

COMMANDS_SWITCH = {
    "включи": COMMAND_ON,
    "выключи": COMMAND_OFF,
}

COMMANDS_INFO = {
    "состояние": COMMAND_INFO,
}

COMMANDS_COLOR = {
    "красный": COMMAND_RED,
    "желтый": COMMAND_YELLOW,
    "зелёный": COMMAND_GREEN,
    "синий": COMMAND_BLUE,
}

COMMANDS = {**COMMANDS_SWITCH, **COMMANDS_INFO, **COMMANDS_COLOR}

UTTERANCE_LIST = list(COMMANDS.keys())

SUCCESS_ANSWER_BY_COMMAND = {
    COMMAND_ON: "включаю",
    COMMAND_OFF: "выключаю",
    COMMAND_RED: "включаю красный",
    COMMAND_YELLOW: "включаю желтый",
    COMMAND_GREEN: "включаю зелёный",
    COMMAND_BLUE: "включаю синий",
}


def get_suggests() -> list:
    """
    Получить все подсказки (команды)

    Returns
    -------
    list
        подсказки
    """

    suggests = list()
    for utterance in UTTERANCE_LIST:
        suggests.append({'title': utterance, 'hide': True})
    return suggests


def get_command_by_utterance(frase: str) -> str:
    """
    Получение команды по фразе

    Parameters
    ----------
    frase : str
        фраза

    Returns
    -------
    str
        команда
    """

    return COMMANDS[frase]


def get_success_answer_by_command(command: str) -> str:
    """
    Получение ответа для пользователя

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    str
        ответ
    """

    return SUCCESS_ANSWER_BY_COMMAND[command]


def is_color_command(command: str) -> bool:
    """
    Является ли команда командой изменения цвета

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    bool
        результат
    """

    return command in list(COMMANDS_COLOR.values())


def is_switch_command(command: str) -> bool:
    """
    Является ли команда командой включения/выключения

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    bool
        результат
    """

    return command in list(COMMANDS_SWITCH.values())


def is_info_command(command: str) -> bool:
    """
    Является ли команда командой отдачи информации

    Parameters
    ----------
    command : str
        команда

    Returns
    -------
    bool
        результат
    """

    return command in list(COMMANDS_INFO.values())


__all__ = ['is_switch_command', 'is_color_command', 'is_info_command', 'get_success_answer_by_command',
           'get_command_by_utterance', 'get_suggests', 'UTTERANCE_LIST', 'COMMAND_ON', 'COMMAND_OFF', 'COMMAND_RED',
           'COMMAND_YELLOW', 'COMMAND_GREEN', 'COMMAND_BLUE']
