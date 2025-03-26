import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import settings

def setup_logging():
    """初始化日志系统"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True, parents=True)
    
    logging.basicConfig(
        level=logging.DEBUG if settings.settings.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                log_dir/"app.log",
                maxBytes=10*1024*1024,
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    # 禁用passlib的调试日志
    logging.getLogger('passlib').setLevel(logging.WARNING)

#gpt改
class APILogger:
    def __init__(self, name: str):
        """初始化日志器"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 添加日志处理器
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    # ✅ 标准日志方法
    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)

    def error(self, message: str):
        """记录错误日志"""
        self.logger.error(message)

    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)

    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)

    # ✅ 自定义方法，保持向后兼容
    def log_request(self, path: str, client: str):
        """记录请求日志"""
        self.logger.info(f"Request: {path} from {client}")

    def log_error(self, error: Exception):
        """记录异常日志"""
        self.logger.error(f"Error: {str(error)}", exc_info=True)


# 初始化日志
setup_logging()

