import os
import sys
import logging

# 1. Define the format of the logs
# [Timestamp] : [Log Level] : [Module Name] : [Message]
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# 2. Create the 'logs' folder if it doesn't exist
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# 3. Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        # Save logs to a file
        logging.FileHandler(log_filepath),
        # Also print logs to the terminal (stdout)
        logging.StreamHandler(sys.stdout)
    ]
)

# 4. Create the logger object
logger = logging.getLogger("victimDetectorLogger")