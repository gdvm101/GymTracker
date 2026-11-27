# GymTracker · План тестирования\n\n[Редакция на вики](https://se.cs.petrsu.ru/w/index.php?oldid=340457). Уточнения для разработки перечислены в разделе [Уточнения пакета](00_Start.md#package-notes).\n\n[На страницу проекта](00_Start.md) · [Спецификация требований](02_Requirements.md) · [Матрица решений](01_Architecture.md#trace) · [Документ о выполнении тестирования](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82_%D0%BE_%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B8_%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F)

<span id="test-method"></span>

<span id="Как_проводится_тестирование"></span>

## Как проводится тестирование

Редакция от 19.11.2026. Проверки описаны для разработки и показа инструктору. Обозначения UT, IT и AT используются в матрице требований и журнале прогонов.

[Стенд и данные](#test-setup) · [Блочные тесты](#unit) · [Интеграционные тесты](#integration) · [Аттестационные тесты](#acceptance) · [Указатель ФТ и ФО](#coverage)

| Уровень | Объект и способ | Когда и кто показывает |
|---|---|---|
| Блочный · UT | На сервере pytest вызывает один метод или валидирует DTO. Подставной репозиторий возвращает известные данные. Три клиентские функции C-01–C-03 проверяются Vitest в Node. Для граничных входов выполняются отдельные параметризованные случаи. | Разработчик запускает набор своего модуля при изменении функции. На демонстрации показывает вход, ожидаемое значение и вывод проверки. |
| Интеграционный · IT | pytest и FastAPI TestClient посылают HTTP-запросы приложению. Запрос проходит реальные зависимости, сервис, SQLAlchemy и отдельную PostgreSQL. После ответа проверяется чтение через API и состояние БД в новой сессии. Только внешний AI заменяется управляемой заглушкой; отказ до commit вводится в указанной тестовой точке. | После соединения модулей Халык показывает тренировочные операции и БД, Умалат — доступ и интеграцию, Захид — социальные функции. |
| Аттестационный · AT | В браузере исполнитель вручную проходит перечисленные шаги из роли пользователя, сравнивает экран с ожидаемым результатом. Для скрытого хранения пароля и ролей прилагает результат указанной серверной проверки на той же сборке. | На очной или дистанционной встрече Самир показывает интерфейс, второй участник сверяет критерии и записывает наблюдения. Инструктор может повторить шаги на стенде. |

<span id="test-setup"></span>

<span id="Подготовка_и_запуск"></span>

### Подготовка и запуск

1.  Зафиксировать идентификатор коммита, ОС, версии Python, PostgreSQL, Node и браузеров, часовой пояс Europe/Moscow и включённые функции. Поднять тестовый стенд с рабочей схемой и отдельную БД для автоматических тестов.
2.  Из корня проекта выполнить `make setup`. Для демонстрационной БД — `make migrate` и `make seed`. Для автоматических тестов выставить TEST_DATABASE_URL отдельной БД. Фикстура сверяет адрес с DATABASE_URL, применяет миграции и создаёт отдельную схему или очищает только свои тестовые данные. Каждый случай получает исходный набор заново. Для проверок конкуренции — независимые соединения и чистая схема. Для показа отдельно подготовить учётные записи А и Б и первую контрольную тренировку за 09.10.2026. Порядок и значения приведены в разделе «Исходные данные и порядок показа».
3.  Локально или по SSH на учебный стенд запустить `make test-unit`, затем `make test-integration`. Для клиентских функций из каталога frontend выполнить `npm run test:unit` (Vitest в режиме run). `make test` запускает все три автоматических набора. Ненулевой код возврата означает сбой; в отчёт записывают ID и сообщение проверки.
4.  Для ручной демонстрации запустить `make backend` и `make frontend` в двух терминалах, открыть адрес стенда. При дистанционной сдаче один участник включает демонстрацию экрана: сначала показывает команду и итог прогона, затем в двух окнах браузера выполняет сценарии от имени А и Б. Пароли вводятся заранее или скрытно. Используются Chrome и Firefox, обычная ширина 1280 и узкая 390 CSS-пикселей.
5.  Основной прогон H использует пустые FEATURES и AI_ENABLED=false. Дополнения M/L проверяются отдельными прогонами с флагами их раздела. Например, для проверки видимости нужны friends и privacy, для событий — notifications и соответствующий источник, для графика — charts. В журнале отмечают конфигурацию и причину неприменимости конкретного шага.

<span id="fixtures"></span>

<span id="Исходные_данные_и_порядок_показа"></span>

### Исходные данные и порядок показа

| Набор | Данные и ожидаемые ориентиры |
|---|---|
| А, Б, В, admin | Разные учётные записи. А ведёт дневник, Б используется для проверки чужих данных и дружбы, В — скрытый пользователь группы. Роль администратора назначена отдельному аккаунту. Для регистрации берут новый адрес на каждый независимый прогон. |
| Пустой набор | Каталог содержит «Жим гантелей» с внешним отягощением и «Тяга верхнего блока». У А нет записей, у Б данные отдельные. Идентификаторы берутся из ответов или фиксируются фикстурой, например жим id=10. |
| Контрольный набор | 09.10.2026 — жим 30×10, 30×8, 32×6; 10.10.2026 — 34×8, 34×6. Суммарный вес обеих гантелей указывается в кг. Первое занятие даёт 732 кг·повт., второе 476, вместе 1208. Максимумы — 32 и 34 кг. |
| Время и отказы | Для недельных границ фиксируется календарь приложения. При эмуляции ошибки БД исключение возникает после flush до commit, новый запрос читает БД через отдельное соединение. Для AI детерминированный HTTP-ответ, тайм-аут или некорректный ответ задаются фикстурой. |
| Пять демонстрационных блоков | Д-01 → AT-01, AT-03, AT-05. Д-02 → AT-08, AT-09. Для Д-03 заранее подготовить у А занятие за 09.10.2026 и на показе сохранить занятие за 10.10.2026 по шагам AT-11 с данными второй контрольной тренировки. Для Д-04 использовать обе записи и ожидаемые результаты AT-13. Д-05 → AT-03, AT-12, AT-14 и проверки ограничений. AT-11 и AT-12 как отдельные тесты запускать с их собственными исходными данными. |

<span id="unit"></span>

<span id="Блочные_тесты"></span>

## Блочные тесты

Каждая строка обозначает одну проверяемую функцию. Указанные пути отсчитываются от backend/app для Python и frontend/src для JSX. Проверка сравнивает конкретное возвращаемое значение либо ожидаемый тип ошибки.

| Тест · приоритет · тип | Функция и алгоритм | Вход | Ожидаемый выход | Требования |
|---|---|---|---|---|
| <span id="ut-01"></span>UT-01 · H · позитивный | `normalize_email()` · `schemas/auth.py` · [A-01](01_Architecture.md#alg-A-01) | Строка «  Athlete@Example.TEST  ». | athlete@example.test. Пробелы отсечены, регистр приведён к нижнему. | [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФО 2.1](02_Requirements.md#req-fo-2-1) |
| <span id="ut-02"></span>UT-02 · H · граничный | `RegisterDTO.model_validate()` · `schemas/auth.py` · [A-01](01_Architecture.md#alg-A-01) | Один допустимый адрес; пароли из 7, 8, 128, 129 символов. | Для длин 8 и 128 создан DTO. Для 7 и 129 — ValidationError с полем password. | [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФО 2.3](02_Requirements.md#req-fo-2-3) |
| <span id="ut-03"></span>UT-03 · H · позитивный, негативный | `verify_password()` · `core/security.py` · [A-02](01_Architecture.md#alg-A-02) | Хеш, полученный hash_password() из тестового пароля; верный и изменённый пароли. | True для верного, False для изменённого. Хеш имеет формат Argon2id, равенство случайных хешей не проверяется. | [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФО 2.2](02_Requirements.md#req-fo-2-2) |
| <span id="ut-04"></span>UT-04 · H · негативный | `verify_csrf()` · `core/security.py` · [A-04](01_Architecture.md#alg-A-04) | Токен, полученный make_csrf() для сеанса S, валидация в S и в независимом сеансе T. | Проверка в S успешна, в T отклонена. HTTP-отказ проверяет IT-05. | [ФТ 2.2](02_Requirements.md#req-ft-2-2), [ФО 1.2](02_Requirements.md#req-fo-1-2) |
| <span id="ut-05"></span>UT-05 · H · граничный | `ProfilePatchDTO.model_validate()` · `schemas/auth.py` · [A-03](01_Architecture.md#alg-A-03) | height=180.5 и current_weight=70.25; отдельные случаи height=0, current_weight=−0.01, лишнее поле user_id. | Первый объект принят с заданной точностью. Каждый из трёх остальных даёт ValidationError с ошибочным полем. | [ФТ 3.2](02_Requirements.md#req-ft-3-2), [ФТ 3.3](02_Requirements.md#req-ft-3-3), [ФО 1.3](02_Requirements.md#req-fo-1-3), [ФО 3.4](02_Requirements.md#req-fo-3-4) |
| <span id="ut-06"></span>UT-06 · H · граничный | `ProgramExerciseInput.model_validate()` · `schemas/training.py` · [T-01](01_Architecture.md#alg-T-01) | exercise_id=10, position=1; пары (planned_sets,planned_reps) = (1,0), (0,1), (1,−1), (1.5,2). | Первая пара принята. Остальные отклонены по planned_sets или planned_reps. | [ФТ 5.3](02_Requirements.md#req-ft-5-3), [ФТ 5.4](02_Requirements.md#req-ft-5-4), [ФО 3.1](02_Requirements.md#req-fo-3-1), [ФО 3.2](02_Requirements.md#req-fo-3-2) |
| <span id="ut-07"></span>UT-07 · H · негативный, позитивный | `WorkoutCreateDTO.model_validate()` · `schemas/training.py` · [T-02](01_Architecture.md#alg-T-02) | Дата 2026-10-09. Массив упражнений пуст; затем одна позиция с пустыми sets; затем одно упражнение с одним подходом 30×10. | В первых двух случаях ошибка в exercises или exercises.0.sets. Последний вход принят. | [ФТ 6.1](02_Requirements.md#req-ft-6-1), [ФТ 6.2](02_Requirements.md#req-ft-6-2), [ФТ 6.3](02_Requirements.md#req-ft-6-3), [ФТ 6.6](02_Requirements.md#req-ft-6-6), [ФО 3.6](02_Requirements.md#req-fo-3-6) |
| <span id="ut-08"></span>UT-08 · H · граничный | `SetInput.model_validate()` · `schemas/training.py` · [T-02](01_Architecture.md#alg-T-02) | set_number=1. Пары (repetitions,weight) = (0,0), (1,0.01), (−1,30), (2,−0.01), (2.5,30). | Две первые пары приняты. Остальные дают ValidationError по соответствующему полю. | [ФТ 6.4](02_Requirements.md#req-ft-6-4), [ФТ 6.5](02_Requirements.md#req-ft-6-5), [ФО 3.2](02_Requirements.md#req-fo-3-2), [ФО 3.3](02_Requirements.md#req-fo-3-3) |
| <span id="ut-09"></span>UT-09 · H · граничный | `DateRangeDTO.model_validate()` · `schemas/statistics.py` · [S-01](01_Architecture.md#alg-S-01) | 09.10–09.10, только date_from=09.10, 10.10–09.10. Даты передаются в ISO. | Один день и открытая граница допустимы; обратный диапазон даёт ValidationError. | [ФТ 8.1](02_Requirements.md#req-ft-8-1), [ФТ 7.3](02_Requirements.md#req-ft-7-3), [ФТ 8.6](02_Requirements.md#req-ft-8-6) |
| <span id="ut-10"></span>UT-10 · H · позитивный, конфликт | `program_revision()` · `services/training_service.py` · [T-01](01_Architecture.md#alg-T-01) | Два снимка одного плана с теми же id и значениями, строки перечислены в разном порядке. В третьем меняется planned_reps с 10 на 8. | У первых двух один и тот же 64-значный hex-результат после сортировки по position. У третьего иное значение. | [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.7](02_Requirements.md#req-fo-3-7) |
| <span id="ut-11"></span>UT-11 · M · граничный | `is_new_record()` · `services/statistics_service.py` · [S-05](01_Architecture.md#alg-S-05) | (предыдущий максимум, новый) = (32,34), (34,34), (34,32), (нет,32). | True, False, False, False. Первая запись устанавливает базовый максимум, сообщение о превышении требует прежний результат. | [ФТ 9.1](02_Requirements.md#req-ft-9-1), [ФТ 9.2](02_Requirements.md#req-ft-9-2) |
| <span id="ut-12"></span>UT-12 · M · граничный | `new_award_codes()` · `services/achievements_service.py` · [S-06](01_Architecture.md#alg-S-06) | Число тренировок 0, 1, 9, 10, 100. В первых двух случаях выданных кодов нет, при 9 и 10 уже есть workout_1, при 100 есть workout_1 и workout_10. | По порядку \[\], \[workout_1\], \[\], \[workout_10\], \[workout_100\]. | [ФТ 9.3](02_Requirements.md#req-ft-9-3), [ФТ 9.4](02_Requirements.md#req-ft-9-4) |
| <span id="ut-13"></span>UT-13 · M · позитивный, приватность | `visible_metrics()` · `services/social_service.py` · [P-01](01_Architecture.md#alg-P-01) | Масса 70.5, число 2. Для подтверждённого друга пары (показать массу, показать статистику): (false,false), (true,false), (false,true), (true,true). | В части метрик выходы {}, {current_weight:70.5}, {workout_count:2} и оба ключа, согласно соответствующим флагам. | [ФТ 3.5](02_Requirements.md#req-ft-3-5), [ФТ 10.5](02_Requirements.md#req-ft-10-5), [ФО 5.3](02_Requirements.md#req-fo-5-3) |
| <span id="ut-14"></span>UT-14 · M · граничный | `BodyWeightInputDTO.model_validate()` · `schemas/auth.py` · [S-04](01_Architecture.md#alg-S-04) | Дата 2026-10-09; масса 70.25, 0, −1. Действительную дату сверяют в сервисе по часам приложения. | Первая масса принята. Остальные отклонены по weight. | [ФТ 8.7](02_Requirements.md#req-ft-8-7), [ФТ 8.8](02_Requirements.md#req-ft-8-8), [ФО 3.4](02_Requirements.md#req-fo-3-4) |
| <span id="ut-15"></span>UT-15 · L · позитивный, граничный | `rank_visible_members()` · `services/groups_service.py` · [G-02](01_Architecture.md#alg-G-02) | Уже разрешённые пары (id,число) = (11,2), (9,2), (8,3). Затем пустая выборка. | Порядок id 8,9,11 с местами 1,2,3. Для пустого входа — \[\]. | [ФТ 11.5](02_Requirements.md#req-ft-11-5) |
| <span id="ut-16"></span>UT-16 · L · негативный, граничный | `AIRequestDTO.model_validate()` · `schemas/ai.py` · [I-01](01_Architecture.md#alg-I-01) | sample с goal=Сила и duration_min=1, 180, 0, 181. Отдельно пустой text после обрезки пробелов. | 1 и 180 приняты. Остальные входы дают ошибку поля. | [ФТ 12.1](02_Requirements.md#req-ft-12-1), [ФТ 12.4](02_Requirements.md#req-ft-12-4) |
| <span id="ut-17"></span>UT-17 · L · позитивный, негативный | `normalize_response()` · `integrations/ai.py` · [I-01](01_Architecture.md#alg-I-01) | Ответ заглушки {choices:\[{message:{content:" Готово "}}\]}, затем пустой choices и пустой content. | Строка «Готово». Для двух некорректных ответов ошибка AI_UNAVAILABLE. | [ФТ 12.2](02_Requirements.md#req-ft-12-2), [ФО 6.2](02_Requirements.md#req-fo-6-2) |
| <span id="ut-18"></span>UT-18 · H · позитивный, негативный | `normalize_error()` · `core/errors.py` · [C-02](01_Architecture.md#alg-C-02) | Ошибка значения weight по пути exercises → 0 → sets → 1 → weight. | ErrorDTO с кодом INVALID_INPUT и details.field=exercises.0.sets.1.weight. | [ФТ 15.3](02_Requirements.md#req-ft-15-3), [ФО 2.3](02_Requirements.md#req-fo-2-3), [ФО 3.3](02_Requirements.md#req-fo-3-3) |
| <span id="ut-19"></span>UT-19 · H · негативный | `ProgramPatchDTO.model_validate()` · `schemas/training.py` · [T-01](01_Architecture.md#alg-T-01) | {exercises:\[\]} без expected_revision; затем тот же объект с корректной 64-значной ревизией. | Первый вход отклонён; второй описывает допустимую команду очистки состава. | [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.7](02_Requirements.md#req-fo-3-7) |
| <span id="ut-20"></span>UT-20 · H · позитивный, граничный | `resolveRoute()` · `app/routes.jsx` · [C-01](01_Architecture.md#alg-C-01) | Гость + /app/workouts/new; А + /login; user без роли admin + /app/admin при включённом admin. | Маршрут входа /login; личная главная /app; состояние «Нет доступа». Проверка в браузере дополняет серверную авторизацию. | [ФТ 15.1](02_Requirements.md#req-ft-15-1), [ФО 1.1](02_Requirements.md#req-fo-1-1), [ФО 1.2](02_Requirements.md#req-fo-1-2), [ФО 1.5](02_Requirements.md#req-fo-1-5) |
| <span id="ut-21"></span>UT-21 · H · позитивный, граничный | `toWorkoutPayload()` · `components/WorkoutForm.jsx` · [C-02](01_Architecture.md#alg-C-02) | Черновик 2026-10-09, упражнение 10, позиция 1, подход 1, повторы «8», вес «12,5». Отдельно вес «−5». | Для первого входа JSON содержит date и exercises\[0\].sets\[0\] = {set_number:1,repetitions:8,weight:12.5}. Для второго — ошибка поля, запрос не отправляется. | [ФТ 6.3](02_Requirements.md#req-ft-6-3), [ФТ 6.4](02_Requirements.md#req-ft-6-4), [ФТ 6.5](02_Requirements.md#req-ft-6-5), [ФТ 15.3](02_Requirements.md#req-ft-15-3) |
| <span id="ut-22"></span>UT-22 · H · позитивный, порядок ответов | `acceptProgressResponse()` · `pages/StatisticsPage.jsx` · [C-03](01_Architecture.md#alg-C-03) | Текущий номер запроса 2. По очереди приходят результаты с номерами 2 и 1. | Возвращает true, затем false. На экране остаются данные упражнения из второго запроса. | [ФТ 8.2](02_Requirements.md#req-ft-8-2), [ФТ 8.5](02_Requirements.md#req-ft-8-5) |
| <span id="ut-23"></span>UT-23 · H · позитивный, граничный | `StatisticsService.workout_count()` · `services/statistics_service.py` · [S-01](01_Architecture.md#alg-S-01) | Подставной TrainingRepository возвращает последовательно 2 и 0; пользователь А, пустой диапазон дат. | SummaryDTO.workout_count равен соответственно 2 и 0. Репозиторий получает именно id А и обе открытые границы. | [ФТ 8.1](02_Requirements.md#req-ft-8-1), [ФО 4.1](02_Requirements.md#req-fo-4-1) |
| <span id="ut-24"></span>UT-24 · H · негативный | `TrainingService.get_workout()` · `services/training_service.py` · [T-03](01_Architecture.md#alg-T-03) | AuthContext Б, id=101. Подставной репозиторий возвращает отсутствие для пары (Б,101). | Предметная ошибка NOT_FOUND. Метод не пробует прочитать ту же запись без условия владельца. | [ФТ 7.2](02_Requirements.md#req-ft-7-2), [ФО 1.4](02_Requirements.md#req-fo-1-4) |

<span id="integration"></span>

<span id="Интеграционные_тесты"></span>

## Интеграционные тесты

Одна цепочка показывает прохождение данных через границы модулей. Последовательные HTTP-вызовы в одном сценарии получают свои ответы. Коды R ведут к контрактам с полным адресом, DTO и условиями доступа. При нескольких входах каждый ожидаемый результат относится к входу на той же позиции.

<span id="it-01"></span>

<span id="IT-01_·_Учётная_запись_и_сеанс"></span>

### IT-01 · Учётная запись и сеанс

**Тип** позитивный · H. [R01](01_Architecture.md#api-R01), [R02](01_Architecture.md#api-R02), [R04](01_Architecture.md#api-R04).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Свободный a@example.test, регламентный пароль; после регистрации вход и чтение /users/me с выданной cookie. | `register_route() → AuthService.register() → UsersRepository.insert_account() → UnitOfWork.commit()` · `login_route() → AuthService.login() → UsersRepository.insert_session()` · `get_me_route() → ProfileService.get_me()` | 201, 200, 200. Одна пара User/Profile, проверяемый хеш, одна активная сессия. В R04 тот же id и роль user; заголовок CSRF доступен клиенту. |

**Связь с требованиями** [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФТ 3.1](02_Requirements.md#req-ft-3-1), [ФО 2.2](02_Requirements.md#req-fo-2-2), [ФО 2.4](02_Requirements.md#req-fo-2-4).

<span id="it-02"></span>

<span id="IT-02_·_Проверки_адреса_и_пароля"></span>

### IT-02 · Проверки адреса и пароля

**Тип** негативный, конфликт · H. [R01](01_Architecture.md#api-R01), [R02](01_Architecture.md#api-R02).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Существующий A@example.test, повтор регистрации с иным регистром; отдельно неверный адрес и слишком короткий пароль; вход с неверным паролем. | `register_route() → AuthService.register() → UsersRepository.find_user_by_email()` · `login_route() → AuthService.login() → verify_password(). Неверный DTO останавливается до сервиса` | 409 EMAIL_TAKEN, 422 INVALID_INPUT, 401 INVALID_CREDENTIALS соответственно. В БД один аккаунт и исходное число сессий. |

**Связь с требованиями** [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФО 2.1](02_Requirements.md#req-fo-2-1), [ФО 2.3](02_Requirements.md#req-fo-2-3).

<span id="it-03"></span>

<span id="IT-03_·_Независимые_сеансы"></span>

### IT-03 · Независимые сеансы

<span id="T-INT-04"></span> **Тип** позитивный, изоляция · H. [R02](01_Architecture.md#api-R02), [R03](01_Architecture.md#api-R03), [R04](01_Architecture.md#api-R04).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Два клиента вошли как А. Клиент 1 выходит с собственным CSRF; каждый вызывает R04. | `logout_route() → AuthService.logout() → UsersRepository.revoke_session() → UnitOfWork.commit()` · `require_auth() → AuthService.get_current_user() → UsersRepository.get_session()` | 204 при выходе, затем 401 у клиента 1 и 200 у клиента 2. Отозвана только первая строка AuthSession. |

**Связь с требованиями** [ФТ 2.2](02_Requirements.md#req-ft-2-2), [ФТ 2.3](02_Requirements.md#req-ft-2-3), [ФО 1.2](02_Requirements.md#req-fo-1-2).

<span id="it-04"></span>

<span id="IT-04_·_Проверка_владельца"></span>

### IT-04 · Проверка владельца

**Тип** негативный · H. [R05](01_Architecture.md#api-R05), [R12](01_Architecture.md#api-R12), [R13](01_Architecture.md#api-R13), [R17](01_Architecture.md#api-R17).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| А владеет планом P и занятием W. С cookie Б прочитать P/W и отправить PATCH P. Отдельно передать user_id А при R05. | `require_auth() → AuthService.get_current_user()` · `update_program_route() → TrainingService.update_program() → TrainingRepository.get_program()` · `get_workout_route() → TrainingService.get_workout() → TrainingRepository.get_workout()` | 404 у всех обращений к чужим P/W, 422 у лишнего поля. Профиль и состав плана А неизменны. |

**Связь с требованиями** [ФО 1.3](02_Requirements.md#req-fo-1-3), [ФО 1.4](02_Requirements.md#req-fo-1-4), [ФО 3.5](02_Requirements.md#req-fo-3-5), [ФО 5.2](02_Requirements.md#req-fo-5-2), [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФТ 7.2](02_Requirements.md#req-ft-7-2).

<span id="it-05"></span>

<span id="IT-05_·_Отказы_до_записи"></span>

### IT-05 · Отказы до записи

<span id="T-INT-03"></span> **Тип** негативный · H. [R15](01_Architecture.md#api-R15).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Отправить корректное дерево: без cookie с допустимым Origin; с cookie и неверным Origin; с cookie и отсутствующим/чужим CSRF. | `require_auth() → AuthService.get_current_user()` · `require_origin() и require_csrf() → verify_csrf(). Сервис записи вызывается только после проверок` | 401 для гостя, 403 для остальных отказов. Счётчики Workout, WorkoutExercise, WorkoutSet неизменны. |

**Связь с требованиями** [ФО 1.2](02_Requirements.md#req-fo-1-2), [ФТ 6.6](02_Requirements.md#req-ft-6-6), [ФТ 15.3](02_Requirements.md#req-ft-15-3).

<span id="it-06"></span>

<span id="IT-06_·_Две_правки_одной_программы"></span>

### IT-06 · Две правки одной программы

<span id="T-INT-01"></span> **Тип** позитивный, конкурентный · H. [R10](01_Architecture.md#api-R10), [R11](01_Architecture.md#api-R11), [R12](01_Architecture.md#api-R12), [R13](01_Architecture.md#api-R13).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Создать P с двумя упражнениями, два клиента А читают одну revision. Первый меняет порядок и имя полным PATCH, второй с исходной revision пробует удалить строку. | `create_program_route() → TrainingService.create_program() → TrainingRepository.insert_program()` · `update_program_route() → TrainingService.update_program() → TrainingRepository.get_program() → program_revision() → UnitOfWork.commit()` | 201 при создании, первый PATCH — 200, второй — 409 CONFLICT. Свежий R12 возвращает только правку первого, в R10 для P число 2. |

**Связь с требованиями** [ФТ 5.1](02_Requirements.md#req-ft-5-1), [ФТ 5.2](02_Requirements.md#req-ft-5-2), [ФТ 5.3](02_Requirements.md#req-ft-5-3), [ФТ 5.4](02_Requirements.md#req-ft-5-4), [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.1](02_Requirements.md#req-fo-3-1), [ФО 3.7](02_Requirements.md#req-fo-3-7).

<span id="it-07"></span>

<span id="IT-07_·_Откат_правки_плана"></span>

### IT-07 · Откат правки плана

<span id="T-INT-02"></span> **Тип** негативный, атомарность · H. [R12](01_Architecture.md#api-R12), [R13](01_Architecture.md#api-R13).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Снимок P с прежним названием и двумя строками. В тестовой точке после первой изменённой строки до commit вызвать управляемый сбой записи. Затем открыть R12 из другой сессии БД. | `update_program_route() → TrainingService.update_program() → TrainingRepository.get_program() → Session.flush() → UnitOfWork.rollback()` | 500 DATABASE_ERROR. Прежние название, id, порядок, значения и revision совпадают со снимком. |

**Связь с требованиями** [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.7](02_Requirements.md#req-fo-3-7), [ФТ 15.3](02_Requirements.md#req-ft-15-3).

<span id="it-08"></span>

<span id="IT-08_·_Сохранение_дерева_и_чтение"></span>

### IT-08 · Сохранение дерева и чтение

**Тип** позитивный · H. [R08](01_Architecture.md#api-R08), [R15](01_Architecture.md#api-R15), [R16](01_Architecture.md#api-R16), [R17](01_Architecture.md#api-R17).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Для А из R08 взять id жима. POST 09.10 с одним упражнением и подходами 30×10, 30×8, 32×6. Читать список и детали новой записью клиента. | `save_workout_route() → TrainingService.save_workout() → TrainingRepository.insert_workout() → Session.flush() → UnitOfWork.commit()` · `get_workout_route() → TrainingService.get_workout() → TrainingRepository.get_workout()` | 201 и id. В БД одна тренировка, одно выполнение и три подхода с непустыми FK; в R16 счётчики 1 и 3, в R17 нумерация 1,2,3. |

**Связь с требованиями** [ФТ 4.1](02_Requirements.md#req-ft-4-1), [ФТ 6.1](02_Requirements.md#req-ft-6-1), [ФТ 6.2](02_Requirements.md#req-ft-6-2), [ФТ 6.3](02_Requirements.md#req-ft-6-3), [ФТ 6.4](02_Requirements.md#req-ft-6-4), [ФТ 6.5](02_Requirements.md#req-ft-6-5), [ФТ 6.6](02_Requirements.md#req-ft-6-6), [ФТ 7.1](02_Requirements.md#req-ft-7-1), [ФТ 7.2](02_Requirements.md#req-ft-7-2), [ФО 3.5](02_Requirements.md#req-fo-3-5), [ФО 3.6](02_Requirements.md#req-fo-3-6).

<span id="it-09"></span>

<span id="IT-09_·_Откат_тренировки"></span>

### IT-09 · Откат тренировки

<span id="T-INT-05"></span> **Тип** негативный, атомарность · H. [R15](01_Architecture.md#api-R15), [R20](01_Architecture.md#api-R20).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Два упражнения. В тестовой точке репозитория после первой дочерней строки до commit вызвать сбой. После ответа подключиться отдельной сессией. | `save_workout_route() → TrainingService.save_workout() → TrainingRepository.insert_workout() → Session.flush() → UnitOfWork.rollback()` · `StatisticsService.workout_count() → TrainingRepository.count_workouts()` | 500 DATABASE_ERROR. Число строк во всех трёх таблицах и R20 не меняется; при включённых наградах нет выдач от этой попытки. |

**Связь с требованиями** [ФТ 6.6](02_Requirements.md#req-ft-6-6), [ФО 3.6](02_Requirements.md#req-fo-3-6), [ФО 3.7](02_Requirements.md#req-fo-3-7), [ФО 4.1](02_Requirements.md#req-fo-4-1).

<span id="it-10"></span>

<span id="IT-10_·_Агрегаты,_фильтры_и_состав_выборки"></span>

### IT-10 · Агрегаты, фильтры и состав выборки

**Тип** позитивный, граничный · H / M. [R16](01_Architecture.md#api-R16), [R20](01_Architecture.md#api-R20), [R21](01_Architecture.md#api-R21), [R22](01_Architecture.md#api-R22).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Два контрольных занятия А. В то же упражнение добавить подход 99×0, а Б дать 100×10. При включённом volume добавить упражнение с собственным весом в уже существующее занятие А. | `workout_count_route() → StatisticsService.workout_count() → TrainingRepository.count_workouts()` · `exercise_progress_route() → StatisticsService.exercise_progress() → TrainingRepository.progress_rows()` · `training_volume_route() → StatisticsService.training_volume() → TrainingRepository.sum_volume()` | R20=2. R21 даёт 32,34. При volume R22=1208; за 10.10 — 476. Условия пользователя, даты и типа нагрузки применены в SQL. Пустой диапазон даёт 0 и \[\]. |

**Связь с требованиями** [ФТ 7.3](02_Requirements.md#req-ft-7-3), [ФТ 7.4](02_Requirements.md#req-ft-7-4), [ФТ 8.1](02_Requirements.md#req-ft-8-1), [ФТ 8.2](02_Requirements.md#req-ft-8-2), [ФТ 8.4](02_Requirements.md#req-ft-8-4), [ФТ 8.5](02_Requirements.md#req-ft-8-5), [ФТ 8.6](02_Requirements.md#req-ft-8-6), [ФО 4.1](02_Requirements.md#req-fo-4-1), [ФО 4.2](02_Requirements.md#req-fo-4-2).

<span id="it-11"></span>

<span id="IT-11_·_Профиль_и_хронология_массы"></span>

### IT-11 · Профиль и хронология массы

**Тип** позитивный, конфликт · M. [R05](01_Architecture.md#api-R05), [R23](01_Architecture.md#api-R23), [R24](01_Architecture.md#api-R24), [R25](01_Architecture.md#api-R25).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| 09.10 — 70, 10.10 — 70.5. Исправить 09.10 на 69.8, повторить POST на 10.10. R05 с новой массой в день уже имеющегося измерения проверить при фиксированной дате 10.10. | `add_weight_route() → ProfileService.add_weight() → UsersRepository.get_profile() → UsersRepository.insert_weight() → UnitOfWork.commit()` · `update_weight_route() → ProfileService.update_weight() → UsersRepository.get_weight()` | 201,201,200,409. До R05 профиль 70.5, ряд \[69.8,70.5\]. После R05 масса сегодняшней строки и профиля обновлена одной транзакцией, записей по-прежнему две. |

**Связь с требованиями** [ФТ 3.2](02_Requirements.md#req-ft-3-2), [ФТ 8.3](02_Requirements.md#req-ft-8-3), [ФТ 8.7](02_Requirements.md#req-ft-8-7), [ФТ 8.8](02_Requirements.md#req-ft-8-8), [ФО 3.4](02_Requirements.md#req-fo-3-4).

<span id="it-12"></span>

<span id="IT-12_·_Согласие_и_публичная_карточка"></span>

### IT-12 · Согласие и публичная карточка

**Тип** позитивный, приватность · M. [R07](01_Architecture.md#api-R07), [R31](01_Architecture.md#api-R31), [R32](01_Architecture.md#api-R32), [R34](01_Architecture.md#api-R34).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| А и Б сначала без связи, затем pending, затем accepted. А разрешает только статистику, у А две тренировки. Б читает карточку А на каждом шаге. | `decide_request_route() → SocialService.decide_request() → SocialRepository.get_pair()` · `friend_profile_route() → SocialService.get_friend_profile() → SocialRepository.get_pair() → UsersRepository.get_settings() → visible_metrics()` | 404,404,200; для последнего ответа есть id, name, workout_count=2, ключ current_weight отсутствует. После удаления дружбы снова 404. |

**Связь с требованиями** [ФТ 3.5](02_Requirements.md#req-ft-3-5), [ФТ 10.2](02_Requirements.md#req-ft-10-2), [ФТ 10.3](02_Requirements.md#req-ft-10-3), [ФТ 10.4](02_Requirements.md#req-ft-10-4), [ФТ 10.5](02_Requirements.md#req-ft-10-5), [ФО 5.1](02_Requirements.md#req-fo-5-1), [ФО 5.3](02_Requirements.md#req-fo-5-3).

<span id="it-13"></span>

<span id="IT-13_·_Блокировка_и_администрирование_справочника"></span>

### IT-13 · Блокировка и администрирование справочника

**Тип** позитивный, права · M. [R35](01_Architecture.md#api-R35), [R36](01_Architecture.md#api-R36), [R37](01_Architecture.md#api-R37), [R38](01_Architecture.md#api-R38).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Б вошёл. На R35 и R36 действует зависимость require_admin(). Обычный А пытается прочитать R35. Admin блокирует Б, создаёт «Подъём на носки», меняет описание и разблокирует Б. | `set_user_status_route() → AdminService.set_user_status() → UsersRepository.revoke_user_sessions() → UnitOfWork.commit()` · `create_exercise_route() → AdminService.create_exercise() → TrainingRepository.insert_exercise()` | А получает 403; изменение статуса 200. Старая cookie Б непригодна и после разблокировки, новый вход успешен. У созданного упражнения один id при создании 201 и правке 200. |

**Связь с требованиями** [ФТ 14.1](02_Requirements.md#req-ft-14-1), [ФТ 14.2](02_Requirements.md#req-ft-14-2), [ФТ 14.3](02_Requirements.md#req-ft-14-3), [ФТ 14.4](02_Requirements.md#req-ft-14-4), [ФТ 14.5](02_Requirements.md#req-ft-14-5), [ФО 1.5](02_Requirements.md#req-fo-1-5).

<span id="it-14"></span>

<span id="IT-14_·_Награда,_рекорд_и_уведомление"></span>

### IT-14 · Награда, рекорд и уведомление

**Тип** позитивный, повторная обработка · M / L. [R15](01_Architecture.md#api-R15), [R26](01_Architecture.md#api-R26), [R27](01_Architecture.md#api-R27), [R46](01_Architecture.md#api-R46).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Включить records, achievements; для события также notifications. А сохраняет два контрольных занятия. Повторно обработать первое событие с тем же ключом. | `TrainingService.save_workout() → StatisticsService.find_new_records()` · `после записи дерева AchievementsService.award_for_workout() → new_award_codes() → NotificationsService.record_event() → UnitOfWork.commit()` | В R26 максимум 34, в результате второго сохранения — новый рекорд. В R27 одна workout_1. Для этого источника в R46 ровно одно уведомление, у Б его нет. |

**Связь с требованиями** [ФТ 9.1](02_Requirements.md#req-ft-9-1), [ФТ 9.2](02_Requirements.md#req-ft-9-2), [ФТ 9.3](02_Requirements.md#req-ft-9-3), [ФТ 9.4](02_Requirements.md#req-ft-9-4), [ФТ 13.1](02_Requirements.md#req-ft-13-1).

<span id="it-15"></span>

<span id="IT-15_·_Членство_и_рейтинг"></span>

### IT-15 · Членство и рейтинг

**Тип** позитивный, права · L. [R39](01_Architecture.md#api-R39), [R40](01_Architecture.md#api-R40), [R41](01_Architecture.md#api-R41), [R42](01_Architecture.md#api-R42), [R43](01_Architecture.md#api-R43), [R44](01_Architecture.md#api-R44).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| А создаёт группу, Б и В вступают. Для А видна статистика Б (3), собственная (2); В скрыт. Неучастник Г запрашивает рейтинг. | `create_group_route() → GroupsService.create_group() → SocialRepository.insert_group_with_owner()` · `ranking_route() → GroupsService.get_ranking() → StatisticsService.workout_count() → rank_visible_members()` | 201 с joined=true, членства созданы по одному. Участников трое, в рейтинге две строки \[Б,А\]. Г получает 404. После выхода Б участники \[А,В\] в порядке имён. |

**Связь с требованиями** [ФТ 11.1](02_Requirements.md#req-ft-11-1), [ФТ 11.2](02_Requirements.md#req-ft-11-2), [ФТ 11.3](02_Requirements.md#req-ft-11-3), [ФТ 11.4](02_Requirements.md#req-ft-11-4), [ФТ 11.5](02_Requirements.md#req-ft-11-5), [ФО 5.3](02_Requirements.md#req-fo-5-3).

<span id="it-16"></span>

<span id="IT-16_·_Обращение_к_помощнику"></span>

### IT-16 · Обращение к помощнику

**Тип** позитивный, отказ зависимости · L. [R45](01_Architecture.md#api-R45), [R16](01_Architecture.md#api-R16).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| У А 2 занятия, у Б 1. Заглушка записывает тело запроса: отдельно text, history, sample. В двух последних прогонах имитировать тайм-аут и пустой choices. | `answer_route() → AIService.answer() → TrainingRepository.history_context() для mode=history → AIAdapter.generate() → normalize_response()` | Три ответа 200 с текстом нужного режима. Контекст history содержит только упражнения и результаты А, без email, id аккаунта и комментариев. Оба отказа — 503 AI_UNAVAILABLE. R16 по-прежнему 200 и возвращает две записи. |

**Связь с требованиями** [ФТ 12.1](02_Requirements.md#req-ft-12-1), [ФТ 12.2](02_Requirements.md#req-ft-12-2), [ФТ 12.3](02_Requirements.md#req-ft-12-3), [ФТ 12.4](02_Requirements.md#req-ft-12-4), [ФО 6.1](02_Requirements.md#req-fo-6-1), [ФО 6.2](02_Requirements.md#req-fo-6-2), [ФО 6.3](02_Requirements.md#req-fo-6-3), [ФО 6.4](02_Requirements.md#req-fo-6-4).

<span id="it-17"></span>

<span id="IT-17_·_Изменение_и_удаление_занятия"></span>

### IT-17 · Изменение и удаление занятия

**Тип** позитивный, целостность · M. [R17](01_Architecture.md#api-R17), [R18](01_Architecture.md#api-R18), [R19](01_Architecture.md#api-R19), [R21](01_Architecture.md#api-R21).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| У занятия 10.10 заменить оба веса 34 на 35. Затем удалить это занятие. После каждой операции перечитать окно 09–10.10 и связанные строки. | `update_workout_route() → TrainingService.update_workout() → TrainingRepository.replace_workout_exercises() → UnitOfWork.commit()` · `delete_workout_route() → TrainingService.delete_workout() → Session.delete() → UnitOfWork.commit()` | 200, затем 204. Максимумы \[32,35\], затем \[32\]. После удаления у упражнения справочника тот же id, дочерних подходов удалённого занятия нет. |

**Связь с требованиями** [ФТ 6.7](02_Requirements.md#req-ft-6-7), [ФТ 6.8](02_Requirements.md#req-ft-6-8), [ФО 3.7](02_Requirements.md#req-fo-3-7), [ФО 4.3](02_Requirements.md#req-fo-4-3).

<span id="it-18"></span>

<span id="IT-18_·_Уведомление_о_заявке"></span>

### IT-18 · Уведомление о заявке

**Тип** позитивный, адресат · L. [R31](01_Architecture.md#api-R31), [R46](01_Architecture.md#api-R46).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| А отправляет запрос Б. А, Б и третий пользователь читают R46. Проверить запись по идемпотентному ключу исходного запроса. | `send_request_route() → SocialService.send_request() → SocialRepository.get_pair() → NotificationsService.record_event() → UnitOfWork.commit()` · `NotificationsService.list_notifications() → SocialRepository.list_notifications()` | 201 для запроса; у Б одна запись friend_request с соответствующим subject_id, у двух остальных этой записи нет. |

**Связь с требованиями** [ФТ 10.2](02_Requirements.md#req-ft-10-2), [ФТ 13.2](02_Requirements.md#req-ft-13-2).

<span id="it-19"></span>

<span id="IT-19_·_Пооперационная_правка_строки_программы"></span>

### IT-19 · Пооперационная правка строки программы

**Тип** позитивный, граничный · H. [R47](01_Architecture.md#api-R47), [R48](01_Architecture.md#api-R48), [R49](01_Architecture.md#api-R49), [R12](01_Architecture.md#api-R12).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| В свой пустой P добавить жим 3×10 в позиции 1, изменить повторения на 8, удалить строку. Каждая команда содержит действующую сессию и CSRF. | `TrainingService.add_program_exercise() → TrainingRepository.add_program_exercise()` · `TrainingService.update_program_exercise() → TrainingRepository.update_program_exercise()` · `TrainingService.remove_program_exercise() → TrainingRepository.remove_program_exercise()` | 201,200,200 и актуальный ProgramDTO после каждой команды. R12 в конце возвращает пустой состав. Ссылка на entry_id другого плана даёт 404. |

**Связь с требованиями** [ФТ 5.3](02_Requirements.md#req-ft-5-3), [ФТ 5.4](02_Requirements.md#req-ft-5-4), [ФТ 5.5](02_Requirements.md#req-ft-5-5).

<span id="it-20"></span>

<span id="IT-20_·_Неверное_поле_и_стабильное_сообщение"></span>

### IT-20 · Неверное поле и стабильное сообщение

**Тип** негативный, обработка ошибок · H. [R15](01_Architecture.md#api-R15).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Второй подход жима содержит weight=−5. Отправить напрямую через TestClient в JSON и сосчитать строки до и после. | `FastAPI → WorkoutCreateDTO.model_validate() → normalize_error() → ErrorDTO` · `TrainingService.save_workout() при ошибочном DTO не вызывается` | 422 INVALID_INPUT, details.field=exercises.0.sets.1.weight. Нет новых тренировок, упражнений и подходов. |

**Связь с требованиями** [ФТ 15.3](02_Requirements.md#req-ft-15-3), [ФО 3.2](02_Requirements.md#req-fo-3-2), [ФО 3.3](02_Requirements.md#req-fo-3-3), [ФО 2.3](02_Requirements.md#req-fo-2-3).

<span id="it-21"></span>

<span id="IT-21_·_Каталог,_поиск_и_отдельная_программа"></span>

### IT-21 · Каталог, поиск и отдельная программа

**Тип** позитивный · M. [R08](01_Architecture.md#api-R08), [R09](01_Architecture.md#api-R09), [R14](01_Architecture.md#api-R14).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Один жим с id=10 и одна тяга. Искать «ЖиМ», открыть R09 для id=10. Затем удалить собственный план, включавший жим. | `list_exercises_route() → TrainingService.list_exercises() → TrainingRepository.find_exercises()` · `delete_program_route() → TrainingService.delete_program() → TrainingRepository.get_program() → Session.delete() → UnitOfWork.commit()` | R08 и R09 возвращают один и тот же id=10. Удаление даёт 204. Строки этого плана удалены, число Exercise и Workout прежнее. |

**Связь с требованиями** [ФТ 4.2](02_Requirements.md#req-ft-4-2), [ФТ 4.3](02_Requirements.md#req-ft-4-3), [ФТ 5.6](02_Requirements.md#req-ft-5-6), [ФО 3.7](02_Requirements.md#req-fo-3-7).

<span id="it-22"></span>

<span id="IT-22_·_Уникальность_регистрации_в_двух_запросах"></span>

### IT-22 · Уникальность регистрации в двух запросах

**Тип** конкурентный, негативный · H. [R01](01_Architecture.md#api-R01).

| Вход и предусловие | Проверяемые вызовы | Ожидаемый ответ и состояние |
|---|---|---|
| Два клиента и две независимые транзакции пытаются зарегистрировать один нормализованный адрес. Синхронизировать обе попытки до вставки. | `register_route() → AuthService.register() → UsersRepository.find_user_by_email() → UsersRepository.insert_account() → UnitOfWork.commit() либо UnitOfWork.rollback()` | Один ответ 201 и один 409 EMAIL_TAKEN, ни одного 500. Новой учётной записи соответствует ровно один профиль. |

**Связь с требованиями** [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФО 2.1](02_Requirements.md#req-fo-2-1).

<span id="acceptance"></span>

<span id="Аттестационные_тесты"></span>

## Аттестационные тесты

Шаги выполняются через видимый интерфейс, если в сценарии отдельно не указан просмотр доказательства внутреннего ограничения. В примерах А и Б используют разные профили браузера. Для сценариев, где названа настройка M/L, она должна быть включена.

<span id="at-01"></span>

<span id="AT-01_·_Регистрация_и_вход"></span>

### AT-01 · Регистрация и вход

**Тип** позитивный · H.

**Исходное состояние** Чистый браузер, свободный адрес new@example.test.

1.  Открыть гостевую → «Создать аккаунт».
2.  Ввести адрес и дважды тестовый пароль длиной 10 знаков. Нажать «Создать аккаунт».
3.  На открывшейся странице входа ввести те же данные и нажать «Войти» внутри формы.

**Ожидаемый результат** После регистрации видны форма входа и подтверждение. После входа открывается 04 с личным меню. В «Профиле» видны поля нового аккаунта.

**Требования** [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФТ 3.1](02_Requirements.md#req-ft-3-1), [ФТ 15.2](02_Requirements.md#req-ft-15-2), [ФО 7.1](02_Requirements.md#req-fo-7-1).

<span id="at-02"></span>

<span id="AT-02_·_Проверки_регистрации_и_входа"></span>

### AT-02 · Проверки регистрации и входа

**Тип** негативный, граничный · H.

**Исходное состояние** Есть аккаунт А.

1.  В регистрации ввести некорректный адрес, затем корректный адрес с паролем из 7 знаков.
2.  Повторить с паролем из 8 знаков, но другим подтверждением.
3.  Ввести занятый адрес А и дважды допустимый пароль.
4.  На экране входа попробовать неверный пароль.

**Ожидаемый результат** Каждая ошибка оставляет пользователя в соответствующей форме. Видны причина и поле, пароль остаётся скрытым. Для занятого адреса второй аккаунт не появляется. Даже при обходе проверки формы сервер отклоняет неверные поля (IT-02).

**Требования** [ФТ 1.1](02_Requirements.md#req-ft-1-1), [ФТ 2.1](02_Requirements.md#req-ft-2-1), [ФТ 15.3](02_Requirements.md#req-ft-15-3), [ФО 2.1](02_Requirements.md#req-fo-2-1), [ФО 2.3](02_Requirements.md#req-fo-2-3).

<span id="at-03"></span>

<span id="AT-03_·_Выход_и_закрытый_раздел"></span>

### AT-03 · Выход и закрытый раздел

**Тип** позитивный, негативный · H.

**Исходное состояние** А вошёл, открыта история.

1.  Нажать «Выйти» в верхней панели.
2.  Вставить в адресную строку /app/workouts/new, затем открыть /app/workouts.

**Ожидаемый результат** После выхода видна гостевая. При прямом переходе открывается вход. История и форма записи гостю недоступны.

**Требования** [ФТ 2.2](02_Requirements.md#req-ft-2-2), [ФТ 15.1](02_Requirements.md#req-ft-15-1), [ФО 1.1](02_Requirements.md#req-fo-1-1), [ФО 1.2](02_Requirements.md#req-fo-1-2).

<span id="at-04"></span>

<span id="AT-04_·_Сохранение_сеанса"></span>

### AT-04 · Сохранение сеанса

**Тип** позитивный · M.

**Исходное состояние** Включён remember_me. Новый профиль браузера без восстановления вкладок.

1.  На 02 ввести данные А, включить «Запомнить меня», войти.
2.  Полностью закрыть и снова запустить браузер до истечения сеанса, открыть /app.
3.  Выйти и повторно открыть адрес.

**Ожидаемый результат** Сначала открывается личная главная А. После явного выхода требуется повторный вход.

**Требования** [ФТ 2.3](02_Requirements.md#req-ft-2-3).

<span id="at-05"></span>

<span id="AT-05_·_Профиль_и_его_поля"></span>

### AT-05 · Профиль и его поля

**Тип** позитивный, граничный · H.

**Исходное состояние** А вошёл.

1.  Открыть «Профиль».
2.  Указать имя «Александр», рост 180 см, массу 70,5 кг и цель «Набор массы». Нажать «Сохранить изменения».
3.  Обновить страницу, затем поочерёдно попробовать сохранить рост 0 и массу −1.

**Ожидаемый результат** После обновления показаны 180, 70,5 и новая цель. Для каждого недопустимого значения есть сообщение у поля. При повторном открытии сохранённые значения прежние.

**Требования** [ФТ 3.1](02_Requirements.md#req-ft-3-1), [ФТ 3.2](02_Requirements.md#req-ft-3-2), [ФТ 3.3](02_Requirements.md#req-ft-3-3), [ФТ 15.2](02_Requirements.md#req-ft-15-2), [ФТ 15.3](02_Requirements.md#req-ft-15-3), [ФО 3.4](02_Requirements.md#req-fo-3-4), [ФО 2.4](02_Requirements.md#req-fo-2-4).

<span id="at-06"></span>

<span id="AT-06_·_Чтение_справочника"></span>

### AT-06 · Чтение справочника

**Тип** позитивный · H.

**Исходное состояние** В справочнике есть «Жим гантелей» и «Тяга верхнего блока».

1.  Нажать «Упражнения» в боковом меню.
2.  Прочитать строки списка.
3.  Открыть новую программу и нажать «+ Добавить упражнение».

**Ожидаемый результат** В разделе показаны имена и тип нагрузки. В диалоге выбора доступны те же упражнения. При выборе в программу передаётся одна запись справочника.

**Требования** [ФТ 4.1](02_Requirements.md#req-ft-4-1), [ФТ 5.3](02_Requirements.md#req-ft-5-3).

<span id="at-07"></span>

<span id="AT-07_·_Поиск_и_подробности_упражнения"></span>

### AT-07 · Поиск и подробности упражнения

**Тип** позитивный, граничный · M.

**Исходное состояние** Включены exercise_search и exercise_details.

1.  На 06 ввести «жИм», выделить «Жим гантелей», нажать «Подробнее».
2.  Закрыть карточку и ввести «несуществующее000». Очистить строку.

**Ожидаемый результат** Поиск игнорирует регистр. Карточка показывает название, описание и тип нагрузки. При отсутствии совпадений виден пустой результат, очистка восстанавливает каталог.

**Требования** [ФТ 4.2](02_Requirements.md#req-ft-4-2), [ФТ 4.3](02_Requirements.md#req-ft-4-3).

<span id="at-08"></span>

<span id="AT-08_·_Создание_и_изменение_плана"></span>

### AT-08 · Создание и изменение плана

**Тип** позитивный · H.

**Исходное состояние** У А нет плана «Тренировка груди». В истории А уже есть контрольная тренировка за 09.10.2026.

1.  На 07 нажать «+ Новая программа», ввести название и нажать «Сохранить».
2.  Выбрать созданную строку и нажать «Изменить». Нажать «+ Добавить упражнение», выбрать жим, указать 3 подхода и 10 повторений. Сохранить.
3.  Повторно открыть на правку, изменить повторения на 8, добавить тягу 2×12. Сохранить и нажать «Открыть».
4.  После сохранения плана открыть тренировку за 09.10.2026 в истории. Сверить упражнение, все три подхода и число сохранённых тренировок.

**Ожидаемый результат** В списке один новый план, у него два упражнения. В режиме чтения жим 3×8, тяга 2×12 в заданном порядке. В истории одна сохранённая тренировка за 09.10.2026 с жимом гантелей и тремя подходами 30 кг × 10, 30 кг × 8 и 32 кг × 6.

**Требования** [ФТ 5.1](02_Requirements.md#req-ft-5-1), [ФТ 5.2](02_Requirements.md#req-ft-5-2), [ФТ 5.3](02_Requirements.md#req-ft-5-3), [ФТ 5.4](02_Requirements.md#req-ft-5-4), [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.1](02_Requirements.md#req-fo-3-1), [ФО 2.4](02_Requirements.md#req-fo-2-4), [ФО 3.7](02_Requirements.md#req-fo-3-7).

<span id="at-09"></span>

<span id="AT-09_·_Границы_чисел_в_плане"></span>

### AT-09 · Границы чисел в плане

**Тип** граничный, негативный · H.

**Исходное состояние** Открыта правка собственного плана с одной строкой.

1.  Проверить по очереди подходы 0 и 1,5, затем ввести 1.
2.  Проверить повторения −1 и 1,5, затем сохранить 0.
3.  Вернуться в редактор, удалить строку, нажать «Отмена» и подтвердить выход без сохранения.

**Ожидаемый результат** Нулевые и дробные подходы, отрицательные и дробные повторения отвергаются. План 1×0 сохраняется. После отмены сохранённая строка по-прежнему в плане.

**Требования** [ФТ 5.4](02_Requirements.md#req-ft-5-4), [ФТ 5.5](02_Requirements.md#req-ft-5-5), [ФО 3.1](02_Requirements.md#req-fo-3-1), [ФО 3.2](02_Requirements.md#req-fo-3-2).

<span id="at-10"></span>

<span id="AT-10_·_Удаление_плана"></span>

### AT-10 · Удаление плана

**Тип** позитивный · M.

**Исходное состояние** Включён program_delete. У А есть план и две проведённые тренировки.

1.  На 07 выбрать план, нажать «Удалить», затем «Отмена».
2.  Снова нажать «Удалить», подтвердить. Открыть историю.

**Ожидаемый результат** После отмены план виден. После подтверждения его нет. Обе тренировки и их подходы доступны.

**Требования** [ФТ 5.6](02_Requirements.md#req-ft-5-6), [ФО 3.7](02_Requirements.md#req-fo-3-7).

<span id="at-11"></span>

<span id="AT-11_·_Запись_занятия_с_подходами"></span>

### AT-11 · Запись занятия с подходами

**Тип** позитивный · H.

**Исходное состояние** А, пустая история, карточка тренировки 09.

1.  Выбрать 09.10.2026, ввести «Вечерняя».
2.  Через «+ Упражнение» выбрать жим. В первом подходе ввести 10 повторений и 30 кг, через «+ Подход» добавить 8 при 30 кг и 6 при 32 кг.
3.  Нажать «Сохранить тренировку», открыть строку в истории.

**Ожидаемый результат** Открывается история с одной записью. На 11 видны дата, комментарий, одно упражнение и три соответствующих подхода. У Б новая строка отсутствует.

**Требования** [ФТ 6.1](02_Requirements.md#req-ft-6-1), [ФТ 6.2](02_Requirements.md#req-ft-6-2), [ФТ 6.3](02_Requirements.md#req-ft-6-3), [ФТ 6.4](02_Requirements.md#req-ft-6-4), [ФТ 6.5](02_Requirements.md#req-ft-6-5), [ФТ 6.6](02_Requirements.md#req-ft-6-6), [ФТ 7.2](02_Requirements.md#req-ft-7-2), [ФТ 15.2](02_Requirements.md#req-ft-15-2), [ФО 3.5](02_Requirements.md#req-fo-3-5), [ФО 3.6](02_Requirements.md#req-fo-3-6).

<span id="at-12"></span>

<span id="AT-12_·_Некорректный_и_нулевой_подход"></span>

### AT-12 · Некорректный и нулевой подход

**Тип** граничный, негативный · H.

**Исходное состояние** А, пустая история, на 09 выбран жим.

1.  Ввести 10 повторений и вес −5, нажать «Сохранить тренировку».
2.  Исправить вес на 0, проверить −1 и 1,5 в повторениях. Затем ввести 0 повторений и сохранить.
3.  Открыть детали и статистику упражнения.

**Ожидаемый результат** Ошибочные значения помечены, черновик сохранён на экране. После исправления записан один подход 0×0. Для жима нет точки прогресса, счётчик тренировок равен 1.

**Требования** [ФТ 6.4](02_Requirements.md#req-ft-6-4), [ФТ 6.5](02_Requirements.md#req-ft-6-5), [ФТ 15.3](02_Requirements.md#req-ft-15-3), [ФО 3.2](02_Requirements.md#req-fo-3-2), [ФО 3.3](02_Requirements.md#req-fo-3-3), [ФО 4.1](02_Requirements.md#req-fo-4-1).

<span id="at-13"></span>

<span id="AT-13_·_История,_повторное_чтение,_счётчик_и_динамика"></span>

### AT-13 · История, повторное чтение, счётчик и динамика

**Тип** позитивный · H.

**Исходное состояние** У А контрольные занятия 09 и 10 октября. У Б собственное отдельное занятие.

1.  У А открыть «История», открыть тренировку от 10.10.
2.  Сверить два подхода, вернуться в историю. Выйти, войти снова.
3.  Открыть «Статистика» и выбрать «Жим гантелей».

**Ожидаемый результат** Сначала показано 10.10, затем 09.10. В деталях от 10.10 записаны 34 кг × 8 и 34 кг × 6. Счётчик 2, таблица максимумов по возрастанию дат — 32 и 34 кг. Занятие Б не влияет на числа.

**Требования** [ФТ 7.1](02_Requirements.md#req-ft-7-1), [ФТ 7.2](02_Requirements.md#req-ft-7-2), [ФТ 8.1](02_Requirements.md#req-ft-8-1), [ФТ 8.2](02_Requirements.md#req-ft-8-2), [ФО 2.4](02_Requirements.md#req-fo-2-4), [ФО 4.1](02_Requirements.md#req-fo-4-1), [ФО 3.5](02_Requirements.md#req-fo-3-5).

<span id="at-14"></span>

<span id="AT-14_·_Границы_доступа_двух_владельцев"></span>

### AT-14 · Границы доступа двух владельцев

**Тип** негативный · H.

**Исходное состояние** Два независимых окна браузера, А и Б. У А есть программа и занятие, известны ссылки из его окна.

1.  От имени Б открыть свой профиль и историю.
2.  Вставить ссылку А на 11 и ссылку на редактор его программы.
3.  При включённой правке тренировок попробовать открыть и путь редактирования чужого занятия. Затем вернуться в окно А.

**Ожидаемый результат** У Б видны только собственные данные, чужие ссылки показывают «Запись не найдена». У А программа и тренировка с прежними значениями. IT-04 отдельно подтверждает серверную проверку владельца и поля user_id.

**Требования** [ФО 1.3](02_Requirements.md#req-fo-1-3), [ФО 1.4](02_Requirements.md#req-fo-1-4), [ФО 5.2](02_Requirements.md#req-fo-5-2), [ФТ 15.3](02_Requirements.md#req-ft-15-3).

<span id="at-15"></span>

<span id="AT-15_·_Правка,_удаление_и_пересчёт"></span>

### AT-15 · Правка, удаление и пересчёт

**Тип** позитивный · M.

**Исходное состояние** Включены workout_edit и workout_delete, контрольные занятия А.

1.  На 11 для 10.10 нажать «Редактировать», заменить оба веса 34 на 35 кг, сохранить.
2.  Проверить результат на 11 и 12.
3.  На 11 нажать «Удалить», сначала отменить, затем подтвердить и снова открыть 12.

**Ожидаемый результат** После правки у жима максимумы 32 и 35 кг. Отмена оставляет занятие. После удаления остаётся точка 32 кг и одна тренировка, справочник сохраняет упражнение.

**Требования** [ФТ 6.7](02_Requirements.md#req-ft-6-7), [ФТ 6.8](02_Requirements.md#req-ft-6-8), [ФО 3.7](02_Requirements.md#req-fo-3-7), [ФО 4.3](02_Requirements.md#req-fo-4-3).

<span id="at-16"></span>

<span id="AT-16_·_Фильтры_истории"></span>

### AT-16 · Фильтры истории

**Тип** позитивный, граничный · M.

**Исходное состояние** Включён history_filters. У А жим 09 и 10 октября, 11 октября только тяга.

1.  На 10 выбрать период 10–11 октября и упражнение «Жим гантелей».
2.  Выбрать «Все упражнения», затем «За всё время».

**Ожидаемый результат** В первом списке только 10 октября, при снятии ограничения по упражнению — 10 и 11 октября. После сброса видны три записи.

**Требования** [ФТ 7.3](02_Requirements.md#req-ft-7-3), [ФТ 7.4](02_Requirements.md#req-ft-7-4).

<span id="at-17"></span>

<span id="AT-17_·_Объём,_график_и_период"></span>

### AT-17 · Объём, график и период

**Тип** позитивный, граничный · M.

**Исходное состояние** Включены charts и volume. Два контрольных занятия.

1.  На 12 выбрать жим, нажать «График», установить 09–10 октября.
2.  Нажать «Тренировочный объём». Затем сузить период до 10.10 и выбрать пустой период.

**Ожидаемый результат** На графике 32 и 34 кг, объём 1208 кг·повт. Для 10.10 одна точка 34 кг и объём 476. В пустом периоде — сообщение об отсутствии данных и нулевой объём.

**Требования** [ФТ 8.4](02_Requirements.md#req-ft-8-4), [ФТ 8.5](02_Requirements.md#req-ft-8-5), [ФТ 8.6](02_Requirements.md#req-ft-8-6), [ФО 4.2](02_Requirements.md#req-fo-4-2).

<span id="at-18"></span>

<span id="AT-18_·_Масса_тела_и_последняя_дата"></span>

### AT-18 · Масса тела и последняя дата

**Тип** позитивный, граничный · M.

**Исходное состояние** Включён weight_history. У А нет измерений.

1.  Открыть «Измерения». Добавить 09.10 — 70,0 кг, затем 10.10 — 70,5 кг.
2.  У записи от 09.10 нажать «Изменить», установить 69,8 и сохранить.
3.  Вернуться в профиль, затем попробовать второе измерение за 10.10.

**Ожидаемый результат** В ряду по датам 69,8 и 70,5. В профиле остаётся 70,5. Дубликат даты отклонён, записей по-прежнему две.

**Требования** [ФТ 8.3](02_Requirements.md#req-ft-8-3), [ФТ 8.7](02_Requirements.md#req-ft-8-7), [ФТ 8.8](02_Requirements.md#req-ft-8-8).

<span id="at-19"></span>

<span id="AT-19_·_Рекорды,_награды_и_профиль"></span>

### AT-19 · Рекорды, награды и профиль

**Тип** позитивный, граничный · M.

**Исходное состояние** Включены profile_progress, records и achievements, у А пустая история.

1.  Сохранить контрольное занятие от 09.10, затем от 10.10.
2.  Прочитать сообщение о сохранении; открыть «Статистика» → «Личные рекорды», затем «Профиль».
3.  Сохранить третье занятие с тем же максимумом 34 кг.

**Ожидаемый результат** Первое занятие даёт «Первая тренировка», второе — новый рекорд 34 кг. До третьего занятия в профиле 2 тренировки и одна награда. Равные 34 кг не дают повторного рекорда, награда не дублируется.

**Требования** [ФТ 3.4](02_Requirements.md#req-ft-3-4), [ФТ 9.1](02_Requirements.md#req-ft-9-1), [ФТ 9.2](02_Requirements.md#req-ft-9-2), [ФТ 9.3](02_Requirements.md#req-ft-9-3), [ФТ 9.4](02_Requirements.md#req-ft-9-4).

<span id="at-20"></span>

<span id="AT-20_·_Запрос,_отказ,_подтверждение_и_удаление"></span>

### AT-20 · Запрос, отказ, подтверждение и удаление

**Тип** позитивный · M.

**Исходное состояние** Включён friends. А, Б и В — разные пользователи, связей нет.

1.  У А открыть «Друзья», найти Б по части имени и нажать «Добавить в друзья».
2.  У Б нажать «Принять». А открывает «Просмотреть».
3.  Пользователь В отправляет запрос Б; Б нажимает «Отклонить».
4.  А выбирает Б и подтверждает «Удалить из друзей».

**Ожидаемый результат** После принятия А и Б появляются в списках друг друга, карточка Б открывается. После отказа В отсутствует среди друзей. После удаления связь исчезает у обеих сторон.

**Требования** [ФТ 10.1](02_Requirements.md#req-ft-10-1), [ФТ 10.2](02_Requirements.md#req-ft-10-2), [ФТ 10.3](02_Requirements.md#req-ft-10-3), [ФТ 10.4](02_Requirements.md#req-ft-10-4), [ФТ 10.5](02_Requirements.md#req-ft-10-5), [ФО 5.1](02_Requirements.md#req-fo-5-1).

<span id="at-21"></span>

<span id="AT-21_·_Независимые_настройки_приватности"></span>

### AT-21 · Независимые настройки приватности

**Тип** позитивный, негативный · M.

**Исходное состояние** Включены friends и privacy. А и Б друзья; у А масса 70,5 и две тренировки.

1.  У А открыть «Профиль», установить массу «Только я», статистику «Друзья», нажать «Сохранить настройки».
2.  У Б открыть карточку А.
3.  У А поменять флаги местами. Повторно открыть карточку у Б; выйти и открыть /app/friends гостем.

**Ожидаемый результат** Сначала Б видит имя и число 2 без массы; затем имя и массу 70,5 без счётчика. Гостю предлагается вход. Ответ R34 проверяется дополнительно в IT-12.

**Требования** [ФТ 3.5](02_Requirements.md#req-ft-3-5), [ФТ 10.5](02_Requirements.md#req-ft-10-5), [ФО 5.1](02_Requirements.md#req-fo-5-1), [ФО 5.3](02_Requirements.md#req-fo-5-3).

<span id="at-22"></span>

<span id="AT-22_·_Администратор_и_обычный_пользователь"></span>

### AT-22 · Администратор и обычный пользователь

**Тип** позитивный, негативный · M.

**Исходное состояние** Включён admin. Отдельные окна администратора и пользователя Б.

1.  У Б открыть /app/admin.
2.  У администратора открыть «Администратор» → «Открыть список», выбрать Б → «Заблокировать», подтвердить.
3.  Проверить повторный вход Б, затем разблокировать Б и войти снова.

**Ожидаемый результат** Б не видит административные списки. Администратор видит статусы. После блокировки прекращается прежний сеанс Б, вход отклоняется. После разблокировки новый вход разрешён.

**Требования** [ФТ 14.1](02_Requirements.md#req-ft-14-1), [ФТ 14.2](02_Requirements.md#req-ft-14-2), [ФТ 14.5](02_Requirements.md#req-ft-14-5), [ФО 1.1](02_Requirements.md#req-fo-1-1), [ФО 1.5](02_Requirements.md#req-fo-1-5).

<span id="at-23"></span>

<span id="AT-23_·_Ведение_общего_справочника"></span>

### AT-23 · Ведение общего справочника

**Тип** позитивный · M.

**Исходное состояние** Включён admin. В справочнике нет «Подъём на носки».

1.  У администратора на 15 нажать «+ Добавить упражнение». Ввести «Подъём на носки», тип «Внешний вес», сохранить.
2.  Нажать «Изменить», дополнить описание, сохранить.
3.  У А открыть «Упражнения».

**Ожидаемый результат** В списке А одна запись с новым описанием и тем же именем. У А нет административных действий редактирования.

**Требования** [ФТ 14.3](02_Requirements.md#req-ft-14-3), [ФТ 14.4](02_Requirements.md#req-ft-14-4), [ФО 1.5](02_Requirements.md#req-fo-1-5).

<span id="at-24"></span>

<span id="AT-24_·_Группы_и_рейтинг"></span>

### AT-24 · Группы и рейтинг

**Тип** позитивный, негативный · L.

**Исходное состояние** Включены groups, friends и privacy. А и Б друзья, Б показывает статистику, В скрывает её. За неделю у А 2 и у Б 3 занятия.

1.  А открывает «Группы», создаёт «Секция». Б и В вступают в «Секцию».
2.  А открывает «Участники», затем «Рейтинг» за эту неделю.
3.  Б нажимает «Покинуть», подтверждает и снова пробует открыть состав по прямой ссылке.

**Ожидаемый результат** А сразу является участником. В составе три имени. В рейтинге Б — 1-е место с 3 занятиями, А — 2-е с 2, данных В нет. После выхода Б отсутствует в составе и не видит закрытый список.

**Требования** [ФТ 11.1](02_Requirements.md#req-ft-11-1), [ФТ 11.2](02_Requirements.md#req-ft-11-2), [ФТ 11.3](02_Requirements.md#req-ft-11-3), [ФТ 11.4](02_Requirements.md#req-ft-11-4), [ФТ 11.5](02_Requirements.md#req-ft-11-5), [ФО 5.3](02_Requirements.md#req-fo-5-3).

<span id="at-25"></span>

<span id="AT-25_·_Три_режима_помощника"></span>

### AT-25 · Три режима помощника

**Тип** позитивный · L.

**Исходное состояние** Включён AI, настроена заглушка с отдельным текстом для каждого режима. А имеет два занятия.

1.  На 18 выбрать «Вопрос», ввести «Каким был мой прогресс?» и отправить.
2.  Выбрать «Анализ истории», задать 09–10.10 и отправить.
3.  Выбрать «Пример тренировки», задать цель «Сила», 45 минут и гантели, отправить. Затем открыть историю.

**Ожидаемый результат** Для каждого режима показан соответствующий текст заглушки и подпись о справочном характере. После всех ответов в истории те же две записи, новых программ нет.

**Требования** [ФТ 12.1](02_Requirements.md#req-ft-12-1), [ФТ 12.2](02_Requirements.md#req-ft-12-2), [ФТ 12.3](02_Requirements.md#req-ft-12-3), [ФТ 12.4](02_Requirements.md#req-ft-12-4), [ФО 6.1](02_Requirements.md#req-fo-6-1), [ФО 6.3](02_Requirements.md#req-fo-6-3), [ФО 6.4](02_Requirements.md#req-fo-6-4).

<span id="at-26"></span>

<span id="AT-26_·_Дневник_при_недоступности_помощника"></span>

### AT-26 · Дневник при недоступности помощника

**Тип** негативный, устойчивость · H / L.

**Исходное состояние** Два прогона. В первом AI выключен. Во втором включён, заглушка отвечает с тайм-аутом.

1.  В первом прогоне открыть меню, создать тренировку и прочитать её в истории.
2.  Во втором открыть 18, отправить вопрос и дождаться сообщения. Затем на 09 записать ещё одно занятие и открыть его через 10.

**Ожидаемый результат** При отключении пункта 18 нет. При отказе ошибка показана в помощнике. В обоих прогонах тренировка сохраняется и читается. Ограничения доступа к основному дневнику действуют в обоих случаях.

**Требования** [ФТ 12.2](02_Requirements.md#req-ft-12-2), [ФО 6.1](02_Requirements.md#req-fo-6-1), [ФО 6.2](02_Requirements.md#req-fo-6-2).

<span id="at-27"></span>

<span id="AT-27_·_Уведомления"></span>

### AT-27 · Уведомления

**Тип** позитивный · L.

**Исходное состояние** Включены notifications, achievements и friends. А ещё не получал наград или запросов.

1.  А сохраняет первую тренировку. Б отправляет заявку А.
2.  У А открыть «Уведомления», нажать «Обновить», открыть достижение, вернуться в список, открыть запрос.
3.  Открыть список Б.

**Ожидаемый результат** У А ровно одно событие каждого типа. Переходы ведут к наградам (05) и входящим запросам (14). В списке Б этих событий А нет.

**Требования** [ФТ 13.1](02_Requirements.md#req-ft-13-1), [ФТ 13.2](02_Requirements.md#req-ft-13-2).

<span id="at-28"></span>

<span id="AT-28_·_Шапка,_меню_и_возвраты"></span>

### AT-28 · Шапка, меню и возвраты

<span id="T-SYS-01"></span>**Тип** позитивный, удобство использования · H.

**Исходное состояние** Чистый браузер, есть аккаунт А.

1.  С гостевой открыть «Регистрация», нажать GymTracker, затем «Войти» в шапке. Авторизоваться.
2.  С помощью Tab и Enter открыть каждую ссылку основного меню, на каждой странице нажать GymTracker.
3.  Прямой ссылкой открыть редактор программы, нажать «Отмена»; из прямой ссылки на занятие нажать «Вернуться к истории».

**Ожидаемый результат** Из регистрации логотип ведёт на гостевую, после входа — на 04. Меню выделяет текущий раздел, повторный выбор не меняет данные. Явные возвраты работают в новой вкладке и приводят на 07 и 10.

**Требования** [ФТ 15.1](02_Requirements.md#req-ft-15-1), [ФО 7.1](02_Requirements.md#req-fo-7-1).

<span id="at-29"></span>

<span id="AT-29_·_Узкое_окно_и_браузеры"></span>

### AT-29 · Узкое окно и браузеры

**Тип** совместимость, позитивный · H / M.

**Исходное состояние** Два браузера, актуальные Chrome и Firefox. Один адрес стенда и аккаунт А.

1.  В каждом браузере повторить вход и запись одного занятия в независимом наборе при ширине 1280, затем при 390 CSS-пикселях.
2.  На узком экране открыть и закрыть «Меню», выбрать историю, перемещаться по форме клавиатурой.
3.  На телефоне открыть тот же адрес и сверить запись.

**Ожидаемый результат** Все поля и кнопки доступны, фокус виден, после сохранения запись читается по тому же адресу. Для телефона используется тот же веб-клиент. Указать размеры и версии в журнале.

**Требования** [ФТ 15.1](02_Requirements.md#req-ft-15-1), [ФО 7.1](02_Requirements.md#req-fo-7-1), [ФО 7.2](02_Requirements.md#req-fo-7-2), [ФО 7.3](02_Requirements.md#req-fo-7-3).

<span id="at-30"></span>

<span id="AT-30_·_Сбой_при_чтении_или_отправке"></span>

### AT-30 · Сбой при чтении или отправке

**Тип** негативный, восстановление · H.

**Исходное состояние** Открыта свежая форма и доступен переключатель offline в DevTools.

1.  Отключить сеть при чтении истории. Восстановить связь и нажать «Повторить».
2.  Заполнить тренировку, отключить сеть до отправки, нажать сохранение. Проверить сообщение и черновик. Включить сеть, проверить историю и сохранить один раз, если записи нет.

**Ожидаемый результат** После повтора история загружается. При неуспешной отправке заполненные поля остаются. При неопределённом результате POST интерфейс предлагает сверить историю. Контрольное занятие видно один раз.

**Требования** [ФТ 15.2](02_Requirements.md#req-ft-15-2), [ФТ 15.3](02_Requirements.md#req-ft-15-3).

<span id="at-31"></span>

<span id="AT-31_·_Хранение_пароля_и_серверная_валидация"></span>

### AT-31 · Хранение пароля и серверная валидация

**Тип** приёмочный контроль хранения · H.

**Исходное состояние** Отдельная демонстрационная БД, учётная запись создаётся в ходе проверки.

1.  Создать тестовый аккаунт через 03 и войти.
2.  Вместе с инструктором открыть итог IT-01 и IT-02 для той же сборки и маскированную выборку по тестовому аккаунту.
3.  Проверить, что проверка пароля подтверждается библиотекой и неверный ввод сервер отвергает.

**Ожидаемый результат** Демонстрация подтверждает вход, наличие хеша Argon2id и отсутствие открытого пароля в записи; при неверном пароле сеанс не создан. В журнал попадают код теста и результат проверки без пароля, токенов или полного хеша.

**Требования** [ФО 2.2](02_Requirements.md#req-fo-2-2), [ФО 2.3](02_Requirements.md#req-fo-2-3).

<span id="at-32"></span>

<span id="AT-32_·_Ручной_ввод_тренировки"></span>

### AT-32 · Ручной ввод тренировки

**Тип** приёмка границ поставки · L.

**Исходное состояние** Веб-клиент в браузере телефона, поставка с каталогом упражнений.

1.  Открыть «Тренировка», посмотреть доступные источники данных и поля.
2.  Выбрать упражнение вручную, ввести 8 повторений и 10 кг, сохранить.
3.  Открыть подробности, сверить состав версии с описанием проекта.

**Ожидаемый результат** В деталях вручную введённый подход 8×10 кг. Подключение часов или загрузка видео не требуется; управление этими действиями и интерфейсы импорта в поставке отсутствуют.

**Требования** [ФО 7.4](02_Requirements.md#req-fo-7-4), [ФО 7.5](02_Requirements.md#req-fo-7-5).

<span id="at-33"></span>

<span id="AT-33_·_Основная_сборка_без_расширений"></span>

### AT-33 · Основная сборка без расширений

**Тип** позитивный, границы ролей · H.

**Исходное состояние** FEATURES пуст, AI_ENABLED=false. А и пустая история.

1.  Открыть сайт гостем, войти как А.
2.  Проверить меню, записать тренировку и открыть 12.
3.  Ввести адреса /app/admin и /app/assistant. Проверить состав маршрутов в материалах сборки.

**Ожидаемый результат** Работают семь основных пунктов, счётчик и таблица. Дополнительные страницы и административные данные недоступны. При включении admin проверка ролей продолжается в AT-22, при включении AI — проверки AT-25 и AT-26.

**Требования** [ФО 1.1](02_Requirements.md#req-fo-1-1), [ФО 1.5](02_Requirements.md#req-fo-1-5), [ФО 6.2](02_Requirements.md#req-fo-6-2), [ФО 6.3](02_Requirements.md#req-fo-6-3), [ФО 6.4](02_Requirements.md#req-fo-6-4).

<span id="coverage"></span>

<span id="Покрытие_требований_и_ограничений"></span>

## Покрытие требований и ограничений

По номеру требования можно открыть его формулировку, проектное решение и каждый сценарий. Обозначение «—» означает, что для этой строки отдельная проверка данного уровня не выделена.

<span id="tests-ft-H"></span>

<span id="Обязательные_функциональные_требования"></span>

### Обязательные функциональные требования

| ФТ или ФО | Архитектура | Блочные | Интеграционные | Аттестационные |
|---|---|---|---|---|
| <span id="test-ft-1-1"></span>[ФТ 1.1](02_Requirements.md#req-ft-1-1) · H | [Решение](01_Architecture.md#trace-ft-1-1) | [UT-01](#ut-01), [UT-02](#ut-02) | [IT-01](#it-01), [IT-02](#it-02), [IT-22](#it-22) | [AT-01](#at-01), [AT-02](#at-02) |
| <span id="test-ft-2-1"></span>[ФТ 2.1](02_Requirements.md#req-ft-2-1) · H | [Решение](01_Architecture.md#trace-ft-2-1) | [UT-01](#ut-01), [UT-03](#ut-03) | [IT-01](#it-01), [IT-02](#it-02) | [AT-01](#at-01), [AT-02](#at-02) |
| <span id="test-ft-2-2"></span>[ФТ 2.2](02_Requirements.md#req-ft-2-2) · H | [Решение](01_Architecture.md#trace-ft-2-2) | [UT-04](#ut-04) | [IT-03](#it-03) | [AT-03](#at-03) |
| <span id="test-ft-3-1"></span>[ФТ 3.1](02_Requirements.md#req-ft-3-1) · H | [Решение](01_Architecture.md#trace-ft-3-1) | — | [IT-01](#it-01) | [AT-01](#at-01), [AT-05](#at-05) |
| <span id="test-ft-3-2"></span>[ФТ 3.2](02_Requirements.md#req-ft-3-2) · H | [Решение](01_Architecture.md#trace-ft-3-2) | [UT-05](#ut-05) | [IT-11](#it-11) | [AT-05](#at-05) |
| <span id="test-ft-3-3"></span>[ФТ 3.3](02_Requirements.md#req-ft-3-3) · H | [Решение](01_Architecture.md#trace-ft-3-3) | [UT-05](#ut-05) | — | [AT-05](#at-05) |
| <span id="test-ft-4-1"></span>[ФТ 4.1](02_Requirements.md#req-ft-4-1) · H | [Решение](01_Architecture.md#trace-ft-4-1) | — | [IT-08](#it-08) | [AT-06](#at-06) |
| <span id="test-ft-5-1"></span>[ФТ 5.1](02_Requirements.md#req-ft-5-1) · H | [Решение](01_Architecture.md#trace-ft-5-1) | — | [IT-06](#it-06) | [AT-08](#at-08) |
| <span id="test-ft-5-2"></span>[ФТ 5.2](02_Requirements.md#req-ft-5-2) · H | [Решение](01_Architecture.md#trace-ft-5-2) | — | [IT-06](#it-06) | [AT-08](#at-08) |
| <span id="test-ft-5-3"></span>[ФТ 5.3](02_Requirements.md#req-ft-5-3) · H | [Решение](01_Architecture.md#trace-ft-5-3) | [UT-06](#ut-06) | [IT-06](#it-06), [IT-19](#it-19) | [AT-06](#at-06), [AT-08](#at-08) |
| <span id="test-ft-5-4"></span>[ФТ 5.4](02_Requirements.md#req-ft-5-4) · H | [Решение](01_Architecture.md#trace-ft-5-4) | [UT-06](#ut-06) | [IT-06](#it-06), [IT-19](#it-19) | [AT-08](#at-08), [AT-09](#at-09) |
| <span id="test-ft-5-5"></span>[ФТ 5.5](02_Requirements.md#req-ft-5-5) · H | [Решение](01_Architecture.md#trace-ft-5-5) | [UT-10](#ut-10), [UT-19](#ut-19) | [IT-04](#it-04), [IT-06](#it-06), [IT-07](#it-07), [IT-19](#it-19) | [AT-08](#at-08), [AT-09](#at-09) |
| <span id="test-ft-6-1"></span>[ФТ 6.1](02_Requirements.md#req-ft-6-1) · H | [Решение](01_Architecture.md#trace-ft-6-1) | [UT-07](#ut-07) | [IT-08](#it-08) | [AT-11](#at-11) |
| <span id="test-ft-6-2"></span>[ФТ 6.2](02_Requirements.md#req-ft-6-2) · H | [Решение](01_Architecture.md#trace-ft-6-2) | [UT-07](#ut-07) | [IT-08](#it-08) | [AT-11](#at-11) |
| <span id="test-ft-6-3"></span>[ФТ 6.3](02_Requirements.md#req-ft-6-3) · H | [Решение](01_Architecture.md#trace-ft-6-3) | [UT-07](#ut-07), [UT-21](#ut-21) | [IT-08](#it-08) | [AT-11](#at-11) |
| <span id="test-ft-6-4"></span>[ФТ 6.4](02_Requirements.md#req-ft-6-4) · H | [Решение](01_Architecture.md#trace-ft-6-4) | [UT-08](#ut-08), [UT-21](#ut-21) | [IT-08](#it-08) | [AT-11](#at-11), [AT-12](#at-12) |
| <span id="test-ft-6-5"></span>[ФТ 6.5](02_Requirements.md#req-ft-6-5) · H | [Решение](01_Architecture.md#trace-ft-6-5) | [UT-08](#ut-08), [UT-21](#ut-21) | [IT-08](#it-08) | [AT-11](#at-11), [AT-12](#at-12) |
| <span id="test-ft-6-6"></span>[ФТ 6.6](02_Requirements.md#req-ft-6-6) · H | [Решение](01_Architecture.md#trace-ft-6-6) | [UT-07](#ut-07) | [IT-05](#it-05), [IT-08](#it-08), [IT-09](#it-09) | [AT-11](#at-11) |
| <span id="test-ft-7-1"></span>[ФТ 7.1](02_Requirements.md#req-ft-7-1) · H | [Решение](01_Architecture.md#trace-ft-7-1) | — | [IT-08](#it-08) | [AT-13](#at-13) |
| <span id="test-ft-7-2"></span>[ФТ 7.2](02_Requirements.md#req-ft-7-2) · H | [Решение](01_Architecture.md#trace-ft-7-2) | [UT-24](#ut-24) | [IT-04](#it-04), [IT-08](#it-08) | [AT-11](#at-11), [AT-13](#at-13) |
| <span id="test-ft-8-1"></span>[ФТ 8.1](02_Requirements.md#req-ft-8-1) · H | [Решение](01_Architecture.md#trace-ft-8-1) | [UT-09](#ut-09), [UT-23](#ut-23) | [IT-10](#it-10) | [AT-13](#at-13) |
| <span id="test-ft-8-2"></span>[ФТ 8.2](02_Requirements.md#req-ft-8-2) · H | [Решение](01_Architecture.md#trace-ft-8-2) | [UT-22](#ut-22) | [IT-10](#it-10) | [AT-13](#at-13) |
| <span id="test-ft-15-1"></span>[ФТ 15.1](02_Requirements.md#req-ft-15-1) · H | [Решение](01_Architecture.md#trace-ft-15-1) | [UT-20](#ut-20) | — | [AT-03](#at-03), [AT-28](#at-28), [AT-29](#at-29) |
| <span id="test-ft-15-2"></span>[ФТ 15.2](02_Requirements.md#req-ft-15-2) · H | [Решение](01_Architecture.md#trace-ft-15-2) | — | — | [AT-01](#at-01), [AT-05](#at-05), [AT-11](#at-11), [AT-30](#at-30) |
| <span id="test-ft-15-3"></span>[ФТ 15.3](02_Requirements.md#req-ft-15-3) · H | [Решение](01_Architecture.md#trace-ft-15-3) | [UT-18](#ut-18), [UT-21](#ut-21) | [IT-05](#it-05), [IT-07](#it-07), [IT-20](#it-20) | [AT-02](#at-02), [AT-05](#at-05), [AT-12](#at-12), [AT-14](#at-14), [AT-30](#at-30) |

<span id="tests-ft-M"></span>

<span id="Дополнительные_функциональные_требования"></span>

### Дополнительные функциональные требования

| ФТ или ФО | Архитектура | Блочные | Интеграционные | Аттестационные |
|---|---|---|---|---|
| <span id="test-ft-2-3"></span>[ФТ 2.3](02_Requirements.md#req-ft-2-3) · M | [Решение](01_Architecture.md#trace-ft-2-3) | — | [IT-03](#it-03) | [AT-04](#at-04) |
| <span id="test-ft-3-4"></span>[ФТ 3.4](02_Requirements.md#req-ft-3-4) · M | [Решение](01_Architecture.md#trace-ft-3-4) | — | — | [AT-19](#at-19) |
| <span id="test-ft-3-5"></span>[ФТ 3.5](02_Requirements.md#req-ft-3-5) · M | [Решение](01_Architecture.md#trace-ft-3-5) | [UT-13](#ut-13) | [IT-12](#it-12) | [AT-21](#at-21) |
| <span id="test-ft-4-2"></span>[ФТ 4.2](02_Requirements.md#req-ft-4-2) · M | [Решение](01_Architecture.md#trace-ft-4-2) | — | [IT-21](#it-21) | [AT-07](#at-07) |
| <span id="test-ft-4-3"></span>[ФТ 4.3](02_Requirements.md#req-ft-4-3) · M | [Решение](01_Architecture.md#trace-ft-4-3) | — | [IT-21](#it-21) | [AT-07](#at-07) |
| <span id="test-ft-5-6"></span>[ФТ 5.6](02_Requirements.md#req-ft-5-6) · M | [Решение](01_Architecture.md#trace-ft-5-6) | — | [IT-21](#it-21) | [AT-10](#at-10) |
| <span id="test-ft-6-7"></span>[ФТ 6.7](02_Requirements.md#req-ft-6-7) · M | [Решение](01_Architecture.md#trace-ft-6-7) | — | [IT-17](#it-17) | [AT-15](#at-15) |
| <span id="test-ft-6-8"></span>[ФТ 6.8](02_Requirements.md#req-ft-6-8) · M | [Решение](01_Architecture.md#trace-ft-6-8) | — | [IT-17](#it-17) | [AT-15](#at-15) |
| <span id="test-ft-7-3"></span>[ФТ 7.3](02_Requirements.md#req-ft-7-3) · M | [Решение](01_Architecture.md#trace-ft-7-3) | [UT-09](#ut-09) | [IT-10](#it-10) | [AT-16](#at-16) |
| <span id="test-ft-7-4"></span>[ФТ 7.4](02_Requirements.md#req-ft-7-4) · M | [Решение](01_Architecture.md#trace-ft-7-4) | — | [IT-10](#it-10) | [AT-16](#at-16) |
| <span id="test-ft-8-3"></span>[ФТ 8.3](02_Requirements.md#req-ft-8-3) · M | [Решение](01_Architecture.md#trace-ft-8-3) | — | [IT-11](#it-11) | [AT-18](#at-18) |
| <span id="test-ft-8-4"></span>[ФТ 8.4](02_Requirements.md#req-ft-8-4) · M | [Решение](01_Architecture.md#trace-ft-8-4) | — | [IT-10](#it-10) | [AT-17](#at-17) |
| <span id="test-ft-8-5"></span>[ФТ 8.5](02_Requirements.md#req-ft-8-5) · M | [Решение](01_Architecture.md#trace-ft-8-5) | [UT-22](#ut-22) | [IT-10](#it-10) | [AT-17](#at-17) |
| <span id="test-ft-8-6"></span>[ФТ 8.6](02_Requirements.md#req-ft-8-6) · M | [Решение](01_Architecture.md#trace-ft-8-6) | [UT-09](#ut-09) | [IT-10](#it-10) | [AT-17](#at-17) |
| <span id="test-ft-8-7"></span>[ФТ 8.7](02_Requirements.md#req-ft-8-7) · M | [Решение](01_Architecture.md#trace-ft-8-7) | [UT-14](#ut-14) | [IT-11](#it-11) | [AT-18](#at-18) |
| <span id="test-ft-8-8"></span>[ФТ 8.8](02_Requirements.md#req-ft-8-8) · M | [Решение](01_Architecture.md#trace-ft-8-8) | [UT-14](#ut-14) | [IT-11](#it-11) | [AT-18](#at-18) |
| <span id="test-ft-9-1"></span>[ФТ 9.1](02_Requirements.md#req-ft-9-1) · M | [Решение](01_Architecture.md#trace-ft-9-1) | [UT-11](#ut-11) | [IT-14](#it-14) | [AT-19](#at-19) |
| <span id="test-ft-9-2"></span>[ФТ 9.2](02_Requirements.md#req-ft-9-2) · M | [Решение](01_Architecture.md#trace-ft-9-2) | [UT-11](#ut-11) | [IT-14](#it-14) | [AT-19](#at-19) |
| <span id="test-ft-9-3"></span>[ФТ 9.3](02_Requirements.md#req-ft-9-3) · M | [Решение](01_Architecture.md#trace-ft-9-3) | [UT-12](#ut-12) | [IT-14](#it-14) | [AT-19](#at-19) |
| <span id="test-ft-9-4"></span>[ФТ 9.4](02_Requirements.md#req-ft-9-4) · M | [Решение](01_Architecture.md#trace-ft-9-4) | [UT-12](#ut-12) | [IT-14](#it-14) | [AT-19](#at-19) |
| <span id="test-ft-10-1"></span>[ФТ 10.1](02_Requirements.md#req-ft-10-1) · M | [Решение](01_Architecture.md#trace-ft-10-1) | — | — | [AT-20](#at-20) |
| <span id="test-ft-10-2"></span>[ФТ 10.2](02_Requirements.md#req-ft-10-2) · M | [Решение](01_Architecture.md#trace-ft-10-2) | — | [IT-12](#it-12), [IT-18](#it-18) | [AT-20](#at-20) |
| <span id="test-ft-10-3"></span>[ФТ 10.3](02_Requirements.md#req-ft-10-3) · M | [Решение](01_Architecture.md#trace-ft-10-3) | — | [IT-12](#it-12) | [AT-20](#at-20) |
| <span id="test-ft-10-4"></span>[ФТ 10.4](02_Requirements.md#req-ft-10-4) · M | [Решение](01_Architecture.md#trace-ft-10-4) | — | [IT-12](#it-12) | [AT-20](#at-20) |
| <span id="test-ft-10-5"></span>[ФТ 10.5](02_Requirements.md#req-ft-10-5) · M | [Решение](01_Architecture.md#trace-ft-10-5) | [UT-13](#ut-13) | [IT-12](#it-12) | [AT-20](#at-20), [AT-21](#at-21) |
| <span id="test-ft-14-1"></span>[ФТ 14.1](02_Requirements.md#req-ft-14-1) · M | [Решение](01_Architecture.md#trace-ft-14-1) | — | [IT-13](#it-13) | [AT-22](#at-22) |
| <span id="test-ft-14-2"></span>[ФТ 14.2](02_Requirements.md#req-ft-14-2) · M | [Решение](01_Architecture.md#trace-ft-14-2) | — | [IT-13](#it-13) | [AT-22](#at-22) |
| <span id="test-ft-14-3"></span>[ФТ 14.3](02_Requirements.md#req-ft-14-3) · M | [Решение](01_Architecture.md#trace-ft-14-3) | — | [IT-13](#it-13) | [AT-23](#at-23) |
| <span id="test-ft-14-4"></span>[ФТ 14.4](02_Requirements.md#req-ft-14-4) · M | [Решение](01_Architecture.md#trace-ft-14-4) | — | [IT-13](#it-13) | [AT-23](#at-23) |
| <span id="test-ft-14-5"></span>[ФТ 14.5](02_Requirements.md#req-ft-14-5) · M | [Решение](01_Architecture.md#trace-ft-14-5) | — | [IT-13](#it-13) | [AT-22](#at-22) |

<span id="tests-ft-L"></span>

<span id="Расширения"></span>

### Расширения

| ФТ или ФО | Архитектура | Блочные | Интеграционные | Аттестационные |
|---|---|---|---|---|
| <span id="test-ft-11-1"></span>[ФТ 11.1](02_Requirements.md#req-ft-11-1) · L | [Решение](01_Architecture.md#trace-ft-11-1) | — | [IT-15](#it-15) | [AT-24](#at-24) |
| <span id="test-ft-11-2"></span>[ФТ 11.2](02_Requirements.md#req-ft-11-2) · L | [Решение](01_Architecture.md#trace-ft-11-2) | — | [IT-15](#it-15) | [AT-24](#at-24) |
| <span id="test-ft-11-3"></span>[ФТ 11.3](02_Requirements.md#req-ft-11-3) · L | [Решение](01_Architecture.md#trace-ft-11-3) | — | [IT-15](#it-15) | [AT-24](#at-24) |
| <span id="test-ft-11-4"></span>[ФТ 11.4](02_Requirements.md#req-ft-11-4) · L | [Решение](01_Architecture.md#trace-ft-11-4) | — | [IT-15](#it-15) | [AT-24](#at-24) |
| <span id="test-ft-11-5"></span>[ФТ 11.5](02_Requirements.md#req-ft-11-5) · L | [Решение](01_Architecture.md#trace-ft-11-5) | [UT-15](#ut-15) | [IT-15](#it-15) | [AT-24](#at-24) |
| <span id="test-ft-12-1"></span>[ФТ 12.1](02_Requirements.md#req-ft-12-1) · L | [Решение](01_Architecture.md#trace-ft-12-1) | [UT-16](#ut-16) | [IT-16](#it-16) | [AT-25](#at-25) |
| <span id="test-ft-12-2"></span>[ФТ 12.2](02_Requirements.md#req-ft-12-2) · L | [Решение](01_Architecture.md#trace-ft-12-2) | [UT-17](#ut-17) | [IT-16](#it-16) | [AT-25](#at-25), [AT-26](#at-26) |
| <span id="test-ft-12-3"></span>[ФТ 12.3](02_Requirements.md#req-ft-12-3) · L | [Решение](01_Architecture.md#trace-ft-12-3) | — | [IT-16](#it-16) | [AT-25](#at-25) |
| <span id="test-ft-12-4"></span>[ФТ 12.4](02_Requirements.md#req-ft-12-4) · L | [Решение](01_Architecture.md#trace-ft-12-4) | [UT-16](#ut-16) | [IT-16](#it-16) | [AT-25](#at-25) |
| <span id="test-ft-13-1"></span>[ФТ 13.1](02_Requirements.md#req-ft-13-1) · L | [Решение](01_Architecture.md#trace-ft-13-1) | — | [IT-14](#it-14) | [AT-27](#at-27) |
| <span id="test-ft-13-2"></span>[ФТ 13.2](02_Requirements.md#req-ft-13-2) · L | [Решение](01_Architecture.md#trace-ft-13-2) | — | [IT-18](#it-18) | [AT-27](#at-27) |

<span id="tests-fo"></span>

<span id="Функциональные_ограничения"></span>

### Функциональные ограничения

| ФТ или ФО | Архитектура | Блочные | Интеграционные | Аттестационные |
|---|---|---|---|---|
| <span id="test-fo-1-1"></span>[ФО 1.1](02_Requirements.md#req-fo-1-1) · H | [Решение](01_Architecture.md#trace-fo-1-1) | [UT-20](#ut-20) | — | [AT-03](#at-03), [AT-22](#at-22), [AT-33](#at-33) |
| <span id="test-fo-1-2"></span>[ФО 1.2](02_Requirements.md#req-fo-1-2) · H | [Решение](01_Architecture.md#trace-fo-1-2) | [UT-04](#ut-04), [UT-20](#ut-20) | [IT-03](#it-03), [IT-05](#it-05) | [AT-03](#at-03) |
| <span id="test-fo-1-3"></span>[ФО 1.3](02_Requirements.md#req-fo-1-3) · H | [Решение](01_Architecture.md#trace-fo-1-3) | [UT-05](#ut-05) | [IT-04](#it-04) | [AT-14](#at-14) |
| <span id="test-fo-1-4"></span>[ФО 1.4](02_Requirements.md#req-fo-1-4) · H | [Решение](01_Architecture.md#trace-fo-1-4) | [UT-24](#ut-24) | [IT-04](#it-04) | [AT-14](#at-14) |
| <span id="test-fo-1-5"></span>[ФО 1.5](02_Requirements.md#req-fo-1-5) · H | [Решение](01_Architecture.md#trace-fo-1-5) | [UT-20](#ut-20) | [IT-13](#it-13) | [AT-22](#at-22), [AT-23](#at-23), [AT-33](#at-33) |
| <span id="test-fo-2-1"></span>[ФО 2.1](02_Requirements.md#req-fo-2-1) · H | [Решение](01_Architecture.md#trace-fo-2-1) | [UT-01](#ut-01) | [IT-02](#it-02), [IT-22](#it-22) | [AT-02](#at-02) |
| <span id="test-fo-2-2"></span>[ФО 2.2](02_Requirements.md#req-fo-2-2) · H | [Решение](01_Architecture.md#trace-fo-2-2) | [UT-03](#ut-03) | [IT-01](#it-01) | [AT-31](#at-31) |
| <span id="test-fo-2-3"></span>[ФО 2.3](02_Requirements.md#req-fo-2-3) · H | [Решение](01_Architecture.md#trace-fo-2-3) | [UT-02](#ut-02), [UT-18](#ut-18) | [IT-02](#it-02), [IT-20](#it-20) | [AT-02](#at-02), [AT-31](#at-31) |
| <span id="test-fo-2-4"></span>[ФО 2.4](02_Requirements.md#req-fo-2-4) · H | [Решение](01_Architecture.md#trace-fo-2-4) | — | [IT-01](#it-01) | [AT-05](#at-05), [AT-08](#at-08), [AT-13](#at-13) |
| <span id="test-fo-3-1"></span>[ФО 3.1](02_Requirements.md#req-fo-3-1) · H | [Решение](01_Architecture.md#trace-fo-3-1) | [UT-06](#ut-06) | [IT-06](#it-06) | [AT-08](#at-08), [AT-09](#at-09) |
| <span id="test-fo-3-2"></span>[ФО 3.2](02_Requirements.md#req-fo-3-2) · H | [Решение](01_Architecture.md#trace-fo-3-2) | [UT-06](#ut-06), [UT-08](#ut-08) | [IT-20](#it-20) | [AT-09](#at-09), [AT-12](#at-12) |
| <span id="test-fo-3-3"></span>[ФО 3.3](02_Requirements.md#req-fo-3-3) · H | [Решение](01_Architecture.md#trace-fo-3-3) | [UT-08](#ut-08), [UT-18](#ut-18) | [IT-20](#it-20) | [AT-12](#at-12) |
| <span id="test-fo-3-4"></span>[ФО 3.4](02_Requirements.md#req-fo-3-4) · H | [Решение](01_Architecture.md#trace-fo-3-4) | [UT-05](#ut-05), [UT-14](#ut-14) | [IT-11](#it-11) | [AT-05](#at-05) |
| <span id="test-fo-3-5"></span>[ФО 3.5](02_Requirements.md#req-fo-3-5) · H | [Решение](01_Architecture.md#trace-fo-3-5) | — | [IT-04](#it-04), [IT-08](#it-08) | [AT-11](#at-11), [AT-13](#at-13) |
| <span id="test-fo-3-6"></span>[ФО 3.6](02_Requirements.md#req-fo-3-6) · H | [Решение](01_Architecture.md#trace-fo-3-6) | [UT-07](#ut-07) | [IT-08](#it-08), [IT-09](#it-09) | [AT-11](#at-11) |
| <span id="test-fo-3-7"></span>[ФО 3.7](02_Requirements.md#req-fo-3-7) · H | [Решение](01_Architecture.md#trace-fo-3-7) | [UT-10](#ut-10), [UT-19](#ut-19) | [IT-06](#it-06), [IT-07](#it-07), [IT-09](#it-09), [IT-17](#it-17), [IT-21](#it-21) | [AT-08](#at-08), [AT-10](#at-10), [AT-15](#at-15) |
| <span id="test-fo-4-1"></span>[ФО 4.1](02_Requirements.md#req-fo-4-1) · H | [Решение](01_Architecture.md#trace-fo-4-1) | [UT-23](#ut-23) | [IT-09](#it-09), [IT-10](#it-10) | [AT-12](#at-12), [AT-13](#at-13) |
| <span id="test-fo-4-2"></span>[ФО 4.2](02_Requirements.md#req-fo-4-2) · M | [Решение](01_Architecture.md#trace-fo-4-2) | — | [IT-10](#it-10) | [AT-17](#at-17) |
| <span id="test-fo-4-3"></span>[ФО 4.3](02_Requirements.md#req-fo-4-3) · M | [Решение](01_Architecture.md#trace-fo-4-3) | — | [IT-17](#it-17) | [AT-15](#at-15) |
| <span id="test-fo-5-1"></span>[ФО 5.1](02_Requirements.md#req-fo-5-1) · M | [Решение](01_Architecture.md#trace-fo-5-1) | — | [IT-12](#it-12) | [AT-20](#at-20), [AT-21](#at-21) |
| <span id="test-fo-5-2"></span>[ФО 5.2](02_Requirements.md#req-fo-5-2) · H | [Решение](01_Architecture.md#trace-fo-5-2) | — | [IT-04](#it-04) | [AT-14](#at-14) |
| <span id="test-fo-5-3"></span>[ФО 5.3](02_Requirements.md#req-fo-5-3) · M | [Решение](01_Architecture.md#trace-fo-5-3) | [UT-13](#ut-13) | [IT-12](#it-12), [IT-15](#it-15) | [AT-21](#at-21), [AT-24](#at-24) |
| <span id="test-fo-6-1"></span>[ФО 6.1](02_Requirements.md#req-fo-6-1) · L | [Решение](01_Architecture.md#trace-fo-6-1) | — | [IT-16](#it-16) | [AT-25](#at-25), [AT-26](#at-26) |
| <span id="test-fo-6-2"></span>[ФО 6.2](02_Requirements.md#req-fo-6-2) · H | [Решение](01_Architecture.md#trace-fo-6-2) | [UT-17](#ut-17) | [IT-16](#it-16) | [AT-26](#at-26), [AT-33](#at-33) |
| <span id="test-fo-6-3"></span>[ФО 6.3](02_Requirements.md#req-fo-6-3) · H | [Решение](01_Architecture.md#trace-fo-6-3) | — | [IT-16](#it-16) | [AT-25](#at-25), [AT-33](#at-33) |
| <span id="test-fo-6-4"></span>[ФО 6.4](02_Requirements.md#req-fo-6-4) · H | [Решение](01_Architecture.md#trace-fo-6-4) | — | [IT-16](#it-16) | [AT-25](#at-25), [AT-33](#at-33) |
| <span id="test-fo-7-1"></span>[ФО 7.1](02_Requirements.md#req-fo-7-1) · H | [Решение](01_Architecture.md#trace-fo-7-1) | — | — | [AT-01](#at-01), [AT-28](#at-28), [AT-29](#at-29) |
| <span id="test-fo-7-2"></span>[ФО 7.2](02_Requirements.md#req-fo-7-2) · H | [Решение](01_Architecture.md#trace-fo-7-2) | — | — | [AT-29](#at-29) |
| <span id="test-fo-7-3"></span>[ФО 7.3](02_Requirements.md#req-fo-7-3) · M | [Решение](01_Architecture.md#trace-fo-7-3) | — | — | [AT-29](#at-29) |
| <span id="test-fo-7-4"></span>[ФО 7.4](02_Requirements.md#req-fo-7-4) · L | [Решение](01_Architecture.md#trace-fo-7-4) | — | — | [AT-32](#at-32) |
| <span id="test-fo-7-5"></span>[ФО 7.5](02_Requirements.md#req-fo-7-5) · L | [Решение](01_Architecture.md#trace-fo-7-5) | — | — | [AT-32](#at-32) |

<span id="test-exit"></span>

<span id="Критерий_и_фиксация_результата"></span>

## Критерий и фиксация результата

Успех отдельного теста требует совпадения всех наблюдений и отсутствия лишних записей. При расхождении записываются фактический результат, идентификатор дефекта и сборка. Исправление проверяется тем же тестом и затронутыми соседними сценариями. Обязательный набор принимается после успешного прохождения применимых проверок H. Отключённые расширения указываются отдельно; каждое включённое расширение проходит свои проверки и регрессию обязательного сценария.

[Журнал выполнения](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82_%D0%BE_%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B8_%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F) · [Список ошибок](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BE%D1%88%D0%B8%D0%B1%D0%BE%D0%BA) · [Метрики проекта](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%9C%D0%B5%D1%82%D1%80%D0%B8%D0%BA%D0%B8_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0)

<span id="Примеры_оформления_из_архива_курса"></span>

### Примеры оформления из архива курса

- [Fitness App — примеры входов, ожидаемых результатов и взаимодействия модулей](https://se.cs.petrsu.ru/wiki/Fitness_App:_%D0%9F%D0%BB%D0%B0%D0%BD_%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F).
- [Flixie — позитивные и негативные сценарии пользовательских действий](https://se.cs.petrsu.ru/wiki/Flixie:_%D0%9F%D0%BB%D0%B0%D0%BD_%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F).

Подробное описание команд и клиента для тестов приведено в документации. <a href="https://docs.pytest.org/en/stable/how-to/usage.html" class="external text" rel="nofollow">pytest</a>, <a href="https://fastapi.tiangolo.com/tutorial/testing/" class="external text" rel="nofollow">FastAPI TestClient</a>, <a href="https://vitest.dev/guide/cli.html" class="external text" rel="nofollow">Vitest CLI</a>.
