<template>
  <div class="main-container">
    <input type="file" @change="handleFileChange" ref="fileInput" style="display: none" accept=".mid">
    <button @click="openFileInputClick" class="load-midi-button">Load MIDI</button>

    <!-- Play button -->
    <button @click="parseAndDisplayTracksClick" class="parse-midi-button">Parse MIDI</button>
    <!-- Play toggle button -->
    <button @click="loadMidiOnServerClick" class="load-server-button">
      Load MIDI on server
    </button>
    <button @click="togglePlayClick" class="play-toggle-button">
      {{ isPlaying ? 'Pause' : 'Play' }}
    </button>
    <input v-model="comPort" @change="comPortChanged" type="text" placeholder="Insert COM Port" class="com-port-input my-input" />
    <multi-select v-if="parsedMidi"
                  v-model="selectedChannels"
                  :options="channelNumbers"
                  label=""
                  class="multi-select-container"
                  @update:selectedOptions="updateSelectedChannels"
    ></multi-select>

    <!-- Display parsed MIDI data -->
    <div v-if="parsedMidi" class="parsed-midi">
      <h2>Parsed MIDI Data:</h2>
      <div class="channels-container">
        <div v-for="(channel, index) in channels" :key="index" class="channel-column">
          <h3>Channel {{ index }}:</h3>
          <pre>{{ channel }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MultiSelect from './MultiSelect.vue';
import {Midi} from '@tonejs/midi';
import * as Tone from 'tone';
import * as ServerUtils from '../utils/server/python-server-utils'
import * as MidiUtils from '../utils/midi/midi-utils'
import GlobalConfig from '../config/globalConfigManager';

export default {
  name: 'MainPage',
  props: {
    msg: String
  },
  components: {
    MultiSelect,  // Register the MultiSelect component
  },
  data() {
    return {
      loadedMidi: null,
      loadedMidiOnServer: false,
      parsedMidi: null,
      channels: [], // Array to store MIDI channels data
      selectedChannels: [],
      comPort: 'COM3',
      player: null, // Store Tone.js player instance
      lowestNote: 24,
      highestNote: 83,
      isPlaying: false,
    };
  },
  created() {
    Tone.start(); // Start the audio context on user interaction
  },
  computed: {
    channelNumbers() {
      return this.channels.map((_, index) => ({
        value: (index).toString(),
        label: `Channel ${index}`,
      }));
    },
    selectedChannels() {
      return this.selectedChannels.map((_, index) => ({
        value: (index).toString(),
        label: `Selected Channel ${index}`,
      }));
    },
  },

  methods: {
    openFileInputClick() {
      this.$refs.fileInput.click();
    },

    loadMidiFile(file) {
      // read the file
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          this.loadedMidi = new Midi(e.target.result);
          console.log('Loaded MIDI:', this.loadedMidi);
        } catch (error) {
          console.error('Error while loading MIDI:', error);
        }
      };
      reader.readAsArrayBuffer(file);
    },

    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.loadMidiFile(file);
      }
    },

    comPortChanged() {
      // This method will be called when the COM Port input value changes
      console.log('COM Port changed:', this.comPort);
      const COM = {
        'com_port': this.comPort
      }
      ServerUtils.server_change_COM_port(COM)
    },

    parseAndDisplayTracksClick() {
      if (this.loadedMidi) {
        try {
          this.channels = []; // Clear previous data
          const tracks = this.loadedMidi.tracks || [];
          tracks.forEach((track) => {
            const notes = (track?.notes || []).map((note) => ({
              midi: note.midi,
              // name: note.name,
              // ticks: note.ticks !== undefined ? note.ticks : null,
              time: Tone.Ticks(note.ticks).toMilliseconds(),
              // durationTicks: note.durationTicks,
              duration: Tone.Ticks(note.durationTicks).toMilliseconds(),
              velocity: note.velocity,
              serialNote: MidiUtils.midiNoteToSerial(note.midi, true),
              // Add more properties as needed
            }));
            const filteredNotes = notes
                .filter(note => (
                    note.midi >= GlobalConfig.lowOrganMidiNote &&
                    note.midi <= GlobalConfig.highOrganMidiNote &&
                    note.duration > 0
                ));
            this.channels.push(filteredNotes);
            this.parsedMidi = true;

          });
          console.log('Channels Data:', this.channels);
        } catch (error) {
          console.error('Error while accessing MIDI tracks:', error);
        }
      } else {
        console.error('No MIDI file loaded yet.');
      }
    },

    loadMidiOnServerClick() {
      if (this.loadedMidi) {
        if(this.selectedChannels.length < 1){
          console.error('No channels selected!')
        }
        const serverMidi = MidiUtils.prepareMidiForServer(this.loadedMidi, this.selectedChannels)
        if (serverMidi.length < 1) {
          console.error('Only empty channels selected!');
        } else {

          ServerUtils.sendMIDIToServer(serverMidi)
          this.loadedMidiOnServer = true
        }
      } else {
        console.error('No MIDI file loaded yet.');
      }
    },

    togglePlayClick() {
      function playMidi(midi) {
        if (midi) {
          ServerUtils.serverPlay()
        } else {
          console.error('No MIDI file loaded yet.');
        }
      }
      if (!this.isPlaying) {
        playMidi(this.loadedMidi);
      } else {
        // Pause MIDI playback or implement logic for pause functionality
        // Example: pause playback using Tone.js if needed
      }
      this.isPlaying = !this.isPlaying;
    },

    updateSelectedChannels(selectedOptions) {
      this.selectedChannels = selectedOptions;
    },
  }
}
</script>

<style scoped>
/* Your button styles */
.load-midi-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.parse-midi-button {
  margin-top: 10px; /* Adjust as needed */
  /* Additional styling for the parse button */
  padding: 10px 20px;
  background-color: #2ecc71;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.play-midi-button {
  margin-top: 10px;
  /* Additional styling for the play button */
  padding: 10px 20px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.load-server-button {
  margin-top: 10px;
  /* Additional styling for the play button */
  padding: 10px 20px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.play-toggle-button {
  margin-top: 10px;
  /* Additional styling for the play button */
  padding: 10px 20px;
  background-color: rgba(174, 60, 231, 0.92);
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.my-input {
  /* Additional styling for the COM Port input */
  padding: 10px 20px;
  background-color: rgba(219, 158, 52, 0.87);
  color: #fff;
  border: none;
  border-radius: 5px;
  margin-top: 10px;
  cursor: pointer;
}
/* Additional styles for displaying parsed MIDI data */
.parsed-midi {
  margin-top: 50px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.channels-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
.channel-column {
  flex: 1;
  margin-right: 20px;
}
.channel-column h3 {
  margin-top: 0;
}
.channel-column pre {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  white-space: pre-wrap;
  font-family: 'Courier New', Courier, monospace;
}
</style>
