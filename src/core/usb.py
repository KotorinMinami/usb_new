import numpy as np
import pandas as pd
import utils
import pyarrow as pa
import csv
from pyts.approximation import PiecewiseAggregateApproximation
from pyts.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#import cv2
from PIL import Image
import numpy as np
from fastdtw import fastdtw
import time
'''# 假设有两组不同长度的时间序列数据
time_series_1 = np.array([1, 2, 3, 4, 5])
time_series_2 = np.array([1, 3, 5, 7, 9, 11, 13])

# 使用fastdtw计算两组时间序列之间的DTW距离
distance, path = fastdtw(time_series_1, time_series_2)

print("DTW距离：", distance)'''


# 新建一个空字典，用于存储读取的数据框
dfs = {}

# 遍历100个文件的读取，并存储到字典中
for i in range(2, 102):
    filename = f'TEST/Kingston_64GB_2/output_{i}.csv'  # 生成文件名
    num = i - 2;
    df_name = f'df_{num}'  # 生成数据框名称
    dfs[df_name] = pd.read_csv(filename)  # 读取文件并存储到字典中

# 将字典中的数据框赋值给 df_1 到 df_100
for i in range(0, 100):
    globals()[f'df_{i}'] = dfs[f'df_{i}']  # 获取原始数据框

# 打印已读取的数据框
for i in range(0, 100):
    print(globals()[f'df_{i}'])

final = []

# 正则表达式匹配Info列中的格式
pattern = r'SCSI: Read\(10\) LUN: 0x00 \(LBA: 0x[0-9a-f]{8}, Len: (\d+)\)'

for i in range(0, 100):
    final.append(utils.USBUtils().timeGet(pattern, globals()["df_" + str(i)]))

print(final)

usb=utils.USBUtils()
usb.draw(final, len_value=1)
'''for row in final:
    print(len(row))'''

'''final_1 = utils.USBUtils().timeGet(pattern,df_1)
final_2 = utils.USBUtils().timeGet(pattern,df_2)
final_3 = utils.USBUtils().timeGet(pattern,df_3)
final_4 = utils.USBUtils().timeGet(pattern,df_4)
final_5 = utils.USBUtils().timeGet(pattern,df_5)
print(final_1)
utils.USBUtils().draw(final_1,final_2,final_3,final_4,final_5,1)'''

'''for i in range(len(df_1)):
    # 只有当记录匹配特定格式时，才视为事务的开始
    match = re.search(pattern, df_1.loc[i, 'Info'])
    if match:
        len_value = match.group(1)  # 提取Len值
        print(len_value)
        # 确保当前记录后至少还有5条记录作为事务的一部分
        if i + 5 < len(df_1):
            start_time = df_1.loc[i, 'Time']  # 事务开始的时间
            end_time = df_1.loc[i + 5, 'Time']  # 事务结束的时间（第6条记录）
            # 直接计算时间差
            #print("len:",len_value,"start end",start_time,end_time)
            transaction_time = end_time - start_time
            transaction_time = round(end_time - start_time, 9)
            # transaction_time = round(end_time - start_time, 9)
            # 根据Len值将事务时间存储到相应的列表中
            if len_value not in transactions_time_1:
                transactions_time_1[len_value] = []
            transactions_time_1[len_value].append(transaction_time)'''


'''for i in range(len(df_2)):
    # 只有当记录匹配特定格式时，才视为事务的开始
    match = re.search(pattern, df_2.loc[i, 'Info'])
    if match:
        len_value = match.group(1)  # 提取Len值
        print(len_value)
        # 确保当前记录后至少还有5条记录作为事务的一部分
        if i + 5 < len(df_2):
            start_time = df_2.loc[i, 'Time']  # 事务开始的时间
            end_time = df_2.loc[i + 5, 'Time']  # 事务结束的时间（第6条记录）
            # 直接计算时间差
            #print("len:",len_value,"start end",start_time,end_time)
            transaction_time = end_time - start_time
            transaction_time = round(end_time - start_time, 9)
            # transaction_time = round(end_time - start_time, 9)
            # 根据Len值将事务时间存储到相应的列表中
            if len_value not in transactions_time_2:
                transactions_time_2[len_value] = []
            transactions_time_2[len_value].append(transaction_time)'''
# 打印结果
'''for len_value, times in transactions_time_1.items():
    print(f"Len: {len_value} 的事务时间列表: {times}")'''




'''# 遍历事务时间字典
for len_value, times in transactions_time_1.items():

    #if len(times) > 500:
    if len_value == '1':

        with open('data1.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(times)
        # 折线图
        # 生成 x 轴数据，从1开始递增
        x = list(range(1, len(times) + 1))
        # 绘制折线图
        #plt.plot(x, times, marker='o', color='b', linestyle='-')
        plt.plot(x, times,color='red',alpha = 0.1)
        # 添加标题和标签
        plt.title(f"Transaction Time Distribution for Len: {len_value}")
        plt.xlabel("Transaction Time (units of 1μs)")
        plt.ylabel("Frequency")
        plt.yticks([i * 0.0001 for i in range(int(max(times) / 0.0001) + 1)])
        final_1 = times
        print(final_1)
        # 显示图例
        #plt.legend(['Line'])
        # 显示网格线
        #plt.grid(True)
        # 显示图形
        plt.show()

        X = [[i + 1 for i in range(len(times))], times]

        # PAA 处理
        transformer = PiecewiseAggregateApproximation(window_size=2)
        #result = transformer.transform(X)

        # Scaling in interval [0,1]
        scaler = MinMaxScaler()
        scaled_X = scaler.fit_transform(X)

        # 绘制经过缩放的结果
        plt.plot(scaled_X[0, :], scaled_X[1, :])
        plt.title("After scaling")
        plt.xlabel("Timestamp")
        plt.ylabel("Value")
        plt.show()




        arccos_X = np.arccos(scaled_X[1, :])
        fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
        ax.plot(result[0, :], arccos_X)
        ax.set_rmax(2)
        ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
        ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        ax.grid(True)

        ax.set_title("Polar coordinates", va ="bottom")
        plt.show()'''


'''# 使用fastdtw计算两组时间序列之间的DTW距离
distance_1,path= utils.USBUtils.dtw_distance_with_path(final[1],final[2])

print("DTW距离：", distance_1)
print("DTW路径：", path)

di = [[] for _ in range(len(path))]
for num in path:
    di[num[1]].append(final[1][num[0]])
print(di)'''


while(1):
    continue

# 创建一个空列表来存储所有的distance和path
distance_paths = []

# 循环计算100次distance和path
for i in range(0, 100):
    distance, path = utils.USBUtils.dtw_distance_with_path(final[i], final[1])
    distance_paths.append((distance, path))  # 将每一对distance和path作为元组添加到列表里

# 创建一个包含100个空列表的列表di
di = [[] for _ in range(len(path))]

# 循环遍历所有的distance和path，并加入到di中
for idx, (distance, path) in enumerate(distance_paths):
    #if distance < 0.0017:
        print(distance)
        for num in path:
            di[num[1]].append(final[idx][num[0]])

finger = []
# 打印di
print(di)
for i in range(len(di)):
    if di[i]:
        finger.append(utils.USBUtils.most_concentrated_range(di[i]))
#

'''# 创建 x 轴的数据，假设 x 轴数据为 1 到列表长度的整数
x = list(range(1, len(finger)+1))
# 绘制折线图
plt.plot(x, finger, color='red', alpha=1)
# 设置图表标题和轴标签
plt.title('fff')
plt.xlabel('x')
plt.ylabel('y')
# 显示网格
plt.grid(True)
# 显示图表
plt.show()
'''



distance_range = []

#用于对比归一化以后的效果
distance_paths = []

# 循环计算100次distance和path
for i in range(0, 100):
    distance, path = utils.USBUtils.dtw_distance_with_path(final[i], finger)
    distance_paths.append((distance, path))  # 将每一对distance和path作为元组添加到列表里

# 创建一个包含100个空列表的列表di
di = [[] for _ in range(len(path))]

# 循环遍历所有的distance和path，并加入到di中
for idx, (distance, path) in enumerate(distance_paths):
    #if distance < 0.0017:
        print(distance)
        distance_range.append(distance)
        for num in path:
            di[num[1]].append(final[idx][num[0]])

utils.USBUtils.most_concentrated_range_or2(distance_range)


















dfs_1 = {}
count = 0
# 遍历100个文件的读取，并存储到字典中
for i in range(2, 102):
    #filename = f'TEST/Aigo_32GB_re_2/output_{i}.csv'  # 生成文件名
    filename = f'first_gai/kingston_3/output_{i}.csv'  # 生成文件名
    num = i - 2
    df_name = f'df_{num}'  # 生成数据框名称
    dfs[df_name] = pd.read_csv(filename)  # 读取文件并存储到字典中

# 将字典中的数据框赋值给 df_1 到 df_100
for i in range(0, 100):
    globals()[f'df_{i}'] = dfs[f'df_{i}']  # 获取原始数据框

# 打印已读取的数据框
for i in range(0, 100):
    print(globals()[f'df_{i}'])

final_1 = []

# 正则表达式匹配Info列中的格式
pattern = r'SCSI: Read\(10\) LUN: 0x00 \(LBA: 0x[0-9a-f]{8}, Len: (\d+)\)'

for i in range(0, 100):
    final_1.append(utils.USBUtils().timeGet(pattern, globals()["df_" + str(i)]))


usb=utils.USBUtils()
usb.draw(final_1, len_value=1)

distance_paths = []

# 循环计算100次distance和path
for i in range(0, 100):
    start_time = time.time()
    distance, path = utils.USBUtils.dtw_distance_with_path(final_1[i], finger)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"函数执行时间: {execution_time:.4f}秒")
    distance_paths.append((distance, path))  # 将每一对distance和path作为元组添加到列表里


# 循环遍历所有的distance和path，并加入到di中
for idx, (distance, path) in enumerate(distance_paths):
    #if distance < 0.0017:
    print(distance)
    if distance < 0.0008553862120088955:
        count = count + 1
print(count)

'''with open('distance_6/a2.txt', 'w', encoding='utf-8') as f:
    for idx, (distance, path) in enumerate(distance_paths):
        f.write(f'Distance: {distance}, Path: {path}\n')'''

