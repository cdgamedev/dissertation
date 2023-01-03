import numpy as np
import csv
import time

def sd_anomaly_detection(costs, data, threshold):
    # calculate the mean and standard deviation of the data
    mean = np.mean(costs)
    std = np.std(costs)
    
    # define the threshold for detecting an anomaly
    # based on the standard deviation of the data
    anomaly_threshold = threshold * std
    
    # initialize a list to store the anomalies
    anomalies = []
    
    # iterate through the data and detect anomalies
    for i in range(len(data)):
        if abs(data[i]["Cost"] - mean) > anomaly_threshold:
            anomalies.append(data[i]["ID"])
        
    return anomalies

# function to parse the gems from ids
def parse_from_id(gem_id, all_data):
    # get the selected gem
    gem = all_data[gem_id - 1]
    
    # get the gem information
    id = gem['ID']
    page = gem['Page']
    entry_no = gem['EntryNo']
    level = gem['Level']
    tier = gem['Tier']
    gem_type = gem['GemType']
    cost = gem['Cost']
    date = gem['Date']
    
    # return the gem data
    return r"{0},{1},{2},{3},{4},{5},{6},{7}".format(
        id, page, entry_no, level, tier, gem_type, cost, date
    )

# open the dataset file
with open('Dataset 1 - 08.09.2022.csv', newline='') as csvfile:
    # parse the data to a dict
    data_reader = csv.DictReader(csvfile, delimiter=',')
    # create a list for all the data
    all_data = []
    
    # store data, in a dict (separated by GemType)
    data = {}
    # store costs, in a dict (separated by GemType)
    costs = {}
    
    # for each row in the data
    for row in data_reader:
        # add the row to all data
        all_data.append(row)
        
        # if the gem type is not in the data yet
        # add the gem type to the data and costs dicts
        if (not row['GemType'] in data):
            data[row['GemType']] = []
            costs[row['GemType']] = []
            
        # add the gem cost to the array for that GemType
        costs[row['GemType']].append(int(row['Cost']))
        
        # add the gem id and cost to the array for that GemType
        data[row['GemType']].append({
            "ID": int(row['ID']),
            "Cost": int(row['Cost'])
        })
    
    for i in range(10):
        # total number of anomalies
        total_anomalies = 0
        
        output = open('anomalies.csv', "w+")
        output.write("ID,Page,EntryNo,Level,Tier,GemType,Cost,Date\n")
        start = time.time()
        
        # for each key in data
        for i in data:
            # detect anomalies in the cost and data with a threshold of 2
            anomalies = sd_anomaly_detection(costs[i], data[i], 2)
            # for each anomaly in anomalies
            for anomaly in anomalies:
                # get the gem info in the form of a string
                gem_info = parse_from_id(anomaly, all_data)
                output.write(gem_info + "\n")
                # increment the total number of anomalies
                total_anomalies = total_anomalies + 1
                
        end = time.time()
        
        total_time = end - start
        print("Computation took " + str(total_time))
        
        output.close()
        # print the total number of anomalies
        print(r"Total Anomalies: {0}".format(total_anomalies))