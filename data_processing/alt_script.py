# -*- coding: utf-8 -*-

from data_processing import untitledutils, dbutils, procutils
from data_processing.SourceSparknotes import SourceSparknotes
import logging, logging.config

getdocs = True
build_database = True
build_vocabulary = True
init_graph = True


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

