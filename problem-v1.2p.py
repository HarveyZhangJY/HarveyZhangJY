import random
import xlwt
import time
import tempfile
import win32api
import win32print
c = set()
book = xlwt.Workbook()
sheet1 = book.add_sheet('1')
sheet2 = book.add_sheet('2')
font = xlwt.Font()
font.height = 20 * 16
style0 = xlwt.XFStyle()
style0.font = font
i = 1
num = []
max = int(input("最大多少？\n"))
min = int(input("最小多少？\n"))
n = int(input("您要出几道题？\n"))
col = int(input("您要出几列？\n"))
while 1:
    a = random.randint(1,max)
    b = random.randint(1,max)
    num.append(a)
    num.append(b)
    num.sort()
    if random.randint(1,2) == 1:
        if a+b > max or (a<min and b<min):
            continue
        d = len(c)
        c.add(str(a)+"+"+str(b)+"=")
        if d == len(c):
            continue
        else:
            sheet1.col((i-1) % col).width = 19 * 256
            sheet2.col((i-1) % col).width = 19 * 256
            sheet1.write((i-1) // col,(i-1) % col,str(a)+"+"+str(b)+"=______",style0)
            sheet2.write((i-1) // col,(i-1) % col,str(a)+"+"+str(b)+"="+str(a+b),style0)
            i+=1
    else:
        if a-b < 0 or (a<min and b<min):
            continue
        d = len(c)
        c.add(str(a)+"-"+str(b)+"=")
        if d == len(c):
            continue
        else:
            sheet1.write((i-1) // col,(i-1) % col,str(a)+"-"+str(b)+"=______",style0)
            sheet2.write((i-1) // col,(i-1) % col,str(a)+"-"+str(b)+"="+str(a-b),style0)
            i+=1
    if i == n+1:
        break
name = "problem"+str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) )+'.xls'
book.save(name)
wannaprint = str(input("是否要打印？[y|n]\n"))
if wannaprint == "y":
    win32api.ShellExecute(0, "print", name, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
print("done")