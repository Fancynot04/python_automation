import pandas
def process_data(df,df_check_crs,camel_to_snake):  
    df['combine'] = df.apply(lambda row:row['字典值'].astype(str) + '-' + row['中文描述'], axis=1) # axis=1即为在行方向进行计算
    df['字典名称'] = df.apply(lambda row:row['中文描述'] if row['字典值']=='#' else None)
    mask = df_check_crs['对应字段'].isnull() | (df_check_crs['对应字段'] == '')  
    df_check_crs.loc[mask,'对应字段'] = df_check_crs.loc[mask,'元素'].apply(camel_to_snake)
    df_check_crs.to_excel(r'D:\workspace\src\df_check_crs.xlsx', index=False)
           
 
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
    """
        function:
            类似handler_excel的逆过程,不过源文件涉及到两个excel处理
    """
    df_map1 = pandas.read_excel(r'D:\workspace\src\规范正文：金融监管总局信托业监管数据标准化规范一览表（2024版）.xlsx',sheet_name='Sheet1')\
            .rename(columns={0: '字典编码', 1: '字典名'}) # 直接在read_excel中使用columns参数，列名必须在excel中存在
    df_map2 = pandas.read_excel(r'D:\workspace\src\East数据字典设置.xlsx',usecols=['字典名','字典项列表'],sheet_name='数据来源')    
    df_goal = pandas.DataFrame()
    # 拆分函数，接受一个字符串，返回一个列表 
    def split_str(text):
        if '；' in text:
            return [item.strip('。 ') for item in text.split('；') if item.strip()]
        if '，' in text:
            return [item.strip('。 ') for item in text.split('，') if item.strip()]
        if '、' in text:
            return [item.strip('。 ') for item in text.split('、') if item.strip()]
        else:
            return [text.strip('。 ')]
               
    df_goal = df_map2.assign(字典描述=df_map2['字典项列表'].apply(split_str))\
            .explode('字典描述')\
            .drop(columns=['字典项列表']) # df.drop('字典项列表', axis=1, inplace=True) 删除列，并修改源df
    
    df_goal['字典码值'] = df_goal.groupby('字典名').cumcount() + 1    
    df_goal = pandas.merge(df_map1, df_goal,on='字典名', how='right')\
        .reindex(columns=['字典编码','字典名','字典码值','字典描述'])
    df_goal.to_excel(r'D:\workspace\src\目标字典映射文件.xlsx', index=False)
    # print(df_goal)

    unique_count = df_goal['字典名'].nunique()
    print(f'字典名个数：{unique_count}')
    
def compare_excel():
    df_new_1 = df_new[ ~ df_new['数据项名称'].isna()].groupby(['表编号','表名']).agg({'数据项编号':'count'}).reset_index()
    # rs = pandas.merge(df_new_1,name_map,left_on='表名',right_on='表中文名',how='left')
    name_map = pandas.read_excel(r'D:\文档\对比专用表格.xlsx',sheet_name='中英对应').drop_duplicates() 
    pandas.merge(df_new_1,name_map,left_on='表名',right_on='表中文名',how='left')\
        .drop('表中文名',axis=1)\
        .reindex(
            columns=['表编号','表名','表英文名','数据项编号']
        ).reset_index(drop=True)\
        .to_excel(r'D:\文档\输出结果.xlsx',index=False)
        
    df_old_1 = df_old[ ~ df_old['数据项名称'].isna()].groupby(['表名','传输文件名称']).agg({'数据项编号':'count'}).reset_index()
        


if __name__ == '__main__':
    # deal2in1_excel()
    path_1 = 'D:\文档'
    path_2 = 'D:\donghua\6-7 对比'
    
    df_new = pandas.read_excel(r'D:\文档\对比专用表格.xlsx',sheet_name='新')
    df_new_1 = df_new[~ df_new['数据项名称new'].isna()]
    df_new_1['是否主键'] = df_new.apply(lambda row: '是' if pandas.notna(row['备注']) and 'PK' in str(row['备注']) else '否',axis=1)
    df_new_1['是否必填'] = df_new['是否必填'].apply(lambda x: '是' if pandas.notna(x) and '必填' in str(x) else '否')  
    
    df_old = pandas.read_excel(r'D:\文档\对比专用表格.xlsx',sheet_name='旧')
    df_old_1 = df_old[~ df_old['数据项名称old'].isna()]
    df_old_1['是否主键'] = df_old.apply(lambda row: '是' if pandas.notna(row['备注']) and 'PK' in str(row['备注']) else '否',axis=1)
    df_old_1['是否必填'] = df_old['是否必填'].apply(lambda x: '是' if pandas.notna(x) and '必填' in str(x) else '否')

    
    df_link = pandas.read_excel(r'D:\文档\对比专用表格.xlsx',sheet_name='关联',usecols=['新规表中文名','新规表英文名','原表中文名','原表英文名'])
    df_m1 = pandas.merge(df_new_1.loc[:,['表名','数据项代码','数据项名称new','数据元','数据元编码','是否主键','是否必填','具体差异','格式']],df_link,left_on='表名',right_on='新规表中文名', how='left')	
    df_m2 = pandas.merge(df_m1.loc[:,['具体差异','表名','新规表英文名','数据项代码','数据项名称new','格式','数据元','数据元编码','是否主键','是否必填','原表中文名']],
                         df_old_1.loc[:,['表名','数据项代码','数据项名称old','格式','数据元','数据元编码','是否必填','是否主键']],
                         left_on=['原表中文名','数据项名称new'],right_on=['表名','数据项名称old'], how='left').drop(columns=['原表中文名'],axis=1)
    df_m2.to_excel(r'D:\文档\输出结果2.xlsx',index=False)
    
    
    
    
    
    # df_old_1.to_excel(r'D:\文档\输出结果2.xlsx',index=False)
    


    
     









