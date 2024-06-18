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









