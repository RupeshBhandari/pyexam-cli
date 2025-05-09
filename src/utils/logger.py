import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Set up the logger
        self.logger = logging.getLogger("pyexam")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create file handler for all log messages
        log_file = os.path.join(logs_dir, f"pyexam_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler for error messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Create formatters and add to handlers
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, user: Optional[str] = None):
        self._log(logging.DEBUG, message, user)
    
    def info(self, message: str, user: Optional[str] = None):
        self._log(logging.INFO, message, user)
    
    def warning(self, message: str, user: Optional[str] = None):
        self._log(logging.WARNING, message, user)
    
    def error(self, message: str, user: Optional[str] = None):
        self._log(logging.ERROR, message, user)
    
    def critical(self, message: str, user: Optional[str] = None):
        self._log(logging.CRITICAL, message, user)
    
    def _log(self, level: int, message: str, user: Optional[str] = None):
        if user:
            message = f"[User: {user}] {message}"
        self.logger.log(level, message)