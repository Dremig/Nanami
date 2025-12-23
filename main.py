import os
from src.analysis import Analysis
from src.init import Init
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logger.info('Welcome to Nanami-cli version qwq, ciallo~')
    if not os.path.exists('config.json') and os.path.exists('config.json.example'):
        logger.warning("It seems that you don't have a config file, so I will copy the example file for you.")
        os.system("cp config.json.example config.json")
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    init = Init(config_path)
    logger.info('Initializing and loading config...')
    upload_path , temp_path , output_path = init.load_config()
    # for file in os.listdir(upload_path):
    if os.listdir(upload_path):
        if len(os.listdir(upload_path)) > 1:
            logger.warning("I'm so sorry, but currently Nanami can only analyze one file at a time.")
            exit(0)
    else:
        logger.warning("It seems that you haven't uploaded any files yet, please upload a file first.")
        exit(0)
    file_path = os.path.join(upload_path, os.listdir(upload_path)[0])
    available_tools = init.examine_tools()
    print(available_tools)
    if available_tools is None:
        logger.warning("It seems that you don't have any tools installed, please install them first.")
        exit(0)
    logger.info('Nanami has these tools available: ')
    for index, tool in enumerate(available_tools, start=1):
        logger.info(f"{index}. {tool}")
    logger.info('You will choose : ...')
    logger.info("Input as: 1 2 3 ...")
    input = input()
    tools = []
    for i in input.split(' '):
        tools.append(available_tools[int(i)-1])
    logger.info('Will you want to deep analyze this file? This will take more time .(Y/n)')
    input = input()
    if input == 'Y':
        logger.info('Deep analyzing...')
        analysis = Analysis(file_path, tools, temp_path, output_path, True)
    else:
        logger.info('Analyzing...')
        analysis = Analysis(file_path, tools, temp_path, output_path, False)
    
    
    # analysis = Analysis()
    analysis.main_logic()