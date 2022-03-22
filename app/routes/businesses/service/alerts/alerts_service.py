"""Alert Service"""
import json
from app.core.database.db import db_select


def get_acronym(account_id):
    query = '''
                SELECT acronym FROM accounts WHERE id = :account_id
            '''
    acronym = db_select(query, {'account_id': account_id})
    return acronym[0][0]


def setDate(from_date, to_date):
    try:
        now = from_date
        year = now.strftime("%Y")
        month = now.strftime("%m")
        if len(str(month)) == 1:
            month = '0' + str(month)

        date1 = str(year) + str(month)

        now = to_date
        year = now.strftime("%Y")
        month = now.strftime("%m")
        if len(str(month)) == 1:
            month = '0' + str(month)

        date2 = str(year) + str(month)
        return date1, date2
    except Exception as e:
        print(e)


class AlertsService:
    def get_alerts(self, params):
        acronym = get_acronym(params['account_id'])
        tabel_name = acronym + '_alert_social_history'
        params['start_date'], params['end_date'] = setDate(
            params['start_date'], params['end_date'])
        query = '''
                SELECT bi.business_name, ash.created_date AS created_date, ash.alert_properties, alts.* FROM ''' + tabel_name + ''' ash     JOIN business_info bi ON bi.id = ash.business_id                 JOIN alert_social alts ON alts.id = ash.alert_id 
                WHERE date_format(ash.created_date,'%Y%m')>=:start_date AND date_format(ash.created_date,'%Y%m')<=:end_date        
                ORDER BY  ash.created_date  ASC
                '''
        alerts_data = db_select(query, params)
        result = []
        last_30_days = 'in the last 30 days'
        bsi_score_decreased = 'The BSI score decreased from '
        try:
            for row in alerts_data:
                res = {}
                res['business_name'] = row['business_name']
                res['date'] = row['created_date']
                res['title'] = row['description']
                res['priority'] = row['priority']
                alert_properties = json.loads(row['alert_properties'])

                if(row['code'] == 'ALTBSI01'):
                    res['alert_description'] = bsi_score_decreased + str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTBSI02'):
                    res['alert_description'] = bsi_score_decreased + str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTBSI03'):
                    res['alert_description'] = bsi_score_decreased + str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTBSI04'):
                    res['alert_description'] = bsi_score_decreased + str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTBSI05'):
                    res['alert_description'] = 'The watch level changed from '+str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTSNT01'):
                    res['alert_description'] = 'No relevant  posts/news found in the last 90 days'

                elif(row['code'] == 'ALTRDF01'):
                    list = []
                    for key in alert_properties['red_flag'].keys():
                        list.append(key)
                    res['alert_description'] = bsi_score_decreased + str(alert_properties['previous_value'])+' to '+str(
                        alert_properties['current_value']) + last_30_days+' The following Red flags were found: '+",".join(list)

                elif(row['code'] == 'ALTSNT02'):
                    res['alert_description'] = 'Negative articles count increased from '+str(
                        alert_properties['previous_value'])+' to '+str(alert_properties['current_value']) + last_30_days

                elif(row['code'] == 'ALTBSI06'):
                    res['alert_description'] = 'BSI score constantly decreased over the last 180 days'

                elif(row['code'] == 'ALTSNT03'):
                    res['alert_description'] = 'Average sentiment score constantly decreased over the last 180 days'

                elif(row['code'] == 'ALTEMO01'):
                    emotion = max(alert_properties, key=alert_properties.get)
                    res['alert_description'] = 'Public perception is '+emotion
                result.append(res)

            return result
        except Exception as e:
            print(e)
