import numpy as np

def anomaly_detection(data, threshold):
  # calculate the mean and standard deviation of the data
  mean = np.mean(data)
  std = np.std(data)
  
  # define the threshold for detecting an anomaly
  # based on the standard deviation of the data
  anomaly_threshold = threshold * std
  
  # initialize a list to store the anomalies
  anomalies = []
  
  # iterate through the data and detect anomalies
  for i in range(len(data)):
    if abs(data[i] - mean) > anomaly_threshold:
      anomalies.append(data[i])
      
  return anomalies

# example usage
data = [10, 12, 14, 11, 10, 11, 15, 16, 11, 10, 100]
anomalies = anomaly_detection(data, 2)
print(anomalies)