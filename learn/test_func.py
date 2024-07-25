import pandas as pd
from dbfread import DBF


path = r'D:\donghua\mission\7-24 底层资产相关资料\bond_info-8\PAR_BOND_INFO.dbf' # 文件目录
table = DBF(path, encoding='GBK')
df = pd.DataFrame(iter(table))

# df2 = pd.DataFrame(iter(DBF(r'D:\donghua\mission\7-24 底层资产相关资料\bond_info-8\',encoding='GBK')))

df_filter = df[df['ZQDM'].apply(
    lambda x:True if x in ('1828009',
        '1828012',
        '1928036',
        '1928021',
        '1928018',
        '1928028',
        '1928011',
        '1928009',
        '1928004') 
        else False)
    ]

















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




