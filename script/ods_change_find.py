import pymysql 
import pandas as pd 
import json

# 1.登录配置读取
d_config = {}
with open(r'D:\donghua\登录相关信息.txt',mode='r',encoding='utf-8') as f:
    flag = 0 
    for line in f:
        if line.strip() == "【25测试环境】：":
            flag = 3
            continue
        if flag != 0:
            d_config[line.strip().split('：')[0]] = line.strip().split('：')[1]
            flag -= 1
host,user,pwd = d_config.values()        

   
# 2.连接数据库
connection = pymysql.connect(host=host,user=user,password=pwd,  
                             database=user,   
                             charset='utf8mb4',
                             port=3307,
                             cursorclass=pymysql.cursors.DictCursor)  

# 3.获取表数据并处理 
try:  
    with connection.cursor() as cursor:  
        # SQL 查询   
        sql = """
            select sys_code,tab_code,tab_name,rul_name,exc_sql from hnupsr.tab_rul_info a  
            where sys_code not in ('east','market') and RUL_STS = '1' 
            order by TAB_CODE,RUL_SEQ;  
        """
        cursor.execute(sql)  # 接受以元组形式的位置参数 
        result = cursor.fetchall()
          
        df = pd.DataFrame(result)
        df.columns = ['sys_code','tab_code','tab_name','rul_name','exc_sql']
        df['exc_sql'] = df['exc_sql'].apply(lambda x: x.decode('utf-8'))
        df.to_excel(r'D:\data.xlsx',index=False)
        
        # rs_decode = [item if type(item)!= 'bytes' else item.decode('utf-8') for item in result ]
        rs_decode = [
            d['exc_sql'].decode('utf-8') if isinstance(d['exc_sql'],bytes) else d['exc_code']
            for d in result
        ] #
        # with open(r'D:\data.xlsx', 'w') as f:  
        #     # 使用json.dump()将字典写入文件  
        #     # 确保文件是以文本模式（'w'）打开的  
        #     json.dump(rs_decode, f)  
        
finally:  
    connection.close()