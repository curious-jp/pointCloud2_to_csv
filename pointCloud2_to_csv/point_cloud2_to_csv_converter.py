# write ros node to subscribe point cloud and convert it to csv file
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2 as pc2

import numpy as np
import csv

speed = 25 / 3600 * 1000 # km/h
play_speed = 5 # times

class PointCloud2ToCSVConverter(Node):

  csv_data = []
  last_data_time = None
  start_time = None

  # initialize node
  def __init__(self):
    super().__init__('point_cloud2_to_csv_converter')
    print(speed, play_speed)
    self.subscription = self.create_subscription(
      pc2,
      'cloud_fullframe',
      self.listener_callback,
      10)
    self.subscription  # prevent unused variable warning
    # print message
    self.get_logger().info('Point cloud to csv converter started')
    # set start time
    self.start_time = self.get_clock().now()

  # callback function
  def listener_callback(self, msg):
    # convert uint8 array to float32 array but its not big endian
    cloud = np.frombuffer(msg.data, dtype=np.float32)
    # print info
    self.get_logger().info('Received point cloud with %d points' % cloud.shape[0])
    # reshape array by ellemt of x y z intensity
    cloud = cloud.reshape(cloud.shape[0] // 4, 4)
    # add up speed info in z axis
    cloud[:, 2] += speed * (self.get_clock().now() - self.start_time).nanoseconds / 1e9 * play_speed
    # print info
    # for i in range(0, len(cloud), 10):
    #   print(cloud[i:i+10])

    # add data to csv_data
    self.csv_data.append(cloud)
    # print info
    self.get_logger().info('Added data to csv_data in size %d' % len(self.csv_data))
    # set last_data_time
    self.last_data_time = self.get_clock().now()

  # watch dog function
  def watch_dog(self):
    # if csv_data is empty, do nothing
    if len(self.csv_data) == 0:
      return
    # if csv_data is not empty, start watching time
    else:
      # get current time
      current_time = self.get_clock().now()
      if self.last_data_time is None:
        return
      # if time is over 5 second, save csv file
      elif (current_time - self.last_data_time).nanoseconds > 5e9:
        # save csv file
        with open('1111_25km_50Hz_0.25.csv', 'w') as f:
          writer = csv.writer(f)
          # write csv file
          for data in self.csv_data:
            writer.writerows(data)
        # clear csv_data
        self.csv_data.clear()
        # print message
        self.get_logger().info('##################################################')
        self.get_logger().info('                 Saved csv file')
        self.get_logger().info('##################################################')


  # test function
  def get_only_one(self):
    # if csv_data is empty, do nothing
    if len(self.csv_data) == 0:
      return
    # if csv_data is not empty, start watching time
    else:
      # save csv file
      with open('point_cloud.csv', 'w') as f:
        writer = csv.writer(f)
        # overwrite csv file
        for data in self.csv_data:
          writer.writerows(data)
      # clear csv_data
      self.csv_data.clear()

def main(args=None):
  rclpy.init(args=args)
  # create node
  point_cloud2_to_csv_converter = PointCloud2ToCSVConverter()

  while rclpy.ok():
    # create timer
    timer_period = 0.1  # seconds
    point_cloud2_to_csv_converter.create_timer(timer_period, point_cloud2_to_csv_converter.watch_dog)
    # spin node
    rclpy.spin(point_cloud2_to_csv_converter)
    # destroy node
    point_cloud2_to_csv_converter.destroy_node()
    # shutdown ros
    rclpy.shutdown()