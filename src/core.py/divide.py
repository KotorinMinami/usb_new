import csv

input_file = 'first_gai/kingston_3/kingston_3.csv'
output_prefix = 'first_gai/kingston_3/output_'

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    current_split = 1
    output_file = open(f'{output_prefix}{current_split}.csv', 'w', newline='')
    writer = csv.writer(output_file)

    # 读取第一行，即列名
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        if "host" in row and "2.98.0" in row and "USBMS" in row and "64" in row and "GET MAX LUN Request" in row:
        #if "host" in row and "2.18.0" in row and "USB" in row and "64" in row and "SET INTERFACE Response" in row:
            output_file.close()
            current_split += 1
            output_file = open(f'{output_prefix}{current_split}.csv', 'w', newline='')
            writer = csv.writer(output_file)

            # 写入列名到新文件
            writer.writerow(header)

        writer.writerow(row)

    output_file.close()