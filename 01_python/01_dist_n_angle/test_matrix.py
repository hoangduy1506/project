import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Đọc file và parse data
file_path = "D:\\git\\project\\01_python\\01_dist_n_angle\\00_data\\test.csv"
df = pd.read_csv(file_path)

total_index = 73
theta_ = 40
index_io = math.ceil(40 * total_index / 360)

x0 = df['XCoordinate0'].to_numpy()
y0 = df['YCoordinate0'].to_numpy()
z0 = df['ZCoordinate0'].to_numpy()

x1 = df['XCoordinate1'].to_numpy()
y1 = df['YCoordinate1'].to_numpy()
z1 = df['ZCoordinate1'].to_numpy()

P1 = np.vstack((x1, y1, z1, [1]*len(x1)))
P0 = np.vstack((x0, y0, z0, [1]*len(x0)))
P0_new = np.vstack(([0]*len(x1),[0]*len(x1),[0]*len(x1),[0]*len(x1)))

for i in range(total_index):
    
    if(i + index_io) >= total_index:
        print(i + index_io, i + index_io - total_index)
        P0_new[:,i] = P0[:,i + index_io - total_index]
    else:
        print(i + index_io)
        P0_new[:,i] = P0[:,i + index_io]
    print(i, P0[:,i], P0_new[:,i])


