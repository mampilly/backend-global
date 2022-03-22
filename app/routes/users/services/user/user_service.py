from app.core.database.db import db_select


class UserService:
    def get_user_info(self, user_id):
        params = {"user_id": user_id}
        query = '''
                SELECT first_name,username,ac.name as account_name
                FROM users u join user_account_mapping uac ON u.id = uac.user_id
                join accounts ac on ac.id=uac.account_id
                where u.id= :user_id and uac.is_api_access_required = 1;
            '''
        user_data = db_select(query, params)
        return user_data

    def get_users_info_by_username(self, username):
        params = {"username": username}
        query = '''
                    SELECT u.id AS user_id, username, password AS hashed_password,uac.account_id,uac.client_id
                    FROM  users u JOIN user_account_mapping uac ON u.id = uac.user_id WHERE
                    u.username = :username and uac.is_api_access_required = 1;'''
        user_data = db_select(query, params)
        user_data_map = [{**row} for row in user_data]
        user_data = {user['username']: user for user in user_data_map}
        return user_data

    def get_user_info_by_client_credentials(self, client_id, client_secret):
        params = {"client_id": client_id, "client_secret": client_secret}

        query = '''select uac.user_id as user_id,uac.account_id,u.username,u.password AS hashed_password,\
                   uac.client_id FROM  users u JOIN user_account_mapping uac ON u.id = uac.user_id WHERE
                   uac.client_id = :client_id  AND uac.client_secret= :client_secret AND uac.is_api_access_required = 1;         '''
        user_data = db_select(query, params)
        user_data_map = [{**row} for row in user_data]
        user_data = {user['username']: user for user in user_data_map}
        if not user_data:
            return False
        return user_data

    def get_user_info_by_client_id(self, client_id):
        params = {"client_id": client_id}

        query = '''select uac.user_id as user_id,uac.account_id,u.username, uac.client_id FROM  \
                   users u JOIN user_account_mapping uac ON u.id = uac.user_id WHERE
                   uac.client_id = :client_id AND uac.is_api_access_required = 1;'''
        user_data = db_select(query, params)
        user_data_map = [{**row} for row in user_data]
        user_data = {user['username']: user for user in user_data_map}
        return user_data
