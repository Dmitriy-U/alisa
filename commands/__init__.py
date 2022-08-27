COMMAND_ON = "on"
COMMAND_OFF = "off"
COMMAND_RED = "red"
COMMAND_YELLOW = "yellow"
COMMAND_GREEN = "green"
COMMAND_BLUE = "blue"

COMMANDS = {
    "включи": COMMAND_ON,
    "выключи": COMMAND_OFF,
    "красный": COMMAND_RED,
    "желтый": COMMAND_YELLOW,
    "зелёный": COMMAND_GREEN,
    "синий": COMMAND_BLUE,
}

SUCCESS_ANSWER_BY_COMMAND = {
    COMMAND_ON: "включаю",
    COMMAND_OFF: "выключаю",
    COMMAND_RED: "включаю красный",
    COMMAND_YELLOW: "включаю желтый",
    COMMAND_GREEN: "включаю зелёный",
    COMMAND_BLUE: "включаю синий",
}

UTTERANCE_LIST = list(COMMANDS.keys())


def get_suggests():
    suggests = list()
    for utterance in UTTERANCE_LIST:
        suggests.append({'title': utterance, 'hide': True})
    return suggests


def get_command_by_utterance(frase: str) -> str:
    return COMMANDS[frase]


def get_success_answer_by_command(command: str) -> str:
    return SUCCESS_ANSWER_BY_COMMAND[command]
