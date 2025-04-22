from loguru import logger
import sys
from pathlib import Path

# Set up logger
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger.remove()  # Remove default logger
logger.add(sys.stdout, level="INFO", colorize=True)
logger.add(str(LOG_DIR / "spindle.log"), rotation="500 KB", level="DEBUG", backtrace=True, diagnose=True)
