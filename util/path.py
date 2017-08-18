# -*- coding: utf-8-*-
import os
import redis
#
r_server = redis.Redis("localhost")

# Jasper main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

DATA_PATH = os.path.join(APP_PATH, "util")  # goed opletten Jasper-Dev kan moeilijk doen!
STATIC_PATH = os.path.join(APP_PATH, "static")
PKG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
# deze is dus afhankelijk.
# let er op!!
components = r_server.lrange("components", 0, -1)
MODULE_PATH= {}
COMPONENT_PATH = {}
for component in components:
    LIB_PATH = os.path.join(APP_PATH, component)
    COMPONENT_PATH[component] = os.path.join(APP_PATH, component)
    MODULE_PATH[component] = os.path.join(LIB_PATH, "modules")

CONFIG_PATH = os.path.expanduser(os.getenv('JASPER_CONFIG', '~/.jasper'))
#PLUGIN_PATH = os.path.join(APP_PATH, "audio/modules") # for Jasper compatible # zou zo moeten...
PLUGIN_PATH = os.path.normpath(os.path.join(PKG_PATH, os.pardir, "plugins")) # kijken hoe dit werkt...
CASCADE_PATH = os.path.join(CONFIG_PATH, "cascades")

def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)

# Jasper-dev wil deze naar eigen sub folder \ data
def data(*fname):
    return os.path.join(STATIC_PATH, *fname)

