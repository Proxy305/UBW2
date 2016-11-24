# import requests
# import re


# # Notice: A link could fail at anytime. Get a new address everytime.
# r = requests.get("http://202.116.13.24:8197/Jpath_sky/DsrPath.do?code=CFE90D011B9BFEA3DD0DA0B79328C2FC&ssnumber=11270171&netuser=1&jpgreadmulu=1&displaystyle=0&channel=0&ipside=0")
# file = open('result.html', 'w+')
# contents = r.text.encode('utf-8')
# file.write(contents)

# # str1 = "kkkkk; var str='http://123.com/233?p=1234'"
# match = re.search(r"(var str\=\')(.*)(\')", contents)
# #match = re.search(r".*var str(.*)\'.*", str1)
# result = match.group(0)
# print(result)

# trimmed = result.lstrip("var str='")
# trimmed = trimmed.rstrip("'")

# print trimmed

# class obj1:
#     def __init__(self):
#         self.val = 1

#     def alter(self, value):
#         self.val = value

#     def display(self):
#         print(self.val)

# class obj2:
#     def __init__(self, obj):
#         self.obj = obj

#     def op(self):
#         self.obj.alter(5)
#         self.obj.display()

# obj1 = obj1()
# obj2 = obj2(obj1)
# obj1.display()
# obj2.op()
# obj1.display()


# for i in range(13,544):
#     print('Requesting Image:' + str(i))
#     contents = requests.get('http://202.116.13.24:8077/ss2jpg/ss2jpg.dll?did=a174&pid=E4D4C405513E1EA7EEBD5738340769D287C3F3B14D355ACC360A4434688F39405F579CD00D3C5CE384B04CD60D9BD618DB47A7B55488BDB578911703B29A5537DA5155CFAD0FB4ED8B545CEAB50656224886ECD6DBC61CC3F6E7A6255BA68775D9C684E0A70A2EE53A15C8F1D3B05BAB3C37&jid=/' + str(i).zfill(6) + '.jpg').content
#     file = open('z' + str(i) + '.jpg', 'wb+')
#     file.write(contents)

# im

# l = ['5.rb', '2.rb', '201.rb', '51.rb', '7.rb', '4.rb']
# print 'Before:'
# print l
# for i in range(len(l)):
#         l[i] = l[i].split('.')    
#         l[i][0] = int(l[i][0])
# print 'After:'
# print l
# l.sort()
# print 'Sorted:'
# print l
# for i in range(len(l)):
#         l[i][0] = str(l[i][0])
#         l[i] = l[i][0] + '.' + l[i][1]
# print 'Recover:'
# print l

import os

def file_list_sort(l):
    for i in range(len(l)):
            l[i] = l[i].split('.')    
            l[i][0] = int(l[i][0])
    l.sort()
    for i in range(len(l)):
            l[i][0] = str(l[i][0])
            l[i] = l[i][0] + '.' + l[i][1]

    return l

print(os.listdir('wx/main'))
print(file_list_sort(os.listdir('wx/main')))

