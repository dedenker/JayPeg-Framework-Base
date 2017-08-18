# -*- coding: utf-8-*-
import re

PUT = ["Output", "Example", "Module"] # This is coming from This module = So what is might "say"
GET = ["Input","Example","Listen"] # This is going to This module = So where it "listen" for

PRIORITY = 4 # Sets the priority on acting and Commands (PUT & GET) importants = If two modules have same Output command, priority makes a different. If both also have same priority -> both modules will be noticed/notified

def handle(input, device, profile):
    """
        Arguments:
        input -- input, typically from message bus
        device -- used to interact back to message bus
        profile -- contains information (config file?)
    """

    print "Example Module"

def monitor(device,profile):
    # This should fork a process for example monitoring a port or website.
    # And will put one of the PUT commands on the bus, then predefined the message bus master will know which module is SAY-ing this.
    print "Monitoring a port?"

def isValid(input):
    """
        Returns True if the input is related to jokes/humor.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    for part in GET:
        if re.search(part, input, re.IGNORECASE):
            return True
