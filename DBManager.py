import os
import sqlite3
import re
from wordbook import *
class DB:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
    def close(self):
        self.conn.close()

class WordBook(DB):
    #굳이 필요하지 않을 수도 ?

    def makeWordBook(self):
        sql = "Select * From WordBook"
        c = self.cursor
        for row in self.cursor.execute(sql):
            eng = row[0]
            kor = row[1]
            state = row[2]

    def addWord(self, word : Word):
        sql = 'SELECT * FROM "WordBook" where eng = "' + word.eng + '";'
        result = self.cursor.execute(sql).fetchone()
        if result: #kr 뜻 추가 state는 0으로 리셋
            originWord = Word(eng = result[0], kor = result[1])
            word.addAns(originWord.kor) #최신 갱신된 의미가 앞으로
            sql = f'UPDATE "WordBook" SET kor = "{originWord.kor}" , state = 0 where eng is "{originWord.eng}";'
            self.cursor.execute(sql)
            self.conn.commit()

        else: #없던 단어 추가
            sql = f'INSERT INTO "WordBook" (eng, kor) VALUES ("{word.eng}", "{word.kor}");'
            self.cursor.execute(sql)
            self.conn.commit()

        self.addProblem(word) #아무튼 문제에 추가

    def addProblem(self, word : Word):
        time = str(datetime.datetime.now().date())
        sql = f'SELECT * FROM "Problem" where eng = "{word.eng}" and date = "{time}";'
        result = self.cursor.execute(sql).fetchall()
        if result.__len__() == 0:
            sql = f'INSERT INTO "Problem" (eng, date) VALUES ("{word.eng}", "{time}");'
            self.cursor.execute(sql)
            self.conn.commit()

    def print(self, target):
        sql = f'SELECT * FROM "{target}";'
        for p in self.cursor.execute(sql).fetchall():
            print(p)

    def readFile(self): #csv 읽기
        time = str(datetime.datetime.now().date())
        for day in DayState.listName:
            if os.path.isfile(day+time+".csv"): #오늘날 볼 문제지가 있다면
                file = open(day+"/"+time+".csv") #읽기
                wordList = self.csv2wordList(file, day) #단어 리스트 생성
                for word in wordList:
                    self.addWord(word)


    #해당 파일을 읽어 단어에 추가
    def csv2wordList(self, file , day):
        csv = pandas.read_csv(file, names=["eng", "kor"])
        wordList = []
        for i in range(len(csv)):
            df = csv.iloc[i]
            wordList.append(Word(df[0], df[1], day))
        return wordList

def addWord(db : DB):
    while True:
        eng = input("eng:")
        kor = input("kor:")
        word = Word(eng, kor)
        db.addWord(word)
        db.makeProblem()

class Problem(DB):
    def __init__(self, path):
        DB.__init__(self, path)
        self.wordList = []

    def getTodayWordList(self):
        time = str(datetime.datetime.now().date())
        sql = f'SELECT eng FROM "Problem" where date = "{time}";'
        wordList = []
        for c in self.cursor.execute(sql).fetchall():
            wordList.append(c[0])
        return wordList

    def setWordList(self, eng : str):
        sql = f'SELECT * from WordBook where eng = "{eng}";'
        for c in self.cursor.execute(sql).fetchall():
            word = Word(c[0], c[1], c[2])
            self.wordList.append(word)

    #DB에서 ansList 정보 가져오기 (self.wordList 기준 )
    def getAnsList(self):
        for word in self.wordList:
            sql = f'SELECT  kor, count, correct from AnsList where eng = {word.eng};'
            for result in self.cursor.execute(sql).fetchall():
                print(result)

    def setAns(self, word : Word):
        


    def makeProblem(self):
        for eng in self.getTodayWordList():
            self.setWordList(eng)

        for eng in self.wordList:







def wordbookTest():
    db = WordBook("test.db")
    db.readFile()
    # db.makeWordBook()
    # addWord(db)
    # db.addWord(Word("lid", "병 측정하다222"))
    db.print("WordBook")
    db.close()

def probTest():
    db = Problem("test.db")
    for eng in db.getTodayWordList():
        db.makeQuiz(eng)

if __name__ == "__main__":
    wordbookTest()
    probTest()

