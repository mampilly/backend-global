from uuid import uuid4
import time
from app.core.database.db import db_select, db_execute


class BaseService:
    def generate_client_credentials(self, user_id, account_id):
        current_time = int(time.time())
        client_id = str(user_id+100) + str(current_time) + str(uuid4())
        client_secret = str(uuid4()) + str(user_id+20)
        params = {"client_id": client_id,
                  "client_secret": client_secret, "user_id": user_id, "account_id": account_id}
        query = "update user_account_mapping set client_id = :client_id, \
            client_secret = :client_secret where user_id = :user_id and account_id=:account_id and is_api_access_required = 1;"
        db_execute(query, params)
        return {"client_id": client_id, "client_secret": client_secret}

    def validate_client_credentials(self, user_id, client_id, client_secret):
        params = {"user_id": user_id}
        query = '''
                SELECT client_id,client_secret FROM users where role_id=5 and id= :user_id;
            '''
        user_data = db_select(query, params)
        if user_data:
            if user_data[0][0] == client_id and user_data[0][1] == client_secret:
                return True
        return False
