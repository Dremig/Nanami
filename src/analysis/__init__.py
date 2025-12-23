import os
import subprocess
import logging
import binascii

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Analysis:
    JPG_POTENTIAL_FLAGS = ["4a46494600", "4578696600", "ffdb004300"]
    PNG_POTENTIAL_FLAGS = ["49484452", "49444154", "74455874", "7a545874", "70485973", "504c5445"]
    GIF_POTENTIAL_FLAGS = ["383961", "383761"]
    def __init__(self, path : str, tools_lists : dict, use_lists : list,
                deep: bool = False, potential_passwd: str = None, 
                output_path: str = None):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path does not exist: {path}")
        self.path = path
        self.tools_lists = tools_lists
        self.deep = deep
        self.potential_passwd = potential_passwd
        self.output_path = output_path
        self.use_lists = use_lists

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

        with open(self.path, 'rb') as f:
            file_content = binascii.hexlify(f.read())
            
        if any(flag in file_content for flag in self.JPG_POTENTIAL_FLAGS) or file_content.endswith('ffd9'):
            return "JPG", True
        elif any(flag in file_content for flag in self.PNG_POTENTIAL_FLAGS) or file_content.endswith('49454e44ae426082'):
            return "PNG", True
        elif any(flag in file_content for flag in self.GIF_POTENTIAL_FLAGS):
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
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False

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
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False

    def strings(self):
        '''
        strings command wrapper
        '''
        if not self.tools_lists["strings"]:
            logger.debug("strings command not found")
            return "strings command not found", False
        strings_file = os.path.join(self.output_path, "strings_output")
        strings_cmd = self.tools_lists["strings"]
        if os.path.exists(self.path):
            result = subprocess.run([strings_cmd, self.path], capture_output=True, text=True)
            if result.returncode == 0:
                with open(strings_file, 'w') as f:
                    f.write(result.stdout.strip())
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False


    def zsteg(self):
        '''
        zsteg command wrapper
        pay attention, this command can only support png and bmp file
        '''
        if not self.tools_lists["zsteg"]:
            logger.debug("zsteg command not found")
            return "zsteg command not found", False
        zsteg_cmd = self.tools_lists["zsteg"]
        zsteg_file = os.path.join(self.output_path, "zsteg_output")
        if os.path.exists(self.path):
            if self.deep:
                result = subprocess.run([zsteg_cmd, '-a', self.path], capture_output=True, text=True)
            else:
                result = subprocess.run([zsteg_cmd, self.path], capture_output=True, text=True)
            if result.returncode == 0:
                with open(zsteg_file, 'w') as f:
                    f.write(result.stdout.strip())
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
        return "File not found.", False
    
    def steghide(self):
        '''
        steghide command wrapper
        '''
        if not self.tools_lists["steghide"]:
            logger.debug("steghide command not found")
            return "steghide command not found", False
        steghide_cmd = self.tools_lists["steghide"]
        temp_output = os.path.join(self.output_path, "steghide_output")
        if os.path.exists(self.path): 
            if self.potential_passwd:
                result = subprocess.run([steghide_cmd, 'extract', '-sf', self.path, '-p', self.potential_passwd, '-xf', temp_output], capture_output=True, text=True)
            else:
                result = subprocess.run([steghide_cmd, 'extract', '-sf', self.path, '-xf', temp_output], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip(), True
            else:
                return result.stderr.strip(), False
            
    def main_logic(self):
        '''
        the full chain of analysis
        '''
        file_message, file_success = self.file()
        if file_success:
            if "png" in file_message:
                pngcheck_message, pngcheck_success = self.pngcheck()
                if pngcheck_success:
                    logger.info("pngcheck result: %s", pngcheck_message)
            elif not ("png" or "jpeg" or "gif") in file_message:
                if self.deep:
                    type, found = self.deep_file()
                    if not found:
                        logger.debug("File type not unknown, skip analysis")
                    else:
                        logger.debug("File type is possibly %s, you can try to fix it", type)
                    return
                else:
                    logger.debug("File type not unknown, skip analysis")
                    return
            
            exiftool_message, exiftool_success = self.exiftool()
            if exiftool_success:
                logger.info("exiftool result: %s", exiftool_message)
            else:
                logger.error("exiftool fail with message : %s", exiftool_message)
            for tool in self.tools_lists:
                if tool == "strings":
                    strings_message, strings_success = self.strings()
                    if strings_success:
                        logger.info("strings result:\n %s", strings_message)
                    else:
                        logger.error("strings fail with message : %s", strings_message)
                elif tool == "zsteg":
                    zsteg_message, zsteg_success = self.zsteg()
                    if zsteg_success:
                        logger.info("zsteg result:\n %s", zsteg_message)
                    else:
                        logger.error("zsteg fail with message : %s", zsteg_message)
                elif tool == "steghide":
                    steghide_message, steghide_success = self.steghide()
                    if steghide_success:
                        logger.info("steghide result:\n %s", steghide_message)
                    else:
                        logger.error("steghide fail with message : %s", steghide_message)
        else:
            logger.error("file fail with message : %s, the following steps will be skipped", file_message)
    

