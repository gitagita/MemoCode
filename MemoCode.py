'''
프로젝트 명: MemoCode
설명: 메모장의 강점을 살리면서 개발자의 편의성에 초점을 맞춘 프로그램이다.
버전: 1.0
'''
'''
main 브랜치
'''

from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import os
from tkinter.filedialog import *
from datetime import datetime
from urllib.parse import quote_plus
import webbrowser
import textwrap

es = ""  #특정 문자열 저장(편집 메뉴에서 문자열 복사, 잘라내기, 붙여넣기로 사용)
filepath = None  #파일 경로
index = 0   #표에서 행 삽입시 index 번호 순차 증가
listvalue = []  #표에 삽입한 데이터를 담는 리스트

#파일 메뉴

#새로운 파일 열기
def newFile():
    top.title("제목없음- MemoCode")
    global filepath
    filepath = None 
    text.delete(1.0,END)

#파일 열기
def openFile():
    global filepath
    filepath = askopenfilename(title = "파일 선택", filetypes = (("텍스트 파일", "*.txt"),("모든 파일", "*.*")))
    #취소를 누른 경우
    if filepath == '':
        return
    top.title(os.path.basename(filepath) + " - MemoCode")
    text.delete(1.0, END)
    f = open(filepath,"r")
    text.insert(1.0,f.read())
    f.close()
    
#다른이름으로 파일 저장
def saveFileDef():
    global filepath
    filepath = asksaveasfile(mode = "w", defaultextension=".txt")
    #취소를 누른 경우
    if filepath is None:
        return
    ts = str(text.get(1.0, END))
    filepath.write(ts)
    filepath.close()

#원본 파일에 저장
def saveFile():
    global filepath
    #원본 파일이 없는 경우
    if filepath is None:
        return saveFileDef()    #파일 경로가 없으므로 다른 이름으로 저장되도록 함
    f = open(filepath,"w")
    print("f: ", f)
    ts = str(text.get(1.0, END))
    f.write(ts)
    f.close()
    
    
    
#편집 메뉴

#드래그한 부분의 내용 잘라내기
def cut():
    global es
    es = text.get(SEL_FIRST, SEL_LAST)
    text.delete(SEL_FIRST, SEL_LAST)

#드래그한 부분의 내용 복사
def copy():
    global es
    es = text.get(SEL_FIRST, SEL_LAST)

#내용 붙여넣기
def paste():
    global es
    text.insert(INSERT, es)

#드래그한 부분의 내용 삭제
def delete():
    text.delete(SEL_FIRST, SEL_LAST)
    
#실행 취소 #미완성
def back():
    text.edit_undo()
    
#내용을 찾고 찾은 내용을 모두 빨간 색으로 표시
def findword(target):
    tg = str(target.get())
    text.tag_remove('match','1.0',END)
    if tg:
        start_pos = '1.0'
        while True:
            start_pos = text.search(tg, start_pos, stopindex=END)
            if(not start_pos):
                break
            end_pos = f'{start_pos}+{len(tg)}c'
            text.tag_add('match',start_pos,end_pos)
            start_pos=end_pos
            text.tag_config('match',foreground='red',background='')
    else:
        messagebox.showinfo("알림", "찾을 내용을 입력하세요.")

#빨간 색 글씨 취소(찾은 내용 취소)
def celfind():
    text.tag_remove('match','1.0',END)
    
#내용을 찾는 입력 창, findword함수 호
def search():
    searchtk = Tk()
    searchtk.title("찾기")
    searchtk.geometry("400x200")
    label = Label(searchtk, text="찾을 내용")
    label.grid(row=0, column=0)
    target = Entry(searchtk)
    target.grid(row=0, column=1)
    search_button = Button(searchtk, text="찾기", width=10, command=lambda:findword(target))
    search_button.grid(row=0, column=2)
    cancel_button = Button(searchtk, text="취소", width=10, command=celfind)
    cancel_button.grid(row=0, column=3)
    
#바꿀 글자를 찾아 모두 바꾸기
def changeword(target1, target2):
    ts = str(text.get(1.0, END))
    tg1 = str(target1.get())
    tg2 = str(target2.get())

    s = ts.replace(tg1, tg2)
    if tg1 == "":
        messagebox.showinfo("알림", "찾을 내용을 입력하세요.")
    if tg2 == "":
        messagebox.showinfo("알림", "바꿀 내용을 입력하세요.")
    print(s)
    text.delete(1.0, END)
    text.insert(1.0, s)
    
#찾아 바꿀 내용 입력 창, changeword함수 호출
def change():
    changetk = Tk()
    changetk.title("바꾸기")
    changetk.geometry("400x200")
    label1 = Label(changetk, text="찾을 내용")
    label2 = Label(changetk, text="바꿀 내용")
    label1.grid(row=0, column=0)
    label2.grid(row=1, column=0)
    target1 = Entry(changetk)
    target2 = Entry(changetk)
    target1.grid(row=0, column=1)
    target2.grid(row=1, column=1)
    button = Button(changetk, text="바꾸기", width=10, command=lambda:changeword(target1,target2))
    button.grid(row=0, column=2)

#드래그한 부분을 google에 검색
def google():
    global es
    es = text.get(SEL_FIRST, SEL_LAST)
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl + quote_plus(es)
    webbrowser.open(url)

#날짜와 시간 삽입
def insertdate():
    now = datetime.now()
    dtString = now.strftime("%d/%m/%Y %H:%M:%S")
    text.insert(INSERT, dtString)



#서식 메뉴

#드래그한 부분 글꼴 변경
def fontchange():
    label = text.get(SEL_FIRST, SEL_LAST)
    font = tkFont.Font(family="MS Sans Serif", size=10)
    start_pos = SEL_FIRST
    end_pos = f'{start_pos}+{len(label)}c'
    text.tag_add('font', start_pos, end_pos)
    text.tag_config('font', font=font)

#해당 기호 삽입
def insertsign(n):
    if n==0:
        text.insert(INSERT, "※")
    elif n==1:
        text.insert(INSERT, "★")
    elif n==2:
        text.insert(INSERT, "【")
    elif n==3:
        text.insert(INSERT, "】")
    else:
        text.insert(INSERT, "√")

#기호 삽입 입력 창
def signs():
    signstk = Tk()
    signstk.title("기호")
    signstk.geometry("400x100")
    button = Button(signstk, text="※", width=10, command=lambda:insertsign(0))
    button.grid(row=0, column=0)
    button = Button(signstk, text="★", width=10, command=lambda:insertsign(1))
    button.grid(row=0, column=1)
    button = Button(signstk, text="【", width=10, command=lambda:insertsign(2))
    button.grid(row=0, column=2)
    button = Button(signstk, text="】", width=10, command=lambda:insertsign(3))
    button.grid(row=0, column=3)
    button = Button(signstk, text="√", width=10, command=lambda:insertsign(4))
    button.grid(row=0, column=4)

#드래그한 부분의 글자를 초록색으로 변환
def green(label):
    font = tkFont.Font(size=10, slant="italic")
    start_pos = SEL_FIRST
    end_pos = f'{start_pos}+{len(label)}c'
    text.tag_add('comment', start_pos, end_pos)
    text.tag_config('comment', font=font, foreground="green")
    
#해당 주석 삽입(드래그 한 경우와 안 한 경우 모두 실행 됨)
def insertcomment(n):
    if n==0:
        try:
            label = text.get(SEL_FIRST, SEL_LAST)
        except:
            text.insert(INSERT, "/* */")
        else:
            start_pos = SEL_FIRST
            end_pos = f'{start_pos}+{len(label)}c' 
            text.insert(start_pos, "/* ")
            text.insert(end_pos, " */")
            green(label)
    elif n==1:
        try:
            label = text.get(SEL_FIRST, SEL_LAST)
        except:
            text.insert(INSERT, "#")
        else:
            text.insert(SEL_FIRST, "#")
            green(label)
    elif n==2:
        try:
            label = text.get(SEL_FIRST, SEL_LAST)
        except:
            text.insert(INSERT, "//")
        else:
            text.insert(SEL_FIRST, "//")
            green(label)
    elif n==3:
        try:
            label = text.get(SEL_FIRST, SEL_LAST)
        except:
            text.insert(INSERT, "<!-- -->")
        else:
            start_pos = SEL_FIRST
            end_pos = f'{start_pos}+{len(label)}c' 
            text.insert(start_pos, "<!-- ")
            text.insert(end_pos, " -->")
            green(label)
    else:
        try:
            label = text.get(SEL_FIRST, SEL_LAST)
        except:
            text.insert(INSERT, "'''\n\n'''")
        else:
            start_pos = SEL_FIRST
            end_pos = f'{start_pos}+{len(label)}c' 
            text.insert(start_pos, "'''\n")
            text.insert(end_pos, "\n'''")
            green(label)
            
    
    
    
#주석 삽입 입력 창
def comments():
    commentstk = Tk()
    commentstk.title("주석")
    commentstk.geometry("400x100")
    button = Button(commentstk, text="/* */", width=10, command=lambda:insertcomment(0))
    button.grid(row=0, column=0)
    button = Button(commentstk, text="#", width=10, command=lambda:insertcomment(1))
    button.grid(row=0, column=1)
    button = Button(commentstk, text="//", width=10, command=lambda:insertcomment(2))
    button.grid(row=0, column=2)
    button = Button(commentstk, text="<!-- -->", width=10, command=lambda:insertcomment(3))
    button.grid(row=0, column=3)
    button = Button(commentstk, text="''' '''", width=10, command=lambda:insertcomment(4))
    button.grid(row=0, column=4)

#코드 박스 생성
def codebox():
    try:
        label = text.get(SEL_FIRST, SEL_LAST)
    except:
        messagebox.showinfo("알림", "코드를 드래그하세요")
    else:
        start_pos = SEL_FIRST
        end_pos = f'{start_pos}+{len(label)}c'
        text.tag_add('code', start_pos, end_pos)
        text.tag_config('code', foreground="black", background="lightsteelblue")

#표에 열 삽입
def insertcol(col, treeview, coltext):
    coltext = col.get()
    collist = str(coltext).split(',')

    treeview.column("#0", width=50, anchor="center")
    treeview.heading("#0", text="index", anchor="center")
    
    for i in range(len(collist)):
        treeview.column("#"+str(i+1), width=70, anchor="center")
        treeview.heading("#"+str(i+1), text=collist[i], anchor="center")
    
#표에 데이터 삽입
def insertrow(row, treeview):
    global index
    global listvalue
    rowtext = row.get()
    rowlist = str(rowtext).split(',')
    listvalue.append(rowlist)
    treeview.insert('', 'end', text=index, values=rowlist)
    index += 1
    
#표에서 선택한 행 삭제
def delrow(treeview):
    global listvalue
    selected_item = treeview.selection()[0]
    item = treeview.item(treeview.selection()[0])['text']
    listvalue.pop(item)
    listvalue.insert(item, "")
    treeview.delete(selected_item)

#만들어진 표의 내용을 텍스트에 출력
def inserttable(treeview, col):
    global listvalue
    coltext = col.get()
    collist = str(coltext).split(',')
    text.insert(INSERT, "    ".join(collist))
    text.insert(INSERT, "\n------------------------------\n")
    for value in listvalue:
        if value != "":
            text.insert(INSERT, "    ".join(value))
            text.insert(INSERT, "\n")
    
#표 삽입
def table():
    #표의 결과를 출력하는 창
    coltext = ["#0","#1","#2","#3","#4","#5","#6","#7","#8","#9"]
    commentstk2 = Tk()
    commentstk2.title("표 출력")
    commentstk2.geometry("400x300")
    button = Button(commentstk2, text="텍스트에 추가", width=10, command=lambda:inserttable(treeview, col))
    button.pack(side="top")
    button = Button(commentstk2, text="행 삭제", width=10, command=lambda:delrow(treeview))
    button.pack(side="top")
    treeview = ttk.Treeview(commentstk2, columns=coltext)
    treeview.pack(side="bottom")
    
    #표에 데이터를 입력하는 창
    commentstk = Tk()
    commentstk.title("표 만들기")
    commentstk.geometry("400x200")
    label1 = Label(commentstk, text="열 이름(구분자: ',')")
    label2 = Label(commentstk, text="내용(구분자: ',')")
    label1.grid(row=0, column=0)
    label2.grid(row=1, column=0)
    col = Entry(commentstk)
    row = Entry(commentstk)
    col.grid(row=0, column=1)
    row.grid(row=1, column=1)
    button = Button(commentstk, text="열 추가", width=10, command=lambda:insertcol(col,treeview,coltext))
    button.grid(row=0, column=2)
    button = Button(commentstk, text="한 행 추가", width=10, command=lambda:insertrow(row,treeview))
    button.grid(row=1, column=2)
    
#드래그한 부분의 모든 줄 들여쓰기(드래그 하지 않은 경우는 "    "삽입)
def indent():
    try:
        label = text.get(SEL_FIRST, SEL_LAST)
    except:
        text.insert(INSERT, "    ")
    else:
        line = textwrap.indent(label, "    ")
        text.insert(SEL_FIRST, line)
        text.delete(SEL_FIRST, SEL_LAST)

#드래그한 내용의 줄 맨 앞에 "●"문자 삽입
def listtext():
    try:
        label = text.get(SEL_FIRST, SEL_LAST)
    except:
        text.insert(INSERT, "●")
    else:
        line = textwrap.indent(label, "●")
        text.insert(SEL_FIRST, line)
        text.delete(SEL_FIRST, SEL_LAST)
   
#드래그한 내용에 줄 번호 추가
def listnumber():
    try:
        label = text.get(SEL_FIRST, SEL_LAST)
    except:
        text.insert(INSERT, "1. ")
    else:
        slist = label.split("\n")
        i = 1
        for s in slist:
            formats = str(i)+". "
            newlabel = formats + s + "\n"
            text.insert(SEL_FIRST, newlabel)
            i+=1
            
        text.delete(SEL_FIRST, SEL_LAST)


#코딩메뉴

#한줄씩 문장을 읽어들여 '\n'문자로 연결하기
def delEnter():
    texts = str(text.get(1.0, END))
    tList = texts.split('\n')
    vText = ''
    for t in tList:
        if t == '':
            break;
        vText += t+'\\n'
    text.delete(1.0, END)
    text.insert(INSERT, vText)
    
#'\'를 '\\'로 변환
def delWord():
    texts = str(text.get(1.0, END))
    texts = texts.replace('\\','\\\\')
    text.delete(1.0, END)
    text.insert(INSERT, texts)


#도움말 메뉴

#구글 이메일
def message():
    url = 'https://www.google.com/intl/ko/gmail/about/'
    webbrowser.open(url)
    messagebox.showinfo("의견보내기", "20190955@sungshin.ac.kr로 소중한 의견을 보내주세요.\n갑사합니다.")
    
#MemoCode 정보
def info():
    he = Toplevel(top)
    he.geometry("300x200")
    he.title("정보")
    lb = Label(he, text = "MemoCode\n 버전: 1.1\n 개발언어: python\n개발자의 편의성에 초점을 맞춘 메모장입니다.\n\n개발자 이메일: 20190955@sungshin.ac.kr")
    lb.pack()
    

top = Tk()
top.title("MemoCode")
top.geometry("500x500")


text = Text(top)
scrollbar = Scrollbar(text)
scrollbar.config(command = text.yview)
top.grid_rowconfigure(0, weight=1)
top.grid_columnconfigure(0, weight=1)
scrollbar.pack(side = RIGHT, fill = Y)
text.grid(sticky = N + E + S + W)


#파일 메뉴 생성
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="새로 만들기", accelerator ='Ctrl+N', command=newFile)
filemenu.add_command(label="열기", accelerator ='Ctrl+O', command=openFile)
filemenu.add_command(label="저장", accelerator ='Ctrl+S', command=saveFile)
filemenu.add_command(label="다른 이름으로 저장", accelerator ='Ctrl+Shift+S', command=saveFileDef)
filemenu.add_separator()
filemenu.add_command(label="끝내기", command=top.destroy)
menubar.add_cascade(label="파일", menu=filemenu)


#편집 메뉴 생성
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="잘라내기", accelerator ='Ctrl+X', command=cut)
editmenu.add_command(label="복사", accelerator ='Ctrl+C', command=copy)
editmenu.add_command(label="붙이기", accelerator ='Ctrl+V', command=paste)
editmenu.add_command(label="삭제", accelerator ='Del', command=delete)
editmenu.add_separator()
# =============================================================================
# editmenu.add_command(label="실행취소", command=back)
# editmenu.add_separator()
# =============================================================================
editmenu.add_command(label="찾기", accelerator ='Ctrl+F', command=search)
editmenu.add_command(label="바꾸기", accelerator ='Ctrl+H', command=change)
editmenu.add_command(label="검색", accelerator ='Ctrl+E', command=google)
editmenu.add_separator()
editmenu.add_command(label="날짜/시간", command=insertdate)
menubar.add_cascade(label="편집", menu=editmenu)


#서식 메뉴 생성
formmenu = Menu(menubar, tearoff=0)
formmenu.add_command(label="글꼴변경", command=fontchange)
formmenu.add_command(label="기호", command=signs)
formmenu.add_command(label="주석처리", command=comments)
formmenu.add_command(label="코드박스", command=codebox)
formmenu.add_separator()
formmenu.add_command(label="표 생성", command=table)
formmenu.add_separator()
formmenu.add_command(label="들여쓰기", command=indent)
formmenu.add_command(label="나열하기", command=listtext)
formmenu.add_command(label="줄 번호", command=listnumber)
menubar.add_cascade(label="서식", menu=formmenu)


#코딩 메뉴 생성
codemenu = Menu(menubar, tearoff=0)
codemenu.add_command(label="엔터를 문자로 변환", command=delEnter)
codemenu.add_separator()
codemenu.add_command(label="원기호 문자 추가", command=delWord)
menubar.add_cascade(label="코딩메뉴", menu=codemenu)


#도움말 메뉴 생성
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="의견보내기", command = message)
helpmenu.add_command(label="MemoCode 정보", command = info)
menubar.add_cascade(label="도움말", menu=helpmenu)

top.config(menu=menubar)

top.mainloop()

