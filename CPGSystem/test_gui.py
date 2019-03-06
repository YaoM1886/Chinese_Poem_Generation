import wx
import os
import wx.lib.scrolledpanel
import subprocess
from gensim.models import word2vec
import generate_poem
import pingze
import zhconv


w2v_model = word2vec.Word2Vec.load('word2vec_model_amplified')



class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u'CPGS古诗自动撰写系统',
                          pos=wx.DefaultPosition, size=wx.Size(200, 200),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.Center()

        #构建面板窗口,其中包含静态文字标签和按钮触发标签

        #系统简介这一行
        self.m_panel1 = wx.Panel(self)
        self.m_staticText1 = wx.StaticText(self.m_panel1, wx.ID_ANY, u'系统简介', (20, 20))
        self.m_button1 = wx.Button(self.m_panel1, wx.ID_ANY, u'使用指南', (80, 20),wx.DefaultSize)


        #输入这一行
        self.m_staticText2 = wx.StaticText(self.m_panel1, wx.ID_ANY, u'开始使用',(20, 80))
        self.m_button2 = wx.Button(self.m_panel1, wx.ID_ANY, u'关键字输入', (80, 80),
                                   wx.DefaultSize)

        #按钮触发对话框，使用BIND函数将触发动作与特定函数绑定
        self.m_button1.Bind(wx.EVT_BUTTON, MyDialog1(None).OnClick)
        self.m_button2.Bind(wx.EVT_BUTTON, MyDialog2(None).OnClick)

        #设置按钮的背景色
        self.m_button1.SetBackgroundColour('#0a74f7')
        self.m_button1.SetForegroundColour('white')
        self.m_button2.SetBackgroundColour('#545454')
        self.m_button2.SetForegroundColour('white')

        #设置面板的背景色为白色
        self.m_panel1.SetBackgroundColour('white')

class MyDialog1(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='使用指南',
                           pos=wx.DefaultPosition, size=wx.Size(500, 400),style=wx.DEFAULT_DIALOG_STYLE)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')
        wx.StaticText(self.panel, -1, '我们的系统中文名称叫做\"古诗撰写系统\"\n'
                                      '英文名称叫做Chinese Poetry Generation System,\n'
                                      '旨在为用户写诗提供灵感。\n我们以七言绝句语料集为训练基础，当用户输入关键字\n'
                                      '即可得到系统生成的多首七言绝句，\n用户可以在其中挑选自己喜欢的', (60, 80))

    def OnClick(self, event):
        dialog1 = MyDialog1(None)
        dialog1.ShowModal()

class MyDialog2(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='关键字输入', pos=wx.DefaultPosition, size=wx.Size(500, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')
        vbox = wx.BoxSizer(wx.VERTICAL)
        nm = wx.StaticBox(self.panel, -1, '关键字输入')
        nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL)

        nmbox = wx.BoxSizer(wx.HORIZONTAL)
        fn = wx.StaticText(self.panel, -1, "输入1", (20, 20))

        nmbox.Add(fn, 0, wx.ALL | wx.CENTER, 5)
        self.nm1 = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT)
        self.nm2 = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT)
        self.nm3 = wx.TextCtrl(self.panel, -1, style=wx.ALIGN_LEFT)
        ln = wx.StaticText(self.panel, -1, "输入2", (40, 20))
        tn = wx.StaticText(self.panel, -1, "输入3", (60, 20))

        nmbox.Add(self.nm1, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(ln, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(self.nm2, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(tn, 0, wx.ALL | wx.CENTER, 5)
        nmbox.Add(self.nm3, 0, wx.ALL | wx.CENTER, 5)
        nmSizer.Add(nmbox, 0, wx.ALL | wx.CENTER, 10)
        sbox = wx.StaticBox(self.panel, -1, '按钮')
        sboxSizer = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.okButton = wx.Button(self.panel, -1, '确定输入')
        self.okButton.Bind(wx.EVT_BUTTON, self.find)
        hbox.Add(self.okButton, 0, wx.ALL | wx.LEFT, 10)


        sboxSizer.Add(hbox, 0, wx.ALL | wx.LEFT, 10)
        vbox.Add(nmSizer, 0, wx.ALL | wx.CENTER, 5)
        vbox.Add(sboxSizer, 0, wx.ALL | wx.CENTER, 5)
        self.panel.SetSizer(vbox)
        self.Centre()
        self.panel.Fit()








    def OnClick(self, event):
        dialog2 = MyDialog2(None)
        dialog2.ShowModal()



    def find(self, event):
        v1 = self.nm1.GetValue()
        v2 = self.nm2.GetValue()
        v3 = self.nm3.GetValue()
        MyDialog3(self).vv1 = MyDialog3(self).vv1.replace(MyDialog3(self).vv1, v1)
        MyDialog3(self).vv2 = MyDialog3(self).vv2.replace(MyDialog3(self).vv2, v2)
        MyDialog3(self).vv3 = MyDialog3(self).vv3.replace(MyDialog3(self).vv3, v3)


        if (self.nm1.GetValue() == '') & (self.nm2.GetValue() == '') & (self.nm3.GetValue() == ''):
            wx.MessageBox('请输入关键字！', '提示')
        elif (len(self.nm1.GetValue()) > 1) | (len(self.nm2.GetValue()) > 1) | (len(self.nm3.GetValue()) > 1):
            wx.MessageBox('请输入一个关键字!', '提示')
        else:

            #处理关键字和输出的相似
            generate_poem.generate_poem()
            kl = []
            ml = []
            flag = 1


            # 读取用户所有的输入，构建关键字以及语义相似字字典
            nm_dict = {self.nm1.GetValue(): 1}
            transitory = {}
            for item in [self.nm2.GetValue(), self.nm3.GetValue()]:
                if item != '':
                    flag+=1
                    nm_dict[item] = 1
            for key in nm_dict.keys():
                nm1_similar = w2v_model.most_similar(positive=[key], topn=10)
                for j in range(0, len(nm1_similar)):
                    transitory[nm1_similar[j][0]] = nm1_similar[j][1]
            nm1_dict = {**nm_dict, **transitory}


            #构建诗歌列表
            poems = {}
            with open('./poem_output.txt', 'r') as f1:
                for line in f1.readlines():
                    line = zhconv.convert(line.strip('\n'), 'zh-cn')
                    kl.append(line)
                while '' in kl:
                    kl.remove('')
                i = 0
                while (i >= 0) & ((2 * i + 1) < len(kl)):
                    ml.append(kl[2 * i] + '\n' + kl[2 * i + 1])
                    i += 1
                cl = ml[:]


                #判断输入不同关键字个数的阈值
                for i in ml:
                    score = 0
                    for item in nm1_dict.keys():
                        if item in i:
                            score+=nm1_dict[item]
                    if score ==0:
                        cl.remove(i)
                    elif (flag == 1) & (score >= 1.7):
                        poems[i] = score
                    elif (flag == 2) & (score >= 2.7):
                        poems[i] = score
                    elif (flag == 3) & (score >= 3.7):
                        poems[i] = score


                #输出要排序
            with open('./similar_output.txt', 'w') as fileObject:
                for k in sorted(poems, key=poems.__getitem__, reverse=True):
                    fileObject.write(k)
                    fileObject.write('\n\n\n')


            wx.MessageBox('诗歌已生成！请再次点击确定输入', '提示')
            self.okButton.Bind(wx.EVT_BUTTON, MyDialog3(None).OnClick)




class MyDialog3(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='诗歌输出', pos=wx.DefaultPosition, size=wx.Size(500, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.parent=parent
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1)
        self.panel.SetBackgroundColour('white')
        self.panel.SetupScrolling()
        self.refer_button = wx.Button(self.panel, -1, u'好诗推荐', (20, 20))
        self.refer_button.Bind(wx.EVT_BUTTON, MyDialog4(None).OnClick)
        self.again_button = wx.Button(self.panel, -1, u'换一批诗', (20, 40))
        self.again_button.Bind(wx.EVT_BUTTON, self.again_train)

        self.vv1 = ''
        self.vv2 = ''
        self.vv3 = ''



        with open('./similar_output.txt', 'r') as f2:
            text = wx.StaticText(self.panel, -1, f2.read(), (60, 80))
        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer.Add(text, 0, wx.ALL|wx.CENTER, 5)
        self.panel.SetSizer(bSizer)



    def OnClick(self, event):
        dialog3 = MyDialog3(None)
        dialog3.ShowModal()

    def again_train(self, event):

        #再次训练新的诗歌
        generate_poem.generate_poem()
        kl = []
        ml = []
        flag2 = 1

        nm_dic = {self.vv1: 1}
        transitory = {}
        for item in [self.vv2, self.vv3]:
            if item != '':
                flag2 += 1
                nm_dic[item] = 1
        for key in nm_dic.keys():
            nm1_similar = w2v_model.most_similar(positive=[key], topn=10)
            for j in range(0, len(nm1_similar)):
                transitory[nm1_similar[j][0]] = nm1_similar[j][1]
        nm1_dic = {**nm_dic, **transitory}


        poems = {}
        with open('./poem_output.txt', 'r') as f1:
            for line in f1.readlines():
                line = zhconv.convert(line.strip('\n'), 'zh-cn')
                kl.append(line)
            while '' in kl:
                kl.remove('')
            i = 0
            while (i >= 0) & ((2 * i + 1) < len(kl)):
                ml.append(kl[2 * i] + '\n' + kl[2 * i + 1])
                i += 1
            cl = ml[:]

            # 判断输入不同关键字个数的阈值
            for i in ml:
                score = 0
                for item in nm1_dic.keys():
                    if item in i:
                        score += nm1_dic[item]
                if score == 0:
                    cl.remove(i)
                elif (flag2 == 1) & (score >= 1.7):
                    poems[i] = score
                elif (flag2 == 2) & (score >= 2.7):
                    poems[i] = score
                elif (flag2 == 3) & (score >= 3.7):
                    poems[i] = score


                    # 输出要排序
        with open('./similar_output.txt', 'w') as fileObject:
            for k in sorted(poems, key=poems.__getitem__, reverse=True):
                fileObject.write(k)
                fileObject.write('\n\n\n')

        # with open('./poem_output.txt', 'r') as f1:
        #     for line in f1.readlines():
        #         line = line.strip('\n')
        #         kl.append(line)
        #     while '' in kl:
        #         kl.remove('')
        #     i = 0
        #     while (i >= 0) & ((2 * i + 1) < len(kl)):
        #         ml.append(kl[2 * i] + '\n' + kl[2 * i + 1])
        #         i += 1
        #     cl = ml[:]
        #
        #     for i in ml:
        #         if (self.vv1) not in i:
        #             cl.remove(i)
        #         elif (self.vv2) not in i:
        #             cl.remove(i)
        #         elif (self.vv3) not in i:
        #             cl.remove(i)
        #     ml = cl
        # with open('./similar_output.txt', 'w') as fileObject:
        #     for p in ml:
        #         fileObject.write(p)
        #         fileObject.write('\n\n\n')


        self.again_button.Bind(wx.EVT_BUTTON, MyDialog5(None).OnClick)



class MyDialog4(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='好诗推荐', pos=wx.DefaultPosition, size=wx.Size(500, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1)
        panel.SetBackgroundColour('white')
        panel.SetupScrolling()
        t = pingze.print_poem(10)
        text = wx.StaticText(panel, -1, t, (60, 80))
        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer.Add(text, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(bSizer)


    def OnClick(self, event):
        dialog4 = MyDialog4(None)
        dialog4.ShowModal()


class MyDialog5(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='诗歌输出', pos=wx.DefaultPosition, size=wx.Size(500, 400),
                           style=wx.DEFAULT_DIALOG_STYLE)
        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1)
        self.panel.SetBackgroundColour('white')
        self.panel.SetupScrolling()
        with open('./similar_output.txt', 'r') as f2:
            text = wx.StaticText(self.panel, -1, f2.read(), (60, 80))
        bSizer = wx.BoxSizer(wx.VERTICAL)
        bSizer.Add(text, 0, wx.ALL | wx.CENTER, 5)
        self.panel.SetSizer(bSizer)


    def OnClick(self, event):
        dialog5 = MyDialog5(None)
        dialog5.ShowModal()

if __name__ == '__main__':
    app = wx.App()
    MyFrame1(None).Show()
    app.MainLoop()










