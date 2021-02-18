import _jpype
from googletrans import Translator
from textblob import TextBlob
from konlpy.tag import Okt
import json
import time
#import re

#감정분석은 영어로 하는것이 더 정확하기 때문에 구글 번역 api를 사용해 한국어 > 영어로 번역해준다
translator = Translator()

#분석의 정확도를 높이기위해 형태소(명사, 동사, 접속사, ..)를 나누어 정리한다.
okt = Okt()

#분석한 트윗의 개수를 구한다
count = 0

#분석 점수, 긍정 점수, 부정 점수, 중립 점수를 구한다
polarity = 0
positive = 0
negative = 0
neutral = 0

#JSON파일로 저장한 트윗을 불러온다
with open('2021-02-01 tweet 경제.json',encoding='utf-8-sig') as f:
    json_data = json.load(f)

#반복문을 사용해 점수를 구한다.
for sentence in json_data:
    count += 1

    #형태소를 분리한 후 필요없는 형태소를 정리하고 다시 한 문장으로 정리한다.
    s_okt = okt.morphs(sentence)
    str_okt = " ".join(s_okt)

    #str_okt = re.sub('@[\w_]+', '', str_okt)  
    # 정리한 문장을 영어로 번역한다.  
    translate_sentence = translator.translate(str_okt).text

    #번역을 한 후 감정분석을 통해 점수를 구한다.
    analysis = TextBlob(translate_sentence)

    polarity += analysis.sentiment.polarity
    # -1 ~ -0.3 : 부정적 트윗 / -0.3 ~ +0.3 : 중립적 트윗 / 0.3 ~ 1.0 : 긍정적 트윗
    if (analysis.sentiment.polarity == 0):
        neutral += 1
    elif (analysis.sentiment.polarity > 0.0 and analysis.sentiment.polarity <= 1):
        positive += 1    
    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
        negative += 1

    print(analysis.sentiment)
    #단시간에 너무 많은 일을 처리하면 각 api에서 ip를 막아버리는 것을 방지하기 위해 코드 사이에 시간을 준다.
    time.sleep(1)

print("총 " + str(count) + "개의 트윗을 검색했습니다.")
print("트윗 점수가 1에 가까울수록 긍정 -1에 가까울수록 부정")
print("트윗 점수 : " + str(polarity/count))
print("중립 점수(%) : " + str(format(100*float(neutral)/float(count), '.2f')))
print("긍정 점수(%) : " + str(format(100*float(positive)/float(count), '.2f')))
print("부정 점수(%) : " + str(format(100*float(negative)/float(count), '.2f')))

