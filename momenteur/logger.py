import logging

logger = logging.getLogger('momenteur_backend')
logger.setLevel(logging.DEBUG)

# file / console handler & formatter
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('/tmp/momenteur.log')
fh.setLevel(logging.DEBUG)

f = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - [%(levelname)s] - %(message)s',
                      datefmt='%m/%d/%Y %H:%M:%S')
ch.setFormatter(f)
fh.setFormatter(f)

logger.addHandler(ch)
logger.addHandler(fh)

if __name__=='__main__':
    logger.info('info here')
    logger.debug('debugging')
    logger.warning('warning sign')
