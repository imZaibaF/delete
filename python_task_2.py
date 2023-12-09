#!/usr/bin/env python
# coding: utf-8

# PYTHON TASK 2

# In[1]:


#QUESTION 1: Distance Matrix Calculation
import pandas as pd

def calculate_distance_matrix(dataframe):
    
    distances = dataframe.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    

    distance_matrix = pd.DataFrame(distances.values, index=distances.index, columns=distances.columns)
    
    
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)
    
    
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0
    
  
    for col in distance_matrix.columns:
        for row in distance_matrix.index:
            for intermediate in distance_matrix.index:
                if distance_matrix.at[row, col] == 0 and row != col:
                    if distance_matrix.at[row, intermediate] != 0 and distance_matrix.at[intermediate, col] != 0:
                        distance_matrix.at[row, col] = distance_matrix.at[row, intermediate] + distance_matrix.at[intermediate, col]
    
    return distance_matrix


data = pd.read_csv('dataset-3.csv')


distance_matrix = calculate_distance_matrix(data)
print(distance_matrix)



# In[2]:


# Question 2: Unroll Distance Matrix

import itertools
import pandas as pd

def unroll_distance_matrix(distance_matrix):
    
    indices = distance_matrix.index
    
   
    combinations = list(itertools.permutations(indices, 2))
    
 
    unrolled_data = []
    
   
    for pair in combinations:
        id_start, id_end = pair
        distance = distance_matrix.at[id_start, id_end]
        unrolled_data.append([id_start, id_end, distance])
    
    
    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    
    return unrolled_df


unrolled_distance_df = unroll_distance_matrix(distance_matrix)
print(unrolled_distance_df)



# In[4]:


#Question 3: Finding IDs within Percentage Threshold


def find_ids_within_ten_percentage_threshold(distance_df, reference_value):
    
    reference_avg_distance = distance_df[distance_df['id_start'] == reference_value]['distance'].mean()
    
    threshold_range = reference_avg_distance * 0.1
    

    within_threshold = distance_df[
        (distance_df['id_start'] != reference_value) &
        (distance_df['distance'] >= reference_avg_distance - threshold_range) &
        (distance_df['distance'] <= reference_avg_distance + threshold_range)
    ]['id_start'].unique().tolist()
    

    within_threshold.sort()
    
    return within_threshold


reference_id_start = 123  
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_distance_df, reference_id_start)
print("Values within 10% threshold of reference value's average distance:", result_within_threshold)



# In[5]:


#Question 4: Calculate Toll Rate

def calculate_toll_rate(distance_df):
    
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    # Calculate toll rates for each vehicle type based on distance and rate coefficients
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        distance_df[vehicle_type] = distance_df['distance'] * rate_coefficient
    
    return distance_df


distance_df_with_rates = calculate_toll_rate(unrolled_distance_df)
print(distance_df_with_rates)



# In[6]:


#Question 5: Calculate Time-Based Toll Rates


import pandas as pd
from datetime import datetime, timedelta

def calculate_time_based_toll_rates(dataframe):
    
    dataframe['startTime'] = pd.to_datetime(dataframe['startTime'])
    dataframe['endTime'] = pd.to_datetime(dataframe['endTime'])
    
    
    day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    for index, row in dataframe.iterrows():
        start_day = row['startTime'].dayofweek
        end_day = row['endTime'].dayofweek
        
       
        dataframe.at[index, 'startTay'] = day_map[startDay]
        dataframe.at[index, 'endDay'] = day_map[endDay]
        
        
        weekday_intervals = [
            (datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('10:00:00', '%H:%M:%S').time()),
            (datetime.strptime('10:00:00', '%H:%M:%S').time(), datetime.strptime('18:00:00', '%H:%M:%S').time()),
            (datetime.strptime('18:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time())
        ]
        weekend_intervals = [(datetime.strptime('00:00:00', '%H:%M:%S').time(), datetime.strptime('23:59:59', '%H:%M:%S').time())]
        
        if startDay < 5:  
            for interval in weekday_intervals:
                startTime = interval[0]
                endTime = interval[1]
                
                if startTime <= row['startTime'].time() < endTime:
                    discount_factor = 0.8 if start_time == datetime.strptime('00:00:00', '%H:%M:%S').time() or endTime == datetime.strptime('23:59:59', '%H:%M:%S').time() else 1.2
                    for vehicle_col in ['moto', 'car', 'rv', 'bus', 'truck']:
                        dataframe.at[index, vehicle_col] *= discount_factor
        else:  
            for interval in weekend_intervals:
                startTime = interval[0]
                endTime = interval[1]
                if startTime <= row['startTime'].time() < endTime:
                    for vehicle_col in ['moto', 'car', 'rv', 'bus', 'truck']:
                        dataframe.at[index, vehicle_col] *= 0.7
    
    return dataframe



# In[ ]:




