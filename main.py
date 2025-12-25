import os
from src.analysis import Analysis
from src.init import Init
import src.logger as Logger

logger = Logger.ColoredLogger()



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
            logger.warning("I'm sorry, but currently Nanami can only analyze one file at a time.")
            exit(0)
    else:
        logger.warning("It seems that you haven't uploaded any files yet, please upload a file first.")
        exit(0)
    file_path = os.path.join(upload_path, os.listdir(upload_path)[0])
    available_tools, essential_tools = init.examine_tools()
    if available_tools is None:
        logger.warning("It seems that you don't have any tools installed, please install them first.")
        exit(0)

    logger.info('Nanami has these tools available: ')
    tools_list = []
    for index, tool in enumerate(available_tools, start=1):
        logger.info(f"{index}. {tool}")
        tools_list.append(tool)
    logger.info('You will choose : ...')
    logger.info("Input as: 1 2 3 ...")
    tool_input = input()
    tools = {}
    for i in tool_input.split(' '):
        tools[tools_list[int(i)-1]] = available_tools[tools_list[int(i)-1]]
    available_tools.update(essential_tools)
    logger.info('Will you want to deep analyze this file? This will take more time .(y/N)')
    choice = input()
    logger.info
    if choice.lower() == 'y' or choice.lower() == 'yes':
        deep = True
    else:
        deep = False
    analysis = Analysis(path = file_path, tools_lists = available_tools, deep=deep, output_path=output_path)

    # analysis = Analysis()
    analysis.main_logic()