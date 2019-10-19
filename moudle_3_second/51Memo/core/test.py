import datetime


date = input('date:(示例：年/月/日 时/分/秒)')
date_list = date.split(' ')
print(date_list)
Y, m, d = (int(x) for x in date_list[0].split('/'))
H, M, S = (int(x) for x in date_list[1].split('/'))
# print(type(datetime.date(Y, m, d) ))
# print(datetime.date(Y, m, d))

print(str(datetime.date(Y, m, d)))
print(type(datetime.date(Y, m, d)))
d = str(datetime.date(Y, m, d))
print(d)
print(type(d))
# date = datetime.date(Y, m, d) + datetime.time(H, M, S)