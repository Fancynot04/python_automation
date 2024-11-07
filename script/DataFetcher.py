import pymysql 
import json
import pandas as pd 
import atexit
from datetime import datetime,timedelta


class DataFetcher:
    """
        封装整个执行过程,必要参数提供外接口
        初步功能思路:
            1.基础功能：获取数据，字典转换，列名和表名转换
            2.自定义查询语句,备选几种sql语句
            3.根据表名、日期范围、主键值查询
            4.根据项目查询相关的所有表的时点数据    
    """
    # 常量定义
    CJRQ = (datetime.now().replace(day=1)-timedelta(days=1)).strftime(r'%Y-%m-%d')
    
     
    def __init__(self,select_url:str):
        """
            Init the connection with the database
        """  
        data = self._login_parm(select_url)
        self.host = data['url']
        self.user = data['username']
        self.password = data['password']
        self.port = int(data['port'])
        self.database = 'HNEAST4'
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port)
        self.cursor = self.conn.cursor()
        self.primary_columns = []


    def _login_parm(self,select_url='25'):
        """
            Load the login parameter from json file
        """
        data = {}
        with open(r'D:\donghua\login_config.json','r',encoding='utf-8') as file:
            data = json.load(file)[str(select_url)]
        return data
 
    
    def _dict_fetch(self) -> pd.DataFrame:
        """
            Get the dictionary data of east4 system
        """
        dict_sql=f"SELECT * FROM HNUPSR.UPSR_DICT_DTL WHERE DICT_NO LIKE 'EAST_%'"
        rs_code = self.cursor.execute(dict_sql)
        columns = [col[0] for col in self.cursor.description]
        df_dict = pd.DataFrame(self.cursor.fetchall() if rs_code else None,columns=columns)
        return df_dict


    def _col_match(self,df_tab,df_map,df_dict) -> None:
        """
            Convert the dictionary data in the table
        """
        column_mappings = {}
        for index,row in df_map[df_map['DICT_FLAG']=='Y'].iterrows():
            col_name = row['COLUMN_NAME']
            dict_no = row['DICT_NO']
            dict_data = df_dict[df_dict['DICT_NO']==dict_no].loc[:,('OPT_CODE','OPT_NAME')]
            mapping_dict = dict(zip(dict_data['OPT_CODE'],dict_data['OPT_NAME']))
            column_mappings[col_name] = mapping_dict
            # dict_data.set_index('OPT_CODE',inplace=True)
        for col_name,mapping in column_mappings.items():
            if col_name in df_tab.columns:
                df_tab[col_name] = df_tab[col_name].map(mapping).fillna(df_tab[col_name])
        return 

    
    def _sql_select(self,table_name:str,type:int=1,cjrq:str=CJRQ,xtcpdm_list:list=[]) -> str:
        """
            Get the sql statement of the table
            type:\n
                1: 指定采集日期
                2: 最新时点数据
                3: 指定产品的累计数据
        """
        sql_str = f"SELECT * FROM HNEAST4.{table_name} where cjrq = '{cjrq}';" 
        
        if type == 1:
            # TABLE_DATA_CURR
            pass
        elif type == 2: 
            # TABLE_DATA_INTIME  
            primary_columns_str = ','.join(self.primary_columns)
            sql_str = f"SELECT * FROM (SELECT A.*,ROW_NUMBER() OVER(PARTITION BY {primary_columns_str} ORDER BY CJRQ DESC) RN FROM {self.database}.{table_name} A ) TMP WHERE RN = 1 AND CJRQ <= '{cjrq}';"
        elif type == 3:
            # TABLE_DATA_VARIATION
            if(len(xtcpdm_list)==1):
                xtcpdm_str = str(xtcpdm_list[0])
            else:
                xtcpdm_str = ','.join(xtcpdm_list)
            sql_str = f"SELECT * FROM HNEAST4.{table_name} WHERE CJRQ = '{cjrq}' and XTCPDM IN ('{xtcpdm_str}') " # WHERE xtcpdm in ('{XTCPDM}')
        else:
            # OTHER CASE 
            print("_sql_select: invaild type, return default sql")    
        return sql_str

    
    def _get_data(self,table_name:str,type:int,cjrq:str=CJRQ,xtcpdm_list:list=[]) -> pd.DataFrame:
        """
            执行sql语句
            1.没有获取到列名,可能是cursor.fetchall()的原因
        """  
        cursor = self.cursor
        
        # 列属性(时点数据)
        TABLE_COLUMN_QUERY = f"SELECT TABLE_NAME,COLUMN_NAME,ORDINAL_POSITION,DATA_TYPE,COLUMN_KEY,COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table_name}' ORDER BY ORDINAL_POSITION;"
        rs1_code = self.cursor.execute(TABLE_COLUMN_QUERY)
        columns = [col[0] for col in self.cursor.description] 
        df_col = pd.DataFrame(self.cursor.fetchall()  if rs1_code else None,columns=columns)
        self.primary_columns = df_col[(df_col['COLUMN_KEY']=='PRI') & (df_col['COLUMN_NAME']!='CJRQ')]['COLUMN_NAME'].tolist()
        
        # 表数据
        rs2_code = cursor.execute(self._sql_select(table_name=table_name,type=type,cjrq=cjrq,xtcpdm_list=xtcpdm_list))
        columns = [col[0] for col in cursor.description]
        tmp = pd.DataFrame(cursor.fetchall() if rs2_code else None,columns=columns)
        
        # 注：仅当表数据不为空时，才执行后面的操作，否则直接返回
        if rs2_code == 0 or tmp.empty: 
            return tmp
        tmp.columns = tmp.columns.str.upper()
        df_tab = tmp.iloc[:,2:tmp.columns.get_loc('CJRQ')+1]
            
        # 字典转换
        PARM_COLS_INFO = f"SELECT SYS_CODE,TABLE_NAME,COLUMN_NAME,COLUMN_CHN_NAME,IS_PRIMARY_KEY,DICT_FLAG,DICT_NO FROM HNUPSR.PARM_COLS_INFO WHERE SYS_CODE='EAST4' AND TABLE_NAME = '{table_name}'"
        rs3_code = cursor.execute(PARM_COLS_INFO)
        columns = [col[0] for col in cursor.description]
        df_map = pd.DataFrame(cursor.fetchall() if rs3_code else None,columns=columns) 
        self._col_match(df_tab,df_map,self._dict_fetch()) # 不转换时直接注释掉此行
        
        # 列名替换
        mapping_col_dict = dict(zip(df_col['COLUMN_NAME'],df_col['COLUMN_COMMENT']))
        df_tab.columns = df_tab.columns.map(lambda x:mapping_col_dict.get(x,x))            
        return df_tab
    
    
    def excel_output(self,table_list:list,type:int=1,cjrq:str=CJRQ,xtcpdm_list:list=[],output_path:str=r'D:/donghua/mission/project_ori_select.xlsx') -> str:
        """
            输出到excel\n
            type:\n
                1: 指定采集日期的全量 cjrq=date(?)
                2: 最新时点数据 rn=1
                3: 指定产品的当期数据 
        """
        with pd.ExcelWriter(output_path,engine='openpyxl') as writer:
            num=0
            for table_name in table_list:
                df_tab = self._get_data(table_name=table_name,type=type,cjrq=cjrq,xtcpdm_list=xtcpdm_list)
                TABLE_COMMENT_QUERY = "select table_name, table_comment from information_schema.tables where table_schema = 'hneast4' and table_name in (%s);"
                rs_code = self.cursor.execute(TABLE_COMMENT_QUERY,table_name)
                columns = [col[0] for col in self.cursor.description]
                df_com = pd.DataFrame(self.cursor.fetchall() if rs_code else None,columns=columns)
                df_tab.to_excel(writer,
                                sheet_name=df_com['TABLE_COMMENT'].to_list()[-1],
                                index=False)
                print(f"输出{table_name}表数据成功,共{df_tab.shape[0]}条数据")
        return "ヾ(￣▽￣)Bye~Bye~"
    
    
    def _close_conn(self):
        self.conn.close()
   
global_instance = []

def close_all_conn():
    """
        Auto close the connection
        未正常关闭,自动调用时会缺失self参数
    """
    for instance in global_instance:
        instance._close_conn()
atexit.register(close_all_conn)


if __name__ == '__main__':
    conn = DataFetcher(187) # 25,187
    xtcpdm_list = ['240807001']
    table_list=['east_xtcpjbxx','east_xtyyxx','east_xtzcfztjb']
    info = conn.excel_output(table_list=table_list,type=3,xtcpdm_list=xtcpdm_list,output_path=r'D:/donghua/mission/data_east4.xlsx')
    print(info)
   