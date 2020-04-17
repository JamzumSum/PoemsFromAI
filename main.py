# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:34:31 2020

@author: a99gc
"""
import pro_py.pch
import sys
from pro_py.mainwindow import mainwindow
from pro_py.include import include
from pro_py.two import two
from pro_py.three import three
from PySide2.QtWidgets import QApplication
#from PySide2.QtCore import Slot,Signal,QObject

from comment import Rater
from imp import reload
import compose
import os
from contextlib import closing

#新增维度
start_token = 'B'
add_feature_dim = {
    "sentense": {
        "position": 9
    },
    "word": {
        "vowel": 5, 
        "tune": 1
    }
}
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"#设置log输出信息级别


class All:
    model_name=""
    model="" 
    '''初始化，并且设置各个窗口之间的跳转，如按下“开始”从mainwindow转至two窗口等
    设置model_name(诗的格式)和model（诗的模式）
    '''
    def __init__(self,ui_0,ui_1,ui_2,ui_3):
         self.ui_1 =ui_1  
         self.ui_1.show()       
         self.ui_0 =ui_0  
         self.ui_2 =ui_2
         self.ui_3 =ui_3
         self.ui_1.ui.Button_1.clicked.connect(self.ui_0.show)
         self.ui_0.ui.pushButton.clicked.connect(self.ui_0.hide)
         self.ui_1.ui.Button_2.clicked.connect(self.ui_2.show)
         self.ui_1.ui.Button_2.clicked.connect(self.ui_1.hide)
         self.ui_2.ui.Button_4.clicked.connect(self.ui_3.show)
         self.ui_2.ui.Button_4.clicked.connect(self.ui_2.hide)
         self.ui_3.ui.Button_5.clicked.connect(self.ui_1.show)
         self.ui_3.ui.Button_5.clicked.connect(self.ui_3.hide)
         self.ui_3.ui.Button_6.clicked.connect(self.ui_2.show)
         self.ui_3.ui.Button_6.clicked.connect(self.ui_3.hide)
         self.model_name=self.get_n1()
         self.model=self.get_n2()
      
#取得用户名字
    def get_name(self):
        #输入完成后调用函数w_1
         self.ui_1.ui.Number_1.editingFinished.connect(self.w_1)
    def w_1(self):
        #将最终窗口的姓名栏设置为for+姓名
        name=self.ui_1.ui.Number_1.text()
        self.ui_3.ui.text_8.setText("for "+name)   
        return  name        
#取得格式：五绝、五律、七绝、七律 ，根据按下的按键设置model_name的值 
    def get_n1(self):
        self.ui_1.ui.select_1.clicked.connect(self.set_n11) 
        self.ui_1.ui.select_2.clicked.connect(self.set_n12) 
        self.ui_1.ui.select_3.clicked.connect(self.set_n13) 
        self.ui_1.ui.select_4.clicked.connect(self.set_n14)        
    def set_n11(self):
        self.model_name="wujue-all"  
        return self.model_name
    def set_n12(self):
        self.model_name="wulv-all"
        return self.model_name
    def set_n13(self):
        self.model_name="qijue-all"  
        return self.model_name
    def set_n14(self):
        self.model_name="qilv-all"
        return self.model_name
 #取得诗歌模式（藏头诗或者一字诗）   
    def get_n2(self):
        self.ui_1.ui.select_5.clicked.connect(self.set_n21) 
        self.ui_1.ui.select_6.clicked.connect(self.set_n22) 
    def set_n21(self):
        self.model=1#藏头诗  
        return self.model
    def set_n22(self):
        self.model=2#一字诗
        return self.model
 #取得一字诗和藏头诗的开头字   
    def get_open(self):
        #输入按下回车或返回后开始执行作诗函数，按下不满意同上
        self.ui_2.ui.Number_2.returnPressed.connect(self.set_open)
        self.ui_2.ui.Button_3.clicked.connect(self.set_open)     
    def set_open(self):
        #取得openword，并取得最后的诗歌，在two和three窗口的文字输出栏输出
        openword=self.ui_2.ui.Number_2.text()
        compose_fine=self.compose_ex(self.model_name,self.model,openword)
        self.ui_2.ui.Number_3.setText(compose_fine)
        self.ui_3.ui.Nember_4.setText(compose_fine) 
#调用函数作诗         
    def compose_ex(self,model_name, model, openword):
       
        self.model_name=model_name
        self.model=model
        self.corpus_file=openword
        #model_dir，corpus_file，substr_len分别是模型，语料集和单句的字数
        model_dir = './model/%s' % model_name
        corpus_file = './data/%s.txt' % model_name
        substr_len = 5 if model_name.startswith('wu') else 7 if model_name.startswith('qi') else 0
#对绝句和律诗以及不同的字数和作诗形式设置模型        
        if 'jue' in model_name:
            #一字诗模型
            if  self.model==2:
                start=openword
                pattern = [
                  start+"xxxx", "xxxxx", 
                  "xxxxx", "xxxxx"
                ]
            #藏头诗模型
            elif  self.model==1:
                start=openword
                pattern = [
                  start[0]+"xxxx", start[1]+"xxxx", 
                  start[2]+"xxxx", start[3]+"xxxx"
                ]
            #一字诗模型   
        else:
            if  self.model==2:
                start=openword
                pattern = [
                  start+"xxxx", "xxxxx", 
                  "xxxxx", "xxxxx",
                  "xxxxx","xxxxx",
                  "xxxxx","xxxxx"
                ]
            #藏头诗模型
            elif  self.model==1:
                start=openword
                pattern = [
                  start[0]+"xxxx", start[1]+"xxxx", 
                  start[2]+"xxxx", start[3]+"xxxx",
                  start[4]+"xxxx", start[5]+"xxxx",
                  start[6]+"xxxx", start[7]+"xxxx"
                ]
            
        #在模型里填入文字               
        for i, p in enumerate(pattern): pattern[i] = p.ljust(substr_len, 'x')
        with closing(
            compose.Composer(model_name = self.model_name, model_dir = model_dir, corpus_file = corpus_file, substr_len=substr_len)
        ) as comp:
            os.system('cls')
            poem = comp.compose(pattern)
        compose_fine="" 
        #设置标点符号
        if 'jue' in model_name:
            str_1='，'.join([poem[0],poem[1]]) 
            str_2='，'.join([poem[2],poem[3]])  
            compose_fine=str_1+'。\n'+str_2+'。' 
        else:
            str_1='，'.join([poem[0],poem[1]]) 
            str_2='，'.join([poem[2],poem[3]]) 
            str_3='，'.join([poem[4],poem[5]]) 
            str_4='，'.join([poem[6],poem[7]]) 
            compose_fine=str_1+'。\n'+str_2+'。\n'+str_3+'。\n'+str_4+'。' 
        #调用评价系统来评价所作的诗
        comment1=Rater(model_name, substr_len).rate(poem)
        self.ui_2.ui.Number_5.setText(comment1)  
        return compose_fine


if __name__ == "__main__":
    #创建QApplication,如果已存在不重复创建（避免二次运行报错）
    app=QApplication.instance();
    if app is None:  
      app = QApplication(sys.argv)
    ui_1 =mainwindow()          
    ui_0 =include()    
    ui_2 =two()
    ui_3 =three()
    func=All(ui_0=ui_0,ui_1=ui_1,ui_2=ui_2,ui_3=ui_3)
    func.get_name()    
    func.get_open()
    sys.exit(app.exec_())
