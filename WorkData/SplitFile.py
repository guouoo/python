# import logging
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(levelname)s: %(message)s"
# )
#
# # f = open('C:\\Users\\tguo\\Documents\\BaiduYunDownload\\PWD\\test.txt', 'r')
# #
# #
# # for line in open('C:\\Users\\tguo\\Documents\\BaiduYunDownload\\PWD\\test.txt'):
# #     line = f.readline()
# #     print (line)
#
# # f.close()
#
#
# file = open('C:\\Users\\tguo\\Documents\\BaiduYunDownload\\PWD\\H.txt', 'r')
# sizehint = 1020   # 200M
# position = 0
# lines = file.readlines(sizehint)
# logging.info(lines)
#
# logging.info(file.next())
# # while not file.next() - position < 0:
# #     position = file.next()
# #     lines = file.readlines(sizehint)
#
# file.close()


import os


class SplitFiles():
    """按行分割文件"""

    def __init__(self, file_name, line_count=1000000):
        """初始化要分割的源文件名和分割后的文件行数"""
        self.file_name = file_name
        self.line_count = line_count

    def split_file(self):
        if self.file_name and os.path.exists(self.file_name):
            try:
                with open(self.file_name,'rb') as f:  # 使用with读文件
                    temp_count = 0
                    temp_content = []
                    part_num = 1
                    for line in f:
                        if temp_count < self.line_count:
                            temp_count += 1
                        else:
                            self.write_file(part_num, temp_content)
                            part_num += 1
                            temp_count = 1
                            temp_content = []
                        temp_content.append(line)
                    else:  # 正常结束循环后将剩余的内容写入新文件中
                        self.write_file(part_num, temp_content)

            except IOError as err:
                print(err)
        else:
            print("%s is not a validate file" % self.file_name)

    def get_part_file_name(self, part_num):
        """"获取分割后的文件名称：在源文件相同目录下建立临时文件夹temp_part_file，然后将分割后的文件放到该路径下"""
        temp_path = os.path.dirname(self.file_name)  # 获取文件的路径（不含文件名）
        part_file_name = temp_path + "\\temp_part_file"
        if not os.path.exists(temp_path):  # 如果临时目录不存在则创建
            os.makedirs(temp_path)
        part_file_name += os.sep + "temp_file_" + str(part_num) + ".part"
        return part_file_name

    def write_file(self, part_num, *line_content):
        """将按行分割后的内容写入相应的分割文件中"""
        part_file_name = self.get_part_file_name(part_num)
        print(line_content)
        try:
            with open(part_file_name, "w") as part_file:
                part_file.writelines(line_content[0])
        except IOError as err:
            print(err)


if __name__ == "__main__":
    sf = SplitFiles(r"C:\Users\tguo\Documents\BaiduYunDownload\PWD\RuJia.txt")
    sf.split_file()
