import logging
import os
from datetime import datetime

class Logger:
    """
    A singleton logger class that handles different log levels and outputs.
    
    This logger provides:
    - File logging for all INFO+ messages
    - Separate file for DEBUG+ messages
    - Console output for ERROR+ messages
    - User context tracking in logs
    """
    
    # Singleton instance
    _instance = None
    
    def __new__(cls):
        """
        Ensures only one logger instance exists throughout the application.
        This is the singleton pattern implementation.
        """
        if cls._instance is None:
            # Create a new instance if one doesn't exist yet
            cls._instance = super(Logger, cls).__new__(cls)
            # Initialize the logger for the new instance
            cls._instance._initialize_logger()
        # Return the existing instance
        return cls._instance
    
    def _initialize_logger(self):
        """
        Sets up the logging system with multiple handlers for different output destinations
        and log levels.
        """
        # Create logs directory if it doesn't exist
        # Navigate up three directory levels from the current file to find the project root
        logs_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Set up the main logger object
        self.logger = logging.getLogger("pyexam")
        # Set the minimum level for the logger to capture
        self.logger.setLevel(logging.DEBUG)  # Changed to DEBUG to capture all messages

        # Clear any existing handlers to avoid duplicates when logger is re-initialized
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # === DEBUG FILE HANDLER ===
        # Create a separate log file specifically for debug messages
        debug_log_file = os.path.join(logs_dir, f"pyexam_debug_{datetime.now().strftime('%Y%m%d')}.log")
        debug_file_handler = logging.FileHandler(debug_log_file)
        debug_file_handler.setLevel(logging.DEBUG)
        # Create a detailed formatter for debug logs
        debug_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        debug_file_handler.setFormatter(debug_formatter)
        debug_file_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
        
        # === MAIN LOG FILE HANDLER ===
        # Create file handler for general log messages (INFO and above)
        log_file = os.path.join(logs_dir, f"pyexam_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # === CONSOLE HANDLER ===
        # Create console handler for displaying error messages in the terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Create formatters for the handlers
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Console formatter is simpler for readability in terminal
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # Apply formatters to handlers
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        # Register all handlers with the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(debug_file_handler)
        self.logger.addHandler(console_handler)
    
    # Convenience methods for different log levels
    
    def debug(self, message: str, user: str = None):
        """Log a DEBUG level message."""
        self._log(logging.DEBUG, message, user)
    
    def info(self, message: str, user: str = None):
        """Log an INFO level message."""
        self._log(logging.INFO, message, user)
    
    def warning(self, message: str, user: str = None):
        """Log a WARNING level message."""
        self._log(logging.WARNING, message, user)
    
    def error(self, message: str, user: str = None):
        """Log an ERROR level message."""
        self._log(logging.ERROR, message, user)
    
    def critical(self, message: str, user: str = None):
        """Log a CRITICAL level message."""
        self._log(logging.CRITICAL, message, user)
    
    def _log(self, level: int, message: str, user: str = None):
        """
        Internal method to handle the actual logging.
        
        Args:
            level: The logging level (DEBUG, INFO, etc.)
            message: The message to log
            user: Optional username to include in the log for traceability
        """
        # Add user context to message if provided
        if user:
            message = f"[User: {user}] {message}"
        # Log the message with the appropriate level
        self.logger.log(level, message)