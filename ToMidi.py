import pretty_midi
import glob
import csv
from Score import Score
from Score import chordsDict
from Score import note2MidiDict

for notes_path, meta_path, chords_path in zip(glob.glob("Scores/*/*_notes.csv"), glob.glob("Scores/*/*_meta.csv"), glob.glob("Scores/*/*_chords.csv")):
    #if "四季紅" not in path_notes:
    #    continue
    # Read the csv file
    score = Score(meta_path=meta_path, notes_path=notes_path, chords_path=chords_path)
    prev_measure = 0
    prev_chord = ""
    
    # Get the number of quarter notes per minute
    tempo, unit = float(score.notes[0]["Tempo"].split("_")[0]), int(score.notes[0]["Tempo"].split("_")[-1])
    tempo *= (4/unit)
    piano_c_chord = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    # Get seconds per quarter note
    sec_per_quarter = 60/tempo

    # Create an Instrument instance for a piano instrument
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    t_sig = pretty_midi.TimeSignature(int(score.meta["Time"].split("_")[0]), int(score.meta["Time"].split("_")[1]), 0.0)
    A, B = int(score.meta["Time"].split("_")[0]), int(score.meta["Time"].split("_")[1])
    # A is the number of quarter notes in a measure
    if B==2:
        A *= 2

    for note in score.notes:
        # Note name -> Note numner
        note_number = int(note["Midi"])
        # dur(sec) = #quarter_notes * sec_per_quarter_note = (duration_in_division_units / division_units_per_quarter_note) * sec_per_quarter_note 
        dur = float(note["Duration"]) / float(score.meta['Division']) * sec_per_quarter
        # onset(sec) = (#quarter_notes + #parsed_measures * #quarter_notes_per_measure) * sec_per_quarter_note
        onset = (float(note["Onset"]) / float(score.meta["Division"]) + float(note["Measure"])*A) * sec_per_quarter

        # If this note is not a rest, then add it in. A grace note will have a 0 duration, so it will be ignored.
        if note_number > 0:
            noteMidi = pretty_midi.Note(velocity=100, pitch=note_number, start=onset, end=onset+dur)
            piano.notes.append(noteMidi)

        # Need to add a chord when 1) Measure changed 2) Chord changed within a measure
        # For now, we are just taking the first chord
        current_chord = score.getChordwithNote(note["Key"])[0] 
        current_measure = note["Measure"]
        # Two cases that we have to add a new chord
        #   (1) we enter a new measure
        #   (2) we have a new chord
        if current_measure != prev_measure or current_chord != prev_chord:
            # Add a new chord
            # <Root/Inversion>_<Chord>,
            root_inversion, chord = current_chord.split("_")
            root, inversion = root_inversion.split("/")
            rootMidi = note2MidiDict[root[0]] + int(root[-2:])

            chord_list = chordsDict[chord]
            for offset in chord_list:
                if rootMidi+offset > 0:
                    noteMidi = pretty_midi.Note(velocity=100, pitch=rootMidi+offset, start=onset, end=onset+dur)
                    piano.notes.append(noteMidi)

        prev_chord = current_chord
        prev_measure = current_measure

    # Add the piano instrument to the PrettyMIDI object
    piano_c_chord.instruments.append(piano)
    piano_c_chord.time_signature_changes.append(t_sig)

    # Write out the MIDI data
    filename = meta_path.replace("_meta.csv", "_synth.mid")
    print ("Write to {}".format(filename))
    piano_c_chord.write(filename)