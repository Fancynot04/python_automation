## 迭代器

> 1. 通过覆盖__iter__和__next__方式实现代理迭代，同时执行一些其他的任务：日志记录，权限校验，数据转换;
> 2. 使用生成器生成新的迭代模式 yield(惰性求值，暂停)，如frange(s,e,step);
> 3. yield在函数中创建迭代器，函数在调用时不会立即执行，会返回一个迭代器对象，执行到yield时候会暂停，返回其值;
> 4. 只有在下一次调用next时才会执行，同上；而for语句会自动遍历;

## Low-level code logic 
#### 1.dis & exec
```python
"""
    常用方法：dis、compile、exec
    执行过程：
        0 LOAD_CONST   加载常量到操作栈
        2 STORE_FAST   将操作栈的值存储到局部变量
        4 LOAD_FAST    加载局部变量到操作栈
        6 GET_ITER     获取迭代器，并推送到操作栈
        8 FOR_ITER     开始for循环
        10 STORE_FAST   

        12 LOAD_FAST    
        14 LOAD_GLOBAL  加载全局函数str到操作栈上
        16 LOAD_FAST    
        18 CALL_FUNCTION    调用栈顶函数并传入参数，将结果推送到操作栈
        20 INPLACE_ADD  将操作栈的两个值进行连接，并替换成结果值
        22 STORE_FAST   
        24 JUMP_ABSOLUTE    无条件跳转
                        
        26 LOAD_FAST    
        28 RETURN_VALUE
"""
import dis 

def func(L:list) ->str:
    str1 = ''
    for i in L:
        str1 += str(i)
    return str1

# 返回python虚拟机执行代码的底层逻辑（反汇编）
dis.dis(func)


code = """  
def example_func(x):  
    return x + 1 
print(example_func(2))
"""  
  
# 注意：这里需要先将字符串编译成代码对象  
code_obj = compile(code, 'example_string', 'exec')  
exec(code_obj)
```




## Data Structure Algorithms

#### 1.解压可迭代对象（序列、元组、字符串等）给多个变量：占位符、*表达式

```python
def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head
print(sum((1,2,3,4)))
```

#### 2.保留最后N个元素

```python
from collections import deque
# deque 采取双链表的结构实现，两端插入删除为O(1)；默认无限长
# deque 但如限制长度为5时，超过限制会删除之前的数据，保持长度为5
# deque 常见方法 pop,popleft,append,appendleft
# yield 会在函数执行过程中‘暂停’并返回一个值，实现多次迭代返回值，不同于return只会在函数全部执行完后再返回
def search(lines, pattern, history=5):
    '''
    每次匹配到一个pattern，就会返回pattern当前行及其前5行 
    '''
    previous_lines = deque(maxlen=history)
    for li in lines:
        if pattern in li:
            yield li, previous_lines
        previous_lines.append(li)
```

#### 3.查找N个最大或最小的元素

> 堆：这里的堆为顺序存储的方式，通过二叉树对最后一个有孩子结点的结点(n/2向下取整)进行子内元素的比较，
>
> 获取元素只需‘砍头’即可

```python
"""
可采取三种方法：
	1.当N=1时，直接采用max或min；或使用heapq.nlargest和nsmallest,其底层会使用max或min
	2.当N接近于序列元素个数时，采用排序后切片效率更高 如 sorted(items)[-N:]
	3.当N仅为几个或小于序列长度比如1/2时，采用heapq更好
"""
# 应对复杂类型的比较
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

# 常见的heapq操作
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heapq.heapify(nums) # 在nums上构建小根堆，
print(nums)
print(heapq.heappop(nums)) # 弹出堆顶元素，并重排小根堆
```


#### 4.实现一个优先级队列

```python
"""
前置内容：python中的比较
	如下，直接进行a<b比较会抛出TypeError异常,必须在类中重定义 如 __lt__ 方法(less than)实现类的方法
		isinstance(other,Item): # 当两个对象都是Item的实例时	 
		return NotImplemented  # 当other不是Item的实例时返回，python会尝试使用other的__gt__方法进行逆向比较，如果other也返回NotImplemented，则最终python还是会抛出TypeError异常
	对于a_t,b_t这类元组类型，python会从第一个元素开始比较，如果不相同则直接返回布尔值，相同才会对后面实例进行比较，所以这里能正常运行
"""
class Item:
    def __init__(self,name) -> None:
        self.name = name
    def __repr__(self) -> str:
        return 'Item({!r})'.format(self.name)
    def __lt__(self,name):
        if isinstance(other,Item): # 当两个对象都是Item的实例时
            return self.name < self.name
        return NotImplemented 
a = Item('bob')
b = Item('john')
a_t = (1,a)
b_t = (2,b)
```

> 借用python的比较特性，实现优先级队列

```python
import heapq

 """
    self._queue = [] 
    	# 变量前面加_是一种约定成俗的规定，表示其是私有，受保护的
    return heapq.heappop(self._queue)[-1] 
    	# 移除小根堆（队列）中队头元素，并返回元素（）里最后一个元素
    heapq.heappush(self._queue, (-priority, self._index, item)) 
    	# heappush(heap,item) 插入的是三元组，通过三元组的比较形成构建大根堆（优先级取反），
    	并通过_index保证同优先级元素按照‘先来先到’进行排序，也保证了其不会到三元组最后一个元素（item对象）
    	的比较，如上，没有重写比较方法会抛出TypeError异常
 """
class PriorityQueue:
   
    def __init__(self) -> None:
        self._queue = [] 
        self._index = 0
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1 
    def pop(self):
        return heapq.heappop(self._queue)[-1] 
q = PriorityQueue()
q.push(Item('A'), 1)
q.push(Item('B'), 3)
q.push(Item('C'), 1)
q.push(Item('D'), 8)
q.push(Item('E'), 11)
q.pop()
q.pop()
q.pop()
q.pop()
q.pop() # pop顺序为 E,D,B,A,C
```

#### 5.字典中的键映射多个值 & 通过某个字段将记录分组 & 字典排序 & 字典max，min & 字典集合操作
```python
from collections import defaultdict
    
"""
    defaultdict在被访问时会自动为每个新键提供默认值0,不会抛出TypeError异常
    应用如统计元素的频率,对数据进行group by分组
"""
# 例1
dd = defaultdict(int)
print(dd['c']) # 返回默认值 0
dl = defaultdict(list)
dl['a'].append(1)
dl['a'].append(2)
dl['b'].append(3)
print(dl)
# 例2
rows = [
    {'address': '5412 N CLARK', 'date': '07/03/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'}
]
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row) # 根据日期分组
print(rows_by_date)

# 例3
"""
    实际上在python3.7后，dict已经实现了OrderedDict的按插入顺序排序,Python中的标准字典是无序的,但OrderedDict即使在元素被修改（新增，删除，更新）时，会一直保持元素的插入顺序【有此需求就使用】，但会牺牲一部分空间
"""
from collections import OrderedDict
d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['grok'] = 3
d['spam'] = 4
for key in d:
    print(key, d[key])

# 例4
"""
zip内置函数:
    1.zip能够让多个可迭代对象的元素组成一个个元组，最终返回一个迭代器对象，如z=zip(iter1,iter2,iter3)
    2.unzipped(*z)解包
字典中执行计算操作：
    1.使用zip颠倒键值,再调用聚合函数
    2.直接使用d.values获取值进行比较
    3.在聚合函数中采用匿名函数获取最小/大值的其他信息
"""
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
m1 = min(zip(prices.values(),prices.keys())) # (10.75, 'FB')
m2 = min(prices.values()) # 10.75
# min 函数遍历的是字典的键，并将键作为参数传递给匿名函数
m3 = min(prices, key=lambda key: prices[key]) # Returns 'FB'

# 例5
"""
    d.keys()和d.items()支持集合（唯一，无序）操作，如 &交、|并、-减等操作
"""

```

#### 6.删除重复元素并保持顺序
```python
"""
前置：是否可哈希
    判断一个对象是否可哈希化，用hash()
    一般来说，数字、字符串、元组都是hashable,而其他可变类型都是不能hash
应用：消除文件的重复行，其中key函数对每行应用
    with open(r'./single-chip.md', mode='r',encoding='utf-8') as f:
        for line in dedupe(f):
            print(line)

"""
# 可哈希对象：
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
        seen.add(item)
# 这里的list函数会自动调用__next__函数并持续调用dedupe返回值
list(dedupe([1, 2, 2, 3, 3, 4])) 

# 不可哈希对象:
# 这里改进之前的代码,自定义匿名函数处理如字典的dedupe,by转化为hashable
def dedupe(items, key= None):
    seen = set()
    for item in items:
        val = item if key is None else key(item) # 把item作为参数传入匿名函数key
        if val not in seen:
            yield item
        seen.add(val)
d = [{'x': 1, 'y': 2}, {'x': 2, 'y': 3}, {'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
d_dupe = list(dedupe(d,key=lambda d: (d['x'],d['y'])))

```
#### 7.slice切片对象 & 单词统计 & 通过某个关键字排序一个字典列表
```python
"""
    方便理解和使用，貌似没有其他作用？
    a = slice(start,stop,step)
    a.start/stop/step
"""
record = '....................100 .......513.25 ..........'
SHARES = slice(20,23)
PRICES = slice(31,37)
cost = int(record[SHARES]) * float(record[PRICES]) 


"""
    Counter统计
    支持词频排序、单词扩增
    且支持Counter对象的加减运算 a+b、a-b
"""
from collections import Counter
words = [
    'look', 'into', 'my','into', 'eyes','eyes','eyes', 'look', 'into', 'my', 'eyes'
]
word_counts = Counter(words)
# 返回最多的前四个
a = word_counts.most_common(4)
# 添加字段
morewords = ['why','are','you','not','looking','in','my','eyes']
b = word_counts.update(morewords)

```

#### 8.itemgetter & attrgetter
> 都可以用匿名函数来代替，效率上会有些许差异
> 排序不支持原生比较的对象
```python
"""
    itemgetter函数是callable的，作用于字典类型
"""
from operator import itemgetter
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

m = max(rows, key= itemgetter('uid'))
s = sorted(rows, key= itemgetter('uid'))

"""
    attrgetter作用于对象
"""
by_name = sorted(users, key=attrgetter('last_name', 'first_name'))
```

#### 9.过滤序列元素 & 推导式

```python
"""
    列表推导式 & 生成器表达式（可以不加小括号）
        [x*2 for x in range(10)] 
        一次性生成所有数据并返回列表
        (x*2 for x in range(10)) 
        返回生成器对象，只有迭代时才会返回一个数据，处理大量数据时通常更加内存友好

"""
# 这里展示了join函数对待可迭代对象时的处理方法，边迭代边处理
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s)) 

"""
    过滤
    pos = (n for n in mylist if n > 0)
    clip_neg = [n if n > 0 else 0 for n in mylist]
    filter(function,iterable) 返回生成器
    compress() 它允许你基于一个选择器迭代器来压缩（过滤）另一个可迭代对象中的元素。
"""
values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values))

# 基于选择器过滤
from itertools import compress
addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

more5 = [n>5 for n in counts]
list(compress(addresses, more5))

# 字典推导式
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
p1 = {key: value for key, value in prices.items() if value > 200}
p2 = dict((key,value) for key, value in prices.items() if value > 200)
print(p2)
```

#### 10.命名元组 & ChainMap
```python
"""
    对结构化元组序列进行处理，通过名称去访问元素
    但不可以更改元素值，只能通过s = s._replace(shares=75)重新创建一个
"""
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    total = 0.0
    for rec in records:
        s = Stock(*rec) # 元组解包
        total += s.shares * s.price
    return total
records = (('ACME', 110, 123.45),
    ('BCME', 120, 123.45),
    ('CCME', 130, 123.45),
    ('DCME', 140, 123.45))
# 计算所有人的持股总额
compute_cost(records)

"""
    ChainMap合并字典，使用的是原来的字典，如果键重复则用第一个值
    或者使用d1.update(d2)，这里新创建一个字典
"""
```

## String And Text
略

## File And IO

#### 1.open函数 & print函数
> 打开文件
```python
"""
    mode = 'rt/wt/wb/a'
        rt 只读+文本
        wb 覆盖写+二进制
        a+ 追加写+读取
        x 仅当文件不存在时才写入，否则报错
    encoding='utf-8'
        ascii, latin-1, utf-8和utf-16
    errors='ignore'
        编码格式不正确时采用的策略：ignore,replace,下面有类似的扩展
"""
with open('Learn-Record.txt',encoding='ascii' ,errors='ignore') as f:
    count = 0
    for line in f:
        count += 1
        print('{:d} {}'.format(count,line.strip())) # strip默认去除换行或空格符   

"""
    print支持指定间隔符、行尾符、重定向输出
"""
# print函数支持重定向到文件对象中
print('Hello World!', '是这样的',sep='&&',end=' ', file=f)
# str.join()完成同样的分隔操作
print(','.join(str(x) for x in row))
# 解包实现
print(*row, sep=',')

   
# decode方法将这些字节数据解码成字符串,同理encode 
data = b'\xe4\xbd\xa0\xe5\xa5\xbd' 
text = data.decode('utf-8') 
```


#### 2.类文件对象 
```python
"""
    io.StringIO
    io.ByteIO
    一般用于测试？
"""
import io

s = io.StringIO()
s.write('Hello,World!\n')
print('Fake News!', file=s)
s.getvalue()
# write操作会使文件指针移到末尾
s.seek(0)
s.read(4)
```

#### 3.按固定大小块读取二进制文件
```python
"""
    解释：iter函数接收一个可迭代对象作为参数，同时还有一个可选的sentinel(哨兵),
    当迭代器返回的值等于sentinel，迭代会停止；其中partial会将文件根据参数大小进行分块
"""
from functools import partial
RECORD_SIZE = 32 
with open('后退.mp3',mode='rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...
```
#### 4.文件常用操作
```python
"""
    脚本必备
"""
import os 
path = '/Users/beazley/Data/data.csv'
os.path.dirname(path)
os.path.basename(path)
os.path.join('tmp','data',path)
os.path.expanduser('~/data/data.csv') # 'C:\\Users\\xhh鱼酱/data/data.csv'
os.path.splitext(path) # ('/Users/beazley/Data/data', '.csv')

# 文件是否存在，最终都会返回True，False
os.path.exists('/etc/passwd')
os.path.isfile('/etc/passwd')
os.path.isdir('/etc/passwd')
os.path.islink('/usr/local/bin/python3')
os.path.realpath('/usr/local/bin/python3')

# 获取文件夹中的文件列表
names = [name for name in os.listdir('D:\donghua') if os.path.isfile(os.path.join('D:\donghua', name))]
pynames = [name for name in os.listdir('D:\donghua') if name.endwith('.py')]


"""
    处理非正常编码的文件名
    errors参数，同其他函数中的一样，提供多种对于无法正常编码时的处理方式
        如：ignore,replace,xmlcharrefreplace,surrogateescape
"""
import sys  
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogateescape')
    return temp.decode('latin-1')


def safe_print(s):  
    try:  
        print(s.encode('ascii', 'xmlcharrefreplace').decode('ascii'), end='')  
    except UnicodeEncodeError:  
        # 如果s已经是str且包含无法编码的字符，上面的尝试可能会失败  
        # 这里可以添加额外的错误处理逻辑  
        pass  
  
# 使用这个函数代替print  
safe_print("Hello, 🌁🌁🌁世界!🌞🌞")
```


#### 5.python的IO分层结构
```markdown
- 高级抽象层        提供常见的IO操作     
- 缓冲层            数据会先缓冲在内存的一个缓冲区
- 操作系统接口层     C语言级别的系统调用与OS进行交互
- 硬件层            计算机的磁盘读写，网络通信
```
