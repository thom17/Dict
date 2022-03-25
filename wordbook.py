import os.path
import random
import datetime
import pandas

class Wordbook:
    num = 0
    ok = 0
    def __init__(self, wordList : [], wordBook : []):
        self.wordList = wordList
        self.wordBook = wordBook

    def addWord(self, word):
        self.wordList.append(word)
    def makeProblem(self):
        random.shuffle( self.wordList )
        return Problem(self.wordList)

    def add(self, eng, kr):
        word = self.find(eng, kr)
        if word is None:
            self.wordList.append(Word(eng, kr))
        elif not word.ansList.__contains__(kr):
            word.ansList.append(kr)

    def find(self, eng):
        for word in self.wordList:
            if word.eng == eng:
                return word
        return None


class Word:
    def __init__(self, eng, kor, state = 0):
        self.eng = eng
        self.ansList = []
        self.ansRecord = {}  # { [ kor ] = [ count : int  , isRight : boolean] }
        self.state = state
        self.addAns(kor)
    def addAns(self, kor : str):
        spList = kor.split(',')
        for i in range(len(spList)):
            newAns = spList[i].lstrip()
            if self.ansList.__contains__(newAns):
                continue
            else:
                self.ansList.append(newAns)
                self.ansRecord[newAns] = [0, True]

        self.kor = ', '.join(self.ansList)

    def addRecord(self, str):
        value = self.ansRecord.get(str)
        if value == None:
            self.ansRecord[str] = 1
        else:
            self.ansRecord[str] += 1
        print("%s : %d" %(str, self.ansRecord[str]))

    def makeQuiz(self, wordbook : [], radiosize = 10):
        checklist = []

        while checklist.__len__() < radiosize:
            word = random.choice(wordbook)
            kor = random.choice(word.ansList)
            if self.ansList.__contains__(kor) or checklist.__contains__(kor):
                continue
            else:
                checklist.append(kor)

        anslist = []
        while anslist.__len__() < self.ansList.__len__():
            ans = random.randrange(0, self.ansList.__len__())
            if anslist.__contains__(ans):
                continue
            else:
                anslist.append(ans)

        index = 0
        for ans in anslist:
            checklist[ans] = self.ansList[index]
            index += 1

        tp = (anslist, checklist)

        return tp


class DayState: #요놈을 폴더에서 읽을때 초기화 하여 경로 지정하자/
    list = (1, 3, 7, 30)
    listName = ("prob/", "prob/3day/", "prob/7day", "prob/30day")

    def __init__(self, index):
        self.index = index

    def getDay(self):
        return DayState.list[self.index]


class Problem:
    '''
    시험 단어, 주관식 보기, 음성 출력기능 등 문제 관련 데이터 클래스
    '''
    def __init__(self, wordList : [] , time , wordBook : [] ):
        self.time = time
        #self.file
        #self.path = "prob/"+self.time
        self.wordList = wordList
        self.wordBook = wordBook
        self.quizBook = self.makeQuizBook()

    def makeQuizBook(self):
        quizBook = {}
        for word in self.wordList:
           quizBook[word.eng] = word.makeQuiz(self.wordBook)
        return quizBook

    def exam(self):
        self.printQuizBook()

    def printQuizBook(self):
        for quiz in self.quizBook:
            print(quiz)

if __name__ == "__main__":
    pb = Problem(Wordbook([]))
    #pb.readFile()

    word = Word("4", "원의미")
    word.addAns("이런 의미, 저런 의미,새로운 의미,의미")
    print(word.kor)