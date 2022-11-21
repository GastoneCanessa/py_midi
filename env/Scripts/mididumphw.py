#!C:\Users\Utente\Desktop\py_midi\env\Scripts\python.exe
"""
Print a description of the available devices.
"""
import midi.sequencer as sequencer

s = sequencer.SequencerHardware()

print(s)
