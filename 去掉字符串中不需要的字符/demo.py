#使用字符串的strip(),lstrip(),rstrip()去掉字符串两端的字符
#使用字符串的replace()，re.sub()
import re

s = '---abc+++'
print(s.strip('-+'))#如果不给参数，去掉空格字符

print(s.replace('---','').replace('+++',''))

s = '\tabc\t123\rxyz'
print(re.sub('[\t\r]','',s))

