from music21 import note, chord, converter, stream

from fractions import Fraction

def sigleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

class Music:
    def __init__(self, file_path):
        parsed_file = converter.parse(file_path)
        all_notes_or_chords = parsed_file.flat.notes

        note_sequrnce = []

        for note_or_chord in all_notes_or_chords:
            q = note_or_chord.quarterLength
            if q > 4:
                q = 4
            q = str(q)

            # note
            if isinstance(note_or_chord, note.Note):
                p = note_or_chord.pitch.nameWithOctave
                note_sequrnce.append((p, q))
            # chord
            elif isinstance(note_or_chord, chord.Chord):
                ps = note_or_chord.pitches
                for p in ps[:-1]:
                    note_sequrnce.append((p.nameWithOctave, 'chord'))
                note_sequrnce.append((ps[-1].nameWithOctave, q))
        note_sequrnce.append(('END', 'END'))

        self._note_sequence = note_sequrnce

    def get_note_sequence(self):
        return self._note_sequence[:]

    def combine_music(note_sequence):
        
        note_stream = []
        chord_temp = []
        offset = 0

        for note_or_chord in note_sequence:
            # end flag
            if note_or_chord[0] == 'END' or note_or_chord[1] == 'END':
                break
            # not-last note in chord
            elif note_or_chord[1] == 'chord':
                chord_temp.append(note_or_chord[0])
            # last note in chord
            elif chord_temp != []:
                q = Fraction(note_or_chord[1])
                if q > 4:
                    q = 4
                new_chord = chord.Chord(chord_temp, quarterLength=q)
                new_chord.offset = offset
                note_stream.append(new_chord)
                chord_temp = []
                offset += q
            # normal note
            else:
                q = Fraction(note_or_chord[1])
                if q > 4:
                    q = 4
                new_note = note.Note(note_or_chord[0], offset=offset, quarterLength=q)
                new_note.offset = offset
                note_stream.append(new_note)
                offset += q
                
        midi_stream = stream.Stream(note_stream)

        return midi_stream



@sigleton
class Music_Manager:
    def __init__(self):
        self._music_works = []

    def load_music(self, file_path):
        try:
            parsed_music = Music(file_path)
            self._music_works.append(parsed_music)
        except:
            pass

    def get_note_sequences(self, concat=False):
        sequences = []
        for work in self._music_works:
            if concat:
                sequences.extend(work.get_note_sequence())
            else:
                sequences.append(work.get_note_sequence())
        return sequences
