import logging


logger = logging.getLogger('momenteur_backend')
logger.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - [%(levelname)s] - %(message)s',
                      datefmt='%m/%d/%Y %H:%M:%S')

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)

logger.addHandler(ch)

## file handler (optional)
# fh = logging.FileHandler('/tmp/momenteur.log')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(f)
# logger.addHandler(fh)

if __name__=='__main__':
    logger.info('info here')
    logger.debug('debugging')
    logger.warning('warning sign')
