NOTESDICT = {'c': 60, 'c#': 61, 'db': 61, 'd': 62, 'd#': 63, 'eb': 63, 'e': 64, 'f': 65,
    'f#': 66, 'gb': 66, 'g': 67, 'g#': 68, 'ab': 68, 'a': 69, 'a#': 70, 'bb': 70, 'b': 71}
NOTESARR = ['c','db','d','eb','e','f','f#','g','ab','a','bb','b']
NOTESARR += NOTESARR

class Chords():
    def __init__(self,startNote = str) -> None:
        self.rootNote = startNote.lower()
        self._chords = {}
        self._currentChord = '1'
        self._lastChord = '1'
        self.setChords()

    def setChords(self):
        self._chords.clear()
        index = NOTESARR.index(self.rootNote[0])
        currentChords = {
        "1": NOTESARR[index].upper() + ' Major',
        "2": NOTESARR[index+2].upper() + ' minor',
        "3": NOTESARR[index+4].upper() + ' minor',
        "4": NOTESARR[index+5].upper() + ' Major',
        "5": NOTESARR[index+7].upper() + ' Major',
        "6": NOTESARR[index+9].upper() + ' minor',
        "7":NOTESARR[index+11].upper() + ' Major'
        }
        self._chords.update(currentChords)

    def setRootNote(self,root):
        self.rootNote = root.lower()
        self.setChords()

    def setCurrentChord(self,chord = str):
        self._lastChord = self._currentChord
        self._currentChord = chord

    def getLastChord(self):
        return self._lastChord

    def getCurrnetChord(self):
        return self._currentChord

    def getCurrentChords(self):
        return self._chords

    def getCurrentNoteValue(self):
        return NOTESDICT[self._chords[self._currentChord].split(' ')[0].lower()]

    def setLastNote(self,last):
        self._lastChord = last
    
    def run(self):
        self.setRootNote(self.rootNote)
