import csv
import os
from scipy.signal import butter, filtfilt
import numpy as np

### This Python script will extract the 3ms clip value from a Radioss Head Impact analysis results file
### Radioss will output the time history data as T01 binary file.
### This will need to be converted to a .csv file using the th_to_csv converter provided with OpenRadioss
### This script was intended to be invoked automatically in the directory containing the T01.csv file
###   Therefore no arguments are supplied: the script takes the cwd and locates the file "DynaOptT01.csv" in the directory
###   - It will extract the three columns in the .csv relating to the accelerometer output and write those as separate .csv files
###   - It will filter those three outputs with a cfc1000 filter
###   - It will combine the 3 acceleration components to obtain the acceleration magnitude
###   - It will scale the acceleration magnitude from mm s-2 to g
###   - It will obtain the 3ms clip value and write it to the file "response_IHI3ms.res"
###      - the "3ms clip" is the highest acceleration level that is exceeded for 3ms continuously
###

# Function to read a specific column from a CSV file and write it to a new CSV file
def extract_column(T01csv_file_path, column_index):
    with open(T01csv_file_path, 'r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        new_file_path = f"{T01csv_file_path.split('.csv')[0]}_{column_index}.csv"
        with open(new_file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([headers[0], headers[column_index]])
                
            for row in reader:
                writer.writerow([row[0], row[column_index]])
            
            # Reset the reader to the beginning of the file for the next column
            #infile.seek(0)
            #next(reader)

# Function to apply a CFC filter
def apply_cfc_filter(data, cfc_class):
    # Define the CFC filter parameters based on the class
    cfc_params = {
        60: 100,    # Hz
        180: 300,   # Hz
        600: 1000,  # Hz
        1000: 1650  # Hz
    }
    
    if cfc_class not in cfc_params:
        raise ValueError("Unsupported CFC class")
    
    cutoff_freq = cfc_params[cfc_class]
    nyquist_freq = 0.5 * 10000  # Assuming a sampling rate of 10,000 Hz
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(4, normal_cutoff, btype='low', analog=False)  # Digital filter
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Function to read specific columns from a CSV file and apply CFC filter
def process_csv(file_path, cfc_class):
    time = []
    y_data = []
    
    with open(file_path, 'r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        for row in reader:
            time.append(float(row[0]))
            y_data.append(float(row[1]))
    
    # Apply CFC filter to the y_data
    filtered_y_data = apply_cfc_filter(y_data, cfc_class)
    
    # Write the filtered data to a new CSV file
    new_file_path = f"{file_path.split('.csv')[0]}_CFC{cfc_class}.csv"
    with open(new_file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([headers[0], headers[1]])
        for t, y in zip(time, filtered_y_data):
            writer.writerow([t, y])

# Function to read the filtered CSV files and calculate the acceleration magnitude
def calculate_magnitude(file_paths,new_file_path):
    time = []
    acc_x = []
    acc_y = []
    acc_z = []
    
    # Read the data from the filtered CSV files
    for i, file_path in enumerate(file_paths):
        with open(file_path, 'r') as infile:
            reader = csv.reader(infile)
            headers = next(reader)
            
            if i == 0:
                for row in reader:
                    time.append(float(row[0]))
                    acc_x.append(float(row[1]))
            elif i == 1:
                for row in reader:
                    acc_y.append(float(row[1]))
            elif i == 2:
                for row in reader:
                    acc_z.append(float(row[1]))
    
    # Convert lists to numpy arrays
    acc_x = np.array(acc_x)
    acc_y = np.array(acc_y)
    acc_z = np.array(acc_z)
    
    # Calculate the magnitude of the acceleration vector
    magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
    
    # Write the magnitude to a new CSV file
    with open(new_file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Time', 'Acceleration Magnitude'])
        for t, mag in zip(time, magnitude):
            writer.writerow([t, mag])

# Function to scale the acceleration magnitude from mm/s^2 to g and write to a new CSV file
def scale_acceleration(file_path, output_file):
    time = []
    magnitude = []
    
    # Read the data from the CSV file
    with open(file_path, 'r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        for row in reader:
            time.append(float(row[0]))
            magnitude.append(float(row[1]))
    
    # Scale the acceleration magnitude from mm/s^2 to g
    magnitude = [m / 9810 for m in magnitude]
    
    # Write the scaled data to a new CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([headers[0], 'Scaled ' + headers[1]])
        for t, mag in zip(time, magnitude):
            writer.writerow([t, mag])

# Function to read the filtered CSV file and calculate the 3ms clip value
def calculate_3ms_clip(file_path, sampling_rate=10000):
    time = []
    magnitude = []
    
    # Read the data from the CSV file
    with open(file_path, 'r') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        for row in reader:
            time.append(float(row[0]))
            magnitude.append(float(row[1]))
    
    # Convert lists to numpy arrays
    time = np.array(time)
    magnitude = np.array(magnitude)
    
    # Calculate the number of samples in a 3ms window
    window_size = int(0.003 * sampling_rate)
    
    max_clip_value = -np.inf
    
    # Sweep the 3ms window over the entire dataset
    for start in range(len(time) - window_size + 1):
        end = start + window_size
        window_min = np.min(magnitude[start:end])
        if window_min > max_clip_value:
            max_clip_value = window_min
    
    return max_clip_value

# Function to write the 3ms clip value to a file
def write_clip_value_to_file(clip_value, output_file):
    with open(output_file, 'w') as file:
        file.write(f'{clip_value}\n')

# Arguments:
results_folder = os.getcwd()
T01csv_file_path = os.path.join(results_folder,"DynaOptT01.csv")
column_indices = [751, 752, 753]  # Columns to extract
for column_index in column_indices:
    extract_column(T01csv_file_path, column_index)

cfc_class = 1000  # CFC class (e.g., 60 or 180)
for column_index in column_indices:
    file_path = f"{T01csv_file_path.split('.csv')[0]}_{column_index}.csv"
    process_csv(file_path, cfc_class)

file_paths = [f"{T01csv_file_path.split('.csv')[0]}_{column_indices[0]}_CFC{cfc_class}.csv", f"{T01csv_file_path.split('.csv')[0]}_{column_indices[1]}_CFC{cfc_class}.csv", f"{T01csv_file_path.split('.csv')[0]}_{column_indices[2]}_CFC{cfc_class}.csv"]
new_file_path = f"{T01csv_file_path.split('.csv')[0]}_acc_mag.csv"
calculate_magnitude(file_paths,new_file_path)

file_path = f"{T01csv_file_path.split('.csv')[0]}_acc_mag.csv"
output_file = f"{file_path.split('.csv')[0]}_g.csv"
scale_acceleration(file_path, output_file)

file_path = f"{T01csv_file_path.split('.csv')[0]}_acc_mag_g.csv"
output_filename = "response_IHI3ms.res"
clip_value = calculate_3ms_clip(file_path)
output_file = os.path.join(results_folder,output_filename)
write_clip_value_to_file(clip_value, output_file)
