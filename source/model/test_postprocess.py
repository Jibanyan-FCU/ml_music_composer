#testing
from mido import Message, MidiFile, MidiTrack

def stop_note(note, time):
    return Message('note_off', note = note,
                   velocity = 0, time = time)

def start_note(note, time):
    return Message('note_on', note = note,
                   velocity = 127, time = time)

def roll_to_track(roll):
    delta = 0
    # State of the notes in the roll.
    notes = [False] * len(roll[0])
    # MIDI note for first column.
    midi_base = 60
    for row in roll:
        for i, col in enumerate(row):
            note = midi_base + i
            if col == 1:
                if notes[i]:
                    # First stop the ringing note
                    yield stop_note(note, delta)
                    delta = 0
                yield start_note(note, delta)
                delta = 0
                notes[i] = True
            elif col == 0:
                if notes[i]:
                    # Stop the ringing note
                    yield stop_note(note, delta)
                    delta = 0
                notes[i] = False
        # ms per row
        delta += 500

roll = [[0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 2, 0, 0, 0, 2, 0],
        [0, 1, 0, 2, 0, 0, 0, 2, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0]]

midi = MidiFile(type = 1)
midi.tracks.append(MidiTrack(roll_to_track(roll)))
midi.save('test.mid')