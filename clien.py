#jinsyu.com@gmail.com
#-*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
import webbrowser
import os
#articleList 변수 리스트로 선언
articleList=[]

#데이터폴더 초기화
dataPath = './data'
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)
else:
    import shutil
    shutil.rmtree('./data')
    os.makedirs(dataPath)
#with open('./clien.html', 'w', encoding='utf-8') as x:
    #pass

#함수선언 1인자 게시판이름, 2인자 댓글검색갯수
def BestArticleClien(boardName, replyNumberHope):
    url = 'http://www.clien.net/cs2/bbs/board.php?bo_table=' + boardName
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    for tr in soup.find_all('tr', {'class' : 'mytr'}):
        try:
            #댓글 갯수 검색 [] 제외
            replyNumber = tr.find('span').string[1:-1]
        except:
            pass

        #숫자인지 검색
        if replyNumber.isdigit():
            #설정된 댓글검색갯수보다 댓글갯수가 많을경우
            if int(replyNumber) > replyNumberHope:
                articles = tr.find('td', {'class' : 'post_subject'})
                #링크 상대경로를 절대주소로 변환
                link = articles.a.get('href')
                link = link.replace('..', 'http://www.clien.net/cs2')
                #정규식으로 게시물 번호 검색
                linkNumber = re.findall(r'(\d{3,})+', link)[0]
                #글제목 = 링크에 둘러싸인 문자열
                title = articles.a.string
                #게시물 조회후 실제 화면에 보일 변수 <링크> 게시판이름 게시물제목 [댓글갯수] 원본보기 <링크>
                article = '<a href=./data/' + boardName + linkNumber + '.html>' + title + '</a> [' + replyNumber + ']' + '<a href=' + link + '> ' + '원본' + '</a>'

                with open('clien.html', 'r', encoding='utf-8') as r:
                    #중복게시물 조회를 위하여 clien.html 파일 읽기
                    bestClienViewed = r.read()
                #게시물 번호로 중복게시물이 있는지 조회
                if not re.search(linkNumber, bestClienViewed):
                    #각 게시물별 게시판이름 붙이기
                    if boardName == 'park':
                        boardTitle = ('모공 ')
                    if boardName == 'lecture':
                        boardTitle = ('팁과강의 ')
                    if boardName == 'kin':
                        boardTitle = ('아질게 ')
                    if boardName == 'use':
                        boardTitle = ('사용기게시판 ')
                    if boardName == 'cm_mac':
                        boardTitle = ('맥당 ')
                    #변수 글로벌 선언
                    global articleList
                    #파싱 정보를 articleList라는 리스트에 담아두기
                    articleList.append('<div style="display:none;">' + linkNumber + '</div>' + ' ' + boardTitle + article + '<br>')

                    #조회된 게시물의 본문을 /data/폴더 안에 게시판이름+게시물번호로 저장
                    with open('./data/' + boardName + linkNumber + '.html', 'w', encoding='utf-8') as w:
                        url2 = 'http://www.clien.net/cs2/bbs/board.php?bo_table=' + boardName + '&wr_id=' + linkNumber
                        html2 = urlopen(url2)
                        soup2 = BeautifulSoup(html2, 'html.parser')
                        #게시물 본문검색
                        for body in soup2.find_all('span', {'id' : 'writeContents'}):
                            body = str(body).strip()
                            #게시물 본문 한글깨짐방지 및 클리앙css적용
                            w.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> ')
                            w.write('<link href="../clien.css" rel="stylesheet" type="text/css">')
                            w.write('<meta name="viewport" content="width=device-width">')
                            #게시물 타이틀 삽입
                            w.write(title)
                            w.write('<hr>')
                            #게시자 시그니쳐 및 이미지 파일 경로 수정
                            body = body.replace('<img alt="signature" src="','<img alt="signature" src="http://clien.net')
                            body = body.replace('../skin','http://clien.net/cs2/skin')
                            #본문에 삽입된 이미지 링크 검색
                            image = soup2.find('img', {'name' : 'target_resize_image[]'})
                            #삽입된 이미지가 없을경우 무시하고 있을경우 주소 얻어오기
                            if image:
                                imageSrc = str(image.get('src'))
                                w.write('<img src=' + imageSrc + '><br>')
                            else:
                                pass

                            w.write(body)
                            w.write('<hr>')
                            #본문에 달린 댓글들 검색
                            for replies in soup2.find_all('div', {'class' : 'reply_right'}):
                                #댓글에 달린 멤버이름 이미지 및 댓글 아이콘 경로 수정
                                comment = str(replies).replace('/cs2','http://clien.net/cs2')
                                comment = comment.replace('../skin','http://clien.net/cs2/skin')
                                #댓글의 본문만 검색
                                commentContent = str(replies.find('div', {'class' : 'reply_content'}))
                                #댓글의 유저이름 검색
                                userId = str(replies.find('li',{'class' : 'user_id'}))
                                #댓글에 달린 이미지 및 댓글 아이콘 경로수정, 리스트 태그 삭제
                                userId = userId.replace('/cs2','http://clien.net/cs2')
                                userId = userId.replace('../skin','http://clien.net/cs2/skin')
                                userId = userId.replace('<li class="user_id">', '')
                                userId = userId.replace('</li>', '')
                                #댓글 유저 이름 + 댓글 본문삽입
                                w.write(userId)
                                w.write(commentContent)
                                w.write('<hr>')

    #clien.html 새로 열기 articleList 라는 리스트에 담긴 게시물들을 내림차순 정렬하여 최신글이 앞으로 오도록
    with open('clien.html', 'w', encoding='utf-8') as t:
        t.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> ')
        t.write('<link href="clien.css" rel="stylesheet" type="text/css">')
        t.write('<meta name="viewport" content="width=device-width">')
        t.write('\n'.join(map(str, sorted(articleList, reverse=True))))
#반복
while True:
    BestArticleClien('park', 5)
    #BestArticleClien('use', 30)
    #BestArticleClien('lecture', 10)
    #BestArticleClien('cm_mac', 10)

    #인터넷 브라우저 띄우기
    #clienHtml = 'file:///Volumes/XXX/clien.html'
    #webbrowser.open_new(clienHtml)

    #해당 초만큼 딜레이
    time.sleep(600)
