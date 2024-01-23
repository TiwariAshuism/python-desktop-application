import serial
import time
import tkinter as tk
import threading

MAX_BUFF_LEN = 255
ble_data_list = []
final_ble_data = []
outgoing_serial = None
stop_stream_flag = False


# Function to save the output onto a text file
def save():
    global outgoing_serial
    count = 0
    hex_new = bytes([0xFF])
    # time.sleep(10)
    write_ser(hex_new)

    print("Saving data...")
    stronghold = ""
    for i in ble_data_list:
        hex_string = ' '.join(format(byte, '02X') for byte in i)
        print(hex_string)
        l = hex_string.split(" ")
        for j in l:
            count += 1
            temp = j
            print(temp)
            if temp in mySet:
                final_ble_data.append(stronghold)
                stronghold = ""
            stronghold += temp + " "

    with open("run.txt", "w") as file:
        for item in final_ble_data:
            file.write(f"{item}\n")

    with open("run.txt", "a") as file:
        file.write(f"{count}\n")

    print("Data saved")
    # if outgoing_serial and outgoing_serial.is_open:
    #     outgoing_serial.close()
    #     print("Serial port closed")


# Function to initialize the serial port
def initialize_serial(port_name, baud_rate, timeout_val):
    try:
        serial_port = serial.Serial(port_name, baud_rate, timeout=timeout_val)
        return serial_port
    except Exception as e:
        print(f"Serial port error: {e}")
        return None


# Function to write to the serial port
def write_ser(cmd):
    global outgoing_serial
    if outgoing_serial and outgoing_serial.is_open:
        outgoing_serial.write(cmd)
        time.sleep(1)  # Wait for a while after sending a byte


# Function to stop streaming data
def stop_stream():
    global stop_stream_flag
    stop_stream_flag = True


def start_stream():
    global outgoing_serial, stop_stream_flag
    if not outgoing_serial or not outgoing_serial.is_open:
        print("Serial port not initialized or closed")
        return

    try:
        hex_data = bytes([0xAA])  # Send 0xAA to start streaming
        write_ser(hex_data)
        print("Started streaming:", hex_data)

        start_time = time.time()  # Record start time
        stream_duration = 300  # Streaming duration in seconds

        while time.time() - start_time < stream_duration and not stop_stream_flag:
            read_data = outgoing_serial.read(outgoing_serial.inWaiting())
            if read_data:
                print(read_data)
                ble_data_list.append(read_data)

    except ValueError:
        print("Invalid input. Unable to start streaming.")
    finally:
        if outgoing_serial and outgoing_serial.is_open:
            save()


# Serial Port Initialization
outgoing_port = "COM11"
outgoing_serial = initialize_serial(outgoing_port, 115200, 1)
mySet = {'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1'}

if outgoing_serial and outgoing_serial.is_open:
    root = tk.Tk()
    root.title("Data Stream Control")


    def send_default_sequence():
        # Sending default sequence [0x0b, 0x08, 0x00] byte by byte
        default_sequence = [0x0b, 0x08, 0x00]
        for byte in default_sequence:
            time.sleep(2)
            write_ser(bytes([byte]))
            print("Successfully sent value:", bytes([byte]))
            while outgoing_serial.in_waiting:
                read_data = outgoing_serial.read(outgoing_serial.in_waiting)
                print("Received data:", read_data)


    send_default_sequence()


    def start_stream_task():
        t = threading.Thread(target=start_stream)
        t.start()


    start_button = tk.Button(root, text="Start Stream", command=start_stream_task)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop Stream", command=stop_stream)
    stop_button.pack()

    root.mainloop()

else:
    print("Failed to initialize COM5 or port is not open")
