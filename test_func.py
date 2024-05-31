from pypinyin import pinyin, Style
import pandas 

def chinese_to_pinyin(phrase):
   # 返回汉字短语的每个字的首字母大写构成的字符串
   pinyin_list = pinyin(phrase,style=Style.FIRST_LETTER, strict=False)
   initials = ''.join(char[0].upper() for char in pinyin_list if char)
   return initials


if __name__ == '__main__':
   dqbs_map = pandas.read_excel(r"D:\donghua\数据集市规则定义202404.xlsx",sheet_name="dqbs映射")
   dqbs_phrase = pandas.read_excel(r"D:\donghua\数据集市规则定义202404.xlsx",sheet_name="dqbs字典")
   dqbs_phrase.columns = ['字典值','中文描述','空']
   dqbs_rs = pandas.DataFrame()
   dqbs_rs['NAME_EN'] = dqbs_phrase.apply(
         lambda row:'DQBS_' + chinese_to_pinyin(row['中文描述']) if row['字典值'] == '#' else None,
         axis=1
      )
   dqbs_rs['NAME'] = dqbs_phrase.apply(
         lambda row:row['中文描述'] if row['字典值'] == '#' else None,
         axis=1
      )
   # dqbs_rs.dropna(subset=['NAME','NAME_EN'])
   dqbs_rs = dqbs_rs[dqbs_rs['NAME'].notna()].reset_index(drop=True)
   dqbs_rs.to_excel(r'D:\donghua\dqbs_rs.xlsx')
   