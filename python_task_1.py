#!/usr/bin/env python
# coding: utf-8

# PYTHON TASK 1

# In[88]:


#Question 1: Car Matrix Generation

import pandas as pd

def generate_car_matrix(dataframe):
    
    car_matrix = dataframe.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
   
    for i in range(min(car_matrix.shape)):
        car_matrix.iloc[i, i] = 0
    
    return car_matrix


file_path = 'dataset-1.csv'


data = pd.read_csv(file_path)
car_result_matrix = generate_car_matrix(data)
print(car_result_matrix)


#The provide code generates a matrix from a DataFrame by pivoting 'id_1' and 'id_2', filling with 'car' values, then setting diagonal values to 0.


# In[77]:


#Question 2: Car Type Count Calculation
import pandas as pd

def get_type_count(dataframe):
   
    dataframe['car_type'] = pd.cut(dataframe['car'],
                                   bins=[float('-inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'])
    
    
    type_counts = dataframe['car_type'].value_counts().to_dict()
    
    
    sorted_type_counts = dict(sorted(type_counts.items()))
    
    return sorted_type_counts
file_path = 'dataset-1.csv'

data = pd.read_csv(file_path)

type_count_result = get_type_count(data)
print(type_count_result)


# In[78]:


#Question 3: Bus Count Index Retrieval
import pandas as pd

def get_bus_indexes(dataframe):
    mean_bus = dataframe['bus'].mean()
    bus_indexes = dataframe[dataframe['bus'] > 2 * mean_bus].index.tolist()
    
    bus_indexes.sort()
    
    return bus_indexes
file_path = 'dataset-1.csv'

data = pd.read_csv(file_path)

resulting_indexes = get_bus_indexes(data)
print("Indices where 'bus' values are greater than twice the mean:", resulting_indexes)


# In[79]:


#Question 4: Route Filtering
import pandas as pd

def filter_routes(dataframe):
    route_avg_truck = dataframe.groupby('route')['truck'].mean()
    
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    filtered_routes.sort()
    
    return filtered_routes
file_path = 'dataset-1.csv'

data = pd.read_csv(file_path)
filtered_route_list = filter_routes(data)
print("Routes with average 'truck' values greater than 7:", filtered_route_list)


# In[80]:


#Question 5: Matrix Value Modification

import pandas as pd

def multiply_matrix(input_data):
    if isinstance(input_data, list):
        modified_df = pd.DataFrame(input_data)
    elif isinstance(input_data, pd.DataFrame):
        modified_df = input_data.copy()
    else:
        raise ValueError("Input should be a list or a Pandas DataFrame")
    
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    modified_df = modified_df.round(1)
    
    return modified_df

modified_result_df = multiply_matrix(filtered_route_list)
print(modified_result_df)



# In[102]:


#Question 6: Time Check
import pandas as pd

def verify_timestamp_completeness(dataframe):
    dataframe['start_timestamp'] = pd.to_datetime(dataframe['startDay'] + ' ' + dataframe['startTime'])
    dataframe['end_timestamp'] = pd.to_datetime(dataframe['endDay'] + ' ' + dataframe['endTime'])
    completeness_check = dataframe.groupby(['id', 'id_2']).apply(
        lambda x: (
            x['start_timestamp'].min().date() == x['end_timestamp'].max().date() - pd.DateOffset(days=1) and
            set(x['start_timestamp'].dt.day_name()) == set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        )
    )
    
    return completeness_check

data = pd.read_csv('dataset-2.csv')


print(completeness_check)


# In[ ]:




