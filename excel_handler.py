import pandas
def process_data(df):  
    df['combine'] = df.apply(lambda row:row['字典值'].astype(str) + '-' + row['中文描述'], axis=1) # axis=1即为在行方向进行计算
    df['字典名称'] = df.apply(lambda row:row['中文描述'] if row['字典值']=='#' else None)
           
 
def handler_excel(filepath:str,output_file:str):
    """
        function:
            对xls或xlsx文件处理,处理场景如:\n
            \#	受托职责\n
            0	主动管理 --> 受托职责 0-主动管理;1-被动管理;\n
            1	被动管理
        params:
            filepath---输入文件路径\n
            output_file---输出文件名称\n
    """
    df = pandas.read_excel(filepath,usecols=['字典值','中文描述'],sheet_name='数据源字典表')
    # 初始化一个空字典来存储结果  
    trust_dict = {}  
    values=''
    # 遍历数据框的每一行  
    for index, row in df.iterrows():
        if row.iloc[0] == '#':
            if values != "":
                trust_dict[key]=[values]
                print(key + ' 已插入')
                values=''
            key = row.iloc[1]
        else:
            str_v = str(row.iloc[0])+'-'+row.iloc[1]
            values += str_v+';'
    # 将字典转换为 DataFrame，其中键作为索引，值作为数据  
    df = pandas.DataFrame.from_dict(trust_dict, orient='index', columns=['字典值列表']) 
    # 重置索引，并将索引作为新的列 '键'
    df = df.reset_index().rename(columns={'index': '字典名称'}) 
    df.to_excel(output_file,index=False,sheet_name="数据字典映射")
    print('Excel生成成功')

def deal2in1_excel():
    df_map1 = pandas.read_excel(r'D:\workspace\src\规范正文：金融监管总局信托业监管数据标准化规范一览表（2024版）.xlsx',sheet_name='Sheet1')\
            .rename(columns={1: '字典编码', 2: '字典名'})
    df_map2 = pandas.read_excel(r'D:\workspace\src\East数据字典设置.xlsx',usecols=['字典名','字典项列表'],sheet_name='数据来源')    
    df_goal = pandas.DataFrame()
    # 拆分函数，接受一个字符串，返回一个列表 
    def split_str(text):
        if '；' in text:
            return [item.strip('。 ') for item in text.split('；') if item.strip()]
        if '、' in text:
            return [item.strip('。 ') for item in text.split('、') if item.strip()]
        if '，' in text:
            return [item.strip('。 ') for item in text.split('，') if item.strip()]
        else:
            return [text.strip('。 ')]
            
    df_goal['字典描述'] = df_map2.loc[1].apply(split_str).explode()    
    df_goal = df_map2.assign(字典描述=df_map2['字典项列表'].apply(split_str))\
            .explode('字典描述')\
            .drop(columns=['字典项列表'])
    
    df_goal['字典码值'] = df_goal.groupby('字典名').cumcount() + 1    
    df_goal = pandas.merge(df_map1, df_goal,on='字典名', how='right')\
        .reindex(columns=['字典编码','字典名','字典码值','字典描述'])
    df_goal.to_excel(r'D:\workspace\src\目标字典映射文件.xlsx', index=False)
    # print(df_goal)

    unique_count = df_goal['字典名'].nunique()
    print(f'字典名个数：{unique_count}')
    
if __name__ == '__main__':
    # handler_excel('./数据源字典表.xls','./目标test.xlsx')
    deal2in1_excel()
     









