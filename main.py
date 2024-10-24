from tkinter import *
import requests
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox as mb
import pyperclip
import os
import json


file_save = "history_link.json"


def save_history(file_save, link, file):
    history = []
    if os.path.exists(file_save):
        with open(file_save, "r") as f:
            history = json.load(f)
    history.append({"Name_file": os.path.basename(file),
                    "save_file_history": file_save,
                    "link": link})
    with open(file_save, "w") as f:
        json.dump(history, f, indent=4)


def get_response():
    try:
        file = fd.askopenfilename()
        if file:
            with open(file, "rb") as fi:
                f = {"file" : fi}
                answer_json = requests.post("https://file.io", files=f)
                if answer_json.status_code == 200:
                    link = answer_json.json()["link"]
                    e.delete(0, END)
                    e.insert(0, link)
                    pyperclip.copy(link)
                    save_history(file_save, link, file)
                else:
                    mb.showerror(title="Ошибка", message="Не верно указанный путь к сайту")
    except Exception as exc:
        mb.showerror(title="Ошибка", message=f"Произошла ошибка: {exc}")


def show_history():
    if not os.path.exists(file_save):
        mb.showinfo(title="Информация", message="История пуста")
        return
    window_history = Toplevel()
    window_history.title("История")

    name_listbox = Listbox(window_history, width=50)
    name_listbox.pack(side=LEFT)

    link_listbox = Listbox(window_history, width=50)
    link_listbox.pack(side=LEFT)

    with open(file_save, "r") as file:
        content = json.load(file)
        for i in content:
            name_listbox.insert(END, i["Name_file"])
            link_listbox.insert(END, i["link"])


window = Tk()
window.title("Отправка файлов в file.io")
window.geometry(f"400x300+{window.winfo_screenwidth()//2-200}+{window.winfo_screenheight()//2-150}")


btn = Button(window, text="Выбрать файл", font=("Arial", 16), command=get_response)
btn.pack(pady=10)


e = Entry(window, width=30, font=("Arial", 16))
e.pack(pady=10)


btn_history = Button(window, text="Посмотреть историю", font=("Arial", 16), command=show_history)
btn_history.pack()


window.mainloop()
