import untitledutils
import dbutils
import SourceSparknotes

getdocs = False
build_database = True
build_vocabulary = False
init_graph = False



if (init_graph):
    graph = dbutils.getGraph()
    graph.delete_all()
    dbutils.ConfigureGraph(graph)

if (getdocs):
    source = SourceSparknotes()

if build_vocabulary:
    untitledutils.get_adj_vocabulary(untitledutils.get_documents())

if build_database:
   dbutils.update_database()