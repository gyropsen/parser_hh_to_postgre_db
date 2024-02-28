import requests


class HHParser:
    @staticmethod
    def get_employers() -> list:
        """
        Получение списка из 10 работодателей
        :return: list[dict] если все успешно, и list[] если ответ не 200
        """
        params = {"per_page": 10, "sort_by": "by_vacancies_open"}
        response = requests.get("https://api.hh.ru/employers/", params)
        if response.status_code == 200:
            data = response.json()["items"]
            employers = []
            for emp in data:
                employers.append({"id": emp["id"], "name": emp["name"]})
            return employers
        return []

    @staticmethod
    def get_vacancies_from_employer(_id_) -> list:
        """
        Получение 20 вакансий от заданного работодателя
        :param _id_: id работодателя
        :return: list[dict] если все успешно, и list[] если ответ не 200
        """
        params = {"per_page": 20, "employer_id": _id_}

        response = requests.get("https://api.hh.ru/vacancies/", params)
        if response.status_code == 200:
            return response.json()["items"]
        return []

    def get_all_vacancies(self) -> list[dict]:
        """
        Получение вакансий от всех работодателей
        :return: список вакансий
        """
        employers = self.get_employers()
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_vacancies_from_employer(employer["id"]))
        return vacancies

    def filter_vacancies(self) -> list[dict]:
        """
        Получение нужных данных из необработанных вакансий
        :return: список с полезными данными
        """
        vacancies = self.get_all_vacancies()
        filter_data = []
        for vacancy in vacancies:
            if not vacancy["salary"]:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
            filter_data.append(
                {
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "published_at": vacancy["published_at"],
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "url": vacancy["alternate_url"],
                    "area": vacancy["area"]["name"],
                    "employer": vacancy["employer"]["id"],
                }
            )
        return filter_data
