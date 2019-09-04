from collections import namedtuple
Results = namedtuple('Result','count average')

# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Results(count,average)

# 委派生成器
def grouper(results,key):
    while True:
        results[key] = yield from averager()

# 客户端代码，即调用方
def main(data):
    results = {}
    for key,values in data.items():
        group = grouper(results,key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    report(results)

# 输出报告
def report(results):
    for key,result in sorted(results.items()):
        group,unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count,group,result.average,unit))

data = {
    'girls;kg':[40.9,45.0,44.3,56.2,38.0,62.0,45.2,44.5],
    'boys;kg':[60.9,72.3,40.5,122.2,60.0,45.5,76.3,63.3,46.3]
}

main(data)