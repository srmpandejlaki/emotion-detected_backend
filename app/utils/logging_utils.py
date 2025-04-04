import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message: str):
    """
    Mencatat error ke dalam log.
    """
    logging.error(message)
