import pandas as pd
from tkinter import *
from PIL import Image, ImageTk


class DB:
  def __init__(self, filename):
    self.df = pd.read_excel(filename)
    # поиск по словам

  # результат: все строки удв. условию
  def getTheoremByKeyWord(self, word):
    results = []
    for name, index in zip(self.df['Name'], range(len(self.df))):
      if word.lower() in name.lower().split():
        results.append(self.df.iloc[index])
    return results

  def getNameByKeyWord(self, word):
    results = []
    for name, index in zip(self.df['Name'], range(len(self.df))):
      if word.lower() in name.lower().split():
        results.append(index)
        results.append(name)
        results.append('\n')
    return results
    # поиск по подстроке

  # результат: все строки удв. условию
  def getTheoremBySubStrInContext(self, substr):
    results = []
    for context, index in zip(self.df['Context'], range(len(self.df))):
      if substr.lower() in context.lower():
        results.append(self.df.iloc[index])
    return results

  def getDataById(self, index):
    return self.df.iloc[index]

  def getDataFrame(self):
    return self.df


class Quation(DB):
  def __init__(self, main, fname):
    super().init(fname)  # Конструирование объекта базового класса

    self.__main = main
    self.window_width = 1400
    self.window_height = 900
    self.__main.geometry(str(self.window_width) + 'x' + str(self.window_height))
    self.__main.resizable(1, 1)
    self.lst = []
    self.labelphoto=Label()
    self.labelphoto.grid(row=0,column=3,rowspan=10)

    self.entry1 = Entry(main, font=15)
    self.entry1.grid(row=0, column=0)

    self.textName = Text(main, font=15, wrap=WORD, height=2, width=50)
    self.textName.grid(row=0, column=2)

    self.textContent = Text(main, font=15, wrap=WORD, height=5, width=50)
    self.textContent.grid(row=1, column=2, rowspan=5)


    self.button1 = Button(main, text="Check")
    self.button1.grid(row=0, column=1, rowspan=100)
    self.button1.config(command=self.show_result)

  def show_result(self):
    txt = str(self.entry1.get())
    res = self.getNameByKeyWord(word=txt)

    for i in self.lst:
      i.destroy()
    self.lst = []
    # print(len(self.lst))
    # print(len(res),txt)
    for i in range(len(res)):
      if len(res[i])>50:
        txt=res[i][:50]
      else:
        txt=res[i]
      self.lst.append(Button(self.__main, text=txt))
      # print(res[i]['index'])
      self.lst[i].config(command=lambda x=i: self.btn_result_clicked(res[x]))
      self.lst[i].grid(row=i + 1, column=0)

  def btn_result_clicked(self, index):
    print(index)
    theorem_name = self.getDataById(int(index))['Name']  # название теоремы
    theorem_content = self.getDataById(int(index))['Content']  # содержание теоремы
    theorem_img = self.getDataById(int(index))['Image']  # ссылка на картинку теоремы на жестком диске
    self.textName.delete(1.0, END)
    self.textName.insert(1.0, theorem_name)
    self.textContent.delete(1.0, END)
    self.textContent.insert(1.0, theorem_content)
    self.photo=ImageTk.PhotoImage(Image.open(theorem_img).resize((400,400)))
    self.labelphoto.config(image=self.photo)
    #label = Label(self.__main, image=self.photo)
    #label.grid(row=0,column=3)


filename = 'theorems_v2.xlsx'
root = Tk()
root.title('Теоремы')
q = Quation(root, filename)
root.mainloop()