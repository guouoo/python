# 本文基于：win10(64) + py3.5
# 本人电脑配置：4G内存
# 说明：
# 数据大小：5.6G
# 数据描述：自2010年以来，纽约的311投诉
# 数据来源：纽约开放数据官网(NYC''s open data portal)
# 数据下载：https: // data.cityofnewyork.us / api / views / erm2 - nwe9 / rows.csv?accessType = DOWNLOAD

import pandas as pd
import time

'''python大数据分析工作流程'''
# 5G大数据文件，csv格式
reader = pd.read_csv('311_Service_Requests_from_2010_to_Present.csv', iterator=True, encoding='utf-8')

# HDF5格式文件支持硬盘操作，不需要全部读入内存
store = pd.HDFStore('311_Service_Requests_from_2010_to_Present.h5')

# 然后用迭代的方式转换.csv格式为.h5格式
chunkSize = 100000
i = 0
while True:
    try:
        start = time.clock()

        # 从csv文件迭代读取
        df = reader.get_chunk(chunkSize)

        # 去除列名中的空格
        df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})

        # 转换为日期时间格式
        df['CreatedDate'] = pd.to_datetime(df['CreatedDate'])
        df['ClosedDate'] = pd.to_datetime(df['ClosedDate'])

        # 感兴趣的列
        columns = ['Agency', 'CreatedDate', 'ClosedDate', 'ComplaintType',
                   'Descriptor', 'TimeToCompletion', 'City']
        # 不感兴趣的列
        columns_for_drop = list(set(df.columns) - set(columns))
        df.drop(columns_for_drop, inplace=True, axis=1, errors='ignore')

        # 转到h5文件
        # 通过指定data_columns，建立额外的索引器，可提升查询速度
        store.append('df', df, data_columns=['ComplaintType', 'Descriptor', 'Agency'])

        # 计时
        i += 1
        end = time.clock()
        print('{} 秒: completed {} rows'.format(end - start, i * chunksize))
    except StopIteration:
        print("Iteration is stopped.")
        break

# 转换完成之后，就可以选出想要进行数据分析的行，将其从硬盘导入到内存，如：
# 导入前三行
# store.select('df', "index<3")

# 导入 ComplaintType, Descriptor, Agency这三列的前十行
# store.select('df', "index<10 & columns=['ComplaintType', 'Descriptor', 'Agency']")

# 导入 ComplaintType, Descriptor, Agency这三列中满足Agency=='NYPD'的前十行
# store.select('df', "columns=['ComplaintType', 'Descriptor', 'Agency'] & Agency=='NYPD'").head(10)

# 导入 ComplaintType, Descriptor, Agency这三列中满足Agency IN ('NYPD', 'DOB')的前十行
# store.select('df', "columns=['ComplaintType', 'Descriptor', 'Agency'] & Agency IN ('NYPD', 'DOB')")[:10]


# ======================================
# 下面示范一个groupby操作
# 说明：由于数据太大，远超内存。因此无法全部导入内存。
# ======================================
# 硬盘操作：导入所有的 City 名称
cities = store.select_column('df', 'City').unique()
print("\ngroups:%s" % cities)

# 循环读取 city
groups = []
for city in cities:
    # 硬盘操作：按City名称选取
    group = store.select('df', 'City=%s' % city)

    # 这里进行你想要的数据处理
    groups.append(group[['ComplaintType', 'Descriptor', 'Agency']].sum())

print("\nresult:\n%s" % pd.concat(groups, keys=cities))

# 最后，记得关闭
store.close()

# 把上面的：
#
# # 转到h5文件
# # 通过指定data_columns，建立额外的索引器
# store.append('df', df, data_columns=['ComplaintType', 'Descriptor', 'Agency'])
#
# 改为：
#
# # 转到h5文件
# # 通过指定data_columns，建立额外的索引器
# # 通过指定min_itemsize，设定存储混合类型长度
# store.append('df', df, data_columns=['ComplaintType', 'Descriptor', 'Agency'], min_itemsize={'values': 50})