import threading
from numpy import array
import rtmidi
import time



class MidiWorker(threading.Thread):
    def __init__(self,**kwargs) -> None:
        super(MidiWorker,self).__init__(**kwargs)
        self._isRunning = False
        self._note = 60
        self._playtime = 0.5
        self._interval = 0.5
        self._range = 0
        self._major = True
        self._arpeggiator = False
        self._midiout = rtmidi.MidiOut()
        self.lock = threading.RLock()
        self.start()

    def __del__(self):
        del self._midiout
        del self

    def instantStop(self):
        with self.lock:
            midi = self._midiout
        start = self.getNote()
        notes=[start+x for x in [-9,-5,0,3,7]]
        for x in notes:
            note_off = [0x80, x, 0]
            midi.send_message(note_off)
    
    def setDuration(self,setTime):
        with self.lock:
            self._playtime = setTime

    def increaseRange(self):
        with self.lock:
            if self._range < 4:
                self._range += 1
                self._note += 12

    def decreaseRange(self):
        with self.lock:
            if self._range > -4:
                self._range -= 1
                self._note -= 12

    def setInterval(self,setTime):
        with self.lock:
            self._interval = setTime

    def setArpeggiatror(self,isOn = bool):
        with self.lock:
            self._arpeggiator = isOn

    def setStartNote(self,startNote = int):
        with self.lock:
            self._note = startNote + (self._range*12)

    def setMajor(self,major = bool):
        with self.lock:
            self._major = major

    def setIsRunning(self, is_running = bool):
        with self.lock:
            self._isRunning = is_running

    def getNote(self):
        with self.lock:
            return self._note

    def getArp(self):
        with self.lock:
            return self._arpeggiator

    def getMaj(self):
        with self.lock:
            return self._major

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

    def getPlayNotes(self,notes = array):
        with self.lock:
            return [x for x in notes if 60+(self._range*12) <= x <= 71+(self._range*12)]

    def sendChord(self,midi,note = int,notes=[]):
        if not notes:notes.append(note)
        playnotes = self.getPlayNotes(notes)

        for x in playnotes:
            note_on = [0x90, x, 90]
            midi.send_message(note_on)

        time.sleep(self._playtime)

        for x in playnotes:
            note_off = [0x80, x, 0]
            midi.send_message(note_off)

    def sendNotes(self,midi,notes=[]):
        playnotes = self.getPlayNotes(notes)

        for x in playnotes:
            note_on = [0x90, x, 90]
            midi.send_message(note_on)

            time.sleep(self._playtime/3)

            note_off = [0x80, x, 0] 
            midi.send_message(note_off)

    def play(self):
        start = self.getNote()
        maj = self.getMaj()
        if maj:
            self.major(start=start)
        else:
            self.minor(start=start)

    def minor(self,start = int):
        arp = self.getArp()
        if arp:
            self.sendNotes(self._midiout,notes=[start+x for x in [-9,-5,0,3,7]])
        else:
            self.sendChord(self._midiout,notes=[start+x for x in [-9,-5,0,3,7]])

    def major(self,start = int):
        arp = self.getArp()
        if arp:
            self.sendNotes(self._midiout,notes=[start+x for x in [-8,-5,0,4,7]])
        else:
            self.sendChord(self._midiout,notes=[start+x for x in [-8,-5,0,4,7]])
        



    def run(self):
        self.setMidiOut(self._midiout)
        runnning = True
        while True:
            with self.lock:
                runnning = self._isRunning
            if runnning:
                self.play()
            time.sleep(self._interval)

