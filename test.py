import glob
import music21


midi_path = './chpn-p16.mid'
file = glob.glob(midi_path)[0]

mf = music21.midi.MidiFile()
mf.open(file)
mf.read()
mf.close()

notes = []
chords = []
duration = []
notes_to_parse = None

midix = music21.midi.translate.midiFileToStream(mf)

stream = midix


stream.show()

stream.write('midi', fp='./test1907.mid')