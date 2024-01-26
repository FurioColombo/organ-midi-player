import axios from "axios";

export function sendMIDIToServer(midi) {
    console.log('midi to be sent:', midi);

    // Make a POST request to the Flask server
    axios.post('http://localhost:5000/receive-parsed-midi', midi)
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error('Error sending data to server:', error);
        });
}

export function serverPlay() {
    // Prepare your data to send
    const messageToSend = {
        'argument': 'play'
    };

    // Make a POST request to the Flask server
    axios.post('http://localhost:5000/play', messageToSend)
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error('Error starting midi reproduction on server:', error);
        });
}

export function server_change_COM_port(COM) {
    // Make a POST request to the Flask server
    axios.post('http://localhost:5000/change-com-port', COM)
        .then(response => {
            console.log(response.data);
        })
        .catch(error => {
            console.error('Error changing server com port:', error);
        });
}