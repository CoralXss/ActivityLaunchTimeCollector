# encoding:utf-8
import shutil
import json

'''
方法说明：
  - 普通文件直接读写；
  - 按行读取文件；
  - 拷贝文件；
  
  -----以下为未实现功能-----
  - 按字节读取大文件；
  - 按字节写入文件；
  - 新增 / 删除文件；
  - 查找某个目录下的所有子文件；
  - 查找某个特定的文件或目录；
'''


def read_file(file_path):
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    return content


def read_byte_file(file_path):
    f = open(file_path, 'rb')
    content = f.read()
    f.close()
    return content


# 读取 json 文件数据
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)  # 返回为list类型


# 写入 json 数据
def write_json_content(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)


# 按行读取文件内容
def read_file_by_line(file_path):
    lines = []
    f = open(file_path, 'r')
    for line in f.readlines():
        lines.append(line.strip())

    return lines


# 按字节读取大文件
def read_file_by_byte(file_path, buffer_size):
    f = open(file_path, 'r')
    result = ''
    content = f.read(buffer_size)
    result += content
    while len(content) > 0:
        content = f.read(buffer_size)
        result += content
    f.close()
    return result


# 将某个文件内容按行读到另一个文件中
def write_file(input_file, output_file):
    output = open(output_file, 'w')

    with open(input_file, 'r') as f:
        for line in f.readlines():
            output.writelines(line)


def write_content(content, output_file):
    output = open(output_file, 'w')
    output.write(content)


def write_byte_content(content, output_file):
    output = open(output_file, 'wb')
    output.write(content)


# 一次性写入
def write_string_content(content, output_file):
    output = open(output_file, 'w+')
    output.write(content)


# 文件复制
def copy_file(src_file, dist_file):
    # 文件复制可使用 shutil
    shutil.copyfile(src_file, dist_file)




