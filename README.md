## python_automation

> 一些打工人所需的python脚本
> 持续更新中...

**注意事项**：
- 每次先从GitHub拉取再提交，防止不一致冲突
- 测试没有用git config --global http.sslVerify "false"，是否能推送成功
- 测试关闭梯子是否推送成功
- 等待一段时间重新打开VScode进行验证

## Python with Pandas

一、pandas中的基本数据结构
```properties
panel：三维
dataframe：二维；使用pandas.DataFrame()可以从多种数据类型中创建DF，如列表、字典、excel、csv等
    df.values 把df转化为列表，每行为一组。
    df.T 转置数据
    df[0:3] 切片（每行为一组）
    df.loc['20130102':'20130104', ['A', 'B']] 同时在两个轴上进行切片
    df.iloc[[1, 2, 4], [0, 2]] 按位置切片
    df.iloc[3:5, 0:2] 同上
    df.iloc[3] 选择行
    df.iloc[1, 1] 具体定位某数据
    布尔索引： df[df.A > 0] 对某列进行数据筛选
    df2[df2['E'].isin(['two', 'four'])] isin的返回值是布尔序列，最外层通过索引根据布尔序列返回True的行
    df2[df2 > 0] = -df2[df2 > 0] 所有原始值大于0的元素都已被替换为它们的负数
    df.mean() 返回所有列的平均值
series：一维；类似固定大小的字典，可以通过索引标签对值进行操作
```