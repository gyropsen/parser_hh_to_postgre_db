from unittest.mock import patch

from src.classes.db_manager import DBManager


@patch("DBManager.get_companies_and_vacancies_count")
def test_get_companies_and_vacancies_count(mock):
    mock.return_value = (1, 2)
    dbm = DBManager("test")
    assert dbm.get_companies_and_vacancies_count() == mock
