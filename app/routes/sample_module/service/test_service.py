from app.core.database.db import db_select


def test_req():
    return {"message": "Sucess"}


def test_db():
    query = '''     
                SELECT * from business_info;
            '''
    admin_details = db_select(query)
    return admin_details
