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
  
# 使用示例  
# compress_video_files(r'D:\xhh鱼酱\Videos')

import pandas as pd  
  
# 您的数据字典  
data = {    
    '受益人方式': ['0-自益;1-他益;2-自益+他益;4-公益;'],    
    '受托职责': ['0-主动管理;1-被动管理;']    
}  
  
# 由于每个键只对应一个列表元素（即一个字符串），  
# 我们不需要进一步拆分这些列表。可以直接创建一个 DataFrame。  
 
  
# 将 DataFrame 写入 Excel 文件  
output_file = 'data.xlsx'  
df.to_excel(output_file, index=False, engine='openpyxl')  