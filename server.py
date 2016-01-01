#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    TODO
    Что мы имплементим:
    какой-то init, который дёргает init у socket'ов
    callback, который дёргают socket'ы:
    - на чувак подключился
    - на чувак что-то послал
"""

import random


class AgarioPlayer:
    def __init__(self, name):
        self.name = name
        self.id = random.randint(1, 10 ** 36)
        self.circles = [(random.randint(0, 8000), random.randint(0, 4000), 10)]
    

class AgarioServer:
    def __init__(self):
        """
            call init у сокетов
        """
        self.players = []
