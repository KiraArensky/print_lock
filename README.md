# Мониторинг печати с проверкой пароля

Этот проект включает систему для мониторинга заданий на печать, проверки доступа с использованием ежедневного пароля и бота для Telegram, который предоставляет этот пароль. Система состоит из Python-скрипта для мониторинга, Telegram-бота и сервера Flask.

## Особенности

1. **Мониторинг печати**:
   - Отслеживает задания на печать на принтере по умолчанию.
   - Приостанавливает задания до ввода правильного пароля.
   - Отменяет задания при вводе неправильного пароля.

2. **Генерация ежедневного пароля**:
   - Генерирует уникальный пароль на каждый день на основе текущей даты.
   - Пароль состоит из 6 случайных цифр.

3. **Telegram-бот**:
   - Позволяет администраторам получать ежедневный пароль с помощью команды `/getpass_pr`.
   - Отправляет пароль в безопасном формате Markdown.

4. **API на Flask**:
   - Предоставляет конечную точку (`/daily-password`) для получения ежедневного пароля, используемую в скрипте мониторинга.

---

## Компоненты

### 1. **Скрипт мониторинга печати**
Скрипт `monitor_print_jobs.py`:
- Отслеживает задания на печать с помощью библиотеки `win32print`.
- Приостанавливает задания и запрашивает ввод пароля через графический интерфейс Tkinter.
- Обращается к серверу Flask для получения пароля.

### 2. **Telegram-бот**
Скрипт `bot_main.py`:
- Реализует Telegram-бота с использованием библиотеки `pyTelegramBotAPI`.
- Предоставляет команду `/getpass_pr` для получения пароля.

### 3. **Сервер Flask**
Скрипт `flask_server.py`:
- Обслуживает запросы на получение пароля через REST API.
- Использует ту же логику генерации пароля, что и бот.

---

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Установите зависимости**:
   Установите необходимые библиотеки Python с помощью `pip`:
   ```bash
   pip install pyTelegramBotAPI flask requests pywin32
   ```

3. **Настройте Telegram-бота**:
   - Замените `TOKEN` в файле `bot_main.py` на токен вашего бота, полученный у BotFather.

4. **Запустите сервер Flask**:
   ```bash
   python flask_server.py
   ```

5. **Запустите Telegram-бота**:
   ```bash
   python bot_main.py
   ```

6. **Запустите скрипт мониторинга**:
   ```bash
   python monitor_print_jobs.py
   ```

---

## Использование

1. **Проверка пароля**:
   - При обнаружении задания на печать скрипт приостанавливает его.
   - Пользователь вводит пароль через графический интерфейс.
   - Если пароль верный, задание возобновляется; иначе оно отменяется.

2. **Получение ежедневного пароля**:
   - Администраторы могут использовать команду `/getpass_pr` в Telegram для получения пароля.
   - Альтернативно пароль можно получить программно через сервер Flask.

---

## API

### `GET /daily-password`
- **Описание**: Возвращает ежедневный пароль.
- **Пример ответа**:
  ```json
  {
    "password": "123456"
  }
  ```

---

## Примечания

- Убедитесь, что принтер установлен как принтер по умолчанию, чтобы скрипт мониторинга работал корректно.
- Сервер Flask должен быть доступен с компьютера, на котором выполняется скрипт мониторинга.

---

## Вклад в проект

1. Сделайте форк репозитория.
2. Создайте ветку для новой функции (`git checkout -b feature-name`).
3. Зафиксируйте изменения (`git commit -am 'Добавить новую функцию'`).
4. Отправьте изменения в ветку (`git push origin feature-name`).
5. Создайте pull request.

---

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.
