__author__ = 'Kayla'
# -*- coding: utf-8 -*-
from py2neo import Graph
from data_processing import untitledutils as u


graph = Graph()

u.merge_persons("ron-weasley_harry-potter-and-the-deathly-hallows","ron-weasley","ron-weasley","Ron Weasley","Harry Potter series")
