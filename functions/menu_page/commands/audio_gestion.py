from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
        

def set_volume(vol):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        # set the volume (0.0 to 1.0)
        interface.SetMasterVolume(vol, None)
        
def change_volume(delta):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        # Get the actual volume
        current_volume = interface.GetMasterVolume()
        # Calcul the new volume
        new_volume = max(0.0, min(1.0, current_volume + delta))
        # Set the volume
        interface.SetMasterVolume(new_volume, None)

class VolumeCommands:
    def __init__(self, listen, language, talk):
        self.listen = listen
        self.language = language
        self.talk = talk
        
    def mute(self):
        # Volume Mute
        mute_keywords = ['lumen mute', 'lumen silence', 'lumen mode silence', 'lumen silence mode']
        if any(keyword in self.listen for keyword in mute_keywords):
            self.talk('Mute')
            set_volume(0.0)

    def demute(self):    
        # Volume deMute
        demute_keywords = ['lumen des mutes', 'lumen remets le volume', 'lumen demute', 'lumen de mute']
        if any(keyword in self.listen for keyword in demute_keywords):
            if self.language == 'Fr':
                self.talk('Volume remis')
            else: 
                self.talk('Volume restarted')
            set_volume(0.5)

    def volume_increase(self):        
        # Volume Increase
        volume_increase_keywords = ['lumen augmente le volume', 'lumen monte le volume', 'lumen increase the volume']
        if any(keyword in self.listen for keyword in volume_increase_keywords):
            if self.language == 'Fr':
                self.talk('Volume augmenté')
            else: 
                self.talk('Volume increased')
            change_volume(0.2)

    def volume_decrease(self):
        # Volume Decreases
        volume_decrease_keywords = ['lumen diminue le volume', 'lumen descend le volume', 'lumen decreases the volume']
        if any(keyword in self.listen for keyword in volume_decrease_keywords):
            if self.language == 'Fr':
                self.talk('Volume diminué')
            else: 
                self.talk('Volume decreased')
            change_volume(-0.2)