# Neuro modules
#
# Interne programma communicatie
# MessageBus

"""
bios.py
    \
    startup = check onderdelen (zoals jasper module scrap) en verifeer werking:
        maak message bus met socket server naar log file en triggers die terug kunnen?
        Als een soort module template.
        elke module heeft ieder een lijn als service
        ze starten als singel main ook, maar alleen als test.
        \
        Lees blockly om te weten wat te doen.
            hier moet dus nog wel een reader voor gemaakt worden.
            nood routine?
    
    start modules[blockly input]:
        |
        vision
        &
        audio
        &
        arduino
        &
        lpt
        &
        arm
        &
        system calls
        &
        log read
        
    loop bus:
        foreach (module in modules) { 
            get status 
            messages = time + module + status
            print messages
            }
        if () send CMD
"""
