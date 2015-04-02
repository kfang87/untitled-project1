# -*- coding: utf-8 -*-

import untitledutils
import dbutils
from SourceSparknotes import SourceSparknotes

getdocs = False
build_database = True
build_vocabulary = False
init_graph = False
merge_people = False



if (init_graph):
    graph = dbutils.getGraph()
    graph.delete_all()
    dbutils.ConfigureGraph(graph)

if (getdocs):
    source = SourceSparknotes()

if (merge_people):
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-chamber-of-secrets','ron-weasley_harry-potter-and-the-prisoner-of-azkaban','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-prisoner-of-azkaban','ron-weasley','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-goblet-of-fire','ron-weasley','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-deathly-hallows','ron-weasley','ron-weasley','Ronald Weasley','Harry Potter series')

if build_vocabulary:
    untitledutils.get_adj_vocabulary(untitledutils.get_documents())

if build_database:
   dbutils.update_database()