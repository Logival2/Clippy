import time
import random
import re


def get_random_words(words_count):
    words = open("/usr/share/dict/words").read().splitlines()
    str = ""
    for i in range(0, words_count):
        str += f'{random.choice(words).strip().capitalize()} '
    return str.strip()


def is_valid_ipv4_address(host):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?):([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$'''
    if re.search(regex, host):
        print(host)
        dots_idx = host.rfind(':')
        return (host[:dots_idx], int(host[dots_idx + 1:]))


def exit_error(msg):
    print(msg)
    exit()


def log_to_file(msg):
    with open('./log.txt', 'w') as f:
        f.write(f"{time.time()}:\t{msg}\n")


def get_random_unicode_from_range(ranges_list, length=1):
    """ Receives a list of tuples (list of (range_start, range_end))
    returns {length} chars at random from this range """
    try:
        get_char = unichr
    except NameError:
        get_char = chr
    res = ""
    for i in range(length):
        selected_range = random.choice(ranges_list)
        res += get_char(random.randint(*selected_range))
    return res
