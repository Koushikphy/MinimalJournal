
import re 


txt = 'hi there #new'

pattern = r'((?!:#)\w+)'


t = ['a', 'aaa']
print('a' in t)
print(re.findall(pattern, txt))