from cgitb import reset
import shelve
import psutil
import os
import sys


class DataController(): 
    def __init__(self) -> None:
        pass

    @classmethod
    def get_process_list(self) -> list:
        app_list = []
        try:
            for proc in psutil.process_iter():
                print("----------------------")
                print("プロセスID:" + str(proc.pid))
                try:
                    print("実行モジュール：" + proc.name())
                    app_list.append(proc.pid)
                except psutil.AccessDenied:
                    pass
        finally:
            return app_list


    @classmethod
    def get_restricted_list(self) -> list:
        #データファイルの展開
        f = shelve.open(self.resource_path("force_quit_chan"))
        print(str(self.resource_path("force_quit_chan")))
        #存在するかの検証
        try:
            restricted_list = f["restricted_list"]
        except:
            f["restricted_list"] = []
            restricted_list = f["restricted_list"]
        finally:
            f.close()
            return restricted_list


    @classmethod
    def up_restricted_list(self, list: list) -> None:
        f = shelve.open(self.resource_path("force_quit_chan"))
        print(str(self.resource_path("force_quit_chan")))
        f["restricted_list"] = list
        f.close()


    @classmethod
    def get_web_restricted_list(self) -> list:
        #データファイルの展開
        f = shelve.open(self.resource_path("force_quit_chan"))
        print(str(self.resource_path("force_quit_chan")))

        #存在するかの検証
        try:
            web_restricted_list = f["web_restricted_list"]
        except:
            f["web_restricted_list"] = []
            web_restricted_list = f["web_restricted_list"]
        finally:
            f.close()
            return web_restricted_list
    

    @classmethod
    def up_web_restricted_list(self, list: list) -> None:
        f = shelve.open(self.resource_path("force_quit_chan"))
        print(str(self.resource_path("force_quit_chan")))
        f["web_restricted_list"] = list
        f.close()


    @classmethod
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, "../", relative_path)
        return os.path.join(os.path.abspath("."), relative_path)