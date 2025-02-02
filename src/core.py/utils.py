import pandas as pd
import re
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

class USBUtils:

    def draw(self,identifiers,len_value):
        plt.figure(figsize=(3, 1.6))  # 设置整体图形大小
        for idx, identifier in enumerate(identifiers, start=1):
            if isinstance(identifier, dict):
                identifier = list(identifier.values())
            x = list(range(1, len(identifier) + 1))
            if len(x)>=1 and max(identifier) >= 0.003:
                continue
            plt.plot(x, identifier,linewidth = 0.5, color='red', alpha=0.01)

            plt.xlabel("Sequence Number (Len = 8)", fontsize=7)
            #plt.ylabel("Transaction Time", fontsize=7)
            #plt.xlabel(" ", fontsize=7)
            #plt.ylabel(" ", fontsize=7)

            plt.title("Kingston #2", fontsize=10)
            plt.xticks(fontsize=7)  # 调整 x 轴刻度标签的字体大小为 8
            plt.yticks(fontsize=7)  # 调整 y 轴刻度标签的字体大小为 8
            #plt.title(f"Transaction Time Distribution for Len: {len_value}")
            #plt.show()
        plt.savefig('figure_6/figure4.pdf', format='pdf',bbox_inches='tight', pad_inches=0.01)
        plt.show()

        current_figsize = plt.gcf().get_size_inches()  # 获取当前 figure 的尺寸
        current_width = current_figsize[0]  # 获取当前 figure 的宽度
        current_height = current_figsize[1]  # 获取当前 figure 的高度

        print("当前 PDF 尺寸为：", current_width, "x", current_height, "英寸")




    def timeGet(self,pattern,df):
        transactions_time = {}
        final = {}
        for i in range(len(df)):
            # 只有当记录匹配特定格式时，才视为事务的开始

            match = re.search(pattern, str(df.loc[i, 'Info']))
            #print(i)
            if match:
                len_value = match.group(1)  # 提取Len值
                #print(len_value)
                # 确保当前记录后至少还有5条记录作为事务的一部分
                if i + 5 < len(df):
                    start_time = df.loc[i, 'Time']  # 事务开始的时间
                    end_time = df.loc[i + 5, 'Time']  # 事务结束的时间（第6条记录）
                    # 直接计算时间差
                    #print("len:",len_value,"start end",start_time,end_time)
                    transaction_time = end_time - start_time
                    transaction_time = round(end_time - start_time, 9)
                    # transaction_time = round(end_time - start_time, 9)
                    # 根据Len值将事务时间存储到相应的列表中
                    if len_value not in transactions_time:
                        transactions_time[len_value] = []
                    transactions_time[len_value].append(transaction_time)

        for len_value, times in transactions_time.items():
            if len_value == '1':
                final = times
        return final




    def dtw_distance(series1, series2):
        n = len(series1)
        m = len(series2)

        # 创建一个n x m的矩阵来存储DTW距离
        dtw_matrix = np.zeros((n + 1, m + 1))

        # 初始化矩阵
        for i in range(1, n + 1):
            dtw_matrix[i][0] = np.inf
        for j in range(1, m + 1):
            dtw_matrix[0][j] = np.inf
        dtw_matrix[0][0] = 0

        # 计算DTW距离
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = abs(series1[i - 1] - series2[j - 1])
                dtw_matrix[i][j] = cost + min(dtw_matrix[i - 1][j], dtw_matrix[i][j - 1], dtw_matrix[i - 1][j - 1])

        return dtw_matrix[n][m]



    def dtw_distance_with_path(s1, s2):
        n, m = len(s1), len(s2)
        dtw_matrix = np.zeros((n + 1, m + 1))
        dtw_matrix[0, 0] = 0

        for i in range(1, n + 1):
            dtw_matrix[i, 0] = np.inf
        for i in range(1, m + 1):
            dtw_matrix[0, i] = np.inf

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = abs(s1[i - 1] - s2[j - 1])
                dtw_matrix[i, j] = cost + min(dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1])

        alignment = []
        i, j = n, m
        while i > 0 and j > 0:
            alignment.append((i - 1, j - 1))
            choices = [dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]]
            idx = np.argmin(choices)
            if idx == 0:
                i -= 1
            elif idx == 1:
                j -= 1
            else:
                i -= 1
                j -= 1

        return dtw_matrix[n, m], alignment

    def most_concentrated_range(data):
        # 计算均值和标准差
        mean = np.mean(data)
        std_dev = np.std(data)

        # 计算Z分数
        z_scores = [(x - mean) / std_dev for x in data]

        # 筛选离群值的索引
        outlier_indices = [i for i in range(len(data)) if abs(z_scores[i]) > 1]

        # 创建一个新的列表，不包含离群值
        cleaned_data = [data[i] for i in range(len(data)) if i not in outlier_indices]

        # 找出最集中的数据范围（最小值和最大值）
        central_range = (min(cleaned_data), max(cleaned_data))

        #print("删除离群值后的数据:", cleaned_data)
        print("最集中的数据范围:", central_range)
        average = np.mean(cleaned_data).round(6)

        return average

    def most_concentrated_range_or(data):
        # 计算中位数和绝对中位差（MAD）
        median = np.median(data)
        abs_dev = np.median(np.abs(data - median))

        # 计算修正后的 Z 分数
        z_scores = [(0.6745 * (x - median) / abs_dev) for x in data]

        # 筛选离群值的索引
        outlier_indices = [i for i in range(len(data)) if abs(z_scores[i]) > 1]

        # 创建一个新的列表，不包含离群值
        cleaned_data = [data[i] for i in range(len(data)) if i not in outlier_indices]

        # 找出最集中的数据范围（最小值和最大值）
        central_range = (min(cleaned_data), max(cleaned_data))

        print("删除离群值后的数据:", cleaned_data)
        print("最集中的数据范围:", central_range)
        average = np.mean(cleaned_data).round(6)

        return average


    def most_concentrated_range2(data):
        # 计算均值和标准差
        mean = np.mean(data)
        std_dev = np.std(data)

        # 计算Z分数
        z_scores = [(x - mean) / std_dev for x in data]

        # 筛选离群值的索引
        outlier_indices = [i for i in range(len(data)) if abs(z_scores[i]) > 3]

        # 创建一个新的列表，不包含离群值
        cleaned_data = [data[i] for i in range(len(data)) if i not in outlier_indices]

        # 找出最集中的数据范围（最小值和最大值）
        central_range = (min(cleaned_data), max(cleaned_data))

        #print("删除离群值后的数据:", cleaned_data)
        print("最集中的数据范围:", central_range)
        average = np.mean(cleaned_data).round(6)

        return average



    def most_concentrated_range_or2(data):
        # 计算中位数和绝对中位差（MAD）
        median = np.median(data)
        abs_dev = np.median(np.abs(data - median))

        # 计算修正后的 Z 分数
        z_scores = [(0.6745 * (x - median) / abs_dev) for x in data]

        # 筛选离群值的索引
        outlier_indices = [i for i in range(len(data)) if abs(z_scores[i]) > 3]
        print((-3)*abs_dev/0.6745+median)
        print((3) * abs_dev / 0.6745 + median)
        # 创建一个新的列表，不包含离群值
        cleaned_data = [data[i] for i in range(len(data)) if i not in outlier_indices]

        # 找出最集中的数据范围（最小值和最大值）
        central_range = (min(cleaned_data), max(cleaned_data))

        print("删除离群值后的数据:", cleaned_data)
        print("最集中的数据范围:", central_range)
        average = np.mean(cleaned_data).round(6)

        return average


