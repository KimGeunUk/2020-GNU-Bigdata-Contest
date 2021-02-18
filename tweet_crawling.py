import tweepy
from textblob import TextBlob
import csv
import json

class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):        
        #tweepy api를 사용하기위한 키입력
        consumer_key = 'yjI9PAAYqug2dwWlfj8aDntBh'
        consumer_secret = 'lc5BCBf2Rnd88Ns6AJU3YpuIEnVQUcyO1IL59qncbxRA3FHiaR'
        access_token = '1346751679958376450-ymqlUdnNdsCL6qQQNvp5s0FPxSVF4v'
        access_token_secret = 'IwVKiJryNh0gihXZ19HvdJmbnf0YpTQYdCGDNw3FPTVan'

        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit = True)

        #트윗 개수
        count = 0

        #검색 날짜(tweepy는 현재시간부터 일주일전까지만 트윗을 얻을 수 있다.)
        searchDate = '2021-02-01'

        #여러개를 검색하려면 띄어쓰기를 하면 된다(ex. 코로나 경제)
        keyword = input("검색 단어를 입력하세요 : ").split()
        #검색하고싶은 트윗 개수
        max_tweets = 25000

        #검색어 뒤에 since, geocode 를 이용해 기간, 지역을 정할 수 있다.
        self.tweets = tweepy.Cursor(api.search, q=keyword, lang="ko").items(max_tweets)

        for tweet in self.tweets:
            #필요 없는 특정 단어를 포함하면 리스트에 넣지 않도록 한다.
            if "http" not in tweet.text and "홍보" not in tweet.text and "RT" not in tweet.text and "노래방" not in tweet.text:
                self.tweetText.append(tweet.text)
                #조건에 해당하는 트윗 개수
                count += 1
        #트윗을 보기 편하게 JSON 파일로 정리한다.
        with open(searchDate+' tweet 경제.json','w',encoding='utf-8-sig') as w:
            w.write(json.dumps(self.tweetText,ensure_ascii=False,indent='\t'))

        #트윗을 보기 편하게 csv파일로 정리한다.
        #csv 파일 생성
        F = open('sample.csv', 'a', encoding='utf-8-sig', newline='')
        #csv 파일 쓰기
        W = csv.writer(F)
        W.writerow([searchDate, keyword, count])
        F.close()

        print("트위터 작성 날짜 : " + searchDate)
        print("트위터 검색 단어 : " + str(keyword))
        print("조건에 맞는 트윗 개수 : " + str(count) + "개")     

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
        