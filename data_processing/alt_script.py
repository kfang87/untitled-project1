# -*- coding: utf-8 -*-

from data_processing import untitledutils, dbutils, procutils
from data_processing.SourceSparknotes import SourceSparknotes

getdocs = False
build_database = True
build_vocabulary = True
init_graph = False
merge_people = False



if (init_graph):
    graph = dbutils.getGraph()
    graph.delete_all()
    dbutils.ConfigureGraph(graph)

if (getdocs):
    source = SourceSparknotes()

if (merge_people):
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-chamber-of-secrets','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-prisoner-of-azkaban','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-goblet-of-fire','ron-weasley','Ronald Weasley','Harry Potter series')
    untitledutils.merge_persons('ron-weasley_harry-potter-and-the-deathly-hallows','ron-weasley','Ronald Weasley','Harry Potter series')

if build_vocabulary:
    untitledutils.get_adj_vocabulary(procutils.get_documents())

if build_database:
   dbutils.update_database()