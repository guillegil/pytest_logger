
from datetime import datetime
from functools import wraps
import os
from logging import Logger, Handler

import logging
import shutil

from colored import Fore as fg
from colored import Back as bg
from colored import Style as st

from pathlib import Path

datefmt = "%Y-%m-%d %H:%M:%S"

levels = {
    "debug"     : {"level": logging.DEBUG, "color": fg.CYAN},
    "info"      : {"level": logging.INFO, "color": fg.WHITE},
    "warning"   : {"level": logging.WARNING, "color": fg.YELLOW},
    "error"     : {"level": logging.ERROR, "color": fg.RED},
    "critical"  : {"level": logging.CRITICAL, "color": fg.RED},
    "step"      : {"level": 21, "color": fg.WHITE},
    "substep"   : {"level": 22, "color": fg.light_gray},
    "pass"      : {"level": 23, "color": fg.GREEN},
    "fail"      : {"level": 31, "color": fg.RED},
}

# -- Reverse lookup ------------------------------------------- #
levels_by_value = {v["level"]: k for k, v in levels.items()}



class BlockAllFilter(logging.Filter):
    def filter(self, record):
        return False

class ColorFormatter(logging.Formatter):

    RESET = st.RESET

    def __init__(self, fmt: str = None, datefmt: str = None, style='%'):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"

        # Register custom levels
        logging.addLevelName(levels['step']['level'], "STEP")
        logging.addLevelName(levels['substep']['level'], "SUBSTEP")
        logging.addLevelName(levels['pass']['level'], "PASS")
        logging.addLevelName(levels['fail']['level'], "FAIL")

        super().__init__(fmt, datefmt, style)

    def __get_level_by_value(self, target_level: int) -> tuple:
        key = levels_by_value.get(target_level)
        return (key, levels[key]) if key else (None, None)

    def format(self, record):
        # Get original formatted message
        formatted = super().format(record)

        # Get level info using reverse lookup
        level_key, level_info = self.__get_level_by_value(record.levelno)
        color = level_info["color"] if level_info else self.RESET

        # Add indentation for substep
        if level_key == "substep":
            formatted = "   " + formatted

        # Wrap the entire line in color, then reset
        return f"{color}{formatted}{self.RESET}"


class TestLogger:
    
    def __init__(
        self, 
        logger_name: str = "test_logger",
        *args,
        **kwargs
    ):
        """
            **kwargs:
                - term_format
                - setup_format
                - term_config_loglevel
                - term_setup_loglevel
                - term_call_loglevel
        """
        self.__logger : Logger = logging.getLogger( logger_name )
        self.__logger.setLevel(levels['info']['level'])

        # -- Handler for the test call file ----------------------- #
        self.__call_file_handler     : Handler = None
        # -- Handler for the test setup file ---------------------- #
        self.__setup_file_handler    : Handler = None
        # -- Handler for the test prompt -------------------------- #
        self.__term_handler          : Handler = None
        # -- Handler for the steps file  -------------------------- #
        self.__steps_file_handler    : Handler = None
        # -- Handler for the combined log ------------------------- # 
        self.__combined_file_handler : Handler = None


        self.__term_format  : str = kwargs.get('log_term_format', '[%(levelname)s%(step)s] - %(message)s')
        self.__setup_format : str = kwargs.get('log_setup_format', '[%(levelname)s%(step)s] - %(message)s')
    

        # ! The followign levels affect only to the term handler #
        #   Every other entry is logged into the files always (for now)

        # -- Applied during the test configuration ------------------ #
        self.__term_config_loglevel : int = kwargs.get('term_config_loglevel', levels['info']["level"])
        # -- Applied during the setup stage ------------------------ #
        self.__term_setup_loglevel  : int = kwargs.get('term_setup_loglevel', levels['info']["level"])
        # -- Applied during the call stage ------------------------- #
        self.__term_call_loglevel   : int = kwargs.get('term_call_loglevel', levels['info']["level"])
    
        # -- Applied during the test configuration ------------------ #
        self.__setup_file_loglevel : int = kwargs.get('setup_file_loglevel', levels['info']["level"])
        # -- Applied during the setup stage ------------------------ #
        self.__call_file_loglevel  : int = kwargs.get('call_file_loglevel', levels['info']["level"])


        # -- Step count for the step log --------------------------- #
        self.__stepn    : int = 0
        # -- The substep one --------------------------------------- #
        self.__substepn : int = 0
    
    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def term_config_loglevel(self) -> int:
        return self.__term_config_loglevel

    @term_config_loglevel.setter
    def term_config_loglevel(self, value: int) -> None:
        self.__term_config_loglevel = value

    @property
    def term_setup_loglevel(self) -> int:
        return self.__term_setup_loglevel

    @term_setup_loglevel.setter
    def term_setup_loglevel(self, value: int) -> None:
        self.__term_setup_loglevel = value

    @property
    def term_call_loglevel(self) -> int:
        return self.__term_call_loglevel

    @term_call_loglevel.setter
    def term_call_loglevel(self, value: int) -> None:
        self.__term_call_loglevel = value

    @property
    def stepn(self) -> int:
        return self.__stepn

    @property
    def substepn(self) -> int:
        return self.__substepn

    def __add_handler(self, handler: Handler) -> None:
        self.__logger.addHandler( handler )

    def __remove_handler(self, handler: Handler) -> None:
        self.__logger.removeHandler( handler )

    def __create_file_handler(self, filepath: str, encoding: str = "utf-8") -> Handler:
        return logging.FileHandler(filename=filepath, encoding=encoding)

    def __ensure_path(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

    def init_term_handler(
        self,
        level   : int | None = None,
        fmt     : str | None = None
    ):
        if level is not None:
            self.__term_config_loglevel = level
        
        if fmt is not None:
            self.__term_format = fmt

        self.__term_handler = logging.StreamHandler()
        self.__term_handler.setLevel( self.__term_config_loglevel )
        self.__term_handler.setFormatter(
            ColorFormatter(fmt=self.__term_format, datefmt=datefmt)
        )
        
        self.__add_handler( self.__term_handler )
    

    def init_setup_logger(
        self,
        path    : str,
        level   : int | None = None,
        fmt     : str | None = None
    ):
        if level is not None:
            self.__setup_file_loglevel = level
        
        if fmt is not None:
            self.__setup_format = fmt

        self.__ensure_path( path )

        # -- Configure a new File Handler ------------------------------- #
        self.__setup_file_handler = self.__create_file_handler(path)
        self.__setup_file_handler.setLevel( self.__setup_file_loglevel )
        self.__setup_file_handler.setFormatter(
            logging.Formatter(fmt=self.__setup_format, datefmt=datefmt)
        )

        # -- Add the handler to the global logger ----------------------- #
        self.logger.addHandler( self.__setup_file_handler )

    def configure_term_logger_setup(self):
        self.__term_handler.setLevel( self.__term_setup_loglevel )
    
    def configure_term_logger_call(self):
        self.__term_handler.setLevel( self.__term_call_loglevel )



    def debug(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.__logger.debug(msg, **kwargs, extra=extra)

    def info(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.info(msg, **kwargs, extra=extra)

    def warning(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            self.__logger.warning(msg, **kwargs, extra=extra)

    def error(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.error(msg, **kwargs, extra=extra)

    def passed(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger._log(levels["pass"], msg, (), **kwargs, extra=extra)

    def fail(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.__logger._log(levels["fail"]["level"], msg, (), **kwargs, extra=extra)
    
    def step(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.stepn += 1
        self.substepn = 0
        extra = {"step": f" {self.stepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger._log(levels["step"]["level"], msg, (), **kwargs, extra=extra)

    def substep(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.substepn += 1
        extra = {"step": f" {self.stepn}.{self.substepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            self.__logger._log(levels["substep"]["level"], msg, (), **kwargs, extra=extra)


log : TestLogger = TestLogger()