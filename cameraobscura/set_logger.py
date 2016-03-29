
# python standard library
import logging
import logging.handlers

SCREEN_FORMAT_QUIET = "%(levelname)s: [%(asctime)s] -- %(message)s"
SCREEN_FORMAT = "%(levelname)s: %(name)s.%(funcName)s, Line: %(lineno)d [%(asctime)s] -- %(message)s"
SMALL_TIMESTAMP = "%H:%M:%S"
GIGABYTE = 1073741824
BACKUP_LOGS = 1
LOG_FORMAT = "%(levelname)s,%(module)s,%(threadName)s,%(funcName)s,Line: %(lineno)d,%(asctime)s,%(message)s" 
LOG_TIMESTAMP = "%Y-%m-%d %H:%M:%S"

EVENTLOG = "rate_vs_range.log"

def set_logger(args):
    """
    Creates a logger and sets the logging level 
    """
    for name in (__package__, 'theape', 'paramiko'):
        logger = logging.getLogger(name)
        
        stderr = logging.StreamHandler()
        if args.debug:
            screen_format = SCREEN_FORMAT
        else:
            screen_format = SCREEN_FORMAT_QUIET
        
                
        screen_format = logging.Formatter(screen_format, datefmt=SMALL_TIMESTAMP)
        stderr.setFormatter(screen_format)
        
        
        log_file = logging.handlers.RotatingFileHandler(EVENTLOG,
                                                        maxBytes=GIGABYTE, backupCount=BACKUP_LOGS)
        file_format = logging.Formatter(LOG_FORMAT, datefmt=LOG_TIMESTAMP)
        log_file.setFormatter(file_format)
        
        logger.setLevel(logging.DEBUG)
        log_file.setLevel(logging.DEBUG)
        
        if args.debug:
            stderr.setLevel(logging.DEBUG)
        elif args.silent:
            stderr.setLevel(logging.ERROR)
        else:
            stderr.setLevel(logging.INFO)
            
        logger.addHandler(stderr)
        logger.addHandler(log_file)   
    return