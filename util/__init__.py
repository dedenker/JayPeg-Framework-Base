#from .iproc import getAlpha
#from .iproc import preprocess
#from .iproc import postprocess
#from .iproc import threshold
#from .iproc import writeOSD
#import cascade
import sys,os
#print __file__
import redis
import path
import xml.etree.ElementTree
import logging

# define:
r_server = redis.Redis("localhost")

class Basic(object):
    def __init__(self,logging):
        logging.basicConfig()
        logger = logging.getLogger()
        self._logger = logging.getLogger(__name__)
        logger.debug("Flushing Redis, be careful if Redis DB contains more!!")
        r_server.flushdb()
        #APP_PATH = os.path.normpath(os.path.join(
        #    os.path.dirname(os.path.abspath(__file__)), os.pardir))
        #DATA_PATH = os.path.join(APP_PATH, "util")
        #self.readxml(APP_PATH)  # deze doet het wel
        #LIB_PATH = os.path.join(APP_PATH, "client")
        #PLUGIN_PATH = os.path.join(LIB_PATH, "modules")
        #CONFIG_PATH = os.path.expanduser(os.getenv('JASPER_CONFIG', '~/.jasper'))
        #print "app path=" + path.APP_PATH
        #print "lib path=" + path.LIB_PATH
        #for module_path in path.MODULE_PATH.values():
        #    #print "plugin path=" + path.MODULE_PATH.values()
        #    #print module_path
        r_server.set("data", path.DATA_PATH)
        #r_server.rpush("members", "Adam")
        

    def readxml(cls):# ,APP_PATH):
        poep = []
        e = xml.etree.ElementTree.parse('xmlfile.xml').getroot()
        print e
        print "XML XMLX XMMLX XML XML XML XMLX XML"
        # dit moet duidelijk nog beter worden.
        # ik heb nog geen idee hoe xml moet worden.
        # https://docs.python.org/3/library/xml.etree.elementtree.html
        #import xml.etree.ElementTree as ET
        #tree = ET.parse(APP_PATH + '/jaypeg.xml')
        #e = xml.etree.ElementTree.parse('jaypeg.xml').getroot()
        #for atype in e.findall('components'):
        #root = tree.getroot()
        #    print(atype.get('components'))
        #for subs in root.findall('enabled'):
        #    print(subs.tag, subs.attrib)
        #components = xmldoc.getElementsByTagName('components')
        #for s in components:
        #    print(s.attributes['name'].value)
        terug = "XML doet het dus wel"
        poep.append(terug)
        print poep
        return(e)

if __name__ == "__main__":
    print "can not do by myself"

if __name__ is not "__main__":
    Basic(logging)
