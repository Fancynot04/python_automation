import pandas

def crs_check_excel():
    """
        function:

        params:

    """
    # 读取原始数据
    df_PERS = pandas.read_excel(r'D:\workspace\src\CRS-table.xlsx',sheet_name='CRS_PERS_INFO').iloc[3:,1:].reset_index(drop=True)
    df_CTRLG = pandas.read_excel(r'D:\workspace\src\CRS-table.xlsx',sheet_name='CRS_CTRLG_INFO').iloc[3:,1:].reset_index(drop=True)
    df_ORG = pandas.read_excel(r'D:\workspace\src\CRS-table.xlsx',sheet_name='CRS_ORG_INFO').iloc[3:,1:].reset_index(drop=True)
    df_JOB = pandas.read_excel(r'D:\workspace\src\CRS-table.xlsx',sheet_name='CRS_JOB_INFO').iloc[3:,1:].reset_index(drop=True)
    df_ORG.columns = ['字段','名称','数据类型','长度','小数位数','主键','非空','默认值','备注说明']
    df_CTRLG.columns = ['字段','名称','数据类型','长度','小数位数','主键','非空','默认值','备注说明']
    df_PERS.columns = ['字段','名称','数据类型','长度','小数位数','主键','非空','默认值','备注说明']
    df_JOB.columns = ['字段','名称','数据类型','长度','小数位数','主键','非空','默认值','备注说明']
    df_check_crs = pandas.read_excel(r'D:\workspace\src\校验规则-crs.xlsx',sheet_name='Sheet2')
    
    # 根据每张表需要校验的字段进行分表
    df_1 = df_check_crs.loc[df_check_crs['对应表名'].str.contains('CRS_PERS_INFO')]
    df_2 = df_check_crs.loc[df_check_crs['对应表名'].str.contains('CRS_CTRLG_INFO')]
    df_3 = df_check_crs.loc[df_check_crs['对应表名'].str.contains('CRS_ORG_INFO')]
    df_4 = df_check_crs.loc[df_check_crs['对应表名'].str.contains('CRS_JOB_INFO')]
    # 四个部分分别进行 left join
    df_1 = pandas.merge(df_1.loc[:,['元素','元素描述','对应字段']], df_PERS.loc[:,['字段','名称','数据类型']],left_on='对应字段', right_on='字段', how='left')
    df_2 = pandas.merge(df_2.loc[:,['元素','元素描述','对应字段']], df_CTRLG.loc[:,['字段','名称','数据类型']],left_on='对应字段', right_on='字段', how='left')
    df_3 = pandas.merge(df_3.loc[:,['元素','元素描述','对应字段']], df_ORG.loc[:,['字段','名称','数据类型']],left_on='对应字段', right_on='字段', how='left')
    df_4 = pandas.merge(df_4.loc[:,['元素','元素描述','对应字段']], df_JOB.loc[:,['字段','名称','数据类型']],left_on='对应字段', right_on='字段', how='left')
    # 重新设置四个部分的表名
    df_1['对应表名'] ='CRS_PERS_INFO' # 使用loc无法添加？？？
    df_2['对应表名'] ='CRS_CTRLG_INFO'
    df_3['对应表名'] ='CRS_ORG_INFO'
    df_4['对应表名'] ='CRS_JOB_INFO'
    df_1234 = df_1.append(df_2).append(df_3).append(df_4).reset_index(drop=True)
    
    basic_check_RS = pandas.DataFrame()
    basic_check_RS['TABLE_NAME'] = df_1234['对应表名']
    basic_check_RS['COLUMN_NAME'] = df_1234.apply(lambda row: row['元素'] if row['对应字段']=='暂不配置' else row['对应字段'] if ~pandas.isna(row['对应字段']) else row['元素'],axis=1)  # 实现对应字段为暂不配置则写入列'元素'对应的字段
    basic_check_RS['COLUMN_CHN_NAME'] = df_1234.apply(lambda row: row['元素描述'] if pandas.isna(row['名称']) else row['名称'],axis=1) # 元素描述
    basic_check_RS['DATA_TYPE'] = df_1234['数据类型']
    # 按照TABLE_NAME和COLUMN_CHN_NAME进行去重，保留重复组内的第一个
    basic_check_RS = basic_check_RS.drop_duplicates(subset=['TABLE_NAME','COLUMN_CHN_NAME'], keep='first')
    # 将序号转换为'A001'、'A002'等格式 ,这里使用字符串格式化来在'A'后面添加零填充的序号
    basic_check_RS['ERROR_CODE'] = basic_check_RS.groupby(['TABLE_NAME']).cumcount() + 1 
    basic_check_RS['ERROR_CODE'] = 'A' + basic_check_RS['ERROR_CODE'].apply(lambda x: '{:03d}'.format(x))
    basic_check_RS['SYS_CODE'] = 'crs'
    basic_check_RS['ERROR_DESC'] = '数据缺失或者格式不正确'   #(??)  VALUES (??);   	TABLE_NAME					
    
    def row_split_deal(row):  
        # 假设row是一个Pandas Series对象，并且它有足够的元素来匹配SQL语句中的字段  
        # 注意：这里我们直接使用了Series的索引，而不是假设它是一个元组  
        str_sql = f"""INSERT INTO hnupsr.parm_table_basic_check ('SYS_CODE', 'TABLE_NAME', 'COLUMN_NAME', 'COLUMN_CHN_NAME', 'ERROR_CODE', 'ERROR_DESC', 'DATA_TYPE')  
            VALUES (  
                '{row[5] if pandas.notnull(row[5]) else 'NULL'}', 
                '{row[0]}',  
                '{row[1]}',  
                '{row[2]}', 
                '{row[3] if pandas.notnull(row[3]) else 'NULL'}',  
                '{row[4] if pandas.notnull(row[4]) else 'NULL'}',
                '{row[6]}' 
            );
        """
        return str_sql
    basic_check_RS['INSERT_SQL'] = basic_check_RS.apply(lambda row: row_split_deal(row),axis=1)
    # 按照TABLE_NAME和COLUMN_CHN_NAME进行排序
    # basic_check_RS = basic_check_RS.sort_values(by=['TABLE_NAME', 'COLUMN_CHN_NAME'])  
    # 然后对排序后的DataFrame进行编号  
    # 使用shift检查上一个COLUMN_CHN_NAME是否与当前相同，如果不同则编号递增  
    # 初始化一个与DataFrame同样大小的0数组  
    # group_rank = (basic_check_RS_sorted['COLUMN_CHN_NAME'] != basic_check_RS_sorted['COLUMN_CHN_NAME'].shift()).astype(int).cumsum()  
    # # 如果想要从1开始编号，则使用cumcount() + 1，但这里我们使用上面计算得到的group_rank  
    # # 因为group_rank已经在每次COLUMN_CHN_NAME改变时递增了  
    # basic_check_RS_sorted['group_rank'] = group_rank  
    # # 如果需要将结果放回到原始的DataFrame索引顺序（可能不是必需的，取决于您的需求）  
    # # 可以使用原始DataFrame的index进行重新排序  
    # basic_check_RS['group_rank'] = basic_check_RS_sorted['group_rank'].reindex(basic_check_RS.index)  
    # print(basic_check_RS)
    basic_check_RS.to_excel(r'D:\workspace\src\basic_check_RS.xlsx',index=False)

def crs_rule_excel(): 
    pass

if __name__ == "__main__":
    crs_check_excel()

    
    