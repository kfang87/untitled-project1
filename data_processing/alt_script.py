# -*- coding: utf-8 -*-

import untitledutils
import dbutils
import procutils
from SourceSparknotes import SourceSparknotes
import logging, logging.config

getdocs = False
build_database = True
build_vocabulary = False
init_graph = False


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('root')
logger.info('Logging Started.')

if (init_graph):
    graph = dbutils.getGraph()
    graph.delete_all()
    dbutils.ConfigureGraph(graph)

if (getdocs):
    source = SourceSparknotes()

if build_vocabulary:
    untitledutils.get_adj_vocabulary(procutils.get_documents())

if build_database:
   dbutils.update_database()

