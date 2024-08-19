import pymysql 
import pandas as pd 
from datetime import datetime,timedelta

"""
实现通过项目维度对其相关的east4表的时点数据进行取数和清洗转换
1.获取受益凭据的数据,再从此表维度采集受益所有人、信托合同表
2.获取产品基本表数据,根据受益凭据获取信托客户(三类),且大多项目为自益？
3.获取流水相关的全量数据,获取其他三张财务的当期数据
4.获取中文列名,以及数据字典的转换
"""

"""
进度：
1.循环实现多张表的查询,对查询顺序做要求
2.实现字典的自动转义(从upsr_dict_dtl中,或者服务器)
"""

# -1.字典匹配
def col_match(df_tab,df_dict):
    for col in df_tab.columns:
        col_dict = df_dict[df_dict['df_dict'=='EAST_'+col]]
        for r in df_tab.index:
            if df_tab.loc[r,col] == col_dict['opt_code']:
                df_tab.loc[r,col]=col_dict['opt_name']
    #TODO
   
                
def col_match(df_tab, df_dict):  
    # 假设 df_dict 是一个列表，其中每个元素都是一个字典，包含 'col_name', 'opt_code', 'opt_name'  
    for entry in df_dict:  
        col_name = entry['col_name']  
        if col_name in df_tab.columns:  # 确保列名在 DataFrame 中存在  
            opt_code = entry['opt_code']  
            opt_name = entry['opt_name']  
            # 遍历 DataFrame 的行  
            for r in df_tab.index:  
                if df_tab.loc[r, col_name] == opt_code:  
                    df_tab.loc[r, col_name] = opt_name                  
                
                

# 0.登录配置读取
def loginParm():
    d_config = {}
    with open(r'D:\donghua\登录相关信息.txt',mode='r',encoding='utf-8') as f:
        flag = 0 
        for line in f:
            if line.strip() == "【25测试环境登录】：":
                flag = 3
                continue
            if flag != 0:
                d_config[line.strip().split('：')[0]] = line.strip().split('：')[1]
                flag -= 1
    return d_config.values() 


# 1.参数定义
XTCPDM = ['20024','1103','212452001','220438001']
TABLE_LIST = ['east_xtcpjbxx','east_xtyyxx']
CJRQ = (datetime.now().replace(day=1)-timedelta(days=1)).strftime(r'%Y-%m-%d')
TABLE_COMMENT_QUERY = "select table_name, table_comment from information_schema.tables where table_schema = 'hneast4' and table_name in (%s);"
TABLE_COLUMN_QUERY = "select TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION,DATA_TYPE,COLUMN_KEY,COLUMN_COMMENT from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'HNEAST4' and TABLE_NAME = '{table_name}' order by ORDINAL_POSITION;"
TABLE_DICT_QUERY = r"SELECT DICT_NO,OPT_CODE,OPT_NAME FROM HNUPSR.UPSR_DICT_DTL WHERE DICT_NO like '%EAST4_%';"
TABLE_DATA_INTIME = "SELECT * FROM (SELECT A.*,ROW_NUMBER() OVER(PARTITION BY '{primary_key}' ORDER BY CJRQ DESC) RN FROM HNEAST4.{table_name} A WHERE xtcpdm in ('{XTCPDM}')) TMP WHERE RN = 1;"
TABLE_DATA_CURR = "SELECT * FROM HNEAST4.{table_name} where cjrq = '{cjrq}';"


# 2.连接数据库
host,user,pwd = loginParm()
connection = pymysql.connect(host=host,user=user,password=pwd,  
                database="hneast4",   
                charset='utf8mb4',
                port=3307,
                cursorclass=pymysql.cursors.DictCursor) 
print("Database connect success...")


# 3.获取表数据并处理 
try:  
    with connection.cursor() as cursor: 
        num = 0
        # 字典获取(全部加载)
        print("Load all dictory mapping...")
        rs3 = cursor.execute(TABLE_DICT_QUERY)
        df_dict = pd.DataFrame(cursor.fetchall() if rs3 else None)     
        print("Finished...")
    
        # for cpdm in XTCPDM:
        #     for tabname in TABLE_LIST:
    
        # 列属性
        print("Load east_xtyyxx's column attributes... ")
        rs1 = cursor.execute(TABLE_COLUMN_QUERY.format(table_name='east_xtyyxx'))
        df_col = pd.DataFrame(cursor.fetchall() if rs1 else None)# df = pd.DataFrame(cursor.execute(TABLE_DATA_INTIME).fetchall())
        pri_col = df_col[(df_col['COLUMN_KEY']=='PRI') & (df_col['COLUMN_NAME']!='CJRQ')]['COLUMN_NAME'].tolist()
        print("Finished...")
        
        # 表数据
        print("Load east_xtyyxx's datas...")
        rs2 = cursor.execute(TABLE_DATA_INTIME.format(primary_key="','".join(pri_col),table_name='east_xtyyxx',XTCPDM="','".join(XTCPDM)))
        df_tab = pd.DataFrame(cursor.fetchall() if rs2 else None).iloc[:, :-1]
        print("Finished...")    
        
        # 字典转换&列名替换        
        # TODO  
        print("Dictory is being converted...")
        col_match(df_tab,df_dict)
        df_tab.columns = df_col['COLUMN_COMMENT'].tolist()
        print("Finished...")
        
        # 数据输出
        print("Table output to excel....")
        rs4 = cursor.execute(TABLE_COMMENT_QUERY,'east_xtyyxx')
        df_com = pd.DataFrame(cursor.fetchall() if rs4 else None)
        df_tab.to_excel(r'D:/donghua/mission/project_ori_select.xlsx',
                        index=False,
                        sheet_name=df_com['TABLE_COMMENT'].to_list()[-1])
        print("Finished...")
        num += 1
        print("-------------------{num}---------------------".format(num=num))
    
except Exception as e:
    print("Error happened: " + e)             
finally:  
    connection.close()