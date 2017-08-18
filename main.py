#### System Modules
import logging
import argparse
import time,redis,os,sys
import pkgutil,psutil
import redis
from importlib import import_module
from datetime import datetime
import yaml
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# Communication Modules
import Queue
import asyncore
import socket
import logging
import multiprocessing as mp
#import billiard as mp #= Alternative MP module, but seems to have deadlock issues.

# Own Local Modules
sys.path.append("util")
#?import util
import path
import msgbus

# define
r_server = redis.Redis("localhost")
parser = argparse.ArgumentParser(description='JayPeg')

# arguments
parser.add_argument('--debug', action='store_true', help='Show debug messages')
args = parser.parse_args()

class main(object):
    config_file = None
    file_name = (sys.argv[0].replace(".py",""))
    location = os.getcwd()
    PID = os.getpid()
    process_name = socket.gethostname()
    port = 8080

    def __init__(self, config_file=None, file_name=None, location=None, PID=None, process_name=None,port=None):
        if config_file:
            self.config_file = config_file
        if file_name:
            self.file_name = file_name
        if location:
            self.location = location
        if PID:
            self.PID = PID
        if process_name:
            self.process_name = process_name
        if port:
            self.port = port
        if not config_file and not file_name and not location and not PID and not process_name:
            self.show_defaults()

    def show_defaults(self):
        logger.debug("All defaults settings! \nConfig: %s \nFile: %s \nLocation: %s \nPID: %s \nProcess: %s", self.config_file,self.file_name,self.location,self.PID,self.process_name)

class Jaypeg(object):
    def __init__(self, logging):
        main()
        self.wakeup = datetime.now()
        self.POST()
        self.processes = self.get_process()
        self.modules = self.get_modules()
        if (main.name in r_server.lrange("msgbus", 0, -1)): # Verify is MessageBus is Loaded for this component
            logger.debug("Attemped to load %s a second time, fix this bug!", main.name)
        else:
            r_server.set((str(main.name) + str("port")), main.port)
            logger.debug("Setting up message bus: %s on Port: %s", str(main.file_name) + str("port"),r_server.get(str(main.name) + str("port")))
            self.queue = mp.Queue()
            msgbus.MessageBus(main.name, self.queue)
            bus = mp.Process(target=asyncore.loop, args=())
            bus.start()
        self.showtime() # =cleanup komt dan True terug als gesloten?

    def POST(self):
        #name = (sys.argv[0].replace(".py",""))
        # Next can move to another function for cleaning code.
        try:
            f = open(("events/" + main.file_name + ".yaml"), 'rb')
            content = f.read()
            f.close()
            #self.yaml_content = yaml.load(content)
            main.config_file = yaml.load(content)
        except yaml.YAMLError as exc:
            print(exc)
        except Exception as e: 
            print(e)
            self.yaml_content = None
            print "Something go wrong with %s event loading = ERR: 013" % (sys.argv[0].replace(".py",".yaml"))
            pass
        # Setting Config info
        try:
            #self.name = self.yaml_content["main"]["name"]
            main.name = main.config_file["main"]["name"]
        except: # If no NAME define, use file name.
            print "Info: No name defined in config file."
            main.name = main.file_name

    def get_process(self):
        try_names = []
        self.loaded_component = []
        try_names.append(main.file_name)
        if main.config_file:
            for component in main.config_file["components"]:
                try_names.append(main.config_file["components"][component])
                #print "comps"
                #print [component]
        logger.debug("List of requested components: %s", try_names)
        for component in try_names:
            #print component
            try:
                # No working???
                loaded = __import__(component)
                self.component = component
                #drive = mp.Process(name='audio',target=loaded.main, args=())
                #drive.start()
                print "Component %s loaded" % component
                self.loaded_component.append(loaded)
                r_server.rpush("components", component)
            except Exception as e: 
                print "problem with loading module! %s \n\t--> %s" % (component, e) # Log warning
                pass
        logger.debug("Enabled component(s): %s", r_server.lrange("components", 0, -1))
        logger.debug("List of loaded component(s): %s", self.loaded_component)
        return

    def Start_WatchDog(self):
        # This doesn't work yet.
        logger.info("Starting Watchdog")
        event_handler = LoggingEventHandler()
        self.observer = Observer()
        self.observer.schedule(None, main.location, recursive=True)

    def get_modules(self):
        modules = []
        logger.debug("Getting %s Modules", main.name)
        self.locations = [os.path.join(main.location, main.file_name, "modules")] # not make list?
        #self.locations =  +  + "modules" # not make list?
        logger.debug("Looking for modules in: %s",
                     ', '.join(["'%s'" % self.locations]))
        #             ', '.join(["'%s'" % location for location in self.locations])) = if list!
        for finder, name, ispkg in pkgutil.walk_packages(self.locations):
            logger.debug("Entering module: %s", name)
            # Make REDIS entry for components? for fast cross module/process information.
            loader = finder.find_module(name)
            mod = loader.load_module(name)
            modules.append(name)
        self.Start_WatchDog()
        return(modules)

    def showtime(self):
        cleanup = False
        POST = False
        #time.sleep(3) # To test timing...
        #ready = datetime.now() # 
        print "It did take: %ds , to POST. \nNow wait for components to come online." % (((datetime.now()) - self.wakeup).seconds) # Get POST time.
        checklist = r_server.lrange("components", 0, -1) # Have a components list that must start.
        for component in self.loaded_component:
            logger.debug("Starting component: %s", component)
            try:
                drive = mp.Process(name='dynamic',target=component.main, args=())
                drive.start()        
            except Exception as e: 
                print "problem with loading component! %s \n\t --> %s" % (component, e)
                pass
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                print "next round"
        except KeyboardInterrupt:
            print "User killed me!!!!!!!!!!!!!!!!!"
            # Clean up should be preformed to prevent ghost sockets and zombie processes hanging...
            # Cleaning REDIS:
            r_server.delete("components")
            r_server.delete(str(self.name) + str("port"))
            r_server.delete("msgbus")
            # Cleaning Processes ? Some PID compare? Let processes first try them self?
            if(cleanup):
                # should be list... 
                # asyncore cleanup ?
                drive.join()
                # This needs to proper tested
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    print("\t\t\t************************************************************************")
    print("\t\t\t*                  JayPeg - THE robot FrameWork                        *")
    print("\t\t\t* (c) 2017 JP &(Jasper, Google Search, Stack Overflow)                 *")
    print("\t\t\t************************************************************************")
    print "Number of CPUs %d and PID: %s" % (mp.cpu_count(), os.getpid())
    print "Memory Total: %s - Free: %s - Used: %s" % (psutil.virtual_memory().total,
                                                        psutil.virtual_memory().free,
                                                        psutil.virtual_memory().used)
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger((sys.argv[0].replace(".py","")))

    if args.debug:
        logger.setLevel(logging.DEBUG)

    print "Starting up..."
    Jaypeg(logging)
