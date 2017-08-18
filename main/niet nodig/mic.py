# -*- coding: utf-8-*-
"""
    The Mic class handles all interactions with the microphone and speaker.
"""
import logging
import tempfile
import wave
import audioop
import pyaudio
import alteration
import path


# deze moet dus hele uit elkaar getrokken worden.
# deze zet "iets" om in string, die door WORDS opgepikt worden.

class Mic:

    #speechRec = None
    #speechRec_persona = None

    def __init__(self, speaker, passive_stt_engine, active_stt_engine):
        print "mic? dus luisten"

    def __del__(self):
        print "verwijdering?"

    def get():
        print "getting?"
        return "stop"
