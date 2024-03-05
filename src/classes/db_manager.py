from src.utils import get_connection


class DBManager:
    """
    Класс работы с базой данных
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = get_connection(db_name)

    def execute_query(self, query: str) -> list[tuple]:
        """
        Получает результат запроса
        :param query: Запрос
        :return: Данные, которые получены благодаря запросу
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        return result

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: Компании с количеством вакансий
        """
        result = self.execute_query(
            """
            SELECT vacancies.employer, COUNT(*) as count_vacancies
            FROM vacancies
            INNER JOIN employers ON vacancies.employer=employers.id
            GROUP BY vacancies.employer
            """
        )
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        :return: Подходящие вакансии
        """
        result = self.execute_query(
            """
            SELECT employers.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies as v
            INNER JOIN employers ON v.employer=employers.id
            """
        )
        return result

    def get_avg_salary(self) -> list[tuple]:
        """
        Получает среднюю зарплату по вакансиям
        :return: Средняя зп
        """
        result = self.execute_query(
            """
            SELECT AVG((v.salary_from + v.salary_to) / 2)
            FROM vacancies AS v
            """
        )
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Подходящие вакансии
        """
        result = self.execute_query(
            """
            SELECT v.name, v.area, v.salary_from, v.salary_to, v.url, employers.name
            FROM vacancies AS v
            INNER JOIN employers ON v.employer=employers.id
            WHERE (v.salary_from + v.salary_to) / 2 > (SELECT AVG(v.salary_from + v.salary_to) / 2
                                                       FROM vacancies AS v)
            """
        )
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param keyword: Слово для поиска
        :return: Подходящие вакансии
        """
        result = self.execute_query(
            f"""
            SELECT v.name, v.area, v.salary_from, v.salary_to, v.url, employers.name
            FROM vacancies AS v
            INNER JOIN employers ON v.employer=employers.id
            WHERE v.name LIKE ('%{keyword}%')
            """
        )
        return result
