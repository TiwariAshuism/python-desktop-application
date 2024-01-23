import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pylsl
import csv

# Basic parameters for the plotting window
plot_duration_eeg = 5
plot_duration_imu = 5
update_interval = 50
pull_interval = 500

received_data_eeg = []
received_data_imu = []


# Define a function to save the data to CSV
def save_data_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


# Define a function for the save button
def save_data(_):
    save_data_to_csv('eeg_data.csv', received_data_eeg)
    save_data_to_csv('imu_data.csv', received_data_imu)
    print("Data saved successfully!")


class DataInlet:
    def __init__(self, info, channel_count, plot_duration):
        self.inlet = pylsl.StreamInlet(info, max_buflen=plot_duration,
                                       processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.buffer = np.zeros((channel_count, plot_duration * int(info.nominal_srate())))
        self.channel_count = channel_count

    def pull_data(self):
        chunk, ts = self.inlet.pull_chunk(timeout=0.0)
        if ts:
            ts = np.asarray(ts)
            y = np.asarray(chunk).T

            buffer_length = self.buffer.shape[1]
            if y.shape[1] > buffer_length:
                y = y[:, -buffer_length:]  # Truncate incoming data to fit buffer length

            self.buffer[:, :-y.shape[1]] = self.buffer[:, y.shape[1]:]
            self.buffer[:, -y.shape[1]:] = y

    def get_data(self):
        return self.buffer


def is_eeg_stream(info):
    return info.name() == 'EEG'


def is_imu_stream(info):
    return info.name() == 'IMU'


def plot_data(frame):
    all_eeg_data = []
    for inlet in eeg_inlets:
        inlet.pull_data()
        all_eeg_data.append(inlet.get_data())

    all_imu_data = []
    for inlet in imu_inlets:
        inlet.pull_data()
        all_imu_data.append(inlet.get_data())

    artists = []

    # Plotting EEG data
    if all_eeg_data:
        for eeg_data in all_eeg_data:
            for i in range(eeg_data.shape[0]):
                lines = ax_eeg.plot(np.linspace(0, plot_duration_eeg, eeg_data.shape[1]), eeg_data[i], alpha=0.8)
                artists.extend(lines)

    # Plotting IMU data
    if all_imu_data:
        for imu_data in all_imu_data:
            for i in range(imu_data.shape[0]):
                lines = ax_imu.plot(np.linspace(0, plot_duration_imu, imu_data.shape[1]), imu_data[i], alpha=0.8)
                artists.extend(lines)

    return artists


def main():
    global ax_eeg, ax_imu, eeg_inlets, imu_inlets

    eeg_inlets = []
    imu_inlets = []

    streams = pylsl.resolve_streams()
    for info in streams:
        if is_eeg_stream(info):
            inlet = DataInlet(info, info.channel_count(), plot_duration_eeg)
            eeg_inlets.append(inlet)
        elif is_imu_stream(info):
            inlet = DataInlet(info, info.channel_count(), plot_duration_imu)
            imu_inlets.append(inlet)

    fig, (ax_eeg, ax_imu) = plt.subplots(1, 2, figsize=(12, 6))

    save_button_ax = fig.add_axes([0.8, 0.9, 0.1, 0.05])  # Define the position and size of the button
    save_button = plt.Button(save_button_ax, 'Save')
    save_button.on_clicked(save_data)

    anim = animation.FuncAnimation(fig, plot_data, frames=None, interval=update_interval, blit=True)

    plt.show()


if __name__ == '__main__':
    main()
