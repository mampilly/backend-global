'''Database Implementation'''
import logging
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi_sqlalchemy import db
from app.core.config import config


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://" + config.DB_USERNAME + \
    ":" + config.DB_PASSWORD + "@" + config.DB_HOST + ":" + config.DB_PORT + \
    "/" + config.DB_NAME


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=int(
    config.DB_POOL_SIZE), max_overflow=0, pool_recycle=3600, pool_pre_ping=True)

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=True, bind=engine))


Base = declarative_base()


def db_execute(sqlstr, *query_params: Any):
    '''database querstring exceute'''
    try:
        last_id = db.session.execute(sqlstr, *query_params)
        return last_id.lastrowid
    except Exception as e:
        print(e)
        db.session.rollback()
        return -1
    finally:
        db.session.commit()


def db_select(sqlstr, *query_params: Any):
    '''database select query'''

    if len(query_params) == 0:
        result = db.session.execute(sqlstr).fetchall()
    else:
        result = db.session.execute(sqlstr, *query_params).fetchall()
    return result


def db_bulk_insert(table, params):
    '''database bulk insert'''
    try:
        db.session.bulk_insert_mappings(table, params, render_nulls=True)
    except Exception as e:
        logging.error(e)
        db.session.rollback()
    finally:
        db.session.commit()


def db_insert_or_update(row):
    '''database insert or update'''
    try:
        db.session.merge(row)
    except Exception as e:
        logging.error(e)
        db.session.rollback()
    finally:
        db.session.commit()


def db_insert(row):
    '''database insert'''
    try:
        db.session.add(row)
        db.session.commit()
        db.session.refresh(row)
        return True, row
    except Exception as error:
        logging.info(error)
        db.session.rollback()
        return False, row


def db_inser_all(insert_list, count=100):
    '''database bulk insert'''
    try:

        not_commited_list = []

        if len(insert_list) < count:
            logging.info("DB Merge : 1 - " + str(len(insert_list)))
        else:
            logging.info("DB Merge : 1 - " + str(count))

        for index, item in enumerate(list):
            db.session.merge(item)
            not_commited_list.append(item)

            if (index + 1) % count == 0:
                logging.info("DB Commit (This will take some time) : " +
                             str(index+1) + "/" + str(len(list)))

                if ((index+1) + count) < len(list):
                    logging.info("DB Merge : " + str((index+1)) +
                                 " - " + str((index+1) + count))
                else:
                    logging.info("DB Merge : " + str((index+1)) +
                                 " - " + str(len(list)))

                try:
                    db.session.commit()
                    not_commited_list = []
                except Exception as e:
                    logging.error("Merge Error List : " +
                                  str(not_commited_list) + " | MSG : " + str(e))

        try:
            db.session.commit()
            not_commited_list = []
        except Exception as e:
            logging.error("Merge Error List : " +
                          str(not_commited_list) + " | MSG : " + str(e))

    except Exception as e:
        logging.error(e)
        db.session.rollback()


def db_bulk_inser_all(insert_list, model, count=100):
    '''database bulk insert for model'''
    try:

        sub_list = []
        for index, item in enumerate(insert_list):
            sub_list.append(item)
            if (index + 1) % count == 0:
                db.session.add_all(sub_list)
                db.session.commit()
                sub_list = []
                print("Inserted : " + str(index+1) +
                      "/" + str(len(insert_list)))

        if len(sub_list) > 0:
            db.session.add_all(sub_list)
            print("Inserted : " + str(len(insert_list)) +
                  "/" + str(len(insert_list)))
        return db.session.query(model).count()
    except Exception as e:
        print(e)
        db.session.rollback()
        return -1
    finally:
        db.session.commit()
