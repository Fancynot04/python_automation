from pypinyin import pinyin, Style
import pandas 

def chinese_to_pinyin(phrase):
   # 返回汉字短语的每个字的首字母大写构成的字符串
   pinyin_list = pinyin(phrase,style=Style.FIRST_LETTER, strict=False)
   initials = ''.join(char[0].upper() for char in pinyin_list if char)
   return initials

def past_example(dqbs_phrase):
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

# 此列表为新增的字典项
blocklist = ['ZJLX5', 'ZJLX5_JG', 'ZJLX5_GR', 'ZJLX5_JRCP', 'KFYWLX', 'PHJRLX', 'DBWQLX', 
            'DBPFWGN', 'YXQLX', 'QYZYNJYWLX', 'ZGXGZGQK', 'JGLXEJ_TY', 'FRFFRWTRLX', 'ZGCPFWXTZGCPLX', 
            'JZXTMS', 'YFLMS', 'YFLCJ', 'LSXTYWMS', 'SFCSGX', 'YLCYFL', 'QYFZZL', 'HZJGLX', 'HZJGHZFS', 
            'FXCZLX', 'JYDSTZ', 'TJD_EAST5', 'GBFXFL', 'LSCYFL', 'SZJJFL', 'GXJSLYFL', 'WLCYFL', 'ZLXXCYFL', 
            'HQLX', 'HGRBS', 'HGFSBS', 'YXTKLX', 'RZFKJFL', 'JZLLZL', 'HBCLFS', 'DBLX5_HT', 'DBLXXQ', 'DZYWLX5', 
            'PGFS', 'DBQZLX', 'FDCXMLX5', 'FFDCXMLX5', 'XMTZGLFS', 'GTSTRLX', 'XCZXLX', 'GQTZKZCD', 'JCZCLX_EAST5', 
            'CPYXFS', 'FXCSNL', 'CZQSW', 'WTRXS', 'HZZT', 'DZYWZT5', 'ZCLBDL', 'ZCLBMX', 'PJJGMC', 'WTZCLX5']

def dqbs_merge():
   dqbs_map = pandas.read_excel(r"D:\donghua\数据集市规则定义202404.xlsx",sheet_name="dqbs映射")
   dqbs_map.columns = ['源字典编码','源字典项值','源字典项描述','空','目标字典值','目标字典描述','dqbs描述']
   dqbs_map['dqbs描述'] = dqbs_map['dqbs描述'].apply(lambda x: x.split(':')[0] if pandas.notna(x) else None)\
      .fillna(method='ffill') # forward fill
   dqbs_map['源字典编码'] = dqbs_map['源字典编码'].fillna(method='ffill')
      # .apply(lambda x: 'BP_' + x  if pandas.notnull(x) and x in blocklist else x)

   dqbs_phrase = pandas.read_excel(r"D:\donghua\数据集市规则定义202404.xlsx",sheet_name="dqbs字典")
   dqbs_phrase.columns = ['index','字典编码','字典名称']

   dqbs_rs = pandas.merge(
         dqbs_map.loc[:,['源字典编码','源字典项值','源字典项描述','目标字典值','目标字典描述','dqbs描述']],
         dqbs_phrase.loc[:,['字典编码','字典名称']],
         left_on='dqbs描述',right_on='字典名称',how='left').drop('dqbs描述',axis=1)
   dqbs_rs['系统标识'] = 'DQBS'
   dqbs_rs['有效状态'] = '1'
   dqbs_rs['源系统标识'] = 'MARKET'
   dqbs_rs = dqbs_rs.reindex(
      columns=['系统标识','字典编码','字典名称','源系统标识','源字典编码','源字典项值','源字典项描述','目标字典值','目标字典描述','有效状态']
      ).reset_index(drop=True) # 重新索引，删除之前的索引
   dqbs_rs.to_excel(r'D:\donghua\dqbs_rs_504.xlsx',index=False)

if __name__ == '__main__':
   pass
   dqbs_merge()