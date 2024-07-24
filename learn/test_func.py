def test():
    """
    字符串令牌化：
        模式识别，字符串匹配，数据挖掘等
    """
    text = 'foo = 23 + 42 * 10'

    import re
    NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
    NUM = r'(?P<NUM>\d+)'
    PLUS = r'(?P<PLUS>\+)'
    TIMES = r'(?P<TIMES>\*)'
    EQ = r'(?P<EQ>=)'
    WS = r'(?P<WS>\s+)'

    master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
    scanner = master_pat.scanner('foo = 42')


import pandas as pd
from dbfread import DBF
path = r'D:\Projects\Repo 3\task_files\20191212\000003_ZRTJSTZ.dbf' # 文件目录
table = DBF(path, encoding='GBK')
df = pd.DataFrame(iter(table))












