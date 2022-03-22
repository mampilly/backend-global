from app.core.database.db import db_select
import json
from datetime import datetime


def setDate(date):
    if date == None:
        todays_date = datetime.today()
        year = todays_date.year
        month = todays_date.month
        if len(str(month)) == 1:
            month = '0' + str(month)

    else:
        now = date
        year = now.strftime("%Y")
        month = now.strftime("%m")
        if len(str(month)) == 1:
            month = '0' + str(month)

    date = str(year) + str(month)
    return date


class BusinessMetricService:

    def get_bsi_score(self, params):

        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT bf.bsi_score,date(bf.created_date) as date FROM bsi_facts bf,(SELECT bf.company_id, MAX(created_date) AS dt FROM bsi_facts bf WHERE bf.company_id = :business_id GROUP BY date_format(bf.created_date,'%b %Y')) MAX_DATE WHERE MAX_DATE.company_id = bf.company_id AND MAX_DATE.dt = bf.created_date AND date_format(bf.created_date,'%Y%m')=:date ORDER BY date_format(bf.created_date,'%Y%m')
            '''
        bsi_score = db_select(query, params)
        return bsi_score

    def get_watch_level(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT value FROM app_settings WHERE name="bsi_range" AND account_id = :account_id ; 
            '''
        bsi_range = db_select(query, params)

        for row in bsi_range:
            bsi_range = dict(row)
        bsi_range = json.loads(bsi_range['value'])

        query = '''
                SELECT bf.bsi_score,bf.created_date FROM bsi_facts bf,(SELECT bf.company_id, MAX(created_date) AS dt FROM bsi_facts bf WHERE bf.company_id = :business_id GROUP BY date_format(bf.created_date,'%b %Y')) MAX_DATE WHERE MAX_DATE.company_id = bf.company_id AND MAX_DATE.dt = bf.created_date AND date_format(bf.created_date,'%Y%m')= :date ORDER BY date_format(bf.created_date,'%Y%m')
            '''
        bsi_score = db_select(query, params)
        watch_level = None
        if(len(bsi_score)):
            bsi_score = bsi_score[0][0]
            risk_score = float(bsi_score)
            if(risk_score == 0):
                watch_level = 'N/A'
            else:
                for element in bsi_range:
                    if(risk_score >= element['min'] and risk_score <= element['max']):
                        watch_level = element['label'].lower()
        watch_level = {"watch_level": watch_level}
        return watch_level

    def get_credit_bureau_score(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT cbs.intelliscore, cbs.fsr_score, cbs.score_date, date_format(cbs.score_date,'%b %Y') AS formated_date 
                FROM credit_bureau_score cbs 
                WHERE business_id = :business_id AND date_format(cbs.score_date,'%Y%m') = :date 
            '''
        bureau_score = db_select(query, params)

        return bureau_score

    def get_recent_news(self, params):
        params['date'] = setDate(params['date'])
        query = '''
               SELECT bi.business_name, bni.news_url,bni.sentiment_score,bni.sentiment_label,bni.published_date  FROM business_news_info bni JOIN business_info bi ON bi.id = bni.business_id JOIN account_business_mapping abm ON bi.id = abm.business_id         
               WHERE abm.account_id=:account_id AND bi.is_active = 1 AND bni.title iS NOT NULL AND bni.sentiment_label='negative' AND bni.calculated_entity_relevence=1 AND entity_label='negative'        
               AND date_format(bni.published_date,'%Y%m')= :date ORDER BY bni.published_date DESC limit 6; 
            '''
        recent_news = db_select(query, params)

        return recent_news

    def get_top_news(self, params):
        query = '''
               SELECT bi.business_name, bni.news_url,bni.sentiment_score,bni.sentiment_label,bni.published_date  FROM business_news_info bni JOIN business_info bi ON bi.id = bni.business_id JOIN account_business_mapping abm ON bi.id = abm.business_id 
               WHERE abm.account_id=:account_id AND bi.is_active = 1 AND bni.title iS NOT NULL AND bni.sentiment_label='negative' AND bni.calculated_entity_relevence=1 AND entity_label='negative' 
               AND date(bni.published_date)>= date_sub(now(), interval 3 month) AND date(bni.published_date)<= date(now()) 
               ORDER BY bni.entity_score limit 6;
            '''
        top_news = db_select(query, params)
        return top_news

    def get_current_platform_index(self, params):
        params['business_id'] = params['business_id'] - 1000
        query = '''
               SELECT google_news_platform_index,twitter_platform_index,created_date as date FROM bsi_facts WHERE company_id = :business_id AND created_date = date(now()) ;
            '''

        platform_index = db_select(query, params)
        return platform_index

    def get_avg_sentiment(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                 SELECT date_format(published_date,'%b %Y') AS date, AVG(sentiment_score) AS sentiment_score FROM 
                 (SELECT published_date, entity_score AS sentiment_score, entity_label AS final_label FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')= :date 
                 UNION 
                 SELECT published_date, entity_score AS sentiment_score, entity_label AS final_label FROM business_tweet_info WHERE business_id = business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')= :date ORDER BY published_date ) AS res 
                 GROUP BY date_format(published_date,'%b %Y') ;
            '''

        avg_sentiment = db_select(query, params)
        return avg_sentiment

    def get_sentiment_distribution(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                  SELECT final_label AS sentiment_label,AVG(final_score) AS sentiment_score, COUNT(final_label) AS count, published_date as date FROM 
                    (
                    SELECT business_id, entity_label AS final_label, entity_score AS final_score, date_format(published_date,'%b %Y') as published_date
                    FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')=:date  
                    UNION 
                    SELECT business_id, entity_label AS final_label, entity_score AS final_score, date_format(published_date,'%b %Y') as published_date
                    FROM business_tweet_info WHERE business_id = :business_id  AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')=:date  
                    ) temp_table GROUP BY published_date, final_label, published_date;
            '''

        avg_sentiment = db_select(query, params)
        return avg_sentiment

    def get_entity_details(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''SELECT 'Public News Feeds' as platform, entities, published_date as date FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')=:date
                    UNION ALL 
                    SELECT 'Twitter' as platform, entities, published_date as date FROM business_tweet_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')=:date'''

        entity_details = db_select(query, params)
        result_obj = []

        for item in entity_details:
            result = {}
            entities = json.loads(item['entities'])
            result['entities'] = entities
            result['platform'] = item['platform']
            result['date'] = item['date']
            result_obj.append(result)

        return result_obj

    def get_public_perception(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT SUM(a.emotion='emotion_joy') as emotion_joy, SUM(a.emotion='emotion_anger') as emotion_anger,\
                SUM(a.emotion='emotion_disgust') as emotion_disgust, SUM(a.emotion='emotion_fear') as emotion_fear, SUM(a.emotion='emotion_sadness') as emotion_sadness FROM ((select id,\
                (case when emotion_disgust = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_disgust'\
                when emotion_sadness = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_sadness'\
                when emotion_anger = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_anger'\
                when emotion_joy = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_joy'\
                when emotion_fear = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_fear'\
                end) as emotion from business_news_info WHERE\
                business_id = :business_id and date_format(published_date,'%Y%m') = :date AND calculated_entity_relevence = 1) UNION\
                (select id,\
                (case when emotion_disgust = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_disgust'\
                when emotion_sadness = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_sadness'\
                when emotion_anger = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_anger'\
                when emotion_joy = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_joy'\
                when emotion_fear = greatest(emotion_disgust, emotion_sadness,emotion_anger,emotion_joy,emotion_fear) then 'emotion_fear'\
                end) as emotion\
                from business_tweet_info WHERE\
                business_id = :business_id AND date_format(published_date,'%Y%m') = :date AND calculated_entity_relevence = 1)) as a;
                

            '''

        public_perception = db_select(query, params)
        result_obj = {}
        results = 'results'
        for item in public_perception:
            if(item['emotion_joy'] != None or item['emotion_anger'] != None or item['emotion_disgust'] != None or item['emotion_fear'] != None or item['emotion_sadness']):
                tot = item['emotion_joy'] + item['emotion_anger'] + \
                    item['emotion_disgust'] + \
                    item['emotion_fear'] + item['emotion_sadness']
                result_obj['Joy'] = str(
                    item['emotion_joy']) + results + ' (' + str(round(item['emotion_joy']/tot, 2)) + '%)'
                result_obj['Anger'] = str(
                    item['emotion_anger']) + results + ' (' + str(round(item['emotion_anger']/tot, 2)) + '%)'
                result_obj['Disgust'] = str(
                    item['emotion_disgust']) + results + ' (' + str(round(item['emotion_disgust']/tot, 2)) + '%)'
                result_obj['Fear'] = str(
                    item['emotion_fear']) + results + ' (' + str(round(item['emotion_fear']/tot, 2)) + '%)'
                result_obj['Sadness'] = str(
                    item['emotion_sadness']) + results + ' (' + str(round(item['emotion_sadness']/tot, 2)) + '%)'
        return result_obj

    def get_redflags(self, params):
        '''Month vise'''
        params['date'] = setDate(params['date'])

        query = '''
                SELECT bi.id,bi.business_name,bni.flagged,bni.published_date FROM business_news_info as bni JOIN business_info as bi
                ON bi.id = bni.business_id JOIN account_business_mapping abm on abm.business_id=bni.business_id WHERE JSON_CONTAINS(flagged->'$.*', '1', '$') AND bni.calculated_entity_relevence = 1 AND bni.entity_score!=0  AND date_format(bni.published_date,'%Y%m') = :date
                AND abm.account_id=:account_id group by bi.id,bi.business_name,bni.flagged,bni.published_date union all SELECT bi.id,bi.business_name,bti.flagged,bti.published_date FROM business_tweet_info as bti JOIN business_info as bi
                ON bi.id = bti.business_id JOIN account_business_mapping abm on abm.business_id=bti.business_id WHERE JSON_CONTAINS(flagged->'$.*', '1', '$') AND bti.calculated_entity_relevence = 1 AND bti.entity_score!=0  AND date_format(bti.published_date,'%Y%m') = :date
                AND abm.account_id=:account_id group by bi.id,bi.business_name,bti.flagged,bti.published_date

            '''

        redflags = db_select(query, params)
        res_obj = []
        for item in redflags:
            redflag = json.loads(item[2])
            arr = []
            obj = {}
            obj['business_name'] = item[1]
            for el in redflag:
                if(redflag[el] == 1):
                    arr.append(el)
            obj['redflags'] = arr
            obj['date'] = item[3]
            res_obj.append(obj)
        return res_obj

    def get_keywords(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT 'Public News Feeds' as platform, keywords, date(published_date) FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence =1 AND date_format(published_date,'%Y%m') = :date 
                UNION ALL 
                SELECT 'Twitter' as platform, keywords,  date(published_date)  FROM business_tweet_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')= :date; 
            '''

        keywords_data = db_select(query, params)
        result_arr = []
        for item in keywords_data:
            result = {}
            result['platform'] = item[0]
            result['keywords'] = eval(item[1])
            result['date'] = item[2]
            result_arr.append(result)
        return result_arr

    def get_media_topics(self, params):
        params['date'] = setDate(params['date'])
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT 'Public News Feeds' as platform, concepts, entity_score AS sentiment_score, date(published_date) FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m') = :date 
                UNION ALL 
                SELECT 'Twitter' as platform, concepts, entity_score AS sentiment_score, date(published_date) FROM business_tweet_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')= :date; 
            '''

        media_topics = db_select(query, params)
        result_arr = []
        for item in media_topics:
            result = {}

            result['platform'] = item[0]
            result['media_topics'] = eval(item[1])
            result['date'] = item[3]
            result_arr.append(result)
        return result_arr
