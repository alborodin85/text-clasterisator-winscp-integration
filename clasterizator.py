import sys
import tkinter


def openInSublime():
    import subprocess
    subprocess.Popen([r'C:\Program Files\Sublime Text\sublime_text.exe', sys.argv[1]])
    quit()


if len(sys.argv) > 1:
    openInSublime()

'''
Подстановочные шаблоны:
!! становится восклицательным знаком
!/ становится текущим путём на стороне удалённого сервера
!@ становится именем хоста для текущей сессии
!U становится именем пользователя для текущей сессии
!Р становится паролем для текущей сессии
!# становится номером порта для текущей сессии
!N становится именем текущей сессии
!?prompt[\]?default! становится заданным пользователем значением с заданным приглашением(prompt)
и значением по-умолчанию(default) (опционально \ для избежания escape-преобразования)
!`command` становится выводом результата выполнения локальной комманды(command))
'''
# python "C:\Users\borodin_admin\Desktop\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\clasterizator.py"
# python "C:\Users\borodin_admin\Desktop\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\clasterizator.py" !.! !/ !@ !U !N

from tkinter import *

pr = Tk()
pr.title("Нейросетевой кластеризатор")
pr.geometry('800x200')
pr.iconbitmap(r'C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\winscp-integration\icon.ico')

container = Frame(pr)
container.pack(side='left', anchor='n')

labels = []
rowNum = 0
for parameter in sys.argv:
    label = tkinter.Label(container, text=parameter, justify='left')
    label.grid(row=rowNum, column=0, padx="5", pady="5", sticky='w')
    rowNum += 1

if len(sys.argv) > 1:
    button = Button(pr, text="Открыть в SublimeText", command=openInSublime)
    button.pack(side='right', padx="10", pady='5', anchor='n')

pr.mainloop()
