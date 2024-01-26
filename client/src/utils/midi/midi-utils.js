import GlobalConfig from '../../config/globalConfigManager';
import * as Tone from "tone";

export function midiNoteToSerial(midiNote, noteOn) {
    let serialNote = Math.round(midiNote);
    if(serialNote > 128 || serialNote < 0) throw Error("invalid note: {}".format(serialNote))
    if(noteOn===false) {
        serialNote += 128;
    }
    return serialNote;
}

export function prepareMidiForServer(midi, selectedChannels) {
    const midiTracks = midi.tracks || [];
    const uniqueTrack = new Set();
    const midiParsedTracks = []
    console.log('selectedChannels', selectedChannels)
    let channelCount = 0;

    midiTracks.forEach((track) => {
        const channelNumber = channelCount
        channelCount += 1;
        if (channelNumber && selectedChannels.includes(channelNumber.toString())) {
            // Increment the count of unique channels
            uniqueTrack.add(channelNumber);

            const notesOn = (track?.notes || []).map((note) => ({
                midi: note.midi,
                time: Math.floor(Tone.Ticks(note.ticks).toMilliseconds()),
                velocity: note.velocity,
                serialNote: midiNoteToSerial(note.midi, true),
            }));
            const notesOff = (track?.notes || []).map((note) => ({
                midi: note.midi,
                time: Math.floor(Tone.Ticks(note.ticks).toMilliseconds() + Tone.Ticks(note.durationTicks).toMilliseconds()),
                velocity: note.velocity,
                serialNote: midiNoteToSerial(note.midi, false),
            }));
            console.log('notesOff', notesOff)

            const notes = [...notesOn, ...notesOff].sort((a, b) => a.time - b.time);
            console.log('notes', notes)

            const filteredNotes = notes
                .filter(note => (
                    note.midi >= GlobalConfig.lowOrganMidiNote &&
                    note.midi <= GlobalConfig.highOrganMidiNote &&
                    note.duration > 0
                ));
            console.log('notes', notes)

            midiParsedTracks.push(notes); // TODO: filter! before mapping into noteonoff probably
        }
    });
    console.log('midiParsedTracks', midiParsedTracks)
    console.log('midiParsedTracks', typeof(midiParsedTracks))

    return midiParsedTracks;
}