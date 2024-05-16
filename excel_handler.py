 
def process_data(self):  
    self.df['combine'] = self.df.apply(lambda row:row['字典值'].astype(str) + '-' + row['中文描述'], axis=1) # axis=1即为在行方向进行计算
    self.df['字典名称'] = self.df.apply(lambda row:row['中文描述'] if row['字典值']=='#' else None)
           
 
  
# 假设你的Excel文件名为'trust_institutions.xlsx'，并且数据在第一个工作表中  
df = pandas.read_excel('./数据源字典表.xls',usecols=['字典值','中文描述'],sheet_name='数据源字典表')  # 使用适当的文件路径 ,sheet_name,usecols
# 初始化一个空字典来存储结果  
trust_dict = {}  
values=''
# 遍历数据框的每一行  
for index, row in df.iterrows():
    if row.iloc[0] == '#':
        if values != "":
            trust_dict[key]=[values]
            values=''
        key = row.iloc[1]
    else:
        str_v = str(row.iloc[0])+'-'+row.iloc[1]
        values += str_v+';'
# 将字典转换为 DataFrame，其中键作为索引，值作为数据  
df = pandas.DataFrame.from_dict(trust_dict, orient='index', columns=['字典值列表']) 
# 重置索引，并将索引作为新的列 '键'
df = df.reset_index().rename(columns={'index': '字典名称'}) 
df.to_excel('./目标test.xlsx',index=False,sheet_name="数据字典映射")
print('执行成功')














