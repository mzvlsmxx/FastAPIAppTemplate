from logging import Logger, getLogger, Formatter, DEBUG, INFO, WARNING, ERROR, FileHandler

universal_formatter: Formatter = Formatter(
    '%(asctime)s : [%(levelname)s] : %(name)s : %(message)s'
)

#  Logger for other modules
root_logger: Logger = getLogger('root')

root_error_file_handler: FileHandler = FileHandler('logs/errors.log')
root_error_file_handler.setFormatter(universal_formatter)
root_error_file_handler.setLevel(ERROR)

root_logger.addHandler(root_error_file_handler)
root_logger.setLevel(ERROR)

#  Logger for inner modules
actions_logger: Logger = getLogger('actions')

actions_info_file_handlers: FileHandler = FileHandler('logs/actions.log')
actions_info_file_handlers.setFormatter(universal_formatter)
actions_info_file_handlers.setLevel(DEBUG)

actions_logger.addHandler(actions_info_file_handlers)
actions_logger.setLevel(DEBUG)

#  Logger for error in modules
error_logger: Logger = getLogger('errors')

error_file_handler: FileHandler = FileHandler('logs/errors.log')
error_file_handler.setFormatter(universal_formatter)
error_file_handler.setLevel(ERROR)

error_logger.addHandler(error_file_handler)
error_logger.setLevel(ERROR)