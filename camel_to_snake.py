import xlwt
import re 

def camel_to_snake(name):
    result = [name[0].lower()]
    for char in name[1:]:
        # print(char)
        if char.isupper():
            result.extend(['_', char.upper()])
        else:
            result.append(char)
    return ''.join(result).upper()

def print_snake(camel_names:list):
    """
        function: 将驼峰命名转换为下划线并全大写的写法
        create_date: 2024-05-08
        explanation: result接收结果，函数对每个命名处理，遇到大写则在前添加下划线并将其小写
    """
    for camel_name in camel_names:
        snake_name = camel_to_snake(camel_name)
        print(f'{snake_name}')

def deal_normal(str):
    modified_str = str1.replace("\n", "','")
    print("'"+modified_str+"'")
def set_font():
    # 字体部分
    # 初始化样式
    style1 = xlwt.XFStyle()
    # 为样式创建字体
    font = xlwt.Font()
    font.name = 'Times New Roman'   #字体
    font.bold = True                #加粗
    font.underline = True           #下划线
    font.italic = True              #斜体
    # 设置样式
    style1.font = font
    # 使用样式
    sheet.write(4, 6, "新内容1", style1)

    # 边框部分
    borders = xlwt.Borders()
    # 设置线型
    borders.left = xlwt.Borders.DASHED
    borders.right = xlwt.Borders.DASHED
    borders.top = xlwt.Borders.DASHED
    borders.bottom = xlwt.Borders.DASHED
    # 设置样色
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40
    # 
    style2 = xlwt.XFStyle()
    style2.borders = borders
    # 使用样式
    sheet.write(5, 8, "新内容2", style2)

def deal_row(strs):
    """
        #	受益方式        
        0	自益
        1	他益        -->  受益权类型 0-普通;1-优先;2-中间;3-劣后;
        2	自益+他益
        4	公益
    """
    for str in strs.split('\n'):
        if(str.split('\t')[0]== "#"):
            print('\n')
            print(str.split('\t')[1],end='')
            print('\t',end='')
        else:
            print(str.replace("\t", "-")+';',end='')
def write_in_excel():
    """
        将如a  b c(txt) --> 写入excel    
    """
    f = open('./demo.txt','r',encoding='utf-8') #打开数据文本文档，注意编码格式的影响  
    wb = xlwt.Workbook(encoding = 'utf-8') #新建一个excel文件
    ws1 = wb.add_sheet('数据源字典表') #添加一个新表，名字为数据源字典表
    ws1.write(0,0,'字典名称')
    ws1.write(0,1,'字典值列表')
    row = 1 #写入的起始行
    col = 0 #写入的起始列
    #通过row和col的变化实现指向单元格位置的变化
    for line in f: 
        if(line != '\n'):
            arr= re.split(r'\s+', line) #txt文件中每行的内容按多行空格分割并存入数组中
            for i in range(len(arr)):
                ws1.write(row, col ,arr[i])#向Excel文件中写入每一项
                col += 1
            row += 1
            col = 0
    wb.save("数据源字典表.xls")
if __name__ == '__main__':
    # 测试用例
    camel_names = ['DueDiligenceInd', 'Payment','DueDiligenceInd','FormerCountryName','DistrictName','POB','PostCode']
    # print_snake(camel_names)
    str1 = """
    """
    # deal_row(str1)
    # write_in_excel()
    print()
    




        
        
