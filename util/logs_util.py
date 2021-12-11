import configparser
import logging.config
import os

config = configparser.RawConfigParser()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = BASE_DIR + '/' + 'config/APITest.ini'
config.read(file_path, encoding='utf-8')

standard_format = config.get('logs', 'standard_format')
simple_format = config.get('logs', 'simple_format')
test_format = config.get('logs', 'test_format')
log_file = config.get('logs', 'log_file')

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
            'formatter': 'standard',
            # 可以定制日志文件路径
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # log文件的目录
            # LOG_PATH = os.path.join(BASE_DIR,'a1.log')
            'filename': log_file,  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'formatter': 'test',
            'filename': log_file,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',  # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
        '专门的采集': {
            'handlers': ['other', ],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


def logs_util(task_id, message, rank='info'):
    logging.config.dictConfig(LOGGING_DIC)
    logger1 = logging.getLogger(task_id)
    if rank == 'info':
        logger1.info(message)
    elif rank == 'DEBUG':
        logger1.debug(message)
    elif rank == 'error':
        logger1.error(message)
    elif rank == 'critical':
        logger1.critical(message)
    else:
        logger1.warning(message)
    return logger1


if __name__ == '__main__':
    logs_util('', "wewqawddsdqfcsqasqfgsqfga", 'error')
