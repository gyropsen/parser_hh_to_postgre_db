import psycopg2
from simple_term_menu import TerminalMenu

from src.classes.db_manager import DBManager
from src.utils import create_database, create_tables, insert_data_into_tables


def main() -> None:
    """
    Основная функция
    """
    main_menu_title = "  Главное меню.\n Нажмите Q или Esc, чтобы выйти. \n"
    main_menu_items = ["Получить вакансии из базы данных", "Записать в базу данных вакансии", "Выход"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    database_menu_title = "  Меню базы данных.\n  Нажмите Q или Esc, чтобы вернуться в главное меню. \n"
    database_menu_items = [
        "Получить список всех компаний и количество вакансий у каждой компании",
        "Получить список всех вакансий с указанием названия компании",
        "Получить среднюю зарплату по вакансиям",
        "Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям",
        "Получить список всех вакансий, в названии которых содержатся переданные в метод слова",
        "Вернуться в главное меню",
    ]
    database_menu_back = False
    database_menu = TerminalMenu(
        database_menu_items,
        title=database_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    while True:
        dbname = input("Введите название базы данных: ").strip().lower()
        if dbname.isalpha():
            break
        else:
            print("Некорректное название базы данных. "
                  "Введите другое название. Название "
                  "должно быть только из латинских букв")

    while not main_menu_exit:
        main_sel = main_menu.show()

        if main_sel == 0:
            while not database_menu_back:
                db_sel = database_menu.show()
                try:
                    dbm = DBManager(dbname)
                    if db_sel == 0:
                        print("Получение списка всех компаний и количество вакансий у каждой компании")

                        companies = dbm.get_companies_and_vacancies_count()
                        for company in companies:
                            print(f"Компания {company[0]} имеет {company[1]} вакансий\n")
                        input("Введите что-нибудь, чтобы вернуться в меню базы данных")

                    elif db_sel == 1:
                        print("Получение списка всех вакансий с указанием названия компании")

                        vacancies = dbm.get_all_vacancies()
                        for vacancy in vacancies:
                            print(
                                f"\nКомпания {vacancy[0]}\n"
                                f"Вакансия {vacancy[1]}\n"
                                f"Зарплата от {vacancy[2]}\n"
                                f"Зарплата до {vacancy[3]}\n"
                                f"Ссылка {vacancy[4]}\n"
                            )
                        input("Введите что-нибудь, чтобы вернуться в меню базы данных")

                    elif db_sel == 2:
                        print("Получить среднюю зарплату по вакансиям")

                        salary_avg = dbm.get_avg_salary()
                        print(f"Средняя зарплата всех вакансий в базе данных: {salary_avg[0]}")
                        input("Введите что-нибудь, чтобы вернуться в меню базы данных")

                    elif db_sel == 3:
                        print("Получение списка всех вакансий, " "у которых зарплата выше средней по всем вакансиям")

                        vacancies = dbm.get_vacancies_with_higher_salary()
                        for vacancy in vacancies:
                            print(
                                f"\nВакансия: {vacancy[0]}\n"
                                f"Город: {vacancy[1]}\n"
                                f"Зарплата от: {vacancy[2]}\n"
                                f"Зарплата до: {vacancy[3]}\n"
                                f"Ссылка: {vacancy[4]}\n"
                                f"Компания: {vacancy[5]}\n"
                            )
                        input("Введите что-нибудь, чтобы вернуться в меню базы данных")

                    elif db_sel == 4:
                        print(
                            "Получение списка всех вакансий, " "в названии которых содержатся переданные в метод слова"
                        )

                        keyword = input("Введите ключевое слово: ")
                        vacancies = dbm.get_vacancies_with_keyword(keyword.strip())
                        for vacancy in vacancies:
                            print(
                                f"\nВакансия: {vacancy[0]}\n"
                                f"Город: {vacancy[1]}\n"
                                f"Зарплата от: {vacancy[2]}\n"
                                f"Зарплата до: {vacancy[3]}\n"
                                f"Ссылка: {vacancy[4]}\n"
                                f"Компания: {vacancy[5]}\n"
                            )
                        input("Введите что-нибудь, чтобы вернуться в меню базы данных")

                    elif db_sel == 5 or db_sel is None:
                        database_menu_back = True
                        print("Возврат в главное меню")
                except psycopg2.OperationalError as error:
                    print(error, "Введите другое имя базы данных, или создайте новую")
                    input("Введите что-нибудь, чтобы вернуться в меню базы данных")
                    database_menu_back = True
                except Exception as error:
                    print(error, "Непредвиденная ошибка")
                    input("Введите что-нибудь, чтобы вернуться в меню базы данных")
                    database_menu_back = True

            database_menu_back = False
        elif main_sel == 1:
            create_database(dbname)
            create_tables(dbname)
            insert_data_into_tables(dbname)

        elif main_sel == 2 or main_sel is None:
            main_menu_exit = True
            print("Quit Selected")


if __name__ == "__main__":
    main()
