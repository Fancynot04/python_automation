import logging
import os

class LoggingUtil:
    
    @classmethod
    def init_logger(cls,name=None,level=logging.INFO):
        """
        name: 日志名称\n
        level: 日志输出级别\n
        输出格式：当前时间-级别-名称-文件名-函数名-函数-具体信息
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        file_handler = logging.FileHandler(
            filename= "D:\workspace\python_automation\util\my.log", # os.path.join(conf.log_path,conf.log_name),
            mode="a", # 追加
            encoding="utf-8"
        )
        # 创建日志格式对象
        fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s):%(lineno)d] - %(message)s'")
        # 关联对象
        file_handler.setFormatter(fmt) # 绑定格式
        logger.addHandler(file_handler) # 绑定处理器

        return logger


if __name__ == '__main__':
    logger = LoggingUtil.init_logger("测试日志","INFO")
    logger.info("这是一条测试数据")