import datetime
import os
import sqlite3
import re
from wordbook import *
class DBManager:
    '''
    단어 추가 하기 (csv 읽기) -> 문제 추가 하기
    문제 풀기 -> 문제 생성 -> 결과 반영
    '''
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.wordBook = WordBookDB(self.conn, self.cursor)
        self.problem = ProblemDB(self.conn, self.cursor)
        self.ansList = AnsListDB(self.conn, self.cursor)

    def close(self):
        self.conn.close()

    def print(self, target):
        sql = f'SELECT * FROM "{target}";'
        for p in self.cursor.execute(sql).fetchall():
            print(p)

    def addWord(self):
        time = str(datetime.datetime.now().date())
        wordList = self.csv2wordList(open('prob/'+time+'.csv'), None)

        for word in wordList:
            self.problem.addWord(word.eng)


    def exam(self):
        time = str(datetime.datetime.now().date())
        englist = self.problem.getEngList(time)
        random.shuffle(englist)
        wordlist = []
        for eng in englist:
            word = self.wordBook.getWord(eng)
            word.ansRecord = self.ansList.getAnsList(eng)
            wordlist.append( word )

        #앞으로 구현 할 것
        problem = Problem(wordlist, time, self.wordBook.makeWordBook())
        problem.exam()
        self.finish()










    def readFile(self): #csv 읽기
        time = str(datetime.datetime.now().date())
        for day in DayState.listName:
            if os.path.isfile(day+time+".csv"): #오늘날 볼 문제지가 있다면
                file = open(day+"/"+time+".csv") #읽기
                wordlist = self.csv2wordList(file, day) #단어 리스트 생성
                for word in wordlist:
                    self.wordBook.addWord(word)

    #readFile로 호출됨
    def csv2wordList(self, file, day):
        '''
        해당 csv 파일을 읽어 단어에 추가
        :param File file, str day:
        :return: Word[] wordList
        '''
        csv = pandas.read_csv(file, names=["eng", "kor"])
        wordList = []
        for i in range(len(csv)):
            df = csv.iloc[i]
            wordList.append(Word(df[0], df[1], day))
        return wordList


class WordBookDB:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def makeWordBook(self):
        '''
        모든 단어를 담은 단어 리스트 출력 (문제를 출제시 유용하게 사용)
        :return wordlist : Word(eng, kor, state)[]
        '''
        sql = "Select * From WordBook"
        wordlist = []
        for row in self.cursor.execute(sql).fetchone():
            eng = row[0]
            kor = row[1]
            state = row[2]
            wordlist.append(Word(eng, kor, state))
        return wordlist

    def getWord(self, eng: str):
        '''
        eng 검색하여 word(eng, kor, state) 생성하여 반환
        :param str eng:
        :return Word(eng, kor, state):
        '''
        sql = f'SELECT * from WordBook where eng = "{eng}";'
        for c in self.cursor.execute(sql).fetchall():
            word = Word(c[0], c[1], c[2])
        return word

    #모르는 단어 추가 혹은 의미 추가
    def addWord(self, word : Word):
        '''
        단어 추가, 갱신
        :param word:
        :return bool: update = 1, insert = 0
        '''
        sql = 'SELECT * FROM "WordBook" where eng = "' + word.eng + '";'
        result = self.cursor.execute(sql).fetchone()
        if result: #kr 뜻 추가 state는 0으로 리셋
            originWord = Word(eng = result[0], kor = result[1])
            word.addAns(originWord.kor) #최신 갱신된 의미가 앞으로
            sql = f'UPDATE "WordBook" SET kor = "{originWord.kor}" , state = 0 where eng is "{originWord.eng}";'
            self.cursor.execute(sql)
            self.conn.commit()
            return True

        else: #없던 단어 추가
            sql = f'INSERT INTO "WordBook" (eng, kor) VALUES ("{word.eng}", "{word.kor}");'
            self.cursor.execute(sql)
            self.conn.commit()
            return False
        #self.addProblem(word) #아무튼 문제에 추가

def addWord(db):
    while True:
        eng = input("eng:")
        kor = input("kor:")
        word = Word(eng, kor)
        db.addWord(word)
        db.makeProblem()

class ProblemDB:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor


    def addWord(self, eng:str):
        '''
        단어 문제 테이블에 추가 (중복 방지) (eng, data)
        :param word:
        :return bool: 추가시 1, 중복시 0
        '''
        time = str(datetime.datetime.now().date())
        sql = f'SELECT * FROM "Problem" where eng = "{eng}" and date = "{time}";'
        result = self.cursor.execute(sql).fetchall()
        if result.__len__() == 0:
            sql = f'INSERT INTO "Problem" (eng, date) VALUES ("{eng}", "{time}");'
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        else:
            return False


    def getEngList(self, time : datetime.datetime):
        '''
        시간을 입력하여 해당 일의 모든 문제 단어(eng) 리스트 반환
        :param time:
        :return str[] engList:
        '''
        #time = str(datetime.datetime.now().date())
        sql = f'SELECT eng FROM "Problem" where date = "{time}";'
        engList = []
        for c in self.cursor.execute(sql).fetchall():
            engList.append(c[0])
        return engList
###
class AnsListDB:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    #DB에서 ansList 정보 가져오기 (self.wordList 기준 )
    def getAnsList(self, eng : str):
        '''
        eng를 입력하여 해당하는 ansList 반환
        :param word:
        :return:
        '''
        ansList = {}
        sql = f'SELECT  kor, count, correct from AnsList where eng = {eng};'
        for result in self.cursor.execute(sql).fetchall():
            ansList[result[0]] = [result[1], result[2]] #kor, count, correct
        return ansList
    """
    def setAns(self, word : Word):



    def makeProblem(self):
        for eng in self.getTodayWordList():
            self.setWordList(eng)

        for eng in self.wordList:
    """






def wordbookTest():
    db = DBManager("test.db")
    db.readFile()
    # db.makeWordBook()
    # addWord(db)
    # db.addWord(Word("lid", "병 측정하다222"))
    db.print("WordBook")
    db.close()

def probTest():
    db = DBManager("test.db")
    time = str(datetime.datetime.now().date())
    for eng in db.problem.getWordList(time):
        #db.makeQuiz(eng)

if __name__ == "__main__":
    wordbookTest()
    probTest()

