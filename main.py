# 샘플 Python 스크립트입니다.

# Shift+F10을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.
import DBManager
import wordbook

import pyttsx3

from gtts import gTTS
from playsound import playsound

menustr='''
0. exit
1. Test
2. Add
3. DB Manage
4. Read CSV
5. Read CSV (Target)
reset 

'''

db = DBManager.DBManager("test.db")

while True:
    print(menustr)
    ip = input("->")

    if ip =='1':
        db.exam()
    elif ip =='2':
        eng = input("eng->")
        kr = input("kr->")
        word = wordbook.Word(eng, kr)
        db.addWord(word)
    elif ip =='3':
        target = input("target->")
        db.print(target)
    elif ip=='4':
        print("오늘날 파일 읽음")
        db.readFile()
    elif ip=='5':
        path = input('target File->')
        try:
            with open(path) as f:
                wordlist = db.csv2wordList(f, "")
                for word in wordlist:
                    db.addWord(word)

        except:
            print(path+" 파일 읽기 실패.")



    elif ip =='reset':
        db.reset()
    elif ip =='exit' or '0':
        break

