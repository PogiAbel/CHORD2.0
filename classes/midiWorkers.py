import threading
import rtmidi
import time



class MidiWorker(threading.Thread):
    def __init__(self,**kwargs) -> None:
        super(MidiWorker,self).__init__(**kwargs)
        self._isRunning = False
        self._note = 60
        self._playtime = 0.5
        self._interval = 0.5
        self._major = True
        self._midiout = rtmidi.MidiOut()
        self.lock = threading.RLock()
        self.start()

    def __del__(self):
        del self._midiout
        del self
    
    def setDuration(self,setTime):
        with self.lock:
            self._playtime = setTime

    def setInterval(self,setTime):
        with self.lock:
            self._interval = setTime

    def setStartNote(self,startNote = int):
        with self.lock:
            self._note = startNote

    def setMajor(self,major = bool):
        with self.lock:
            self._major = major

    def setIsRunning(self, is_running = bool):
        with self.lock:
            self._isRunning = is_running

    def setMidiOut(self,midiout):
        # Init midiport
        available_ports = midiout.get_ports()
        for x in available_ports:
            if "PythonMidi" in x:
                port_string = x
        if available_ports:
            midiout.open_port(available_ports.index(port_string))
        else:
            midiout.open_virtual_port("My virtual output")

    def sendNote(self,midi,note = int,notes=[]):
        if not notes:notes.append(note)
        playnotes = [x for x in notes if 60 <= x <= 71]
        for x in playnotes:
            note_on = [0x90, x, 90]
            midi.send_message(note_on)

        time.sleep(self._playtime)

        for x in playnotes:
            note_off = [0x80, x, 0]
            midi.send_message(note_off)

    def minor(self,start = int):
        self.sendNote(self._midiout,notes=[start-9,start-5,start,start+3,start+7])

    def major(self,start = int):
        self.sendNote(self._midiout,notes=[start-8,start-5,start,start+4,start+7])



    def run(self):
        self.setMidiOut(self._midiout)
        runnning = True
        while True:
            with self.lock:
                runnning = self._isRunning
            if runnning:
                with self.lock:
                    if self._major:
                        self.major(self._note)
                    else:
                        self.minor(self._note)
            time.sleep(self._interval)

