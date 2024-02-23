import serial
import csv
import datetime

# 设置串口参数/dev/ttyACM0
ser_screen = serial.Serial('/dev/ttyACM0', 32500, timeout=0.1)
ser_imu = serial.Serial('/dev//dev/ttyprintk', 74880, timeout=0.1)

# 打开CSV文件以写入模式
csv_file_path = 'row_data/signature_Zekai/False_1'
start_record = False

with open(csv_file_path, 'w', newline='') as csv_file:
    # 创建CSV写入器
    csv_writer = csv.writer(csv_file)
    # 写入CSV文件的表头
    csv_writer.writerow(['Time', 'x', 'y', 'pressure', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'])

    try:
        while True:
            # 从串口读取一行数据
            line_screen = ser_screen.readline().decode('utf-8', errors='ignore').strip()
            line_imu = ser_imu.readline().decode('utf-8', errors='ignore').strip()

            if line_screen and line_imu:  # 确保数据有效
                current_time = datetime.datetime.now()
                data_screen = line_screen.split('\t')
                data_imu = line_imu.split(',')

                # 检查是否开始记录
                if len(data_screen) == 3 and int(data_screen[2]) > 10:
                    start_record = True
                    start_time = current_time

                # 写入CSV文件
                if start_record:
                    csv_writer.writerow([current_time] + data_screen + data_imu)
                    if (current_time - start_time).seconds > 2:
                        print("程序已停止")
                        break  # 结束循环
    except KeyboardInterrupt:
        print("程序已手动停止")
    finally:
        ser_screen.close()
        ser_imu.close()
