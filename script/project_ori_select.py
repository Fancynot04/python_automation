import pymysql 
import pandas as pd 
import json

"""
实现通过项目维度对其相关的east4表的时点数据进行取数和清洗转换
1.获取受益凭据的数据,再从此表维度采集受益所有人、信托合同表
2.获取产品基本表数据,根据受益凭据获取信托客户(三类),且大多项目为自益？
3.获取流水相关的全量数据,获取其他三张财务的当期数据
4.获取中文列名,以及数据字典的转换
"""

# 0.参数定义
TABLE_LIST = ('east_xtcpjbxx','east_a')
TABLE_COMMENT_QUERY = " select table_name, table_comment from information_schema.tables where table_schema = 'hneast4' and table_name in (%s)"




# 1.登录配置读取
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
print(d_config.values() )
host,user,pwd = d_config.values()        

   
# 2.连接数据库
connection = pymysql.connect(host=host,user=user,password=pwd,  
                             database="hneast4",   
                             charset='utf8mb4',
                             port=3307,
                             cursorclass=pymysql.cursors.DictCursor)  

# 3.获取表数据并处理 
try:  
    with connection.cursor() as cursor:  
        # SQL 查询   
        
        
        cursor.execute(
            TABLE_COMMENT_QUERY % ','.join('%s' * len(TABLE_LIST)),
            TABLE_LIST)  
        result = cursor.fetchall()
          
        df = pd.DataFrame(result)
        # df.columns = ['sys_code','tab_code','tab_name','rul_name','exc_sql']
        # df['exc_sql'] = df['exc_sql'].apply(lambda x: x.decode('utf-8'))
        # df.to_excel(r'D:\data.xlsx',sheet_name=""index=False)
        
        # rs_decode = [item if type(item)!= 'bytes' else item.decode('utf-8') for item in result ]
        # rs_decode = [
        #     d['exc_sql'].decode('utf-8') if isinstance(d['exc_sql'],bytes) else d['exc_code']
        #     for d in result
        # ] #
        
except Exception as e:
    print("Error happened:\n"+e)        
        
        
finally:  
    connection.close()