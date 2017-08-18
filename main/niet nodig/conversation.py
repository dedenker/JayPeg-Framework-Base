# -*- coding: utf-8-*-
import logging
#from notifier import Notifier 
# hier zou dus een socker client moeten zijn?
#from __init___ import Brain


class Conversation(object):

    def __init__(self, persona, mic, Brain):
        self._logger = logging.getLogger(__name__)
        print "hier is conversation.py"
        self.persona = persona
        self.mic = mic
        self.profile = "dit moet een profiel voorstellen" # dit zou dus moet lezen als dat nodig is.
        self.brain = Brain(mic) #, self.profile)
        #self.notifier = Notifier(profile)

    def handleForever(self):
        """
        Delegates user input to the handling function when activated.
        """
        self._logger.info("Starting to handle conversation with keyword '%s'.",
                          self.persona)
        while True:
            # Print notifications until empty
            #notifications = self.notifier.getAllNotifications()
            #for notif in notifications:
            #    self._logger.info("Received notification: '%s'", str(notif))
            # Noticication kan voor double check zijn....? ook in static

            self._logger.debug("Started listening for keyword '%s'",
                               self.persona)
            threshold, transcribed = ("iets","anders") #self.mic.passiveListen(self.persona)
            self._logger.debug("Stopped listening for keyword '%s'",
                               self.persona)

            if not transcribed or not threshold:
                self._logger.info("Nothing has been said or transcribed.")
                continue
            self._logger.info("Keyword '%s' has been said!", self.persona)

            self._logger.debug("Started to listen actively with threshold: %r",
                               threshold)
            input = "STOP" #self.mic.activeListenToAllOptions(threshold)
            self._logger.debug("Stopped to listen actively with threshold: %r",
                               threshold)

            if input:
                self.brain.query(input)
            else:
                #self.mic.say("Pardon?")
                print "we doen dit!"
