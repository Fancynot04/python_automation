import logging
import time 
import unittest
import os
import pymysql

def log_way():
    logger = logging.getLogger()
    # TODO 创建日志处理对象
    stream_handler = logging.StreamHandler()
    # file_handler = logging.FileHandler(filename,encoding="utf-8")

    # 创建日志格式对象
    fm = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s):%(lineno)d] - %(message)s'"
    fmt = logging.Formatter(fm)

    # TODO 关联对象
    stream_handler.setFormatter(fmt) # 绑定格式
    logger.addHandler(stream_handler) # 绑定处理器

    # 给日志设置打印级别
    logger.setLevel(logging.INFO)

    # TODO 使用日志对象操作
    logger.debug("调试信息")
    logger.info("日常信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重信息")


def time_way():
    # 获取当前时间的对象
    cur_time = time.localtime()
    # 获取当前时间的时间戳（单位：秒）
    print(time.time())
    str_time = time.strftime("%Y年%m月%d日 %H:%M:%S",cur_time)
    # 将字符串日期转换为日期对象
    time_object = time.strptime("2024年05月27日 16:36:40", "%Y年%m月%d日 %H:%M:%S")


def sum2num(a,b):
    return a+b


class TestSum(unittest.TestCase):
    # 建议使用pytest
    # TODO @classmethod，类方法只会在类调用的时候执行一次
    def setUp(self) -> None:
        self.a = 10
        self.b = 20
        print("测试的前置方法")
    # 普通前置、后置方法会在每个测试方法前后执行一次
    def tearDown(self) -> None:
        print("测试的后置方法")

    def test_func(self):
        result = sum2num(self.a,self.b)
        print(result)
        self.assertEqual(result,30)


def os_way():
    path = "d:/workspace/python_automation/etl_log.py"
    os.getcwd()
    os.listdir(r"D:\bigdata")
    # 只能基于当前运行文件的父目录生成绝对路径
    os.path.abspath("bigdata")
    os.path.dirname(path)
    file_name = os.path.dirname(path)
    file_path = os.path.basename(path)
    file_complete_path = os.path.join("d:/workspace/python_automation","etl_log.py")\
                        .replace("\\","/")
    # 当path为文件且存在时，返回True
    os.path.isfile(path)
    os.path.isdir(path)
    print(file_complete_path)


def sql_way():
    conn = pymysql.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        database="learn",
        port=3306,
        charset="utf8"
    )
    # 创建游标
    cursor = conn.cursor()
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    # 执行sql
    insert_sql = f"insert into student(sid,sname,sage,ssex) values ('15','安可','{curr_time}','女')"
    select_sql = "select ssex,count(ssex) from student group by ssex"

    cursor.execute(select_sql)
    
    # 注意：这里的数据只能取一次，所有这里one和many都为空
    all = cursor.fetchall()
    one = cursor.fetchone()
    many = cursor.fetchmany(5)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    # unittest.main() 
    pass