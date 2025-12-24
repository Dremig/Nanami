import logging
import sys

class ColoredLogger:
    '''
    logger with colorful output
    '''

    COLORS = {
        'DEBUG': '\033[36m',      # BLUE-GREEN
        'INFO': '\033[32m',       # GREEN
        'WARNING': '\033[33m',    # YELLOW
        'ERROR': '\033[31m',      # RED
        'CRITICAL': '\033[35m',   # PURPLE
        'RESET': '\033[0m'        # RESET COLOR
    }
    
    def __init__(self, level=logging.DEBUG, 
                 format_str='[%(levelname)s] %(message)s'):
        self.level = level
        self.format_str = format_str
        
        self.logger = logging.getLogger()
        
        self._setup_logger()
    
    def _setup_logger(self):
        '''logger config'''
        self.logger.setLevel(self.level)

        if self.logger.handlers:
            self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        
        formatter = ColoredFormatter(self.format_str)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
    
    def set_level(self, level):
        """logger level setting"""
        self.level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def debug(self, msg, *args, **kwargs):
        """debug output"""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """common output"""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """warning output"""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        """error output"""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        """critcal output"""
        self.logger.critical(msg, *args, **kwargs)
    
    
    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)
    
    def get_logger(self):
        return self.logger


class ColoredFormatter(logging.Formatter):
    """colored formatter"""
    
    def __init__(self, fmt='[%(levelname)s] %(message)s'):
        super().__init__(fmt)
        self.colors = ColoredLogger.COLORS
    
    def format(self, record):
        if self._style._fmt:
            temp_formatter = logging.Formatter(self._style._fmt)
            log_message = temp_formatter.format(record)
        else:
            default_fmt = '[%(levelname)s] %(message)s'
            temp_formatter = logging.Formatter(default_fmt)
            log_message = temp_formatter.format(record)
        
        color = self.colors.get(record.levelname, self.colors['RESET'])

        colored_message = f"{color}{log_message}{self.colors['RESET']}"
        
        return colored_message
    
# if __name__ == '__main__':
#     logger = ColoredLogger()
#     logger.info('hello world')
#     logger.error('hello world')
#     logger.debug('hello world')
#     logger.warning('hello world')
#     logger.critical('hello world')