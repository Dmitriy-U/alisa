commands = {
    "включить": "on",
    "выключить": "off",
    "красный": "red",
    "желтый": "yellow",
    "зелёный": "green",
    "синий": "blue",
    "фиолетовый": "purple",
}

command_list = list(commands.keys())


def get_suggests():
    suggests = list()
    for command in command_list:
        suggests.append({'title': command, 'hide': True})
    return suggests
