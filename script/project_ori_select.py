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
问题总结：
[x]1.尚未完成表的指定范围列的获取,依旧是全表
[x]2.在列名更换中,采用df.columns直接赋值,并没有根据列名匹配
[√]3.字典匹配中,由于无法界定df中数据类型的范围,导致通过col_match无法实现,具体思路去查看col_match函数
[x]4.在采集表数据时,并没有根据时点数据、某些表由受益凭据(xthtbh/nbyyhtbh/syrbh...)来采集、本期数据的要求去采集数据,目前思路是通过字典添加标识,采用case去判定
[x]5.对日志输出的优化问题:由于python可能采用的异步执行方式,导致执行日志没有出现在相应位置,后续可能采用logging等库去优化
"""

# -1.字典匹配
def col_match(df_tab,df_map,df_dict):
    """
    Args:
        df_tab (dataframe): 需要转化的表数据
        df_map (dataframe):字典关系映射表
        df_dict (dataframe): 字典表
    """
    # 构建映射字典
    column_mappings = {}
    for index,row in df_map[df_map['DICT_FLAG']=='Y'].iterrows():
        col_name = row['COLUMN_NAME']
        dict_no = row['DICT_NO']
        dict_data = df_dict[df_dict['DICT_NO']==dict_no][['OPT_CODE','OPT_NAME']]
        mapping_dict = dict(zip(dict_data['OPT_CODE'],dict_data['OPT_NAME']))
        column_mappings[col_name] = mapping_dict
        # dict_data.set_index('OPT_CODE',inplace=True)
    for col_name,mapping in column_mappings.items():
        if col_name in df_tab.columns:
            df_tab[col_name] = df_tab[col_name].map(mapping).fillna(df_tab[col_name])
    return 
    
                
# 0.登录配置读取
def loginParm():
    d_config = {}
    with open(r'D:\donghua\登录相关信息.txt',mode='r',encoding='utf-8') as f:
        flag = 0 
        for line in f:
            if line.strip() == "【25测试环境登录】：":
                flag = 4
                continue
            if flag != 0:
                d_config[line.strip().split('：')[0]] = line.strip().split('：')[1]
                flag -= 1
    return d_config.values() 



# 1.参数定义
XTCPDM = ['20024','1103','212452001','220438001','12062']
TABLE_LIST = ['east_xtcpjbxx','east_xtyyxx','east_xtsyqzrxx','east_xtmjfpls']
CJRQ = (datetime.now().replace(day=1)-timedelta(days=1)).strftime(r'%Y-%m-%d')
TABLE_COMMENT_QUERY = "select table_name, table_comment from information_schema.tables where table_schema = 'hneast4' and table_name in (%s);"
TABLE_COLUMN_QUERY = "select TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION,DATA_TYPE,COLUMN_KEY,COLUMN_COMMENT from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'HNEAST4' and TABLE_NAME = '{table_name}' order by ORDINAL_POSITION;"
PARM_COLS_INFO = "SELECT SYS_CODE,TABLE_NAME,COLUMN_NAME,COLUMN_CHN_NAME,IS_PRIMARY_KEY,DICT_FLAG,DICT_NO FROM HNUPSR.PARM_COLS_INFO WHERE SYS_CODE='EAST4' AND TABLE_NAME = '{table_name}'"
TABLE_DICT_QUERY = r"SELECT DICT_NO,OPT_CODE,OPT_NAME FROM HNUPSR.UPSR_DICT_DTL WHERE DICT_NO like '%EAST4_%';"
TABLE_DATA_INTIME = "SELECT * FROM (SELECT A.*,ROW_NUMBER() OVER(PARTITION BY '{primary_key}' ORDER BY CJRQ DESC) RN FROM HNEAST4.{table_name} A WHERE xtcpdm in ('{XTCPDM}')) TMP WHERE RN = 1;"
TABLE_DATA_CURR = "SELECT * FROM HNEAST4.{table_name} where cjrq = '{cjrq}';"


# 2.连接数据库
host,user,pwd,port = loginParm()
connection = pymysql.connect(host=host,user=user,password=pwd,port=int(port), 
                database="hneast4",   
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor) 
print("0-Database connect success...")


# 3.获取表数据并处理 
try:  
    with connection.cursor() as cursor,\
        pd.ExcelWriter(r'D:/donghua/mission/project_ori_select.xlsx',engine='openpyxl') as writer: 
        num = 0
        # 字典获取(全部加载)
        print("0-Load all dictory mapping...")
        rs3 = cursor.execute(TABLE_DICT_QUERY)
        df_dict = pd.DataFrame(cursor.fetchall() if rs3 else None)     
        print("0-Finished!")
    
    
        for tabname in TABLE_LIST:
            
            # 列属性
            print("1-Load {}'s column attributes... ".format(tabname))
            rs1 = cursor.execute(TABLE_COLUMN_QUERY.format(table_name=tabname))
            df_col = pd.DataFrame(cursor.fetchall() if rs1 else None)# df = pd.DataFrame(cursor.execute(TABLE_DATA_INTIME).fetchall())
            pri_col = df_col[(df_col['COLUMN_KEY']=='PRI') & (df_col['COLUMN_NAME']!='CJRQ')]['COLUMN_NAME'].tolist()
            print("1-Finished!")
            
            # 表数据
            print("2-Load {}'s datas...".format(tabname))
            if tabname == 'east_xtmjfpls':
                rs2 = cursor.execute(TABLE_DATA_CURR.format(table_name=tabname,cjrq='2020-09-30'))
            else:
                rs2 = cursor.execute(TABLE_DATA_INTIME.format(primary_key="','".join(pri_col),table_name=tabname,XTCPDM="','".join(XTCPDM)))
            tmp = pd.DataFrame(cursor.fetchall() if rs2 else None)
            tmp.columns = tmp.columns.str.upper()
            df_tab = tmp.iloc[:,2:tmp.columns.get_loc('CJRQ')+1]
            print("2-Finished!")    
            
            # 字典转换&列名替换
            print("3-Dictory is being converted...")
            rs5 = cursor.execute(PARM_COLS_INFO.format(table_name=tabname))
            df_map = pd.DataFrame(cursor.fetchall() if rs5 else None) 
            col_match(df_tab,df_map,df_dict)
            print("3-Dictionary mappings have been loaded...")
            if not df_tab.empty:
                mapping_col = dict(zip(df_col['COLUMN_NAME'],df_col['COLUMN_COMMENT']))
                new_col = {}
                df_tab.columns = df_tab.columns.map(lambda x:mapping_col.get(x,x))
                # df_tab.columns = [str(comment) for comment in df_col['COLUMN_COMMENT']]
            print("3-Finished!")
            
            # 数据输出
            print("4-Table output to excel....")
            rs4 = cursor.execute(TABLE_COMMENT_QUERY,tabname)
            df_com = pd.DataFrame(cursor.fetchall() if rs4 else None)
            df_tab.to_excel(writer,
                            sheet_name=df_com['TABLE_COMMENT'].to_list()[-1],
                            index=False)
            print("4-Finished!")
            num += 1
            print("-------------------{num}---------------------".format(num=num))
except Exception as e:
    print("Error happened: " + e)             
finally:  
    connection.close()