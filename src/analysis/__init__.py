import os
import subprocess
import logging
import binascii

logger = logging.getLogger(__name__)

class Analysis:
    def __init__(self, path : str, tools_lists: dict, deep: bool = False):
        self.path = path
        self.tools_lists = tools_lists
        self.deep = deep

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
    
    def deep_file(self):
        '''
        Deep Analysis in file format using some flags
        '''
        JPG_POTENTIAL_FLAGS = ["4a46494600", "4578696600", "ffdb004300"]
        PNG_POTENTIAL_FLAGS = ["49484452", "49444154", "74455874", "7a545874", "70485973", "504c5445"]
        GIF_POTENTIAL_FLAGS = ["383961", "383761"]
        with open(self.path, 'rb') as f:
            file_content = binascii.hexlify(f.read())
        if any(flag in file_content for flag in JPG_POTENTIAL_FLAGS) or file_content.endswith('ffd9'):
            return "JPG", True
        elif any(flag in file_content for flag in PNG_POTENTIAL_FLAGS) or file_content.endswith('49454e44ae426082'):
            return "PNG", True
        elif any(flag in file_content for flag in GIF_POTENTIAL_FLAGS):
            return "GIF", True
        else:
            return "Unknown", False



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
        exiftool command wrapper
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

    def strings(self):
        '''
        strings command wrapper
        '''
        if not os.path.exists(self.path):
            return "File not found."
        strings_cmd = self.tools_lists["strings"]
        if os.path.exists(self.path):
            result = subprocess.run([strings_cmd, self.path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return result.stderr.strip()
        return "File not found."


    def zsteg(self):
        '''
        zsteg command wrapper
        pay attention, this command can only support png and bmp file
        '''
        if not self.tools_lists["zsteg"]:
            logger.debug("zsteg command not found")
            return "zsteg command not found", False
        zsteg_cmd = self.tools_lists["zsteg"]
        if os.path.exists(self.path):
            if self.deep:
                result = subprocess.run([zsteg_cmd, '-a', self.path], capture_output=True, text=True)
            else:
                result = subprocess.run([zsteg_cmd, self.path], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False
    
    # def 
    

