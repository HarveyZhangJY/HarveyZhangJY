import msvcrt
import time

import prettytable
import xlwt
from colorama import Fore, init

init(autoreset=True)


# ---------------显示函数----------------
def h(z):
    return f"{z:,.2f}"


print("欢迎使用镐镐的个税计算器2019年沪版")
a = float(input('请输入月薪:(单位:元)\n'))
if a < 2420:
    print(Fore.RED + "你的工资已低于上海最低月工资标准2420元，赶紧找你的老板谈一谈吧!")
    ord(msvcrt.getch())
    quit()
b, c, e = float(input('请输入专项附加扣除:(单位:元)\n')) + 5000, 0, 7132
if b < 5000:
    print(Fore.RED + "专项附加扣除数不能为负，请确认后重新运行。")
    ord(msvcrt.getch())
    quit()


# ---------------年累计个税函数---------------
def f(y):
    if y <= 36000:
        return y * 0.03
    elif y <= 144000:
        return (y - 36000) * 0.1 + f(36000)
    elif y <= 300000:
        return (y - 144000) * 0.2 + f(144000)
    elif y <= 420000:
        return (y - 300000) * 0.25 + f(300000)
    elif y <= 660000:
        return (y - 420000) * 0.3 + f(420000)
    elif y <= 960000:
        return (y - 660000) * 0.35 + f(660000)
    else:
        return (y - 960000) * 0.45 + f(960000)


# ---------------月个税函数---------------
def g(y):
    if y == 1:
        return f(a - b - c)
    else:
        return (f(y * (a - b - c)) - f((y - 1) * (a - b - c)))


# ---------------交金基数---------------
if a >= e * 3:
    c = e * 3 * 0.175
elif a <= e * 0.6:
    c = e * 0.6 * 0.175
else:
    c = a * 0.175
# ---------------免征额调整---------------
if (a - c) < b:
    b = a - c
# ---------------制定表格---------------
x = prettytable.PrettyTable(["月份", "五险一金", "当月纳税", "当月税后收入", "累计纳税", "累计税后收入"])
x.align = "r"
# ---------------输出计算结果---------------
wb = xlwt.Workbook()
n = wb.add_sheet("计算结果")
for d in range(1, 13):
    l = [d, c, g(d), a - g(d) - c, f(d * (a - b - c)), a * d - (f(d * (a - b - c)) + c * d)]
    x.add_row([d, h(c), h(g(d)), h(a - g(d) - c), h(f(d * (a - b - c))), h(a * d - (f(d * (a - b - c)) + c * d))])
    for j in range(0, 6):
        n.write(d, j, l[j])
value = ["月份", "五险一金", "当月纳税", "当月税后收入", "累计纳税", "累计税后收入"]
for i in range(0, 6):
    n.write(0, i, value[i])
print(x)
print("个人交金总额:", h(c * 12))
print("公积金帐户余额:", h(c / 0.175 * 0.14 * 12))
print("医疗保险金帐户余额:", h(c / 0.175 * 0.115 * 12))
print("养老金帐户余额:", h(c / 0.175 * 0.28 * 12))
print("(单位:元)")
name = '2019年度收入构成'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.xls'
wb.save(name)
print(Fore.RED + "2019年度收入构成"+name+".xls 保存成功！")
ord(msvcrt.getch())
