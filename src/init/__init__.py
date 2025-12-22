import json
import os
import logging

logger = logging.getLogger(__name__)


class Init:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        with open(self.config_path, 'r') as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError:
                config = {}
                logger.error("Error loading config file")
            # current, only paths are supported
            paths = config.get("paths", {})
            upload_path = paths.get("upload_folder", "uploads")
            temp_path = paths.get("temp_folder", "temp")
            output_path = paths.get("output_folder", "output")
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
                logger.info(f"Upload folder created: {upload_path}")
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)
                logger.info(f"Temp folder created: {temp_path}")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                logger.info(f"Output folder created: {output_path}")
            return upload_path, temp_path, output_path