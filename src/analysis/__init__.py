import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class Analysis:
    def __init__(self, path : str, tools_lists: dict):
        self.path = path
        self.tools_lists = tools_lists

    def file(self):
        '''
        file command wrapper
        '''
        if not self.tools_lists["file"]:
            logger.debug("file command not found")
            return "file command not found", False
        file_cmd = self.tools_lists["file"]
        if os.path.exists(self.path):
            result = subprocess.run([file_cmd,'-b', self.path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False

    def pngcheck(self):
        '''
        pngcheck command wrapper
        '''
        if not self.tools_lists["pngcheck"]:
            logger.debug("pngcheck command not found")
            return "pngcheck command not found", False
        pngcheck_cmd = self.tools_lists["pngcheck"]
        if os.path.exists(self.path):
            result = subprocess.run([pngcheck_cmd,'-7cpqstvx' , self.path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return result.stderr.strip()
        return "File not found."

    def exiftool(self):
        '''
        exiftool
        '''
        if not self.tools_lists["exiftool"]:
            logger.debug("exiftool command not found")
            return "exiftool command not found", False
        exiftool_cmd = self.tools_lists["exiftool"]
        if os.path.exists(self.path):
            result = subprocess.run([exiftool_cmd, self.path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return result.stderr.strip()
        return "File not found."

    def strings(path):
        '''
        strings command wrapper
        '''
        if not os.path.exists(path):
            return "File not found."
        strings_cmd = "strings"
        if os.path.exists(path):
            result = subprocess.run([strings_cmd, path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return result.stderr.strip()
        return "File not found."


    