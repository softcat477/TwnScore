The file structure to run `python3 ToMidi.py`
```
./
 +-Score.py
 +-ToMidi.py
 +-Scores/
         +<Score name>/
         |            + <score name>.xml
         |            + <score name>.pdf
         |            + <score name>.mid                     
         |            + <score name>_synth.mid
         |            + <score name>_meta.csv
         |            + <score name>_chords.csv
         |            + <score name>_notes.csv|
         |            
```


A song has 7 files:
* `<name>.xml`: The score in musicXML.
* `<name>.pdf`: The score in pdf.
* `<name>.mid`: The score in midi.
* `<name>_synth.mid`: Also the score in midi, but synthesized with python  from csv files.
* `<name>_meta.csv`
* `<name>_chords.csv`
* `<name>_notes.csv`

## _meta.csv
This file contains key, chinese pentatonic scale, time signature, division, and additional notes.
Available csv headers: `Key`, `Pend`, `Time`, `Division`, `Note`.
* `Key` : The key of the song in the subtitle.
    * Naming rule : `A` → A major(?), `A-` → A flat major.
* `Pent` : The chinese pentatonic scale in the subtitle.
    * Naming rule : `1`→宮; `2`→商; `3`→角; `5`→徵, `6`→羽
* `Time` : The time signature.
    * Naming rule : `<numerator>_<denominator>`. Example: three-four time→`3_4`
* `Division` : The number of division units for a quarter note. The definition of `Division` in the csv file is the same as the `<divisions>` element in musicXML. See https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-divisions.htm for details.
    * Naming rule : `<A integer>`
* `Note` : Additional lines in the upper-left corner of the first page.
    * Naming rule : `<string>`


## _notes.csv
A files that contains all notes, rests, and grace notes.
Available csv headers: `Note`, `Midi`, `Key`, `Tempo`, `Arrangement`, `Tie`, `Slur`, `Chn`, `Twn`, `Onset`, `Duration`,`Offset`, `Measure`.
* `Note` : The note name in scientific pitch notation. Ex: `C4` for the middle C.
    * Naming rule : `<note_name>_+0//+1//-1` or `x`. `+0` for no accidentals; `+1` for ♯; `-1` for ♭; `x` for a rest.
    * Example : `C4+1` for C♯, `B4-1` for B, `x` for a rest.
* `Midi` : The midi number of this note.
    * Naming rule : Midi number from 0 to 127 or `-2`. For the midi number, see https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies for details. `-2` for a rest.
    * Example : `60` for `C4+0`, `69` for `A4+0`, `-2` for a rest.
* `Key` : A hash key to get the chord of this note in `_chords.csv`.
    * Naming rule : `<measure index>_<the order of this note its measure>_<chord index>`
* `Tempo` : The beat per minute, and the kind of note that gets one beat.
    * Naming rule : `<BPM>_<note type>`.
        * `<note type>` for what kind of note gets a beat. `2` for half notes; `4` for quarter notes.
* `Arrangement` : Ths structure label.
    * Naming rule : `<label>_instrumental//vocal-in`
* `Tie` : A tie.
    * Naming rule : `s//p//x`. `s`: the tie starts at this note; `p`: the tie ends at this note. If a note `C4+0` has a `p` and its next note also has a `p`, then `C4+0` is connected to two ties : one ends at it, and the other one starts at it. `x`: no tie.
* `Slur` : A slur.
    * Naming rule : `s//p//x//-`. Same as `tie` with an additional `-` for notes within a slur.
* `Chn` : Chinese lyrics.
    * Naming rule : `x//<Chinese characters>`. `x` for no lyrics.
* `Twn` : Taiwanese lyrics.
    * Naming rule : `x//<Taiwanese characters>`. `x` for no lyrics.
* `Onset` : The onset of this note in its measure in division units.
* `Duration` : The duration of this note in division units.
    * Naming rule : `<a float>//0.0`. `0.0` for a grace note.
* `Offset` : The offset of this note in its measure in division units.
* `Measure` : The measure index(starts at 0) of the measure that contains this note. 


## _chords.csv
A file containing chords.
Available csv headers : `Key`, `Chord`, `Next`.
* `Key` : The hash key of each note in `_notes.csv` to retrieve its chord.
    * Naming rule : Same as the `Key` in `_notes.csv`.
* `Chord` : The chord.
    * Naming rule : `<Root/Inversion>_<Chord>//_UNDEFINED_`, `_UNDEFINED_` for no chords attaching to this note.
        * `<Root/Inversion>` : The naming rules for root and inversion are the same : `<Note Name from A to G>_<+0//+1 for ♯//-1 for ♭>`.
        * `<Chord>` : See https://usermanuals.musicxml.com/MusicXML/Content/EL-MusicXML-kind.htm for details.
        * Possible chords in this dataset : 
            * major
            * minor
            * major-seventh
            * minor-seventh
            * dominent
            * diminished
            * augmented
            * suspended-fourth
        * Example :
            * C major triad : `C+0/C+0_major`
            * C major triad on G : `C+0/G+0_major`   
* `Next` : Some note has more than one chord, so `Next` is the hash key to the next chord.
    * Naming rule : `<another Key>//_END_`. `_END_` means this is the last chord.


## Examples

|   |  | 
| -------- | -------- |
| Score  | ![](https://i.imgur.com/hgw6Dmd.jpg)     |
| `_meta.csv` | ![](https://i.imgur.com/hLsTVFy.jpg) |
| `_notes.csv` | ![](https://i.imgur.com/XcTtLJN.jpg) |
* The `Time` is `168_4`. 168 beats per minute, and a quarter note gets a beat.
* A <font color=#f19f8c>Slur</font> that crosses three notes has a `s,-,p` pattern.
* Two connected <font color=#ebe634>Ties</font> have a `s,p,p` pattern.
* The duration of the first `E4-1` note is `4.0`, and it is a half note since 
    ```
    4 division units / 2 division units per quarter note specified in _meta.csv
    = 2 quarter notes 
    = 1 half note.
    ```
    
|   |  | 
| -------- | -------- |
| Score  | ![](https://i.imgur.com/pKpgILk.jpg)     |
| `_notes.csv` | ![](https://i.imgur.com/hWDDvql.jpg) |
| `_chords.csv` | ![](https://i.imgur.com/02QAayy.jpg) |
* The first three notes do not have a chord, so their keys are `_UNDEFINED_`
* The `G4+0` note in the 4th measure has two chords: `G/D` and `G/D♭`. Use its key `3_0_2` to get the first chord `G+0/D+0_major` and use the key `3_1_3` in the next `NEXT` to get the second chord `G+0/D-1_major`.