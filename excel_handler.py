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
        

def com6_12():
    """
        处理新旧版本表的对比
    """
    # 文件路径，后续可替换
    path_1 = 'D:\文档'
    path_2 = 'D:\donghua\6-7 对比'
    
    # 1.对新表规处理
    df_new = pandas.read_excel(r'D:\donghua\6-7 对比\对比专用表格.xlsx',sheet_name='新')
    df_new_1 = df_new[~ df_new['数据项名称new'].isna()]
    df_new_1['是否主键'] = df_new.apply(lambda row: '是' if pandas.notna(row['备注']) and 'PK' in str(row['备注']) else '否',axis=1)
    df_new_1['是否必填'] = df_new['是否必填'].apply(lambda x: '是' if pandas.notna(x) and '必填' in str(x) else '否')  
    
    # 2.对旧表规处理
    df_old = pandas.read_excel(r'D:\donghua\6-7 对比\对比专用表格.xlsx',sheet_name='旧')
    df_old_1 = df_old[~ df_old['数据项名称old'].isna()]
    df_old_1['是否主键'] = df_old.apply(lambda row: '是' if pandas.notna(row['备注']) and 'PK' in str(row['备注']) else '否',axis=1)
    df_old_1['是否必填'] = df_old['是否必填'].apply(lambda x: '是' if pandas.notna(x) and '必填' in str(x) else '否')

    # 3.两张表通过第三表join，以新表规为主表，展示新表的变化
    df_link = pandas.read_excel(r'D:\donghua\6-7 对比\对比专用表格.xlsx',sheet_name='关联',usecols=['新规表中文名','新规表英文名','原表中文名','原表英文名'])
    df_m1 = pandas.merge(df_new_1.loc[:,['表名','数据项代码','数据项名称new','数据元','数据元编码','是否主键','是否必填','具体差异','格式']],df_link,left_on='表名',right_on='新规表中文名', how='left')	
    df_m2 = pandas.merge(df_m1.loc[:,['具体差异','表名','新规表英文名','数据项代码','数据项名称new','格式','数据元','数据元编码','是否主键','是否必填','原表中文名']],
                         df_old_1.loc[:,['表名','数据项代码','数据项名称old','格式','数据元','数据元编码','是否主键','是否必填']],
                         left_on=['原表中文名','数据项名称new'],right_on=['表名','数据项名称old'], how='left').drop(columns=['原表中文名'],axis=1)
    # 3.1不必要字段，仅用于判断两张表对应字段是否有变化
    df_m2['是否相等'] = (
                       (df_m2['数据项名称new'] == df_m2['数据项名称old']) &
                       (df_m2['数据元_x'] == df_m2['数据元_y']) &
                       (df_m2['数据元编码_x'] == df_m2['数据元编码_y']) &
                       (df_m2['是否必填_x'] == df_m2['是否必填_y']) &
                       (df_m2['格式_x'] == df_m2['格式_y']))
    df_m2['是否存在差异'] = df_m2.apply(lambda row: '否' if row['是否相等'] else '是',axis=1)
    # 3.2判断具体的变化类型，暂无细分
    def judge(row):  
        if not row['是否相等']:  # 使用逻辑取反 not 而不是按位取反 ~  
            if row['数据项名称old'] is None or pandas.isna(row['数据项名称old']) or row['数据项名称old'].strip() == '':  
                # 增加了对 pd.isna 和空字符串的检查  
                return '新增'  
            else:  
                return '字段调整' 
    df_m2['变动方式'] = df_m2.apply(lambda row: judge(row),axis=1)
    
    
    # 3.2 对于原表中删除字段判断，不太详细，后续手工处理
    df_m_d = pandas.merge(df_old_1.loc[:,['表名','数据项代码','数据项名称old']],df_link,left_on='表名',right_on='原表中文名', how='left')
    df_m_delete = pandas.merge(df_m_d,
                         df_new_1.loc[:,['表名','数据项代码','数据项名称new']],
                         left_on=['新规表中文名','数据项名称old'],
                         right_on=['表名','数据项名称new'], how='left')
    # df_m_delete['变动方式'] = df_m_delete.apply(lambda row: judge(row),axis=1)
    
    # 4 输出为excel
    df_m2.to_excel(r'D:\donghua\6-7 对比\输出结果2.xlsx',index=False)
    df_m_delete = df_m_delete[df_m_delete['数据项名称new'].isna()]
    df_m_delete.to_excel(r'D:\donghua\6-7 对比\输出结果3.xlsx',index=False)
    
    """
    Questions:
    1.在你的例子中，row['是否相等'] 应该是一个布尔值（或者是一个可以评估为布尔值的表达式），因此你应该使用 not 来取反这个值。如果你错误地使用了 ~，那么 Python 会首先将 row['是否相等'] 转换为一个整数（True 变为 1，False 变为 0），然后对这个整数进行按位取反（1 变为 -2，0 变为 -1），这显然不是你想要的结果
    1的补码0000 00001按位取反1111 1110最终解释成-2
    """
    pass


if __name__ == '__main__':
    # df_d = pandas.read_excel(r'D:\donghua\6-7 对比\对比专用表格.xlsx',sheet_name='删除统计')
    # df_d2 = df_d.groupby(['表中文名','表英文名']).agg({'字段英文名':'count'}).reset_index()
    # df_d2.to_excel(r'D:\donghua\6-7 对比\输出结果4.xlsx',index=False)
    com6_12()
    


    
     









