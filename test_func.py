import numpy

def test_func():
    return


if __name__ == '__main__':
    
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
