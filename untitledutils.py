import logging
import os
import ConfigParser
import sys




def create_entity_document(entityname, content):
    logger = logging.getLogger('UntitledLogger.SourceUtilities')
    
    DOCUMENT_FILEPATH = config.get('Sourcing','DOCUMENT_FILEPATH')
    filename = entityname + '.txt'
    filepath = os.path.join(DOCUMENT_FILEPATH, filename)
    
    try:
        filesize = os.path.getsize(filepath)
        if (os.path.isfile(filepath) and filesize > 0):
            logger.warning('File already exists at %s with size %s, skipping file creation', filepath, filesize)
        else:
            with open(filepath,'w') as f:
                f.write(content)
            logger.info('Creating context file %s for entity %s', filepath, entityname)
    except:
        logger.error('Could not complete creating file for filepath %s, %s',filename,sys.exc_info()[0])
    
    return filepath
    
    
# Initializing Logger

logger = logging.getLogger('UntitledLogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('C:\Logs\UntitledProject\UntitledProject.log')
fh.setLevel(logging.WARNING)

debugfh = logging.FileHandler('C:\Logs\UntitledProject\UntitledProject-DEBUG.log')
debugfh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
debugfh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(debugfh)

logger.info('Logging Started.')

# Initialize Config

config = ConfigParser.ConfigParser()
config.read('config.ini')