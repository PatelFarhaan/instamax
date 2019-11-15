# import logging
#
#
# def get_logger(log_file_path=None, name=__name__):
#     log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s")
#     root_logger = logging.getLogger(name)
#     root_logger.setLevel(logging.DEBUG)
#
#     if log_file_path:
#         log_file_path = log_file_path.rstrip(".log")
#         file_handler = logging.FileHandler("{}.log".format(log_file_path))
#         file_handler.setFormatter(log_formatter)
#         root_logger.addHandler(file_handler)
#
#     console_handler = logging.StreamHandler()
#     console_handler.setFormatter(log_formatter)
#     root_logger.addHandler(console_handler)
#
#     return root_logger
#
