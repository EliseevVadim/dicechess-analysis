# Инструкция по запуску ноутбука

Предполагается, что у Вас уже установлен интерпретатор Python и Jupyter Notebook.

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/EliseevVadim/dicechess-analysis.git
   cd dicechess-analysis

2. Установите зависимости из файла requirements.txt:

   ```bash
   pip install -r requirements.txt

💡 Если не используете виртуальное окружение, может понадобиться флаг --user или запуск от имени администратора.

3. Теперь необходимо настроить параметры авторизации запроса. Для этого:

   3.1. Переименуйте файл `constants_example.py` в `constants.py`;
   
   3.2. Перейдите на главную страницу сайта [dicechess.com](https://www.dicechess.com/), нажмите F12, перейдите на вкладку "Network" и выберете любой запрос обозначенный {}, например "friend", как это показано на скриншоте:
![image](https://github.com/user-attachments/assets/3fb10b1a-6d61-4201-9c80-9736debffd66)

   3.3. Во вкладке "Headers" необходимо прокрутить вниз до секции "Request Headers":
   ![image](https://github.com/user-attachments/assets/26201b6f-58fb-4b92-b6e3-b74fd994e418)

   3.4. Необходимо скопировать значение Authorization и поместить его в поле `API_KEY` в файле `constants.py`:
   ![image](https://github.com/user-attachments/assets/ba6a1c0e-8180-48e8-ad56-96a94494f9ea)

   3.5. Далее необходимо скопировать значения Cookie в соответствующие дочерние значения поля COOKIES из `constants.py`:
   ![image](https://github.com/user-attachments/assets/a1f06dae-737a-4302-a6b3-e808cc8761d9)

   3.6. И наконец необходимо скопировать значение User-Agent из заголовков в значение поля USER_AGENT из `constants.py`:
   ![image](https://github.com/user-attachments/assets/59184c70-f770-4eb0-ac28-5ea712242121)

   3.7. После этого появится возможность отсылать запросы к API [dicechess.com](https://www.dicechess.com/).


4. Запустите Jupyter Notebook:

   ```bash
   jupyter notebook

5. Откройте файл `dicechess-stats.ipynb`, в котором можно редактировать и выполнять ячейки
