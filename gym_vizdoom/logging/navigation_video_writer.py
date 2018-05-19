import numpy as np
import cv2

from gym_vizdoom.logging.video_writer import VideoWriter

class NavigationVideoWriter():
  def __init__(self, save_path, observation_shape):
    height, width, channels = observation_shape
    self.show_width = 4 * width
    self.show_height = 4 * height
    self.show_channels = channels // 2
    self.show_border = 10
    self.video_writer = VideoWriter(save_path,
                                    (2 * self.show_width + self.show_border,
                                     self.show_height),
                                    mode='replace')

  def double_upsampling(self, input):
    return cv2.pyrUp(cv2.pyrUp(input))

  def side_by_side(self, first, second):
    first = self.double_upsampling(first)
    second = self.double_upsampling(second)
    return np.concatenate((first,
                           np.zeros([self.show_height,
                                     self.show_border,
                                     self.show_channels], dtype=np.uint8),
                           second), axis=1)

  def write(self, left, right):
    side_by_side_screen = self.side_by_side(left, right)
    self.video_writer.add_frame(side_by_side_screen)

  def close(self):
    self.video_writer.close()