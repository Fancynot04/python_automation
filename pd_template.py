import pandas as pd  
import numpy as np  
'''
    基本思路：
    1.


'''
# 1. 加载数据  
# 可以从CSV、Excel、SQL数据库、API等加载数据  
file_path = 'data.csv'  # 假设你的数据文件名为data.csv  
df = pd.read_csv(file_path)  
  
# 2. 数据清洗  
# 缺失值处理  
print(df.isnull().sum())  # 检查缺失值  
df = df.dropna(subset=['column_with_missing_values'])  # 删除包含缺失值的行（仅针对某列）  
df = df.fillna(method='ffill')  # 使用前向填充处理缺失值  
  
# 重复值处理  
df = df.drop_duplicates()  # 删除重复行  
  
# 数据类型转换  
df['column_name'] = pd.to_numeric(df['column_name'], errors='coerce')  # 将字符串列转换为数值列（无法转换的变为NaN）  
  
# 文本清洗（如果需要）  
df['text_column'] = df['text_column'].str.lower()  # 转换为小写  
df['text_column'] = df['text_column'].str.strip()  # 去除首尾空格  
  
# 3. 数据转换  
# 创建新列  
df['new_column'] = df['column1'] + df['column2']  # 假设你需要将两列相加得到新列  
  
# 使用函数进行复杂转换  
def complex_transformation(row):  
    # 在这里定义你的转换逻辑  
    return row['column1'] * 2 if row['column2'] > 10 else row['column1']  
  
df['transformed_column'] = df.apply(complex_transformation, axis=1)  
  
# 使用groupby和聚合函数  
grouped_df = df.groupby('group_column').agg({'value_column': 'sum'}).reset_index()  
  
# 4. 数据分析  
# 使用describe()查看数值列的统计信息  
print(df.describe())  
  
# 使用corr()查看列之间的相关性  
print(df.corr())  
  
# 使用绘图库（如matplotlib或seaborn）进行可视化分析  
import matplotlib.pyplot as plt  
df['column_name'].plot(kind='hist')  
plt.show()  
  
# 5. 保存结果  
# 将清洗和转换后的数据保存为新文件  
output_path = 'cleaned_data.csv'  
df.to_csv(output_path, index=False)  
  
# 如果需要，也可以将数据保存为Excel文件或其他格式  
df.to_excel('cleaned_data.xlsx', index=False)