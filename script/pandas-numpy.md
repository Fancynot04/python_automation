## Python with Pandas

*格式要求*：
1. 装到统一的容器中，要求表名在pandas处理前就能够统一，方便操作
2. 对于空行、重复可以pandas处理，尽量做好关联字段一致
3. 关联字段列名不同时都会保留，列名相同时只保留一个

一、pandas中的基本数据结构
```python
panel：三维
dataframe：二维；使用pandas.DataFrame()可以从多种数据类型中创建DF，如列表、字典、excel、csv等
    pandas.read_csv("temp.csv",names=['a','b','c','d','e'],header=0) 通过header参数制定列标签位置，skiprows=2 跳过某行  
    df.values 把df转化为列表，每行为一组。
    df.T 转置数据
    df[0:3] 切片（每行为一组）
    基于标签 `只使用一个维度，则对行选择`
    df.loc['20130102':'20130104', ['A', 'B']] 同时在两个轴上进行切片
    df.loc[df.A>0.5] 选择所有A列大于0.5的行
    df.loc[lambda df:[0,1]] 选择前两行
    基于整数
    df.iloc[[1, 2, 4], [0, 2]] 按位置切片
    df.iloc[3:5, 0:2] 同上
    df.iloc[3] 选择行
    df.iloc[1, 1] 具体定位某数据
    df.A 选择某列
    布尔索引： df[df.A > 0] 对某列进行数据筛选
    df2[df2['E'].isin(['two', 'four'])] isin的返回值是布尔序列，最外层通过索引根据布尔序列返回True的行
    df2[df2 > 0] = -df2[df2 > 0] 所有原始值大于0的元素都已被替换为它们的负数
    df.pop() 删除列
    df.drop(0) 删除行
series：一维；类似固定大小的字典，可以通过索引标签对值进行操作
```

二、pandas中的参数
```python
DataFrame − “index 列方向” (axis=0，默认), “columns 行方向” (axis=1)
pandas.set_option('display.max_rows', 100,'display.max_columns', 1000,"display.max_colwidth",1000,'display.width',1000)
```

三、pandas中的统计函数
```markdown
series/panel/df.pct_change() 
    Series,DatFrames和Panel都有函数，此函数将每个元素与其前一个元素进行比较，并计算变化百分比;比如1,2,计算结果分别是1,0.5.
    默认对列进行操作，设置axis=1可对行操作
Series.rank() 
    方法用于对Series中的元素进行排名。排名可以是整数（默认），也可以是浮点数（当使用method参数时），并且可以是升序（ascending=True）或降序（ascending=False）。
count	非空数据的个数
sum	    数据之和,列的数值类型直接相加，字符串是追加
mean	算术平均值 ,列的平均值
mad	    平均绝对方差
median	中位数
min     最小值
max	    最大值
mode    众数
abs	    绝对值
describe 返回df的统计摘要，设置参数include='all'返回更多统计字段
```

三、DataFrame的基本功能
```python
DataFrame 基础操作
    df.T 转置，行整数和列标签也会转置
    df.axes，返回行轴标签和列轴标签的列表
    df.dtypes，返回每一列的数据类型
    df.empty，当df对象为空时，返回True
    df.shape，返回df的(行数,列数) 维度
    df.size，返回df中元素的个数
    df.value，返回df中每行元素为子列表的列表
    df.head(n)/df.tail(n)，返回前几行或后几行
DataFrame 函数操作
    df.pipe 针对df整体操作，如 df.pipe(add,2);def add(parm1,parm2)
    df.apply(func,axis=1) 逐行操作 
    df['col1'].map() 针对series使用的类似apply的函数
    df2.reindex_like(df1,method='ffill') df2与df1的索引对齐，ffill表示不够的向后填充NaN 但必须列标签一致 
    窗口函数：df.rolling(windows=3).max()  值将为前 n , n-1 和 n-2 元素的最大值
    sort_index(axis=1) 按照列标签排序，ascending=False 降序排序，无参数时(默认axis=0)，按照行索引排序
    sort_values()  by=['col1','col2']先按照col1列排序，col1相同时按照col2；kind='mergesort' 采用合并算法排序
    df.groupby('Year')['Points'].agg([np.mean,np.sum]) 根据year进行分组，并对point进行多种聚合操作
迭代对象只用于读取，返回的是对象的副本，对原始对象的修改不会显示在当前对象上
    for key,value in df.iteritems()  以标签作为键，以列值作为series对象
    for row_index,row in df.iterrows() 遍历行，类似上面
    for i in df 会输出列名
分组&聚合
    # 使用transform计算每个组的均值，并保留原始形状  
    df['group_mean_transform'] = df.groupby('group')['value'].transform('mean') 类似于窗口函数，在原表上新增一列 
    # 使用agg计算每个组的均值，结果是一个新的Series  
    group_means_agg = df.groupby('group')['value'].agg(np.mean)  分组聚合操作，只能在分组后的表上进行聚合，不影响原表
    df.groupby('Team').filter(lambda x: len(x) >= 3) 计算分组后每组的行数，行数>=3才保留
    pd.merge(left, right, how='inner', on=['id','subject_id'], left_on=None, right_on=None,left_index=False, right_index=False, sort=True)
    pd.concat([one,two],ignore_index=True) 行合并并重新建立索引，类似于union all;但是当axies=1时，效果类似于join
    one.append([two,one,two]) 这种形式也能行合并
```

四、pandas处理文本方法
```python
1   lower() 将Series/Index中的字符串转换为小写。
2	upper() 将Series/Index中的字符串转换为大写。
3	len() 计算字符串的长度。
4	strip() 帮助去除Series/Index中每个字符串两侧的空白（包括换行符）。
5	split(‘ ‘) 使用给定的模式拆分每个字符串。
6	cat(sep=’ ‘) 使用给定的分隔符连接Series/Index元素。
7	get_dummies() 返回具有One-Hot编码值的DataFrame。
8	contains(pattern) 对于每个元素，如果子字符串包含在元素中，则返回布尔值True，否则返回False。
9	replace(a,b) 替换值 a 为值 b 。
10	repeat(value) 重复每个元素指定次数。
11	count(pattern) 返回每个元素中模式出现的次数。
12	startswith(pattern) 如果Series/Index中的元素以模式开头，则返回True。
13	endswith(pattern) 如果Series/Index中的元素以pattern结尾，则返回true。
14	find(pattern) 返回pattern第一次出现的位置。
15	findall(pattern) 返回pattern所有出现的位置的列表。
16	swapcase 交换大小写。
17	islower() 检查Series/Index中每个字符串中的所有字符是否都为小写。返回布尔值。
18	isupper() 检查Series/Index中每个字符串中的所有字符是否都为大写。返回布尔值。
19	isnumeric() 检查Series/Index中每个字符串的所有字符是否都是数字。返回布尔值。
```

五、pandas与SQL的对比
```
分组聚合
    SELECT sex, count(*) FROM tips GROUP BY sex;
    tips.groupby('sex').size()
条件查询
    SELECT * FROM tips WHERE time = 'Dinner' LIMIT 5;
    tips[tips['time'] == 'Dinner'].head(5)
```

## Python with Numpy
一、基础概念
```python
    # 0.数组的创建
    arr_1d = numpy.array([1,2,3], dtype=complex) # 设置数据类型
    arr_2d = numpy.array(arr_1d,ndmin=2) # 保证维度至少为2
    arr_33 = numpy.eye(3) # 3x3的单位阵
    arr_range = numpy.arange(1,10,2) # 从1-10步长为2的一维阵
    arr_4 = numpy.asarray(arr_1d) # 这里参数可以是 列表、元组、列表元组组合、多维数组
    # numpy.frombuffer 用于实现动态数组。
    arr_iter = numpy.fromiter(iter(range(5)), dtype=numpy.int64, count=-1)
    # a = np.linspace(1,1,10) 设置等差数列， logspace设置等比数列
       
    # 1.创建数据类型对象dtype
    dt1 = numpy.dtype('>i4') # 大端法，int32
    dt2 = numpy.dtype([('age',numpy.int64)])
    # 1.2创建一个结构化数据类型Student(dtype),并应用到ndarray
    student = numpy.dtype([
        ('name','S20'), 
        ('age',numpy.int8),
        ('marks',numpy.float32)
    ]) # 'S20' 'i1' 'f4'
    stu = numpy.array([('abc', '2', 50),('xyz', 18, 75)], dtype = student) # 强转类型，转不了报错
    
    # 2.类型转换
    ra = numpy.random.random(4) # 长度为4的整型数组
    ra.dtype = 'float64' # 会改变数组的长度
    ra_1 = ra.astype('int64') # 不会改变数组的长度

    # 3.数组属性
    print('ra_1 :\n',ra_1.flags) # 返回内存信息
    z = numpy.zeros((2,2), dtype = [('x', 'i4'), ('y', 'i4')])
    print('维度: ',arr_1d.ndim) # 打印维度

    # 4.切片方式同python，添加slice方法？
    a = numpy.arange(10)
    s = slice(2,7,2)   # 从索引 2 开始到索引 7 停止，间隔为2
    print (a[s])

    # 5.高级索引,整数数组索引，布尔索引，花式索引，BroadCast
    x=numpy.arange(32).reshape((8,4))
    a = numpy.array([[ 0, 0, 0],
            [10,10,10],
            [20,20,20],
            [30,30,30]])
    b = numpy.array([1,2,3])
    #  bb = numpy.tile(b, (4, 1))
    print(a + b)

```