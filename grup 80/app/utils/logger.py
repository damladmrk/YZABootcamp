import logging
import sys

def setup_logger(name, level="INFO"):
    """Yapılandırılmış logger oluşturur"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Formatter oluştur
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger