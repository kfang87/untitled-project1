__author__ = 'Kayla'


from py2neo import Graph
import logging, logging.config



def update_casing_basenames():
    graph = Graph()
    name_list = graph.find("Name")
    for name_node in name_list:
        base_name = name_node.properties["base_name"]
        name_node.properties["base_name"] = base_name.lower()
        name_node.properties["display_name"] = base_name
        name_node.push()
        logging.info("Updating casing for %s", base_name)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('root')
logger.info('Logging Started.')

update_casing_basenames()