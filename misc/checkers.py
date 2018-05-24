# Функции проверки значений введенных пользователем
from re import match


def name_checker(name):
    correct_regexp = '([А-ЯЁ][а-яё]+[\-\s]?){2,}'
    name_elements = []
    for word in name.split(' '):
        if word != ' ' and type(word) is str:
            name_elements.append(word)
    correct_name = str()
    for element in name_elements:
        correct_name += element.capitalize()
        correct_name += ' '
    if match(correct_regexp, correct_name) is not None:
        return correct_name.strip()
    else:
        raise ValueError
