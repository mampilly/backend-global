from app.core.database.db import db_select, db_execute
from datetime import datetime
import requests
from app.core.config import config


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


def id_map_loop_add(dict_data, key):
    for inner in dict_data:
        if key in inner.keys():
            inner[key] += 1000
    return dict_data


def offline(data):
    offline_url = config.OFFLINE_HOST
    response = requests.get(offline_url + '/addBusiness', data=data)
    print(response)


class BusinessService:
    def search_business(self, params):
        query = '''
                SELECT id,business_name,address_line_1,address_line_2,city,state,zip,country,fax,telephone,website,stock_symbol FROM business_info
                WHERE business_name like "%" :business_name "%" AND website like "%" :website "%"
            '''
        business_data = db_select(query, params)
        business_data_map = [{**row} for row in business_data]
        business_data_value = id_map_loop_add(business_data_map, "id")
        return business_data_value

    def get_company_details(self, params):
        params['business_id'] = params['business_id'] - 1000

        query = '''
               SELECT business_name,business_alias_name,address_line_1,address_line_2,city,state,zip,country,telephone,website,stock_symbol,year_founded,industry,contact_name,bsi_score,twitter_handle FROM business_info WHERE id = :business_id;
            '''

        company_details = db_select(query, params)
        return company_details

    def get_entity_details(self, params):
        params['business_id'] = params['business_id'] - 1000

        query = '''
                SELECT entity_name,entity_alias_name,address_line_1,address_line_2,city,state,zip,country,telephone,website,stock_symbol,year_founded,industry,contact_name,bsi_score,bi.twitter_handle FROM business_entity_info bei,business_info bi WHERE bei.business_id = bi.id AND bei.business_id = :business_id AND bei.is_parent = 0;
            '''

        company_details = db_select(query, params)
        return company_details

    def add_business(self, params):
        try:
            query = '''
                    INSERT INTO business_info(business_name,address_line_1,address_line_2,city,state,zip,country,type,year_founded,industry,stock_symbol,contact_name,telephone,website,twitter_handle,business_alias_name,is_active,is_new, notes) VALUES(:business_name,:address_line_1,:address_line_2,:city,:state,:zip,:country,:type,:year_founded,:industry,:stock_symbol,:contact_name,:telephone,:website,:twitter_handle,:business_alias_name,:is_active,:is_new, :additional_notes);
                    '''
            business_data = db_execute(query, params)

            if business_data > -1:
                params['insert_id'] = business_data
                params['is_report_required'] = 0

                query = '''
                    INSERT INTO account_business_mapping (account_id, business_id, is_active, is_report_required) VALUES(:account_id,:insert_id,:is_active, :is_report_required)
                    '''
                business_account_mapping = db_execute(query, params)

                if business_account_mapping > 1:
                    params['is_parent'] = 1
                    query = '''
                    INSERT INTO business_entity_info(business_id,entity_name,twitter_handle,entity_alias_name,is_parent,is_new) VALUES(:insert_id,:business_name,:twitter_handle,:business_alias_name,:is_parent,:is_new)
                    '''
                business_entity = db_execute(query, params)

                if(business_entity > -1):
                    param = params['account_id']
                    offline(param)

            return "Business added successfully."
        except Exception as e:
            print(e)
