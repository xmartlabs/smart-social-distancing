import csv
import logging
import os
import time

import cv2 as cv
from datetime import date

from .raw_data_logger import RawDataLogger

logger = logging.getLogger(__name__)


class FileSystemLogger(RawDataLogger):

    def __init__(self, config, source: str, logger: str, live_feed_enabled: bool):
        super().__init__(config, source, logger, live_feed_enabled)
        self.log_directory = config.get_section_dict(logger)["LogDirectory"]
        self.objects_log_directory = os.path.join(self.log_directory, self.camera_id, "objects_log")
        os.makedirs(self.objects_log_directory, exist_ok=True)

        self.screenshot_period = float(self.config.get_section_dict(logger)["ScreenshotPeriod"]) * 60
        self.start_time = time.time()
        # config.ini uses minutes as the unit for ScreenshotPeriod
        self.screenshot_path = os.path.join(self.config.get_section_dict("App")["ScreenshotsDirectory"], self.camera_id)
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)

    def save_screenshot(self, cv_image):
        dir_path = f'{self.screenshot_path}/default.jpg'
        if not os.path.exists(dir_path):
            logger.info(f"Saving default screenshot for {self.camera_id}")
            cv.imwrite(f'{self.screenshot_path}/default.jpg', cv_image)

    def log_objects(self, objects, violating_objects, violating_objects_index_list, violating_objects_count,
                    detected_objects_cout, environment_score, time_stamp, version, video_time_stamp):
        file_name = str(date.today())
        file_path = os.path.join(self.objects_log_directory, file_name + ".csv")
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a") as csvfile:
            headers = ["VideoTimestamp", "DetectedObjects"]
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow(
                {"VideoTimestamp": video_time_stamp, "DetectedObjects": detected_objects_cout})

    def update(self, cv_image, objects, post_processing_data, fps):
        violating_objects = post_processing_data.get("violating_objects", [])
        # Save a screenshot only if the period is greater than 0, a violation is detected, and the minimum period
        # has occured
        if (self.screenshot_period > 0) and (time.time() > self.start_time + self.screenshot_period) and (
                len(violating_objects) > 0):
            self.start_time = time.time()
            self.save_screenshot(cv_image)
        super().update(cv_image, objects, post_processing_data, fps)
