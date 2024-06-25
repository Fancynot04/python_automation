## 迭代器

> 1. 通过覆盖__iter__和__next__方式实现代理迭代，同时执行一些其他的任务：日志记录，权限校验，数据转换;
> 2. 使用生成器生成新的迭代模式 yield(惰性求值，暂停)，如frange(s,e,step);
> 3. yield在函数中创建迭代器，函数在调用时不会立即执行，会返回一个迭代器对象，执行到yield时候会暂停，返回其值;
> 4. 只有在下一次调用next时才会执行，同上；而for语句会自动遍历;



## Data Structure Algorithms

1.解压可迭代对象（序列、元组、字符串等）给多个变量：占位符、*表达式

```python
def sum(items):
    head, *tail = items
    return head + sum(tail) if tail else head
print(sum((1,2,3,4)))
```

2.保留最后N个元素

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

3.查找N个最大或最小的元素

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


4.实现一个优先级队列

```python
"""
前置内容：python中的比较
	如下，直接进行a<b比较会抛出TypeError异常,必须在类中重定义 如 __lt__ 方法(less than)实现类的方法
		isinstance(other,Item): # 当两个对象都是Item的实例时	 
		return NotImplemented  # 当other不是Item的实例时返回，python会尝试使用other的__gt__方法进			行逆向比较，如果other也返回NotImplemented，则最终python还是会抛出TypeError异常
	对于a_t,b_t这类元组类型，python会从第一个元素开始比较，如果不相同则直接返回布尔值，相同才会对后面实例进     行比较，所以这里能正常运行
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

5.字典中的键映射多个值 & 通过某个字段将记录分组 & 字典排序 & 字典max，min & 字典集合操作
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

6.删除重复元素并保持顺序
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
        val = item if key is None else key(item)
        if val not in seen:
            yield item
        seen.add(val)
d = [{'x': 1, 'y': 2}, {'x': 2, 'y': 3}, {'x': 1, 'y': 2}, {'x': 3, 'y': 4}]
d_dupe = list(dedupe(d,key=lambda d: (d['x'],d['y'])))

```






