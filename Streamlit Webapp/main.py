import csv
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

array = []
with open('AEP_hourly_data.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    array.append(row)


array = array[24:]
array = [[i[0][-8:], float(i[1])] for i in array]

array = [[1 + 4 * int(i[0][:2]), i[1]] for i in array]
array1 = []
element = []

for i in array:
  element.append(i)
  if i[0] == 93:
    array1.append(element)
    element = []

output_array = []

for i in array1:
  if len(i) == 24: # Remove days which do not have the data of all days (31 such days exist)
    output_array.append(i)

array = output_array
x, y = [], []
for day in array:
  element_x = []
  element_y = []
  for block in day:
    element_x.append(block[0])
    element_y.append(block[1])
  x.append(element_x)
  y.append(element_y)

y = np.array(y)
y = 150 + (y / np.amax(y)) * 50
y = y.tolist()
def plotting_function(ind):
  global x, y
  fig = plt.figure(figsize=(12, 5))
  plt.grid(True)
  plt.xlabel("Block Number")
  plt.ylabel("Actual Generation (AG)")
  plt.plot(x[ind], y[ind])
  st.pyplot(fig)

plotting_function(6)

def polynomial_regression(X, Y, N):

  input_matrix = [] # Square matrix of order (N+1)
  k = 0
  for i in range(N+1):
    input_matrix.append([sum(X ** (i + j)) for j in range(N+1)])
    k += 1
  
  input_matrix = np.array(input_matrix)

  output_matrix = []
  for i in range(N+1):
    output_matrix.append([sum(Y * (X ** i))])
  
  output_matrix = np.array(output_matrix)

  parameter_matrix = np.matmul(np.linalg.inv(input_matrix), output_matrix)
  
  def regression_function(X_i):
    total = 0
    for i in range(len(parameter_matrix)):
      total += (X_i ** i) * parameter_matrix[i]

    return total

  return regression_function

def train_test_split(arr, percent):
  """Splits an array into train and test set)"""
  L = len(arr) - 1
  last = int(L * percent / 100)
  return (arr[:last]), (arr[last:])

x_train, x_test = train_test_split(x, 20)
y_train, y_test = train_test_split(y, 20)
x_train, y_train = np.array(x_train), np.array(y_train)
x_train, y_train = x_train.flatten(), y_train.flatten()
regression = [polynomial_regression(x_train, y_train, i) for i in range(10)]
x_test, y_test = np.array(x_test), np.array(y_test)

def prediction(test_day, degree):
  #print(x_test[test_day])
  fig = plt.figure(figsize=(12, 5))
  bk=regression[degree](x_test[test_day])
  plt.plot(x_test[test_day], bk)
  plt.plot(x_test[test_day], y_test[test_day])
  plt.grid(True)
  plt.legend(["Predicted Value", " Actual Value"])
  plt.xlabel("Block Number")
  plt.ylabel("Actual Generation (MW)")
  #plt.show()
  st.pyplot(fig)

prediction(0, 4)