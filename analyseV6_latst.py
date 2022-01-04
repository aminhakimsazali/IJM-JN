import pandas as pd
import math
import numpy as np
from pandas import Timedelta
from math import sqrt
from sklearn.metrics import mean_squared_error
from scipy.signal import find_peaks
import json
import os
import datetime as dt
import time
from shapely.geometry import Point, Polygon
import warnings
import requests
warnings.filterwarnings('ignore')


def mps_to_kmph(mps):
    return (3.6 * mps)

def plot_chart_one_by_one(df, start_time, end_time, mode =  1, x_min = -10, x_max = 20, y_min = 0, y_max = 20):
    temp_df = df.set_index("Time")
    all_x = []
    all_y = []
    count = 0
    velo_list = []
    
    lol = temp_df.between_time(start_time.split(" ")[1],  end_time.split(" ")[1])
    lol['PC Counts'] = [len(each) for each in lol['Coordinates']]
    return lol


def plot_chart_one(df, start_time, end_time, mode =  2,  x_min = -10, x_max = 20, y_min = 0, y_max = 20):
    temp_df = df.set_index("Time")
    all_x = []
    all_y = []
    count = 0
    velo_list = []
    
    for freq in pd.date_range(start=start_time, end=end_time, freq = "S"):
        time_range_df = temp_df.between_time( freq.time(),  ((freq + Timedelta(seconds = 1)).time()))
        for index , (time_ , row) in enumerate(time_range_df.iterrows()):
            velo = row['Velocity']
    #         velo_list = [velos for velos in velo]
            for velos in velo:
    #             print(velos)
                velo_list.append(velos)
            coor = row['Coordinates']
            x_coor = []
            y_coor = []
            x_coor = [x for x,y in coor]
            y_coor = [y for x,y in coor]

            #append x coordinates
            all_x += x_coor
            all_y += y_coor

    if mode == 1:        
        title = freq.strftime("%d-%m-%Y %H-%M-%S")
    elif mode == 2:
        title = start_time + " to " + end_time

    print(f"{title}\t PC Counts: {len(all_x)}")
    print("Average Velocity", mps_to_kmph(np.mean(velo_list)))
    if len(all_x)!= 0 and len(all_y) != 0:
        print(f"Min X: {min(all_x)}, Max X: {max(all_x)}, Min y: {min(all_y)}, Max Y: {max(all_y)}")

    all_x = []
    all_y = []
    velo_list = []
    
    lol = temp_df.between_time(start_time.split(" ")[1],  end_time.split(" ")[1])
    print(start_time, end_time)
    print(lol)
    lol['PC Counts'] = [len(each) for each in lol['Coordinates']]
    return lol


def read_raw_data(file):
    
    data_file = file
    # Delimiter
    data_file_delimiter = ','

    # The max column count a line in the file could have
    largest_column_count = 0

    # Loop the data lines
    with open(data_file, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(data_file_delimiter)) + 1

            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    # Close file
    temp_f.close()

    # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
    column_names = [i for i in range(0, largest_column_count)]

    # Read csv
    df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)
    df.dropna(axis = 1, how = 'all', inplace = True) #drop columns with no data
    return df

def process_df(df):
    preprocessed_data = []
    for index, row in df.iterrows():
        time_count = row[0]
        data =  eval(row[1])

        coordinates = []
        velocities = []

        A_Zone_count = 0
        B_Zone_count = 0
        C_Zone_count = 0

        for j in range(len(eval(row[1]))):
            x = 0
            y = 0

            range_ = data[j][0]
            azimuth = data[j][1]
            elevation = data[j][2]
            velocity = data[j][3]

            # point Struct:
            #     range:    float   #Range in meters
            #     azimuth:  float   #Azimuth in radians
            #     elevation: float  #Elevation in radians
            #     velocity:  float   #Doppler in m/s

            #     V6 =: [(range,azimuth,elevation,velocity),......]

            # Based on IWR6843 3D(r,az,el) -> (x,y,z)
            # el: elevation φ <Theta bottom -> Obj    
            # az: azimuth   θ <Theta Obj ->Y Axis 

            # z = r * sin(φ)
            # x = r * cos(φ) * sin(θ)
            # y = r * cos(φ) * cos(θ)

            # z = r * sin(el)
            # x = r * cos(el) * sin(az)
            # y = r * cos(e1) * cos(az)
            
            z = range_ * math.sin(elevation)
            x = range_ * math.cos(elevation) * math.sin(azimuth)
            y = range_ * math.cos(elevation) * math.cos(azimuth)
            coordinates.append([x,y])

            cur_point = Point(x,y)
            velocities.append(velocity)

        preprocessed_data.append([time_count,coordinates, velocities])
    preprocess_data_df = pd.DataFrame(preprocessed_data, columns = ['Time',"Coordinates", "Velocity"])
    return preprocess_data_df        


def vehicle_counting(file,  lane, counting_threshold, duration_sampling, classification_threshold):
    df = read_raw_data(file)
    df[0] = pd.to_datetime(df[0],format='%d %m %Y %H:%M:%S.%f')  
    df.dropna(how='all', inplace = True)


    # Process data to get x,y,z coordinates of point clouds
    preprocess_data_df = process_df(df)

    start_time = df[0].iloc[0].strftime("%Y-%m-%d %H:%M:%S")
    end_time = df[0].iloc[-1].strftime("%Y-%m-%d %H:%M:%S")

    print(start_time, end_time)

    dfA = plot_chart_one(preprocess_data_df, start_time, end_time, mode =  2)

    # Remove PC outside of secified lane 
    coor_all = []
    for coor in dfA['Coordinates'].values:
        coor_list = []
        for x,y in coor:
            #LANE 2
            if lane == 2 and x >= -4.0 and x <= 1 and y > 0 and y <= 15:
                coor_list.append([x,y])
            #LANE 3
            if lane == 3 and  x >= 1 and x <= 4.5 and y >= 0 and y <= 15:
                coor_list.append([x,y])
        coor_all.append(coor_list)

    dfA['Coordinates'] = coor_all
    dfA['PC Counts'] = [len(each) for each in dfA['Coordinates']]


    #Extract All Xs, Ys
    all_x = []
    all_y = []
    for coor in dfA['Coordinates'].values:
        for x,y in coor :
            all_x.append(x)
            all_y.append(y)

    print(dfA.head())
    start_time = start_time.split(" ")[1] #"17:22:00"
    end_time = end_time.split(" ")[1]  #"17:49:00"

    dfA['Total Point Cloud'] = [len(each) for each in dfA.Coordinates]
    newDF = dfA.reset_index().resample(duration_sampling, on = 'Time').sum()
    results = []

    for freq in pd.date_range(start=start_time, end=end_time, freq = "min")[:-1]:
        time_range_df = newDF.between_time( freq.time(),  ((freq + Timedelta(minutes = 1)).time()))
    #     print(time_range_df.head())
        print("----------------------------------------------")
        peaks = find_peaks(time_range_df['Total Point Cloud'], height=counting_threshold) # Lane 2
        
        # if lane == 2:
        #     peaks = find_peaks(time_range_df['Total Point Cloud'], height=14) # Lane 2
        # elif lane == 3:
        #     peaks = find_peaks(time_range_df['Total Point Cloud'], height=3) # Lane 3


        predict = len(peaks[0])
        peaks_time = time_range_df.reset_index().iloc[peaks[0]].Time.values
        print(freq, predict)
        results.append([freq, predict, peaks, peaks_time])
        time_range_df = None

    time_range_df = dfA.between_time( start_time, end_time)   
    predictDF = pd.DataFrame(results, columns = ['Timestamp', 'Count', 'Peaks', 'Peak Timestamp'])
    predictDF['Time'] = predictDF.Timestamp.dt.strftime("%Y-%m-%d %H:%M:%S")

    # for index, row in predictDF.iterrows():
    #     date = row['Time']
    #     date = date.replace(" ", "%20")
    #     count = row['Count']
    #     vehicleType = 1
    #     # req = f"https://398z9ptvcg.execute-api.ap-southeast-1.amazonaws.com/Deployement/insertIJM?count={count}&vehicleType={vehicleType}&timestamp={date}"
    #     # time.sleep(1)
    #     # res = requests.get(req)
    #     # print(res)

    print(f"\t\tSmall Count\tBig Count")
    vehicle_classification = []
    for index, row in predictDF.iterrows():

        peaks = row['Peaks'][1]['peak_heights']
        smallCount = 0
        bigCount = 0
        for peak in peaks:
            if peak >= classification_threshold : #100 as the threshold to differentiate small and big vehicle
                bigCount+=1
            else:
                smallCount+=1

        date = row['Time']
        date = date.replace(" ", "%20")
        count = row['Count']
        vehicleType = 1 #Small vehicle
        req = f"https://398z9ptvcg.execute-api.ap-southeast-1.amazonaws.com/Deployement/insertIJM?count={smallCount}&vehicleType={vehicleType}&timestamp={date}"
        # time.sleep(1)
        # res = requests.get(req)
        # print(res)

        vehicleType = 2 #Big Vehicle
        req = f"https://398z9ptvcg.execute-api.ap-southeast-1.amazonaws.com/Deployement/insertIJM?count={bigCount}&vehicleType={vehicleType}&timestamp={date}"
        # time.sleep(1)
        # res = requests.get(req)
        # print(res)

        vehicle_classification.append([row['Time'], smallCount, bigCount])

    print("vehicle_classification\n\n", vehicle_classification)


if __name__ == '__main__':
    with open("config.json") as f:
            data = json.load(f)

    highest_index = 0
    for file in os.listdir("./"):
        if file.startswith("v6 data") and file.endswith('.csv'):
            file = file.replace("v6 data", "")
            file = file.replace(".csv", "")
            if int(file) > highest_index:
                highest_index = int(file)
    print("highest_index: ", highest_index)

    # f"v6 data {highest_index -1}.csv"
    # vehicle_counting(file = f"v6 data {highest_index -1}.csv", lane = 3, counting_threshold = 2 , duration_sampling = "0.2S" , classification_threshold = 40) # Lane 3
    # vehicle_counting(file = f"v6 data {highest_index -1}.csv", lane = 2, counting_threshold = 23 ,duration_sampling = "0.5S" ,  classification_threshold = 100) #Lane 2


    vehicle_counting(file = "v6 data 2084.csv", lane = 3, counting_threshold = 2 , duration_sampling = "0.2S" , classification_threshold = 40) # lane 3
    vehicle_counting(file = "v6 data 2084.csv", lane = 2, counting_threshold = 23 ,duration_sampling = "0.5S" ,  classification_threshold = 100 ) # lane 2
