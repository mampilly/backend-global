from pydantic.types import Json
from app.core.database.db import db_select
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math


def setDate(date):
    todays_date = datetime.today()
    year = todays_date.year
    month = todays_date.month
    if len(str(month)) == 1:
        month = '0' + str(month)

    to_date = str(year) + str(month)
    if date == "Last Year":
        one_yr_ago = datetime.now() - relativedelta(years=1)
        year = one_yr_ago.year
        month = one_yr_ago.month
        if len(str(month)) == 1:
            month = '0' + str(month)
    if date == "Last 6 Months":
        six_months_ago = datetime.now() - relativedelta(months=+6)
        year = six_months_ago.year
        month = six_months_ago.month
        if len(str(month)) == 1:
            month = '0' + str(month)
    if date == "Month":
        one_yr_ago = datetime.today()
        year = one_yr_ago.year
        month = one_yr_ago.month
        if len(str(month)) == 1:
            month = '0' + str(month)
    from_date = str(year) + str(month)
    return (from_date, to_date)


def correlationCoefficient(coie_x, coie_y, n):
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    square_sum_x = 0
    square_sum_y = 0

    for i in range(1, n):

        sum_x = sum_x + coie_x[i]

        sum_y = sum_y + coie_y[i]

        sum_xy = sum_xy + coie_x[i] * coie_y[i]

        square_sum_x = square_sum_x + coie_x[i] * coie_x[i]
        square_sum_y = square_sum_y + coie_y[i] * coie_y[i]

    corr = (n * sum_xy - sum_x * sum_y)/(math.sqrt((n * square_sum_x -
                                                    sum_x * sum_x) * (n * square_sum_y - sum_y * sum_y)))

    return corr


class BusinessTrendsService:
    def get_bsi_trend(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT bi.business_name, bf.bsi_score, DATE_FORMAT(bf.created_date, '%b %Y') as date FROM bsi_facts bf, business_info bi,
                (SELECT bf.company_id, MAX(created_date) AS dt FROM bsi_facts bf WHERE bf.company_id = :business_id GROUP BY date_format(bf.created_date,'%b %Y')) MAX_DATE 
                WHERE bi.id = bf.company_id AND MAX_DATE.company_id = bf.company_id AND MAX_DATE.dt = bf.created_date AND date_format(bf.created_date,'%Y%m')>=:from_date AND date_format(bf.created_date,'%Y%m')<=:to_date ORDER BY date_format(bf.created_date,'%Y%m')
                '''
        bsi_data = db_select(query, params)
        return bsi_data

    def get_watch_level_trend(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT value FROM app_settings WHERE name="bsi_range" AND account_id = :account_id ; 
                '''
        bsi_range = db_select(query, params)

        query = '''
                SELECT bi.business_name, bf.bsi_score, DATE_FORMAT(bf.created_date, '%M %Y') as created_date FROM bsi_facts bf, business_info bi,
                (SELECT bf.company_id, MAX(created_date) AS dt FROM bsi_facts bf WHERE bf.company_id = :business_id GROUP BY date_format(bf.created_date,'%b %Y')) MAX_DATE 
                WHERE bi.id = bf.company_id AND MAX_DATE.company_id = bf.company_id AND MAX_DATE.dt = bf.created_date AND date_format(bf.created_date,'%Y%m')>=:from_date AND date_format(bf.created_date,'%Y%m')<=:to_date ORDER BY date_format(bf.created_date,'%Y%m')
                '''
        bsi_scores = db_select(query, params)
        for row in bsi_range:
            bsi_range = dict(row)
            bsi_range = json.loads(bsi_range['value'])

        watch_level = None
        result_obj = []
        if(len(bsi_scores)):
            for item in bsi_scores:
                result = {}
                bsi_score = item[1]
                risk_score = float(bsi_score)
                if(risk_score == 0):
                    watch_level = 'N/A'
                else:
                    for element in bsi_range:
                        if(risk_score >= element['min'] and risk_score <= element['max']):
                            watch_level = element['label'].lower()
                result['business_name'] = item['business_name']
                result['watch_level'] = watch_level
                result['date'] = item['created_date']
                result_obj.append(result)
        return result_obj

    def get_stock_price_trend(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                    SELECT DATE_FORMAT(bsi_facts.created_date, '%d %M %Y') as date,bsi_facts.bsi_score,stockprice_info.split_adjusted_stock FROM (select * from bsi_facts where company_id= :business_id and date_format(created_date,'%Y%m')>= :from_date and date_format(created_date,'%Y%m')<= :to_date ) as bsi_facts LEFT JOIN stockprice_info on bsi_facts.created_date=stockprice_info.date AND bsi_facts.company_id=stockprice_info.business_id AND stockprice_info.business_id = :business_id ;
                '''
        stock_data = db_select(query, params)
        result_obj = []
        weekend_stock = 0
        for element in stock_data:
            result = {}
            result['date'] = element['date']
            result['bsi_score'] = element['bsi_score']

            if element['split_adjusted_stock'] == None:
                ind = stock_data.index(element)
                if(ind == 0):
                    if(stock_data[ind+1].split_adjusted_stock != None):
                        result['stock_price'] = stock_data[ind +
                                                           1].split_adjusted_stock
                        weekend_stock = result['stock_price']
                    else:
                        result['stock_price'] = stock_data[ind +
                                                           2].split_adjusted_stock
                        weekend_stock = result['stock_price']
                else:
                    if stock_data[ind-1].split_adjusted_stock != None:
                        result['stock_price'] = stock_data[ind -
                                                           1].split_adjusted_stock
                    else:
                        result['stock_price'] = weekend_stock
            else:
                result['stock_price'] = element['split_adjusted_stock']
                weekend_stock = result['stock_price']
            if(result['stock_price'] != None):
                result['stock_price'] = round(float(result['stock_price']), 2)
            result_obj.append(result)
        return result_obj

    def correlation_bsi_vs_stockprice(self, params):
        params['business_id'] = params['business_id'] - 1000

        query = '''
                    SELECT bsi_facts.company_id as business_id,bsi_facts.created_date,bsi_facts.bsi_score,0 + stockprice_info.split_adjusted_stock as split_adjusted_stock,stockprice_info.volume FROM (select * from bsi_facts where company_id=:business_id) as bsi_facts LEFT JOIN stockprice_info on bsi_facts.created_date=stockprice_info.date AND bsi_facts.company_id=stockprice_info.business_id AND stockprice_info.business_id = :business_id ;
                '''
        stock_data = db_select(query, params)
        stock_data = [x for x in stock_data if x.split_adjusted_stock != None]

        obj_stock = []
        obj_bsi = []
        result = {}
        if(len(stock_data) != 0):
            for item in stock_data:
                obj_stock.append(item.split_adjusted_stock)
                obj_bsi.append(float(item.bsi_score))
            length = len(obj_bsi)

            same_day_corr = correlationCoefficient(
                obj_bsi, obj_stock, len(obj_bsi))
            x = obj_bsi[0:length-1]
            y = obj_stock[1:length]
            next_day_corr = correlationCoefficient(x, y, len(x))
            x = obj_bsi[0:length-7]
            y = obj_stock[7:length]
            seven_day_corr = correlationCoefficient(x, y, len(x))
            x = obj_bsi[0:length-14]
            y = obj_stock[14:length]
            fourteen_day_corr = correlationCoefficient(x, y, len(x))
            x = obj_bsi[0:length-30]
            y = obj_stock[30:length]
            thirty_day_corr = correlationCoefficient(x, y, len(x))
            result['same_day_correlation'] = same_day_corr
            result['next_day_correlation'] = next_day_corr
            result['seven_day_correlation'] = seven_day_corr
            result['fourteen_day_correlation'] = fourteen_day_corr
            result['thirty_day_correlation'] = thirty_day_corr
        return result

    def get_average_sentiment(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT date_format(published_date,'%b %Y') AS published_date, AVG(sentiment_score) AS sentiment_score FROM 
                (SELECT published_date, entity_score AS sentiment_score, entity_label AS final_label FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')>=:from_date AND date_format(published_date,'%Y%m')<=:to_date 
                UNION 
                SELECT published_date, entity_score AS sentiment_score, entity_label AS final_label FROM business_tweet_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')>=:from_date  AND date_format(published_date,'%Y%m')<=:to_date ORDER BY published_date ) AS res 
                GROUP BY date_format(published_date,'%b %Y') 
                '''
        sentiment_data = db_select(query, params)
        result_obj = []
        for item in sentiment_data:
            result = {}
            result['date'] = item['published_date']
            result['sentiment_score_percentage'] = str(
                round(item['sentiment_score'] * 100, 2)) + "%"
            result_obj.append(result)
        return result_obj

    def get_sentiment_distribution(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT final_label AS sentiment_label,AVG(final_score) AS total_sentiment, COUNT(final_label) AS sentiment_count, published_date, published_date_formated FROM 
                ( 
                SELECT business_id, entity_label AS final_label, entity_score AS final_score, date_format(published_date,'%Y%m') as published_date, date_format(published_date,'%b %Y') as published_date_formated 
                FROM business_news_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')>=:from_date AND date_format(published_date,'%Y%m')<=:to_date   
                UNION 
                SELECT business_id, entity_label AS final_label, entity_score AS final_score, date_format(published_date,'%Y%m') as published_date, date_format(published_date,'%b %Y') as published_date_formated 
                FROM business_tweet_info WHERE business_id = :business_id AND calculated_entity_relevence = 1 AND date_format(published_date,'%Y%m')>=:from_date AND date_format(published_date,'%Y%m')<=:to_date 
                ) temp_table GROUP BY published_date, final_label, published_date_formated ORDER BY published_date; 
                '''
        sentiment_data = db_select(query, params)
        result_obj = []
        setiment_object_count = {}

        for element in sentiment_data:
            formatted_date = element['published_date_formated']
            if formatted_date in setiment_object_count:
                setiment_object_count[formatted_date] += element['sentiment_count']

            else:
                setiment_object_count[formatted_date] = element['sentiment_count']

        for item in sentiment_data:
            result = {}
            result['date'] = item['published_date_formated']
            result['sentiment_distribution_percentage'] = str(round(
                (item['sentiment_count']/setiment_object_count[formatted_date]*100), 2)) + "%"
            result['article_count'] = item['sentiment_count']
            result['total_articles'] = setiment_object_count[item['published_date_formated']]
            result_obj.append(result)
        return result_obj

    def get_platform_index_trend(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT bf.google_news_platform_index,date_format(bf.created_date,'%b %Y') as date FROM bsi_facts bf, 
                (SELECT bf.company_id, MAX(created_date) AS dt FROM bsi_facts bf WHERE bf.company_id = :business_id GROUP BY date_format(bf.created_date,'%b %Y')) MAX_DATE 
                WHERE MAX_DATE.company_id = bf.company_id AND MAX_DATE.dt = bf.created_date AND date_format(bf.created_date,'%Y%m')>=:from_date AND date_format(bf.created_date,'%Y%m')<=:to_date ORDER BY date_format(bf.created_date,'%Y%m') ;
                '''
        platform_index_data = db_select(query, params)
        result_obj = []
        for item in platform_index_data:
            result = {}
            result['date'] = item['date']
            result['google_news_platform_index'] = (
                round(item['google_news_platform_index'] * 100, 2))
            result_obj.append(result)
        return result_obj

    def get_redflag_trend(self, params):
        params['business_id'] = params['business_id'] - 1000
        from_date, to_date = setDate(params['date'])
        params['to_date'] = to_date
        params['from_date'] = from_date

        query = '''
                SELECT bi.id,bi.business_name,bni.flagged,bni.published_date FROM business_news_info as bni JOIN business_info as bi
                ON bi.id = bni.business_id JOIN account_business_mapping abm on abm.business_id=bni.business_id WHERE bni.business_id=:business_id AND JSON_CONTAINS(flagged->'$.*', '1', '$') AND bni.calculated_entity_relevence = 1 AND bni.entity_score!=0  AND date_format(bni.published_date,'%Y%m') >= :from_date AND date_format(bni.published_date,'%Y%m') <= :to_date
                AND abm.account_id=:account_id group by bi.id,bi.business_name,bni.flagged,bni.published_date union all SELECT bi.id,bi.business_name,bti.flagged,bti.published_date FROM business_tweet_info as bti JOIN business_info as bi
                ON bi.id = bti.business_id JOIN account_business_mapping abm on abm.business_id=bti.business_id WHERE bti.business_id=:business_id AND JSON_CONTAINS(flagged->'$.*', '1', '$') AND bti.calculated_entity_relevence = 1 AND bti.entity_score!=0  AND date_format(bti.published_date,'%Y%m') >= :from_date AND date_format(bti.published_date,'%Y%m') <= :to_date
                AND abm.account_id=:account_id group by bi.id,bi.business_name,bti.flagged,bti.published_date ORDER BY published_date
                '''
        redflag_data = db_select(query, params)
        res_obj = []
        for item in redflag_data:
            redflag = json.loads(item[2])
            arr = []
            obj = {}
            obj['business_name'] = item[1]
            obj['date'] = item[3].strftime("%b %Y ")
            for el in redflag:
                if(redflag[el] == 1):
                    arr.append(el)
            try:
                temp_index = [x['date'] for x in res_obj].index(obj['date'])
            except ValueError:
                temp_index = -1
            if temp_index >= 0:
                res_obj[temp_index]['redflags'] += arr
            else:
                obj['redflags'] = arr
                res_obj.append(obj)

        for data in res_obj:
            count_dict = {i: data['redflags'].count(
                i) for i in data['redflags']}
            data['redflags'] = count_dict
        return res_obj
