import logging

logger = logging.getLogger('momenteur_backend')
logger.setLevel(logging.DEBUG)

# file / console handler & formatter
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('momenteur.log')
fh.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
ch.setFormatter(f)
fh.setFormatter(f)

logger.addHandler(ch)
logger.addHandler(fh)
