import psycopg2

from src.classes.hh_parser import HHParser
from src.config import config


def get_connection(db_name="postgres") -> psycopg2:
    return psycopg2.connect(dbname=db_name, **config())


def create_database(db_name: str) -> None:
    """
    Создание базы данных
    :param db_name: название базы данных
    :return: None
    """
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    finally:
        cur.close()
        conn.close()


def create_tables(db_name: str) -> None:
    """
    Создание таблиц в азе данных
    :param db_name: название базы данных
    :return: None
    """
    conn = get_connection(db_name)
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers
                (
                    id int PRIMARY KEY,
                    name varchar(255) UNIQUE NOT NULL
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE vacancies
                (
                    id int PRIMARY KEY,
                    name varchar(255) NOT NULL,
                    area varchar(255),
                    salary_from int,
                    salary_to int,
                    published_at timestamp,
                    url varchar(255),
                    employer int REFERENCES employers(id) NOT NULL
                )
                """
            )
    conn.close()


def insert_data_into_tables(db_name: str) -> None:
    """
    Добавление сущностей в базу данных
    :param db_name: название базы данных
    :return: None
    """
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.filter_vacancies()
    conn = get_connection(db_name)
    with conn:
        with conn.cursor() as cur:
            for employer in employers:
                cur.execute(
                    """
                        INSERT INTO employers VALUES (%s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """,
                    (employer["id"], employer["name"]),
                )
            for vacancy in vacancies:
                cur.execute(
                    """
                        INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        vacancy["id"],
                        vacancy["name"],
                        vacancy["area"],
                        vacancy["salary_from"],
                        vacancy["salary_to"],
                        vacancy["published_at"],
                        vacancy["url"],
                        vacancy["employer"],
                    ),
                )
    conn.close()


def delete_database(db_name: str) -> None:
    """
    Удаление базы данных
    :param db_name: название базы данных
    :return: None
    """
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(
            f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
            f"FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{db_name}' "
            f"AND pid <> pg_backend_pid();"
        )
        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    finally:
        cur.close()
        conn.close()
