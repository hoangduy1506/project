import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

# Đọc file và parse data
file_path = "D:\\git\\project\\01_python\\01_dist_n_angle\\00_data\\storeDataCalculated.csv"
df = pd.read_csv(file_path)
num_rows, num_columns = df.shape

total_index = 3201
theta_ = 40
index_io = math.ceil(40 * total_index / 360)
print(index_io)

the0 = df['Degree0']
x0 = df['XCoordinate0'].to_numpy()
y0 = df['YCoordinate0'].to_numpy()
z0 = df['ZCoordinate0'].to_numpy()

the1 = df['Degree1']
x1 = df['XCoordinate1'].to_numpy()
y1 = df['YCoordinate1'].to_numpy()
z1 = df['ZCoordinate1'].to_numpy()

array_1 = [1] * 3201

# Ghép hai mảng thành một ma trận
P1 = np.vstack((x1, y1, z1, array_1))
P0 = np.vstack((x0, y0, z0, array_1))

the = math.radians(40)
tx = 17
ty = -43

# Ma trận chuyển đổi đồng nhất
matrix_T = [
    [np.cos(the),   -(np.sin(the)), 0,  tx],
    [np.sin(the),   np.cos(the),    0,  ty],
    [0,             0,              1,  0],
    [0,             0,              0,  1]
]
matrix_T = np.array(matrix_T)

sample = P1[:,600]
print(sample)
result = np.dot(matrix_T, sample)
print(result)

Pnew = np.dot(matrix_T, P1)

# Trích xuất tọa độ x và y từ ma trận
x_coords = Pnew[0, :]  # Hàng 0 là tọa độ x
y_coords = Pnew[1, :]  # Hàng 1 là tọa độ y

print("Abs X0 - X_C = ", abs(x0[600+index_io]-x_coords[600]))

fig, ax = plt.subplots(1, 1)

ax.scatter(x0,y0,s=0.1,c='green')
ax.scatter(x1, y1, s=0.1, c = 'red')
ax.scatter(x_coords, y_coords, s=0.1, c = 'blue')
ax.scatter(0, 0, s=30, c = 'red')
ax.set_xlim(-400, 400)
ax.set_ylim(-400, 400)

plt.show()