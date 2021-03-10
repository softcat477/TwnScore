import csv
import glob

chordsDict = {"major":[0, 4, 7],
          "minor":[0, 3, 7],
          "major-seventh":[0, 4, 7, 11],
          "minor-seventh":[0, 3, 7, 10],
          "dominant":[0, 4, 7, 10],
          "diminished":[0, 3, 6],
          "augmented":[0, 4, 8],
          "suspended-fourth":[0, 5, 7],
          "U":[0]}

note2MidiDict = {"C":48, "D":50, "E":52, "F":53, "G":55, "A":57, "B":59, "U":-1}

class Score(object):
    def __init__(self, meta_path:str, notes_path:str, chords_path:str):
        # A list of ordered notes. Each note is a dictinoary with entries:
        #   Note : Note number. ex C4+0 for middle C
        #   Midi : Midi number
        #   Key  : Unique hash key to get the chord of this note
        #   Tempo : <bpm>_<note type>
        #   Arrangement : <arrangement>_<instrumental/vocal-in>
        #   Tie : 
        #       "x" -> no tie; 
        #       "s" -> tie starts from this note; 
        #       "-"" -> tie passes this note;  
        #       "p" -> tie ends at this note
        #   Slur : Available types are the same as Tie
        #   Chn : Lyrics in Chinese; 
        #       "x" -> No lyrics
        #       "-" -> Notes between two lyrics.
        #   Twn : Lyrics in Taiwanese. Available types are the same as Chn
        #   Onset : The onset time in division unit in the measure that contains this note.
        #   Duration : The duration of this note in division unit.
        #   Offset : The offset time in division unit.
        #   Measure : The measure index. Starts with ZERO.
        self.notes = []

        # A dictionary of metadata with entries:
        #   Key : Key Signature
        #   Pent : Chinese Pentatonic scale
        #   Time : Time signature, <numerator>_<denominator>
        #   Division : The division unit per quarter note
        #   Note : Notes
        self.meta = {}

        # A nested dictionary of chords: 
        # {<hash key>:{"Chord":<Chord>, "Next":<another hash key> or "_END_"}}
        # <Chord> naming rule:
        #   <Root/Inversion>_<Chord>,
        #       <Root/Inversion> : Naming rule for Root and Inversion are the same: 
        #           <Note Name>_<+0/+1:sharp/-1:flat>. Example: E-1 for E flat, C+1 for C sharp.
        #           More Example, This is a C major triad : C+0/C+0_major
        #           More Eaample! This is a C major triad on G : C+0/G+0_major
        #       <Chord> : see https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-kind.htm for details
        #           major : major triad
        #           minor : minor triad
        #           major-seventh :
        #           minor-seventh :
        #           dominent :
        #           diminished : 
        #           augmented :
        #           suspended-fourth :
        self.chords = {}

        with open(notes_path, newline="") as fp:
            notes = csv.DictReader(fp)
            self.notes = [i for i in notes]

        with open(meta_path, newline="") as fp:
            meta = csv.DictReader(fp)
            self.meta = [i for i in meta][0]

        with open(chords_path, newline="") as fp:
            reader =  csv.DictReader(fp)
            for item in reader:
                self.chords[item["Key"]] = {"Chord":item["Chord"], "Next":item["Next"]}

    def getChordwithNote(self, u_hash_key:str) -> list: 
        if u_hash_key == "_END_":
            return []
        else:
            _ret = self.getChordwithNote(self.chords[u_hash_key]["Next"])
            _ret.append(self.chords[u_hash_key]["Chord"])
            return _ret