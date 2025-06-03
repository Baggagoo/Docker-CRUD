import logging
from logging.handlers import RotatingFileHandler

log_handler = RotatingFileHandler(
    'escola_infantil.log', maxBytes=5 * 1024 * 1024, backupCount=3  # 5 MB por arquivo, até 3 backups
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[log_handler, logging.StreamHandler()]
)
logger = logging.getLogger("escola_infantil")

def log_operacao(tipo_operacao, sucesso, detalhes=None, erro=None):
    if sucesso:
        logger.info(f"Operação {tipo_operacao} realizada com sucesso. Detalhes: {detalhes}")
    else:
        logger.error(f"Erro na operação {tipo_operacao}. Detalhes: {detalhes}. Erro: {erro}")