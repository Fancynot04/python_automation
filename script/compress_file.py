import os  
import zipfile  
  
def compress_video_files(folder_path, extensions=('.mp4', '.avi', '.mov')):  
    """  
    压缩指定文件夹下的所有视频文件到同名zip文件。  
      
    :param folder_path: 包含视频文件的文件夹路径  
    :param extensions: 要压缩的视频文件扩展名列表  
    """  
    for root, dirs, files in os.walk(folder_path):  
        for file in files:  
            if os.path.splitext(file)[1].lower() in extensions:  # 文件路径拆分为文件名和扩展名,返回(filename, extension)
                # 获取文件完整路径  
                file_path = os.path.join(root, file)  
                # 创建zip文件名（同名）  
                zip_file_path = os.path.splitext(file_path)[0] + '.zip'    
                # 创建zip文件对象  
                with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:  
                    # 将文件添加到zip中  
                    zipf.write(file_path, arcname=os.path.relpath(file_path, os.path.dirname(zip_file_path)))
                    
                print(f"Compressed {file_path} to {zip_file_path}")  

import os  
  
def get_size(path):  
    """  
    递归地获取目录或文件的大小（以GB为单位）  
    """  
    total_size = 0 # 总大小
    if os.path.isfile(path): 
        return os.path.getsize(path) 
    elif os.path.isdir(path): 
        for item in os.listdir(path):  
            item_path = os.path.join(path, item)  
            total_size += get_size(item_path)  
    return round(total_size/(1024*1024),5)  
  

def print_tree_to_file(path, indent=0, output_file=''):  
    """  
    打印目录树状结构到文件中，包括文件和目录的大小  
    """  
    with open(output_file, 'w', encoding='utf-8') as f:  
        f.write('--' * indent + os.path.basename(path) + '\n')  
        if os.path.isdir(path):  
            size = get_size(path)  
            f.write('--' * (indent + 1) + f'Size: {size} MB\n')  
            for item in os.listdir(path):  
                item_path = os.path.join(path, item)  
                print_tree_to_file(item_path, indent + 2, output_file)  
  
# 使用示例  
# root_path = os.getcwd()  # 替换为你的目录路径  
# output_file = 'directory_tree.txt'     # 输出的文件名  
# print_tree_to_file(root_path, 0, output_file)
# print()
path = os.getcwd() #+'\cap_seat.py'
print(str(round(os.path.getsize(os.getcwd()+'\cap_seat.py')/1024,2))+' KB')

if os.path.isdir(path):
    for item in os.listdir(path): # path: 这种遍历的是path字符串中的每个字符 
        item_path = os.path.join(path,item) # 自动添加/，自动修正/
        # total_size = get_size(item_path) 对当前函数递归调用