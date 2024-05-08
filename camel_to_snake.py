def camel_to_snake(name):
    """
        function: 将驼峰命名转换为下划线并全大写的写法
        create_date: 2024-05-08
        explanation: result接收结果，函数对每个命名处理，遇到大写则在前添加下划线并将其小写
    """
    result = [name[0].lower()]
    for char in name[1:]:
        # print(char)
        if char.isupper():
            result.extend(['_', char.upper()])
        else:
            result.append(char)
    return ''.join(result).upper()

def print_snake(camel_names:list):
    for camel_name in camel_names:
        snake_name = camel_to_snake(camel_name)
        print(f'{snake_name}')

if __name__ == '__main__':
    # 测试用例
    camel_names = ['DueDiligenceInd', 'Payment','DueDiligenceInd','FormerCountryName','DistrictName','POB','PostCode']
    print_snake(camel_names)   
        
        
