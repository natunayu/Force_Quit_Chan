
import tkinter
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as tkm
from Data_Controller import DataController
import threading
import time
from win32gui import GetWindowText, GetForegroundWindow
import psutil
from PIL import ImageTk
import os
import subprocess
import win32process
import pyautogui
import sys

sys.dont_write_bytecode = True

concent_mode = False
website_list = ["iexplore.exe,", "msedge.exe", "chrome.exe", "firefox.exe"]

class Window_Controller(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("強制終了ちゃん!!!")
        self.master.geometry("472x455")
        self.label0 = tk.Label(self.master, text="制限中のアプリ")
        self.master.protocol('WM_DELETE_WINDOW', self.quit_app)

        self.on_image = ImageTk.PhotoImage(file=self.resource_path("on.png"))
        self.off_image = ImageTk.PhotoImage(file=self.resource_path("off.png"))

        #並列処理でアクティブウィンドウを取得する
        self.thread1 = threading.Thread(target=self.loop_get_active_window)
        self.thread1.setDaemon(True)
        self.thread1.start()

        self.list_value = tk.StringVar()
        self.act_text = tk.StringVar()
        self.act_text.set("None")

        #制限アプリリストを取得・表示・変更
        self.rest_value_check()
        self.list_frame = tk.Frame(master=self.master, relief=tk.RAISED, height=100, width=100, bg="white")
        self.listbox = tk.Listbox(master=self.list_frame, height=10, width=50, listvariable=self.list_value, selectmode="single")
        self.list_scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.listbox.yview)
        
        #アクティブウィンドウの表示
        self.active_frame = tk.LabelFrame(master=self.master, text="現在のアクティブウィンドウ", relief=tk.FLAT, height=100, width=200, bg="white") 
        #self.label1 = tk.Label(master=self.master, text="") 
        self.active_label = tk.Label(master=self.active_frame, width=20, height=8, textvariable=self.act_text)  

        #ボタンの設定
        self.add_button = tk.Button(master=self.list_frame, width=20, height=2, text = "起動中アプリから追加", command=self.create_modal_dialog)
        self.delete_button = tk.Button(master=self.list_frame, width=20, height=2, text = "削除", command=self.delete_rest_app)

        self.con_label = tk.LabelFrame(master=self.master, text="集中モードOFF", fg = "grey")         
        self.on_button = tk.Button(master=self.con_label, image=self.off_image, bd=0, command=self.con_switch) 
        self.on_button.grid(row=1, column=2)
        

        #Webサイトの制限ワード設定リスト
        self.web_list_value = tk.StringVar()
        self.web_rest_value_check()

        self.web_list_frame = tk.Frame(master=self.master, relief=tk.RAISED, height=100, width=100)
        self.web_listbox = tk.Listbox(master=self.web_list_frame, height=10, width=50, listvariable=self.web_list_value, selectmode="single")
        self.web_list_scrollbar = ttk.Scrollbar(self.web_list_frame, orient='vertical', command=self.listbox.yview)
        self.label2 = tk.Label(self.master, text="\n制限中のウェブワード")

        self.web_textbox = tkinter.Entry(master=self.web_list_frame, width=22)
        self.web_add_button = tk.Button(master=self.web_list_frame, width=10, height=1, text = "追加", command=self.append_rest_word)
        self.web_delete_button = tk.Button(master=self.web_list_frame, width=10, height=1, text = "削除", command=self.delete_rest_word)

        #gridで配置
        #master
        self.label0.grid(row=0, column=0)
        self.con_label.grid(row=1, column=1)
        self.list_frame.grid(row=1, column=0)
        self.web_list_frame.grid(row=3, column=0)
        self.label2.grid(row=2, column=0)
        self.active_frame.grid(row=3, column=1, columnspan=3)
        self.active_label.grid(row=0, column=0, columnspan=2)
        
        #listframe
        self.add_button.grid(row=1, column=0)
        self.delete_button.grid(row=1, column=1)
        self.listbox.grid(row=0, column=0, columnspan=3)
        self.list_scrollbar.grid(row=0, column=3, rowspan=2, sticky=(tk.N, tk.S))

        #web list frame 
        self.web_listbox.grid(row=2, column=0, columnspan=3)
        self.web_list_scrollbar.grid(row=2, column=3, rowspan=2, sticky=(tk.N, tk.S))
        self.web_textbox.grid(row=3, column=0)
        self.web_add_button.grid(row=3, column=1)
        self.web_delete_button.grid(row=3, column=2)
        

    def loop_get_active_window(self) -> None:
        global concent_mode
        global act_win
        while True:
            time.sleep(0.5)
            if concent_mode == True:
                act_win = GetWindowText(GetForegroundWindow())
                self.force_quit(act_win)
                if len(act_win) / 10 >= 1:
                    a_len = len(act_win)
                    n = 0
                    for i in range(a_len):
                        if i % 13 == 0:
                            act_win = act_win[:i + 2 * n] + "\n" + act_win[i + 2 * n:]
                            n += 1
                self.act_text.set(act_win)
            else:
                self.act_text.set("集中モードがOFFです。")


    def create_modal_dialog(self):
        #ダイアログの表示
        self.dlg_modal = tk.Toplevel(self)
        self.dlg_modal.title("強制終了ちゃん!!!(起動しているアプリから選ぶ)")
        self.dlg_modal.geometry("320x500")
        self.dlg_modal.resizable(width=0, height=0)
        self.dlg_list_value = tk.StringVar()

        #実行中のアプリを取得andセット
        self.app_list = self.get_process_app()
        self.dlg_list_value.set(self.app_list)

        self.dlg_list_frame = tk.Frame(master=self.dlg_modal, relief=tk.RAISED, height=100, width=100, bg="white")
        self.dlg_listbox = tk.Listbox(master=self.dlg_list_frame, height=20, width=50, listvariable=self.dlg_list_value, selectmode="single")
        self.dlg_add_button = tk.Button(master=self.dlg_list_frame, width=20, height=2, text = "追加する", command=self.append_rest_app)
        self.dlg_back_button = tk.Button(master=self.dlg_list_frame, width=20, height=2, text = "戻る", command=self.back_button)
        self.dlg_scrollbar = ttk.Scrollbar(self.dlg_list_frame, orient='vertical', command=self.dlg_listbox.yview)

        self.dlg_list_frame.grid(row=1, column=0)
        self.dlg_listbox.grid(row=0, column=0, columnspan=2)
        self.dlg_scrollbar.grid(row=0, column=2, rowspan=2, sticky=(tk.N, tk.S))
        self.dlg_add_button.grid(row=1, column=0)
        self.dlg_back_button.grid(row=1, column=1)

        self.dlg_modal.grab_set()        # モーダルにする
        self.dlg_modal.focus_set()       # フォーカスを新しいウィンドウをへ移す
        self.dlg_modal.transient(self.master) 

        self.master.wait_window(self.dlg_modal)


    def delete_rest_app(self):
        try:
            del_point = self.listbox.curselection()
            del_content = self.listbox.get(del_point)
        except Exception:
            self.delete_error()
            return

        list = DataController.get_restricted_list()
        try:
            list.remove(del_content)
            DataController.up_restricted_list(list)
        except Exception:
            self.delete_error()
            return
        finally:
            self.rest_value_check()


    def append_rest_app(self):
        try:
            app_point = self.dlg_listbox.curselection()
            app_content = self.dlg_listbox.get(app_point)
        except Exception:
            self.append_error()
            return

        app_content = str(app_content).replace(".exe", "")
        list = DataController.get_restricted_list()
        list.append(app_content)
        if 1 < list.count(app_content):
            tkm.showerror(title="強制終了ちゃん!!!", message="既に追加されています。")
            return
        else:
            DataController.up_restricted_list(list)
            self.rest_value_check()
            self.dlg_modal.destroy()
            return


    def back_button(self):
        self.dlg_modal.destroy()


    def add_error(self):
        tkm.showerror('強制終了ちゃん!!!', '既に追加されてます!!!')
        return


    def delete_error(self):
        tkm.showerror('強制終了ちゃん!!!', '値がありません!!!\n(リストから選択してください。)')
        return


    def append_error(self):
        tkm.showerror('強制終了ちゃん!!!', '値を選択してください!!!')
        return


    def get_process_app(self) -> list:
        app_list = []
        for proc in psutil.process_iter():
            app_list.append(proc.name())   
        app_list = list(set(app_list))
        app_list.sort()    
        return app_list


    def rest_value_check(self):
        list = DataController.get_restricted_list()
        #制限アプリが無い場合
        if not list:
            self.list_value.set(["制限中のアプリはありません。"])
        #制限アプリがある場合
        else:
            self.list_value.set(list)


    def web_rest_value_check(self):
        list = DataController.get_web_restricted_list()
        #制限アプリが無い場合
        if not list:
            self.web_list_value.set(["制限中のワードはありません。"])
        #制限アプリがある場合
        else:
            self.web_list_value.set(list)        


    def append_rest_word(self):
        text = self.web_textbox.get()
        list = DataController.get_web_restricted_list()
        list.append(text)
        if 1 < list.count(text):
            tkm.showerror('強制終了ちゃん!!!', '既に追加されてます!!!')
            return

        elif not text:
            tkm.showerror('強制終了ちゃん!!!', 'ワードを入力してください!!!')
            self.web_textbox.delete(0, tkinter.END)
            return

        elif text.count(" ") == len(text):
            tkm.showerror('強制終了ちゃん!!!', 'ワードを入力してください!!!')
            self.web_textbox.delete(0, tkinter.END)
            return            

        elif text.count("　") == len(text):
            tkm.showerror('強制終了ちゃん!!!', 'ワードを入力してください!!!')
            self.web_textbox.delete(0, tkinter.END)  
            return

        else:
            DataController.up_web_restricted_list(list)
            self.web_rest_value_check()
            self.web_textbox.delete(0, tkinter.END)
            return            


    def delete_rest_word(self):
        try:
            del_point = self.web_listbox.curselection()
            del_content = self.web_listbox.get(del_point)
        except Exception:
            self.delete_error()
            return
        list = DataController.get_web_restricted_list()

        try:
            list.remove(del_content)
            DataController.up_web_restricted_list(list)
        except Exception:
            self.delete_error()
            return
        finally:
            self.web_rest_value_check()


    def con_switch(self):
        global concent_mode
        
        if concent_mode:
            self.on_button.config(image = self.off_image)
            self.con_label.config(text = "集中モードはOFFです。", fg = "grey")
            concent_mode = False
        else:
            self.on_button.config(image = self.on_image)
            self.con_label.config(text = "集中モードがONです！", fg = "green")
            tkm.showinfo("強制終了ちゃん!!!", "集中モードがONになりました！\n(制限リストのアプリとサイトを起動すると強制終了します)")
            concent_mode = True


    def force_quit(self, win: str):
        list1 = DataController.get_restricted_list()
        list2 = DataController.get_web_restricted_list()
        try:
            pname_list = []
            pid_list = []

            for proc in psutil.process_iter():
                pname_list.append(proc.name())
                pid_list.append(proc.pid)
            p_info = dict(zip(pid_list, pname_list))
            pid = GetForegroundWindow()
            act_pid = win32process.GetWindowThreadProcessId(pid)
            act_pid = int(act_pid[1])
            #print(act_pid)
            if act_pid not in pid_list:
                print("id error")
                return

            if str(p_info[act_pid]).replace(".exe", "") in list1:
                for i in list1:
                    if str(p_info[act_pid]) == str(i) + ".exe":
                        subprocess.run('taskkill /IM {0}'.format(act_pid), shell=True, capture_output=True, text=True)
                        tkm.showerror('強制終了ちゃん!!!', 'このアプリは今制限中です!!!\n集中しましょう…')
                        return
                    return
                return

            elif str(p_info[act_pid]) in website_list:
                page_title = ""
                for w in win:
                    w = w.lower()
                    page_title += w
                print(page_title)

                for i in range(len(list2)):
                    word = ""
                    l = list2[i]
                    for ln in str(l):
                        ln = ln.lower()
                        word += ln
                    print(word)
                    if word in page_title:
                        pyautogui.keyDown('ctrl')
                        pyautogui.press(['w'])
                        pyautogui.keyUp('ctrl')
                        tkm.showerror('強制終了ちゃん!!!', 'このサイトは今制限中です!!!\n集中しましょう…')
                        return
                return

            else:
                return

        except subprocess.TimeoutExpired as e:
            print(e.cmd)


    def quit_app(self):
        print("a")
        #self.thread1.join()
        self.master.destroy()
        sys.exit()


    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    root = tkinter.Tk()
    con =  Window_Controller(master = root)
    con.mainloop()