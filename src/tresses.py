from tools.tipe_tresses import double_simplification
from tools.tipe_tresses import EXEMPLE_1, LOGGER

if __name__ == "__main__":
    LOGGER.debug(EXEMPLE_1)
    result = double_simplification(EXEMPLE_1)
    LOGGER.info(result)