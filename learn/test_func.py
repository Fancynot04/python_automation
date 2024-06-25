
a = {
    'x' : 1,
    'y' : 2,
    'z' : 3
}

b = {
    'w' : 10,
    'x' : 11,
    'y' : 2
}

def dedupe(items, key= None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
        seen.add(val)
        
with open(r'./single-chip.md', mode='r',encoding='utf-8') as f:
        for line in dedupe(f):
            print(line)