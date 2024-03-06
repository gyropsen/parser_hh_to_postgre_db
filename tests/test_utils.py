from functools import wraps

from src.classes.db_manager import DBManager
from src.utils import create_database, create_tables, delete_database, insert_data_into_tables

dbname = "test"


def create_delete_database(db_name):
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            create_database(db_name)
            function(*args, **kwargs)
            delete_database(db_name)

        return inner

    return wrapper


@create_delete_database(dbname)
def test_create_database_delete_database():
    dbm = DBManager(dbname)
    lst_db = dbm.execute_query(
        "SELECT (pg_stat_file('base/'||oid ||'/PG_VERSION')).modification, datname FROM pg_database;"
    )
    for db in lst_db:
        if db[1] == dbname:
            assert db[1] == dbname


@create_delete_database(dbname)
def test_create_tables():
    create_tables(dbname)
    dbm = DBManager(dbname)
    table_employers = dbm.execute_query(
        """
        SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'test'
                AND table_name = 'employers'
            ) AS table_exists;
        """
    )
    table_vacancies = dbm.execute_query(
        """
        SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'test'
                AND table_name = 'vacancies'
            ) AS table_exists;
        """
    )
    assert table_employers
    assert table_vacancies


@create_delete_database(dbname)
def test_insert_data_into_tables():
    create_tables(dbname)
    insert_data_into_tables(dbname)
    dbm = DBManager(dbname)
    vacancies = dbm.execute_query(
        """
        SELECT * FROM vacancies;
        """
    )
    employers = dbm.execute_query(
        """
        SELECT * FROM employers;
        """
    )
    assert len(vacancies) == 200
    assert len(employers) == 10
