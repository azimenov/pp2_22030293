import re
text_to_search = '''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
qwerty
QWERTY
123456789

characters = [ ] ; : { } ' " < > , . ? / \ | 
abc

agcfcabc

555.555.555
444.444.444
444-444-444
23456

sb

33
333
333
Ha HaHa
abbb
abb
coryr.com

cat
mat
pat
Aiii
AAiii
aaa_zzz
Mr Add
Mr Bdo
Mr. Coc
'''
sent = 'Start a sent and bring it to an end'


pattern = re.compile(r'[A-Z][a-z]+')
matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)