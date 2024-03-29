# Parser HH to PostgreSQL, Coursework_5

### Приложение предназначено для получения и внесения вакансий топ-10 работодатей в России в базу данных PostgreSQL

ВНИМАНИЕ!!! Для корректной работы в PyCharm, необходимо включить эмуляцию терминала!!!
Для этого необходимо открыть файл main.py, вызвать контекстное меню нажатием правой кнопки мыши
и перейти в пункт "Modify Run Configuration...". Нажать на "Modify Options" и установить галочку на 
"Emulate terminal in out console"

В файл database.ini небходимо вместо 'Enter your ...' ввести свои значения.
Чаще всего значения будут такие:
```

user=postgres
password='Enter your password'
host=localhost
port=5432

```

### Имеет следующие возможности:
- Поиск вакансий у топ-10 работодатей в России
- Сохранение в базу данных PostgreSQL
- Возможность удаления вакансий из базы данных PostgreSQL
- Возможности работы с БД:
  - Получать список всех компаний и количество вакансий у каждой компании
  - Получать список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
  - Получать среднюю зарплату по вакансиям.
  - Получать список всех вакансий, у которых зарплата выше средней по всем вакансиям.
  - Получать список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
 
Запуск программы осуществляется запуском main.py в корне проекта

### Интерфейс приложения имеет следущую структуру:

### Предложение ввести название базы данных

```
Введите название базы данных: 
```

#### Главное меню:

```
  Главное меню.                                                                                                                                                                                                             
 Нажмите Q или Esc, чтобы выйти.                                                                                                                                                                                            
                                                                                                                                                                                                                            
> Получить вакансии из базы данных                                                                                                                                                                                          
  Записать в базу данных вакансии                                                                                                                                                                                           
  Выход
          
```

#### Меню базы данных:

```
  Меню базы данных.                                                                                                                                                                                                         
  Нажмите Q или Esc, чтобы вернуться в главное меню.                                                                                                                                                                        
                                                                                                                                                                                                                            
> Получить список всех компаний и количество вакансий у каждой компании                                                                                                                                                     
  Получить список всех вакансий с указанием названия компании                                                                                                                                                               
  Получить среднюю зарплату по вакансиям                                                                                                                                                                                    
  Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям                                                                                                                                          
  Получить список всех вакансий, в названии которых содержатся переданные в метод слова                                                                                                                                     
  Вернуться в главное меню      
```





