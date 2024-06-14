# Data Structure Algorithms
# 1.解压可迭代对象（序列、元组、字符串等）给多个变量：占位符、*表达式
# def sum(items):
#     head, *tail = items
#     return head + sum(tail) if tail else head
# print(sum((1,2,3,4)))

# 2.保留最后N个元素
from collections import deque
# deque 采取双链表的结构实现，两端插入删除为O(1)
# 通过覆盖__iter__和__next__方式实现代理迭代，同时执行一些其他的任务：日志记录，权限校验，数据转换
# 使用生成器生成新的迭代模式 yield(惰性求值，暂停)，如frange(s,e,step)
# yield在函数中创建迭代器，函数在调用时不会立即执行，会返回一个迭代器对象，执行到yield时候会暂停，返回其值
# 只有在下一次调用next时才会执行，同上；而for语句会自动遍历
def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for li in lines:
        if pattern in li:
            yield li, previous_lines
        previous_lines.append(li)

# Example use on a file
if __name__ == '__main__':
    with open(r'../../cookbook/somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-' * 20)