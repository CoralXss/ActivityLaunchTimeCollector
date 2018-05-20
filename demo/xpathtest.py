from util import fileutil
from lxml import etree

content = fileutil.read_byte_file('../file/book.xml')
print(content)

xml = etree.XML(content)
print(type(xml))       # <class 'lxml.etree._Element'>

# 选取 bookstore 下的所有子节点
result = xml.xpath('/bookstore')
print('1. ', result)   # <class 'list'> [<Element bookstore at 0x10322ef88>]

# 1）选取所有的 title 元素
result = xml.xpath('/bookstore/book/title')
print('2. ', result)   # <class 'list'> [<Element title at 0x10322c048>]

# 2）选取第一个 book 元素下的 title 元素
result = xml.xpath('/bookstore/book[1]/title')
print('3. ', result)

result = xml.xpath('//title[@lang]')
print('4. ', result)

result = xml.xpath('//@lang')
print('5. ', result)
