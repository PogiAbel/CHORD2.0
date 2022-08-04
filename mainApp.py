from cmath import pi
import PySimpleGUI as sg
import math
from classes.midiWorkers import MidiWorker
from classes.chord import Chords

# Variables
FIFTHSROMAN = ['I', 'IV', 'ii', 'vi', 'iii', 'V']
FIFTHSLATIN = ['1','4','2','6','3','5']
CHORDS = [['A', 'C'], ['D', 'F'], ['G', 'A#'], ['C', 'D#'], ['F', 'G#'], ['A#', 'C#'], [
    'D#', 'F#'], ['G#', 'B'], ['C#', 'E'], ['F#', 'A'], ['B', 'D'], ['E', 'G']]
NOTESDICT = {'c': 60, 'c#': 61, 'db': 61, 'd': 62, 'd#': 63, 'eb': 63, 'e': 64, 'f': 65,
    'f#': 66, 'gb': 66, 'g': 67, 'g#': 68, 'ab': 68, 'a': 69, 'a#': 70, 'bb': 70, 'b': 71}
NOTESARR = [k for k, v in NOTESDICT.items() if 'b' not in k]+['b']
NOTESARR += NOTESARR
DEGSMALLCIRCLE = [0.5, 1, 4/3, 1.5, 5/3, 2]
circleSmallId = {x[1]: {} for x in CHORDS}
DEGBIGCIRCLE = []
ROTATE = []
for i in range(12):
    r = (i*1/6)
    ROTATE.append(r)
    DEGBIGCIRCLE.append(0.5+r)
circleBigId = {}
text_chordsId = {}
lastBigCircleId = False
lastSmallCircleId = False
playing = False
centerTextId = 0
centerChordTextId = 0


# GUI layout
col_graph = [[sg.Graph(key='-G-', canvas_size=(700, 700), enable_events=True, graph_bottom_left=(-320, -320),
                       graph_top_right=(320, 320), background_color="black", change_submits=True)]]

col_input = [
    [sg.Checkbox("Minor", enable_events=True, key='-M-')],
    [sg.Checkbox("Arpeggiator", enable_events=True, key='-ARP-')],
    [sg.Text('Duration')],
    [sg.Input( expand_x=True, size=(5, 5),
              key='-INP1-',tooltip='Duration of the notes in ns'), sg.Button('Ok', key='-INP_BUTT1-')],
    [sg.Text('Interval')],
    [sg.Input(enable_events=True, expand_x=True, size=(5, 5),
              key='-INP2-',tooltip='Time between chords in ms'), sg.Button('Ok', key='-INP_BUTT2-')],
    [sg.Text('BPM')],
    [sg.Input(enable_events=True, expand_x=True, size=(5, 5),
              key='-INP3-'), sg.Button('Ok', key='-INP_BUTT3-')],
]

layout = [
    [sg.Button('Exit'),sg.Button('Start'), sg.Button('Stop')],
     [sg.Column(col_graph), sg.Column(col_input)]
]

window = sg.Window("Canvas",
                   layout, size=(850, 800),
                   resizable=True,
                   finalize=True
                   )
graph = window['-G-']

# Methods


def drawCircle(center=tuple, r=int, color=str):
    return graph.draw_circle(center,
                             radius=r,
                             fill_color=color,
                             line_color="white",
                             line_width=2)


def drawText(text, location, size, ang):
    return graph.draw_text(text, location, color='white', font=[None, size], angle=ang, text_location='center')


def radiusPoint(length, deg):
    x = length*math.cos(deg*pi)
    y = length*math.sin(deg*pi)
    return (x, y)


def drawP():
    for i in range(4):
        q = ROTATE[i]
        a = radiusPoint(300, q)
        b = radiusPoint(300, q+2/3)
        c = radiusPoint(300, q+4/3)
        graph.draw_line(a, b, color='white', width=2)
        graph.draw_line(b, c, color='white', width=2)
        graph.draw_line(c, a, color='white', width=2)


def drawBigC():
    j = 0
    for i in DEGBIGCIRCLE:
        o = radiusPoint(200, i)
        circleBigId.update({CHORDS[j][1]: drawCircle(o, 100, None)})
        j += 1


def drawSmallC():
    rot = 0
    for i in DEGBIGCIRCLE:
        k = 0
        x = (76*math.cos(i*pi))
        y = (76*math.sin(i*pi))
        o = radiusPoint(76, i)
        drawText(CHORDS[rot][k], o, 10, ROTATE[rot]*180)
        for j in DEGSMALLCIRCLE:
            x = (200*math.cos(i*pi))+(100*math.cos((j+ROTATE[rot])*pi))
            y = (200*math.sin(i*pi))+(100*math.sin((j+ROTATE[rot])*pi))
            circleSmallId[CHORDS[rot][1]].update(
                {FIFTHSLATIN[k]: drawCircle((x, y), 10, 'black')})
            drawText(FIFTHSROMAN[k], (x, y), 10, ROTATE[rot]*180)
            k += 1
        k = 1
        o = radiusPoint(250, i)
        if rot <= 11:
            rot += 1
        text_chordsId.update(
            {drawText(CHORDS[rot-1][k], o, 16, ROTATE[rot-1]*180): CHORDS[rot-1][k]})


def drawRectangel():
    for i in range(12):
        q = ROTATE[i]
        a = radiusPoint(90, q)
        b = radiusPoint(90, q+3/6)
        graph.draw_line(a, b, color='white', width=1)


def colorFigures(figureId, color):
    chordName = text_chordsId[figureId]
    bigCid = circleBigId[chordName]
    graph.Widget.itemconfig(bigCid, outline=color)
    if color != "white":
        color = "#73E14E"
    for k, v in circleSmallId[chordName].items():
        if k == '1' and color != 'white':
            graph.Widget.itemconfig(v, outline='blue')
        else:
            graph.Widget.itemconfig(v, outline=color)

def colorSmallFigure():
    chordName = myChords.rootNote
    graph.Widget.itemconfig(circleSmallId[chordName.upper()][myChords.getLastChord()], outline='#73E14E')
    graph.Widget.itemconfig(circleSmallId[chordName.upper()][myChords.getCurrnetChord()], outline='blue')

def bindInputs():
    inputs = ['1','2','3','4','5','6','7','m','p','<Up>','<Down>']
    for x in inputs:
        graph.bind(x,x)

drawBigC()
drawP()
drawRectangel()
drawSmallC()

graph.set_focus(True)
bindInputs()
myChords = Chords('C')
myMidiWorker = MidiWorker(daemon=True)
# Main loop
while True:
    event, values = window.read()
    match event:
        case sg.WIN_CLOSED:
            del myMidiWorker
            del myChords
            break
        case 'Exit':
            break
        case '-G-':                                                                      # Main interface, the graph
            figure = window['-G-'].get_figures_at_location(values['-G-'])                # Get clicked figure
            if figure:
                figure = figure[0]
            if figure in text_chordsId:                                                  # Set chord progression
                myChords.setRootNote(text_chordsId[figure])
                myChords.setCurrentChord('1')
                currentChords = myChords.getCurrentChords()
                myMidiWorker.setMajor(True)
                if lastBigCircleId :                                                          # Display chord progression
                    colorFigures(lastBigCircleId, "white")
                    graph.delete_figure(centerTextId)
                    graph.delete_figure(centerChordTextId)
                centerTextId = drawText(text_chordsId[figure], (0,0),20,0)
                centerChordTextId = drawText(currentChords[myChords.getCurrnetChord()], (0,-20),10,0)
                colorFigures(figure, "#52acff")
                try:                                                                     # Start playing midi
                    myMidiWorker.setStartNote(
                        NOTESDICT[text_chordsId[figure].lower()])
                    myMidiWorker.setIsRunning(True)
                    playing = True
                except:
                    sg.popup_error('Faild to start', auto_close=True,auto_close_duration=0.5)
                lastBigCircleId = figure

        case 'Stop':
            myMidiWorker.setIsRunning(False)
            myMidiWorker.instantStop()
            try:
                colorFigures(lastBigCircleId, "white")
            except: pass
            playing = False
        case 'Start':
            myMidiWorker.setIsRunning(True)
            try:
                colorFigures(lastBigCircleId, "#52acff")
            except: pass
            playing = True
        case '-INP_BUTT1-':
            graph.set_focus(True)
            try:
                myMidiWorker.setDuration(float(values["-INP1-"]))
            except:
                sg.popup_error('Faild to set duration', auto_close=True,auto_close_duration=0.5)
        case '-INP_BUTT2-':
            window['-INP2-'].block_focus()
            graph.set_focus(True)
            try:
                myMidiWorker.setInterval(float(values["-INP2-"]))
            except:
                sg.popup_error('Faild to set interval', auto_close=True,auto_close_duration=0.5)
        case '-M-':
            myMidiWorker.setMajor(not window['-M-'].get())
        case '-ARP-':
            myMidiWorker.setArpeggiatror(window['-ARP-'].get())
        case '-G-m':
            window['-M-'].update(value=(not window['-M-'].get()))
            myMidiWorker.setMajor(not window['-M-'].get())
        case '-G-p':
            if playing:
                myMidiWorker.setIsRunning(False)
                myMidiWorker.instantStop()
                playing = False
            else:
                myMidiWorker.setIsRunning(True)
                playing = True
        case '-G-1'|'-G-2'|'-G-3'|'-G-4'|'-G-5'|'-G-6'|'-G-7':
            key = event[-1:]
            if key in ['2','3','6']: myMidiWorker.setMajor(False)
            else : myMidiWorker.setMajor(True)
            try:
                myChords.setCurrentChord(chord=key)
                myMidiWorker.setStartNote(myChords.getCurrentNoteValue())
                if centerChordTextId:
                    graph.delete_figure(centerChordTextId)
                centerChordTextId = drawText(currentChords[myChords.getCurrnetChord()], (0,-20),10,0)
                if key != '7' :colorSmallFigure()
            except:
                pass
        case '-G-<Up>':
            myMidiWorker.increaseRange()
        case '-G-<Down>':
            myMidiWorker.decreaseRange()


