import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.optimize import least_squares
from sklearn.neighbors import LocalOutlierFactor
from scipy import stats

# Đọc file và parse data
file_path = "D:\\git\\project\\01_python\\01_dist_n_angle\\00_data\\storeDataCalculated.csv"
df = pd.read_csv(file_path)
num_rows, num_columns = df.shape

total_index = 3201

the0 = df['Degree0']
x0 = df['XCoordinate0'].to_numpy()
y0 = df['YCoordinate0'].to_numpy()
z0 = df['ZCoordinate0'].to_numpy()

the1 = df['Degree1']
x1 = df['XCoordinate1'].to_numpy()
y1 = df['YCoordinate1'].to_numpy()
z1 = df['ZCoordinate1'].to_numpy()

def shift_arr(arr ,index):
    if index >= 0:
        result = np.roll(arr, len(x0) - abs(index))
    else:
        result = np.roll(arr, index)
    return result

# index_io = math.floor(40 * total_index / 360)

# x0_test = shift_arr(x0, index_io)
# y0_test = shift_arr(y0, index_io)
# z0_test = shift_arr(z0, index_io)

points1 = np.column_stack((x0, y0, z0))
points2 = np.column_stack((x1, y1, z1))

# Tính toán khoảng cách giữa các điểm
distances = np.linalg.norm(points1 - points2, axis=1)

# Tính z-score của khoảng cách
z_scores = np.abs(stats.zscore(distances))

# Thiết lập ngưỡng dựa trên z-score (ví dụ: 2 đơn vị độ lệch chuẩn)
threshold_z_score = 0.3

# Lấy chỉ số của các điểm không bị loại bỏ
indices_to_keep = np.where(z_scores < threshold_z_score)[0]

# Tạo lại các mảng x0, y0, x1, y1 chỉ chứa các điểm không bị loại bỏ
x0_test = x0[indices_to_keep]
y0_test = y0[indices_to_keep]
z0_test = z0[indices_to_keep]
x1_test = x1[indices_to_keep]
y1_test = y1[indices_to_keep]
z1_test = z1[indices_to_keep]

def residual(variables, samples):
    tx, ty, cos_the, sin_the = variables
    x0 = samples[:, 0]
    y0 = samples[:, 1]
    x1 = samples[:, 2]
    y1 = samples[:, 3]

    x0_calculated = tx + x1 * cos_the - y1 * sin_the
    y0_calculated = ty + x1 * sin_the + y1 * cos_the

    return np.concatenate([x0_calculated - x0, y0_calculated - y0])

best_theta = 0
best_tx = 0
best_ty = 0
lowest_residual = float('inf')  # Khởi tạo giá trị residual ban đầu là vô cùng lớn
theta_range = np.arange(0, 360, 1)

for theta_degree in theta_range:
    # Shift data
    index_io = math.floor(theta_degree * total_index / 360)
    x0_testing = shift_arr(x0_test, index_io)
    y0_testing = shift_arr(y0_test, index_io)
    z0_testing = shift_arr(z0_test, index_io)
    x1_testing = shift_arr(x1_test, index_io)
    y1_testing = shift_arr(y1_test, index_io)
    z1_testing = shift_arr(z1_test, index_io)

    # Giả định ban đầu
    initial_guess = np.array([0, 0, 1, 0])
    samples = np.column_stack((x0_testing, y0_testing, x1_testing, y1_testing))

    result = least_squares(residual, initial_guess, args=(samples,))
    tx_optimal, ty_optimal, cos_the_optimal, sin_the_optimal = result.x
    the_degrees = math.degrees(math.atan2(sin_the_optimal, cos_the_optimal))
    # Tính residual cho tx, ty hiện tại
    current_residual = result.cost

    # So sánh với residual tốt nhất hiện tại để cập nhật nếu cần
    if current_residual < lowest_residual:
        lowest_residual = current_residual
        best_theta = the_degrees
        best_tx = tx_optimal
        best_ty = ty_optimal



print(f"tx = {best_tx}")
print(f"ty = {best_ty}")
print(f"the = {best_theta} degrees")

# P1 = np.vstack((x1, y1, np.resize(z1, len(x1)), [1] * len(x1)))
# the = math.radians(the_degrees)
# tx = tx_optimal
# ty = ty_optimal

# # Ma trận chuyển đổi đồng nhất
# matrix_T = [
#     [np.cos(the),   -(np.sin(the)), 0,  tx],
#     [np.sin(the),   np.cos(the),    0,  ty],
#     [0,             0,              1,  0],
#     [0,             0,              0,  1]
# ]
# matrix_T = np.array(matrix_T)
# Pnew = np.dot(matrix_T, P1)

# # Trích xuất tọa độ x và y từ ma trận
# x_coords = Pnew[0, :]  # Hàng 0 là tọa độ x
# y_coords = Pnew[1, :]  # Hàng 1 là tọa độ y

# fig, ax = plt.subplots(1, 1)

# ax.scatter(x0,y0,s=0.1,c='green')
# ax.scatter(x_coords, y_coords, s=0.1, c = 'blue')
# ax.scatter(0, 0, s=20, c = 'red')
# ax.scatter(tx, ty, s=20, c = 'red')
# ax.set_xlim(-400, 400)
# ax.set_ylim(-400, 400)

# plt.show()