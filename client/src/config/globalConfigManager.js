import ProjectConfig from './config';

class GlobalConfig {
    // Define static properties to hold global configuration variables
    static lowOrganMidiNote = ProjectConfig.lowOrganMidiNote;
    static highOrganMidiNote = ProjectConfig.highOrganMidiNote;
    // Add more static properties as needed

    // Method to update configuration variables
    static updateLowOrganMidiNote(newLowOrganMidiNote) {
        this.lowOrganMidiNote = newLowOrganMidiNote;
    }

    // Method to update configuration variables
    static updateHighOrganMidiNote(newHighOrganMidiNote) {
        this.highOrganMidiNote = newHighOrganMidiNote;
    }
    // Add more update methods as needed
}

export default GlobalConfig;
