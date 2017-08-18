# JayPeg-Framework-Base

Author: Jan Paul Klompmaker
Date:   18 aug 2017

    Intro:
Robot Framework v0.1
Based on Python 2.7

This is the main opperational base layer.
Upon this, other layers like:
    -Visioning (OpenCV)
    -Audio     (Jasper)
    -Arduino
    -Web-UI    (Flask)
Must be applied to form a complete working system.

Dirs:
    events      =   Contains YAML/XML files which are used as config's
    jasper      =   for now audio listen process...
    main        =   Should contain main process parts (not general parts)
    plugins     =   Now part of jasper, should be moved?
    static      =   contains none pythonic files, DB? Audio files? pictures? etc...
    util        =   contains general python modules = messagebus, path...
Files:
    main.py     =   where it all starts.
    requirements=   which pip/easyinstall...

    Keywords:
Dynamic, inner/outer application communication


    Information:
For now still working progress...
