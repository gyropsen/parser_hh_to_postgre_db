import psycopg2

from src.classes.hh_parser import HHParser
from src.config import config


def create_database(db_name: str) -> None:
    """
    Создание базы данных
    :param db_name: название базы данных
    :return: None
    """
    conn = psycopg2.connect(dbname="postgres", **config())
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
    conn = psycopg2.connect(dbname=db_name, **config())
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
    conn = psycopg2.connect(dbname=db_name, **config())
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
