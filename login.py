from tkinter import *
import MySQLdb
import tkinter.messagebox as messagebox
import jieba
import jieba.analyse
import zhua

global G_user_name


class LoginPage:
    """登录界面"""
    global G_user_name

    def __init__(self, master):
        self.root = master
        self.root.geometry('400x200')
        self.root.title('商品推荐系统')
        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='newsrecommend',
                                    charset='utf8')
        self.username = StringVar()
        self.password = StringVar()
        self.page = Frame(self.root)
        self.creatapage()

    def creatapage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text='用户名:').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text='密码:').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, stick=E, column=1)
        Button(self.page, text='登录', command=self.login).grid(row=3, stick=W, pady=10)
        Button(self.page, text='注册账号', command=self.register).grid(row=3, stick=E, column=1)
        self.page.pack()

    def login(self):
        """登录功能"""

        user_name1 = self.username.get()
        user_password = self.password.get()
        # 数据库链接

        cursor = self.conn.cursor()
        # 数据库操作
        sql = "select password from user where user_name = '%s'"
        cursor.execute(sql % user_name1)
        results = cursor.fetchall()
        cursor.close()
        # 判断用户名和密码是否匹配
        if user_name1 == '' or user_password == '':
            messagebox.showerror(message='用户名或密码为空')
        elif not results:
            messagebox.showerror('登录失败', '账户不存在')
        elif user_password == results[0][0]:
            messagebox.showinfo(title='welcome', message='欢迎您：' + user_name1)
            G_user_name = user_name1
            self.conn.close()
            self.page.destroy()
            tuijianPage(self.root)

            # recommend()
        else:
            messagebox.showerror(message='密码错误')

        # 数据库关闭

    # self.conn.close()

    def register(self):
        """注册功能跳转"""
        self.conn.close()
        self.page.destroy()
        RegisterPage(self.root)


class RegisterPage:
    """注册界面"""

    def __init__(self, master=None):
        self.root = master
        self.root.title('账号注册')
        self.root.geometry('400x250')
        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='newsrecommend',
                                    charset='utf8')
        self.username = StringVar()
        self.password0 = StringVar()  # 第一次输入密码
        self.password1 = StringVar()  # 第二次输入密码
        self.page = Frame(self.root)
        self.createpage()

    def createpage(self):
        """界面布局"""
        Label(self.page).grid(row=0)
        Label(self.page, text="账号:").grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self.page, text="密码:").grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password0, show='*').grid(row=2, column=1, stick=E)
        Label(self.page, text="再次输入:").grid(row=3, stick=W, pady=10)
        Entry(self.page, textvariable=self.password1, show='*').grid(row=3, column=1, stick=E)
        Button(self.page, text="返回", command=self.repage).grid(row=4, stick=W, pady=10)
        Button(self.page, text="注册", command=self.register).grid(row=4, column=1, stick=E)
        self.page.pack()

    def repage(self):
        """返回登录界面"""
        self.page.destroy()
        self.conn.close()
        LoginPage(self.root)

    def register(self):
        """注册"""
        if self.password0.get() != self.password1.get():
            messagebox.showwarning('错误', '密码核对错误')
        elif len(self.username.get()) == 0 or len(self.password0.get()) == 0:
            messagebox.showerror("错误", "不能为空")
        else:
            try:
                cursor = self.conn.cursor()
                sql = "insert into user(user_name,password,history) values('%s','%s','{}')"
                cursor.execute(sql % (self.username.get(), self.password0.get()))
                self.conn.commit()
                cursor.close()
                self.conn.close()
                messagebox.showinfo("成功", "注册成功，按确定返回登录界面")
                self.page.destroy()
                LoginPage(self.root)
            except:
                messagebox.showerror("注册失败", "该账户已存在")


class tuijianPage:
    """推荐界面"""
    global G_user_name
    user_word = {}
    shangpin = []
    keywords = []
    # user_his = []
    recommend_num = [-1, -1, -1, -1, -1]
    recommend_title = [
        "                                                                                                                                  ",
        "                                                                                                                                  ",
        "                                                                                                                                  ",
        "                                                                                                                                  ",
        "                                                                                                                                  "]

    def __init__(self, master=None):
        self.root = master
        self.root.title('商品推荐')
        self.root.geometry('720x480')
        self.conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123456', db='newsrecommend',
                                    charset='utf8')

        self.page = Frame(self.root)
        self.createpage()

    def createpage(self):
        """界面布局"""
        # 新闻框1
        Label(self.page).grid(row=0)
        Label(self.page, text=self.recommend_title[0],width = 80,justify = 'left').grid(row=1, stick=E, pady=10)
        Button(self.page, text='喜欢', command=self.visit1).grid(row=1, column=1)
        Button(self.page, text='不感兴趣', command=self.dislike1).grid(row=1, column=2, stick=E)

        Label(self.page, text=self.recommend_title[1],width = 80,justify = 'left').grid(row=2, stick=E, pady=10)
        Button(self.page, text='喜欢', command=self.visit2).grid(row=2, column=1)
        Button(self.page, text='不感兴趣', command=self.dislike2).grid(row=2, column=2, stick=E)

        Label(self.page, text=self.recommend_title[2],width = 80,justify = 'left').grid(row=3, stick=E, pady=10)
        Button(self.page, text='喜欢', command=self.visit3).grid(row=3, column=1)
        Button(self.page, text='不感兴趣', command=self.dislike3).grid(row=3, column=2, stick=E)

        Label(self.page, text=self.recommend_title[3],width = 80,justify = 'left').grid(row=4, stick=E, pady=10)
        Button(self.page, text='喜欢', command=self.visit4).grid(row=4, column=1)
        Button(self.page, text='不感兴趣', command=self.dislike4).grid(row=4, column=2, stick=E)

        Label(self.page, text=self.recommend_title[4],width = 80,justify = 'left').grid(row=5, stick=E, pady=10)
        Button(self.page, text='喜欢', command=self.visit5).grid(row=5, column=1)
        Button(self.page, text='不感兴趣', command=self.dislike5).grid(row=5, column=2, stick=E)

        Button(self.page, text='重置商品', command=self.get_shangpin).grid(row=6, stick=W, pady=10)
        Button(self.page, text='退出', command=self.repage).grid(row=6, column=2, stick=E)
        self.page.pack()
        self.get_shangpin(1)

    def set_user_word(self, i):
        if i < 0:
            kk = -1
            i = -i
        else:
            kk = 1
        for his in self.user_word.keys():
            self.user_word[his] = self.user_word[his] * 0.9
        for key, value in self.keywords[self.recommend_num[i - 1]]:
            if key in self.user_word:
                self.user_word[key] = self.user_word[key] + value * kk
            else:
                self.user_word[key] = value * kk
        if len(self.user_word.keys()) > 20:
            while len(self.user_word.keys()) > 20:
                minn = 1000
                numm = ''
                for i in self.user_word.keys():
                    if self.user_word[i] < minn:
                        minn = self.user_word[i]
                        numm = i
                self.user_word.pop(numm)
        self.user_word = self.sort_by_value(self.user_word)

    def change_history(self, i):
        self.set_user_word(i)
        self.get_recommend_result()
        self.set_display()

    def set_display(self):
        Label(self.page, text="                                                                                                              "
                              "                           ",width = 80,justify = 'left').grid(row=1, stick=E, pady=10)
        Label(self.page, text="                                                                                                              "
                              "                           ",width = 80,justify = 'left').grid(row=2, stick=E, pady=10)
        Label(self.page, text="                                                                                                              "
                              "                           ",width = 80,justify = 'left').grid(row=3, stick=E, pady=10)
        Label(self.page, text="                                                                                                              "
                              "                           ",width = 80,justify = 'left').grid(row=4, stick=E, pady=10)
        Label(self.page, text="                                                                                                              "
                              "                           ",width = 80,justify = 'left').grid(row=5, stick=E, pady=10)

        Label(self.page, text=self.recommend_title[0],width = 80,justify = 'left').grid(row=1, stick=E, pady=10)
        Label(self.page, text=self.recommend_title[1],width = 80,justify = 'left').grid(row=2, stick=E, pady=10)
        Label(self.page, text=self.recommend_title[2],width = 80,justify = 'left').grid(row=3, stick=E, pady=10)
        Label(self.page, text=self.recommend_title[3],width = 80,justify = 'left').grid(row=4, stick=E, pady=10)
        Label(self.page, text=self.recommend_title[4],width = 80,justify = 'left').grid(row=5, stick=E, pady=10)
        #self.page.pack()
        self.page.update()

    def get_recommend_result(self):
        sim = [-1, -1, -1, -1, -1]
        for i in range(len(self.keywords)):
            simm = 0
            for j, k in self.keywords[i]:
                if j in self.user_word.keys():
                    simm = simm + self.user_word[j] * k
            for l in range(5):
                if simm > sim[l]:
                    for ll in reversed(range(l + 1, 5)):
                        sim[ll] = sim[ll - 1]
                        self.recommend_num[ll] = self.recommend_num[ll - 1]
                        self.recommend_title[ll] = self.recommend_title[ll - 1]
                    sim[l] = simm
                    self.recommend_num[l] = i
                    self.recommend_title[l] = self.shangpin[i]
                    break

    def visit1(self):
        self.change_history(1)

    def visit2(self):
        self.change_history(2)

    def visit3(self):
        self.change_history(3)

    def visit4(self):
        self.change_history(4)

    def visit5(self):
        self.change_history(5)

    def dislike1(self):
        self.change_history(-1)

    def dislike2(self):
        self.change_history(-2)

    def dislike3(self):
        self.change_history(-3)

    def dislike4(self):
        self.change_history(-4)

    def dislike5(self):
        self.change_history(-5)

    def repage(self):
        """返回登录界面"""
        self.conn.close()
        self.page.destroy()
        LoginPage(self.root)

    def get_shangpin(self,i=0):
        self.shangpin = []
        if i==0:
            zhua.get_shangpin(self.shangpin)
            f = open('shangpin.txt', 'w')
            for line in self.shangpin:
                print(line, file=f)
            f.close()
        if i==1:
            f = open('shangpin.txt', 'r')
            shangpin1 = f.readlines()  # 读取全部内容 ，并以列表方式返回
            f.close()
            for line in shangpin1:
                line = line.strip('\n')
                self.shangpin.append(line)


        self.get_keyword()
        self.get_user_his()
        self.change_history(1)

    def get_keyword(self):
        self.keywords = []
        keyword = ""
        for kk in self.shangpin:
            keyword = jieba.analyse.extract_tags(kk, topK=10, withWeight=True, allowPOS=())
            self.keywords.append(keyword)

    def get_user_his(self):
        # self.user_his = []
        return

    def sort_by_value(self, d):
        key1 = list(d.keys())
        value1 = list(d.values())
        for i in range(len(value1) - 1):
            for j in range(i + 1, len(value1)):
                if value1[i] > value1[j]:
                    k = value1[i]
                    value1[i] = value1[j]
                    value1[j] = k
                    k = key1[i]
                    key1[i] = key1[j]
                    key1[j] = k
        dictionary = {}
        for i in range(len(value1)):
            dictionary.update({key1[i]: value1[i]})
        return dictionary


if __name__ == '__main__':
    root = Tk()
    LoginPage(root)
    root.mainloop()
