 **README.md**

# Project Overview

This project includes Python scripts for interacting with Bluetooth devices and visualizing EEG and IMU data.

## Files

* **Last_test.py:**
    - Establishes a serial connection to a Bluetooth device.
    - Sends a default sequence and starts streaming data.
    - Streams data for 5 minutes or until manually stopped.
    - Saves data to text files upon stopping the stream.
* **LSL_Receiver_final.py:**
    - Connects to an EEGLSL Transmitter app.
    - Receives and visualizes EEG and IMU data streams.
* **Ble_connection.py:**
    - Provides information about Bluetooth service characteristics.

## Instructions

**Last_test.py:**

1. Pair your Bluetooth device.
2. Find the outgoing port in Bluetooth settings.
3. Specify the port in the code.
4. Run the code.
5. Click "Start Stream" to start data streaming.
6. Click "Stop Stream" to save data to text files.

**LSL_Receiver_final.py:**

1. Start the data stream in the EEGLSL Transmitter app.
2. Run the code.

**Ble_connection.py:**

1. View commented-out service IDs for reference.

## Additional Notes

* Data is not visible in hex values during streaming.
* Ensure no data loss during transmission and saving.

## Dependencies

* List any required Python libraries here.

## Contact

* Your Name (or project maintainer)
* Email address
