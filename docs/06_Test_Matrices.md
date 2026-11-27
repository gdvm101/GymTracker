# GymTracker · Матрицы тестирования

Редакция 26.11.2026. Строки — ФТ и ФО, столбцы — тесты. Откройте требование слева или карточку теста в заголовке. 🟩 П — позитивный вариант, 🟥 Н — негативный, 🟨 С — специальный. Несколько меток в клетке обозначают разные варианты одной карточки. Пустое поле означает отсутствие прямой связи.

[План тестирования](03_Test_Plan.md) · [Спецификация](02_Requirements.md) · [Архитектура](01_Architecture.md)

<span id="ut"></span>

## Блочные тесты

Матрица на вики с переходами к объектам проверки. [Открыть страницу](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%9C%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0_%D0%B1%D0%BB%D0%BE%D1%87%D0%BD%D1%8B%D1%85_%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2).

| ФТ / ФО | [UT-01](03_Test_Plan.md#ut-01) | [UT-02](03_Test_Plan.md#ut-02) | [UT-03](03_Test_Plan.md#ut-03) | [UT-04](03_Test_Plan.md#ut-04) | [UT-05](03_Test_Plan.md#ut-05) | [UT-06](03_Test_Plan.md#ut-06) |
|---|---|---|---|---|---|---|
| [ФТ 1.1](02_Requirements.md#req-ft-1-1) | 🟩 П | 🟨 С |   |   |   |   |
| [ФТ 2.1](02_Requirements.md#req-ft-2-1) | 🟩 П |   | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 2.2](02_Requirements.md#req-ft-2-2) |   |   |   | 🟥 Н |   |   |
| [ФТ 3.2](02_Requirements.md#req-ft-3-2) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 3.3](02_Requirements.md#req-ft-3-3) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 5.3](02_Requirements.md#req-ft-5-3) |   |   |   |   |   | 🟨 С |
| [ФТ 5.4](02_Requirements.md#req-ft-5-4) |   |   |   |   |   | 🟨 С |
| [ФО 1.2](02_Requirements.md#req-fo-1-2) |   |   |   | 🟩 П / 🟥 Н |   |   |
| [ФО 1.3](02_Requirements.md#req-fo-1-3) |   |   |   |   | 🟥 Н |   |
| [ФО 2.1](02_Requirements.md#req-fo-2-1) | 🟩 П |   |   |   |   |   |
| [ФО 2.2](02_Requirements.md#req-fo-2-2) |   |   | 🟩 П |   |   |   |
| [ФО 2.3](02_Requirements.md#req-fo-2-3) |   | 🟨 С |   |   |   |   |
| [ФО 3.1](02_Requirements.md#req-fo-3-1) |   |   |   |   |   | 🟨 С |
| [ФО 3.2](02_Requirements.md#req-fo-3-2) |   |   |   |   |   | 🟨 С |
| [ФО 3.4](02_Requirements.md#req-fo-3-4) |   |   |   |   | 🟨 С |   |

| ФТ / ФО | [UT-07](03_Test_Plan.md#ut-07) | [UT-08](03_Test_Plan.md#ut-08) | [UT-09](03_Test_Plan.md#ut-09) | [UT-10](03_Test_Plan.md#ut-10) | [UT-11](03_Test_Plan.md#ut-11) | [UT-12](03_Test_Plan.md#ut-12) |
|---|---|---|---|---|---|---|
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) |   |   |   | 🟨 С |   |   |
| [ФТ 6.1](02_Requirements.md#req-ft-6-1) | 🟥 Н |   |   |   |   |   |
| [ФТ 6.2](02_Requirements.md#req-ft-6-2) | 🟥 Н |   |   |   |   |   |
| [ФТ 6.3](02_Requirements.md#req-ft-6-3) | 🟥 Н |   |   |   |   |   |
| [ФТ 6.4](02_Requirements.md#req-ft-6-4) |   | 🟨 С |   |   |   |   |
| [ФТ 6.5](02_Requirements.md#req-ft-6-5) |   | 🟨 С |   |   |   |   |
| [ФТ 6.6](02_Requirements.md#req-ft-6-6) | 🟩 П / 🟥 Н |   |   |   |   |   |
| [ФТ 7.3](02_Requirements.md#req-ft-7-3) |   |   | 🟨 С |   |   |   |
| [ФТ 8.1](02_Requirements.md#req-ft-8-1) |   |   | 🟨 С |   |   |   |
| [ФТ 8.6](02_Requirements.md#req-ft-8-6) |   |   | 🟨 С |   |   |   |
| [ФТ 9.1](02_Requirements.md#req-ft-9-1) |   |   |   |   | 🟨 С |   |
| [ФТ 9.2](02_Requirements.md#req-ft-9-2) |   |   |   |   | 🟨 С |   |
| [ФТ 9.3](02_Requirements.md#req-ft-9-3) |   |   |   |   |   | 🟨 С |
| [ФТ 9.4](02_Requirements.md#req-ft-9-4) |   |   |   |   |   | 🟨 С |
| [ФО 3.2](02_Requirements.md#req-fo-3-2) |   | 🟨 С |   |   |   |   |
| [ФО 3.3](02_Requirements.md#req-fo-3-3) |   | 🟨 С |   |   |   |   |
| [ФО 3.6](02_Requirements.md#req-fo-3-6) | 🟩 П / 🟥 Н |   |   |   |   |   |

| ФТ / ФО | [UT-13](03_Test_Plan.md#ut-13) | [UT-14](03_Test_Plan.md#ut-14) | [UT-15](03_Test_Plan.md#ut-15) | [UT-16](03_Test_Plan.md#ut-16) | [UT-17](03_Test_Plan.md#ut-17) | [UT-18](03_Test_Plan.md#ut-18) |
|---|---|---|---|---|---|---|
| [ФТ 3.5](02_Requirements.md#req-ft-3-5) | 🟨 С |   |   |   |   |   |
| [ФТ 8.7](02_Requirements.md#req-ft-8-7) |   | 🟨 С |   |   |   |   |
| [ФТ 8.8](02_Requirements.md#req-ft-8-8) |   | 🟨 С |   |   |   |   |
| [ФТ 10.5](02_Requirements.md#req-ft-10-5) | 🟨 С |   |   |   |   |   |
| [ФТ 11.5](02_Requirements.md#req-ft-11-5) |   |   | 🟨 С |   |   |   |
| [ФТ 12.1](02_Requirements.md#req-ft-12-1) |   |   |   | 🟨 С |   |   |
| [ФТ 12.2](02_Requirements.md#req-ft-12-2) |   |   |   |   | 🟩 П |   |
| [ФТ 12.4](02_Requirements.md#req-ft-12-4) |   |   |   | 🟨 С |   |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   |   |   |   |   | 🟥 Н |
| [ФО 3.3](02_Requirements.md#req-fo-3-3) |   |   |   |   |   | 🟥 Н |
| [ФО 3.4](02_Requirements.md#req-fo-3-4) |   | 🟨 С |   |   |   |   |
| [ФО 5.3](02_Requirements.md#req-fo-5-3) | 🟩 П / 🟨 С |   |   |   |   |   |
| [ФО 6.2](02_Requirements.md#req-fo-6-2) |   |   |   |   | 🟥 Н |   |

| ФТ / ФО | [UT-19](03_Test_Plan.md#ut-19) | [UT-20](03_Test_Plan.md#ut-20) | [UT-21](03_Test_Plan.md#ut-21) | [UT-22](03_Test_Plan.md#ut-22) | [UT-23](03_Test_Plan.md#ut-23) | [UT-24](03_Test_Plan.md#ut-24) |
|---|---|---|---|---|---|---|
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) | 🟩 П / 🟥 Н |   |   |   |   |   |
| [ФТ 6.3](02_Requirements.md#req-ft-6-3) |   |   | 🟩 П |   |   |   |
| [ФТ 6.4](02_Requirements.md#req-ft-6-4) |   |   | 🟩 П |   |   |   |
| [ФТ 6.5](02_Requirements.md#req-ft-6-5) |   |   | 🟩 П |   |   |   |
| [ФТ 7.2](02_Requirements.md#req-ft-7-2) |   |   |   |   |   | 🟥 Н |
| [ФТ 8.1](02_Requirements.md#req-ft-8-1) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 8.2](02_Requirements.md#req-ft-8-2) |   |   |   | 🟨 С |   |   |
| [ФТ 8.5](02_Requirements.md#req-ft-8-5) |   |   |   | 🟨 С |   |   |
| [ФТ 15.1](02_Requirements.md#req-ft-15-1) |   | 🟨 С |   |   |   |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   |   | 🟥 Н |   |   |   |
| [ФО 1.1](02_Requirements.md#req-fo-1-1) |   | 🟨 С |   |   |   |   |
| [ФО 1.2](02_Requirements.md#req-fo-1-2) |   | 🟩 П / 🟥 Н |   |   |   |   |
| [ФО 1.4](02_Requirements.md#req-fo-1-4) |   |   |   |   |   | 🟥 Н |
| [ФО 1.5](02_Requirements.md#req-fo-1-5) |   | 🟥 Н |   |   |   |   |
| [ФО 4.1](02_Requirements.md#req-fo-4-1) |   |   |   |   | 🟩 П |   |

<span id="it"></span>

## Интеграционные тесты

Матрица на вики с переходами к объектам проверки. [Открыть страницу](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%9C%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0_%D0%B8%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2).

| ФТ / ФО | [IT-01](03_Test_Plan.md#it-01) | [IT-02](03_Test_Plan.md#it-02) | [IT-03](03_Test_Plan.md#it-03) | [IT-04](03_Test_Plan.md#it-04) | [IT-05](03_Test_Plan.md#it-05) | [IT-06](03_Test_Plan.md#it-06) |
|---|---|---|---|---|---|---|
| [ФТ 1.1](02_Requirements.md#req-ft-1-1) | 🟩 П | 🟥 Н |   |   |   |   |
| [ФТ 2.1](02_Requirements.md#req-ft-2-1) | 🟩 П | 🟥 Н |   |   |   |   |
| [ФТ 2.2](02_Requirements.md#req-ft-2-2) |   |   | 🟩 П |   |   |   |
| [ФТ 2.3](02_Requirements.md#req-ft-2-3) |   |   | 🟨 С |   |   |   |
| [ФТ 3.1](02_Requirements.md#req-ft-3-1) | 🟩 П |   |   |   |   |   |
| [ФТ 5.1](02_Requirements.md#req-ft-5-1) |   |   |   |   |   | 🟩 П |
| [ФТ 5.2](02_Requirements.md#req-ft-5-2) |   |   |   |   |   | 🟩 П |
| [ФТ 5.3](02_Requirements.md#req-ft-5-3) |   |   |   |   |   | 🟩 П |
| [ФТ 5.4](02_Requirements.md#req-ft-5-4) |   |   |   |   |   | 🟩 П |
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) |   |   |   | 🟥 Н |   | 🟩 П / 🟨 С |
| [ФТ 6.6](02_Requirements.md#req-ft-6-6) |   |   |   |   | 🟥 Н |   |
| [ФТ 7.2](02_Requirements.md#req-ft-7-2) |   |   |   | 🟥 Н |   |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   |   |   |   | 🟥 Н |   |
| [ФО 1.2](02_Requirements.md#req-fo-1-2) |   |   | 🟥 Н / 🟨 С |   | 🟥 Н |   |
| [ФО 1.3](02_Requirements.md#req-fo-1-3) |   |   |   | 🟥 Н |   |   |
| [ФО 1.4](02_Requirements.md#req-fo-1-4) |   |   |   | 🟥 Н |   |   |
| [ФО 2.1](02_Requirements.md#req-fo-2-1) |   | 🟥 Н / 🟨 С |   |   |   |   |
| [ФО 2.2](02_Requirements.md#req-fo-2-2) | 🟩 П |   |   |   |   |   |
| [ФО 2.3](02_Requirements.md#req-fo-2-3) |   | 🟥 Н |   |   |   |   |
| [ФО 2.4](02_Requirements.md#req-fo-2-4) | 🟩 П |   |   |   |   |   |
| [ФО 3.1](02_Requirements.md#req-fo-3-1) |   |   |   |   |   | 🟩 П |
| [ФО 3.5](02_Requirements.md#req-fo-3-5) |   |   |   | 🟥 Н |   |   |
| [ФО 5.2](02_Requirements.md#req-fo-5-2) |   |   |   | 🟥 Н |   |   |

| ФТ / ФО | [IT-07](03_Test_Plan.md#it-07) | [IT-08](03_Test_Plan.md#it-08) | [IT-09](03_Test_Plan.md#it-09) | [IT-10](03_Test_Plan.md#it-10) | [IT-11](03_Test_Plan.md#it-11) | [IT-12](03_Test_Plan.md#it-12) |
|---|---|---|---|---|---|---|
| [ФТ 3.2](02_Requirements.md#req-ft-3-2) |   |   |   |   | 🟩 П |   |
| [ФТ 3.5](02_Requirements.md#req-ft-3-5) |   |   |   |   |   | 🟨 С |
| [ФТ 4.1](02_Requirements.md#req-ft-4-1) |   | 🟩 П |   |   |   |   |
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) | 🟨 С |   |   |   |   |   |
| [ФТ 6.1](02_Requirements.md#req-ft-6-1) |   | 🟩 П |   |   |   |   |
| [ФТ 6.2](02_Requirements.md#req-ft-6-2) |   | 🟩 П |   |   |   |   |
| [ФТ 6.3](02_Requirements.md#req-ft-6-3) |   | 🟩 П |   |   |   |   |
| [ФТ 6.4](02_Requirements.md#req-ft-6-4) |   | 🟩 П |   |   |   |   |
| [ФТ 6.5](02_Requirements.md#req-ft-6-5) |   | 🟩 П |   |   |   |   |
| [ФТ 6.6](02_Requirements.md#req-ft-6-6) |   | 🟩 П | 🟨 С |   |   |   |
| [ФТ 7.1](02_Requirements.md#req-ft-7-1) |   | 🟩 П |   |   |   |   |
| [ФТ 7.2](02_Requirements.md#req-ft-7-2) |   | 🟩 П |   |   |   |   |
| [ФТ 7.3](02_Requirements.md#req-ft-7-3) |   |   |   | 🟨 С |   |   |
| [ФТ 7.4](02_Requirements.md#req-ft-7-4) |   |   |   | 🟨 С |   |   |
| [ФТ 8.1](02_Requirements.md#req-ft-8-1) |   |   |   | 🟩 П / 🟨 С |   |   |
| [ФТ 8.2](02_Requirements.md#req-ft-8-2) |   |   |   | 🟩 П / 🟨 С |   |   |
| [ФТ 8.3](02_Requirements.md#req-ft-8-3) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 8.4](02_Requirements.md#req-ft-8-4) |   |   |   | 🟩 П / 🟨 С |   |   |
| [ФТ 8.5](02_Requirements.md#req-ft-8-5) |   |   |   | 🟨 С |   |   |
| [ФТ 8.6](02_Requirements.md#req-ft-8-6) |   |   |   | 🟨 С |   |   |
| [ФТ 8.7](02_Requirements.md#req-ft-8-7) |   |   |   |   | 🟨 С |   |
| [ФТ 8.8](02_Requirements.md#req-ft-8-8) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 10.2](02_Requirements.md#req-ft-10-2) |   |   |   |   |   | 🟩 П |
| [ФТ 10.3](02_Requirements.md#req-ft-10-3) |   |   |   |   |   | 🟩 П |
| [ФТ 10.4](02_Requirements.md#req-ft-10-4) |   |   |   |   |   | 🟩 П |
| [ФТ 10.5](02_Requirements.md#req-ft-10-5) |   |   |   |   |   | 🟩 П / 🟥 Н |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) | 🟥 Н |   |   |   |   |   |
| [ФО 3.4](02_Requirements.md#req-fo-3-4) |   |   |   |   | 🟨 С |   |
| [ФО 3.5](02_Requirements.md#req-fo-3-5) |   | 🟩 П |   |   |   |   |
| [ФО 3.6](02_Requirements.md#req-fo-3-6) |   | 🟩 П | 🟨 С |   |   |   |
| [ФО 3.7](02_Requirements.md#req-fo-3-7) |   |   | 🟨 С |   |   |   |
| [ФО 4.1](02_Requirements.md#req-fo-4-1) |   |   | 🟨 С | 🟨 С |   |   |
| [ФО 4.2](02_Requirements.md#req-fo-4-2) |   |   |   | 🟨 С |   |   |
| [ФО 5.1](02_Requirements.md#req-fo-5-1) |   |   |   |   |   | 🟩 П / 🟥 Н |
| [ФО 5.3](02_Requirements.md#req-fo-5-3) |   |   |   |   |   | 🟨 С |

| ФТ / ФО | [IT-13](03_Test_Plan.md#it-13) | [IT-14](03_Test_Plan.md#it-14) | [IT-15](03_Test_Plan.md#it-15) | [IT-16](03_Test_Plan.md#it-16) | [IT-17](03_Test_Plan.md#it-17) | [IT-18](03_Test_Plan.md#it-18) |
|---|---|---|---|---|---|---|
| [ФТ 6.7](02_Requirements.md#req-ft-6-7) |   |   |   |   | 🟩 П |   |
| [ФТ 6.8](02_Requirements.md#req-ft-6-8) |   |   |   |   | 🟩 П |   |
| [ФТ 9.1](02_Requirements.md#req-ft-9-1) |   | 🟩 П |   |   |   |   |
| [ФТ 9.2](02_Requirements.md#req-ft-9-2) |   | 🟩 П |   |   |   |   |
| [ФТ 9.3](02_Requirements.md#req-ft-9-3) |   | 🟩 П / 🟨 С |   |   |   |   |
| [ФТ 9.4](02_Requirements.md#req-ft-9-4) |   | 🟩 П / 🟨 С |   |   |   |   |
| [ФТ 10.2](02_Requirements.md#req-ft-10-2) |   |   |   |   |   | 🟩 П |
| [ФТ 11.1](02_Requirements.md#req-ft-11-1) |   |   | 🟩 П |   |   |   |
| [ФТ 11.2](02_Requirements.md#req-ft-11-2) |   |   | 🟩 П |   |   |   |
| [ФТ 11.3](02_Requirements.md#req-ft-11-3) |   |   | 🟩 П |   |   |   |
| [ФТ 11.4](02_Requirements.md#req-ft-11-4) |   |   | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 11.5](02_Requirements.md#req-ft-11-5) |   |   | 🟨 С |   |   |   |
| [ФТ 12.1](02_Requirements.md#req-ft-12-1) |   |   |   | 🟩 П |   |   |
| [ФТ 12.2](02_Requirements.md#req-ft-12-2) |   |   |   | 🟩 П / 🟥 Н |   |   |
| [ФТ 12.3](02_Requirements.md#req-ft-12-3) |   |   |   | 🟩 П |   |   |
| [ФТ 12.4](02_Requirements.md#req-ft-12-4) |   |   |   | 🟩 П |   |   |
| [ФТ 13.1](02_Requirements.md#req-ft-13-1) |   | 🟨 С |   |   |   |   |
| [ФТ 13.2](02_Requirements.md#req-ft-13-2) |   |   |   |   |   | 🟩 П |
| [ФТ 14.1](02_Requirements.md#req-ft-14-1) | 🟩 П |   |   |   |   |   |
| [ФТ 14.2](02_Requirements.md#req-ft-14-2) | 🟩 П / 🟥 Н |   |   |   |   |   |
| [ФТ 14.3](02_Requirements.md#req-ft-14-3) | 🟩 П |   |   |   |   |   |
| [ФТ 14.4](02_Requirements.md#req-ft-14-4) | 🟩 П |   |   |   |   |   |
| [ФТ 14.5](02_Requirements.md#req-ft-14-5) | 🟥 Н |   |   |   |   |   |
| [ФО 1.5](02_Requirements.md#req-fo-1-5) | 🟩 П / 🟥 Н |   |   |   |   |   |
| [ФО 3.7](02_Requirements.md#req-fo-3-7) |   |   |   |   | 🟩 П |   |
| [ФО 4.3](02_Requirements.md#req-fo-4-3) |   |   |   |   | 🟩 П |   |
| [ФО 5.3](02_Requirements.md#req-fo-5-3) |   |   | 🟨 С |   |   |   |
| [ФО 6.1](02_Requirements.md#req-fo-6-1) |   |   |   | 🟨 С |   |   |
| [ФО 6.2](02_Requirements.md#req-fo-6-2) |   |   |   | 🟥 Н / 🟨 С |   |   |
| [ФО 6.3](02_Requirements.md#req-fo-6-3) |   |   |   | 🟨 С |   |   |
| [ФО 6.4](02_Requirements.md#req-fo-6-4) |   |   |   | 🟨 С |   |   |

| ФТ / ФО | [IT-19](03_Test_Plan.md#it-19) | [IT-20](03_Test_Plan.md#it-20) | [IT-21](03_Test_Plan.md#it-21) | [IT-22](03_Test_Plan.md#it-22) |
|---|---|---|---|---|
| [ФТ 1.1](02_Requirements.md#req-ft-1-1) |   |   |   | 🟨 С |
| [ФТ 4.2](02_Requirements.md#req-ft-4-2) |   |   | 🟩 П |   |
| [ФТ 4.3](02_Requirements.md#req-ft-4-3) |   |   | 🟩 П |   |
| [ФТ 5.3](02_Requirements.md#req-ft-5-3) | 🟩 П |   |   |   |
| [ФТ 5.4](02_Requirements.md#req-ft-5-4) | 🟩 П |   |   |   |
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 5.6](02_Requirements.md#req-ft-5-6) |   |   | 🟩 П |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   | 🟥 Н |   |   |
| [ФО 2.1](02_Requirements.md#req-fo-2-1) |   |   |   | 🟨 С |
| [ФО 3.2](02_Requirements.md#req-fo-3-2) |   | 🟥 Н |   |   |
| [ФО 3.3](02_Requirements.md#req-fo-3-3) |   | 🟥 Н |   |   |
| [ФО 3.7](02_Requirements.md#req-fo-3-7) |   |   | 🟩 П |   |

<span id="at"></span>

## Аттестационные тесты

Матрица на вики с переходами к объектам проверки. [Открыть страницу](https://se.cs.petrsu.ru/wiki/GymTracker:_%D0%9C%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0_%D0%B0%D1%82%D1%82%D0%B5%D1%81%D1%82%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85_%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2).

| ФТ / ФО | [AT-01](03_Test_Plan.md#at-01) | [AT-02](03_Test_Plan.md#at-02) | [AT-03](03_Test_Plan.md#at-03) | [AT-04](03_Test_Plan.md#at-04) | [AT-05](03_Test_Plan.md#at-05) | [AT-06](03_Test_Plan.md#at-06) |
|---|---|---|---|---|---|---|
| [ФТ 1.1](02_Requirements.md#req-ft-1-1) | 🟩 П | 🟥 Н / 🟨 С |   |   |   |   |
| [ФТ 2.1](02_Requirements.md#req-ft-2-1) | 🟩 П | 🟥 Н |   |   |   |   |
| [ФТ 2.2](02_Requirements.md#req-ft-2-2) |   |   | 🟩 П |   |   |   |
| [ФТ 2.3](02_Requirements.md#req-ft-2-3) |   |   |   | 🟨 С |   |   |
| [ФТ 3.1](02_Requirements.md#req-ft-3-1) | 🟩 П |   |   |   | 🟩 П |   |
| [ФТ 3.2](02_Requirements.md#req-ft-3-2) |   |   |   |   | 🟩 П |   |
| [ФТ 3.3](02_Requirements.md#req-ft-3-3) |   |   |   |   | 🟩 П |   |
| [ФТ 4.1](02_Requirements.md#req-ft-4-1) |   |   |   |   |   | 🟩 П |
| [ФТ 5.3](02_Requirements.md#req-ft-5-3) |   |   |   |   |   | 🟩 П |
| [ФТ 15.1](02_Requirements.md#req-ft-15-1) |   |   | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 15.2](02_Requirements.md#req-ft-15-2) | 🟩 П |   |   |   | 🟩 П |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   | 🟥 Н |   |   | 🟥 Н |   |
| [ФО 1.1](02_Requirements.md#req-fo-1-1) |   |   | 🟥 Н |   |   |   |
| [ФО 1.2](02_Requirements.md#req-fo-1-2) |   |   | 🟥 Н |   |   |   |
| [ФО 2.1](02_Requirements.md#req-fo-2-1) |   | 🟥 Н |   |   |   |   |
| [ФО 2.3](02_Requirements.md#req-fo-2-3) |   | 🟥 Н / 🟨 С |   |   |   |   |
| [ФО 2.4](02_Requirements.md#req-fo-2-4) |   |   |   |   | 🟩 П |   |
| [ФО 3.4](02_Requirements.md#req-fo-3-4) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФО 7.1](02_Requirements.md#req-fo-7-1) | 🟩 П |   |   |   |   |   |

| ФТ / ФО | [AT-07](03_Test_Plan.md#at-07) | [AT-08](03_Test_Plan.md#at-08) | [AT-09](03_Test_Plan.md#at-09) | [AT-10](03_Test_Plan.md#at-10) | [AT-11](03_Test_Plan.md#at-11) | [AT-12](03_Test_Plan.md#at-12) |
|---|---|---|---|---|---|---|
| [ФТ 4.2](02_Requirements.md#req-ft-4-2) | 🟩 П / 🟨 С |   |   |   |   |   |
| [ФТ 4.3](02_Requirements.md#req-ft-4-3) | 🟩 П |   |   |   |   |   |
| [ФТ 5.1](02_Requirements.md#req-ft-5-1) |   | 🟩 П |   |   |   |   |
| [ФТ 5.2](02_Requirements.md#req-ft-5-2) |   | 🟩 П |   |   |   |   |
| [ФТ 5.3](02_Requirements.md#req-ft-5-3) |   | 🟩 П |   |   |   |   |
| [ФТ 5.4](02_Requirements.md#req-ft-5-4) |   | 🟩 П | 🟨 С |   |   |   |
| [ФТ 5.5](02_Requirements.md#req-ft-5-5) |   | 🟩 П | 🟨 С |   |   |   |
| [ФТ 5.6](02_Requirements.md#req-ft-5-6) |   |   |   | 🟩 П |   |   |
| [ФТ 6.1](02_Requirements.md#req-ft-6-1) |   |   |   |   | 🟩 П |   |
| [ФТ 6.2](02_Requirements.md#req-ft-6-2) |   |   |   |   | 🟩 П |   |
| [ФТ 6.3](02_Requirements.md#req-ft-6-3) |   |   |   |   | 🟩 П |   |
| [ФТ 6.4](02_Requirements.md#req-ft-6-4) |   |   |   |   | 🟩 П | 🟨 С |
| [ФТ 6.5](02_Requirements.md#req-ft-6-5) |   |   |   |   | 🟩 П | 🟨 С |
| [ФТ 6.6](02_Requirements.md#req-ft-6-6) |   |   |   |   | 🟩 П |   |
| [ФТ 7.2](02_Requirements.md#req-ft-7-2) |   |   |   |   | 🟩 П |   |
| [ФТ 15.2](02_Requirements.md#req-ft-15-2) |   |   |   |   | 🟩 П |   |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   |   |   |   |   | 🟥 Н |
| [ФО 2.4](02_Requirements.md#req-fo-2-4) |   | 🟩 П |   |   |   |   |
| [ФО 3.1](02_Requirements.md#req-fo-3-1) |   | 🟩 П | 🟥 Н / 🟨 С |   |   |   |
| [ФО 3.2](02_Requirements.md#req-fo-3-2) |   |   | 🟥 Н / 🟨 С |   |   | 🟥 Н / 🟨 С |
| [ФО 3.3](02_Requirements.md#req-fo-3-3) |   |   |   |   |   | 🟥 Н / 🟨 С |
| [ФО 3.5](02_Requirements.md#req-fo-3-5) |   |   |   |   | 🟩 П |   |
| [ФО 3.6](02_Requirements.md#req-fo-3-6) |   |   |   |   | 🟩 П |   |
| [ФО 3.7](02_Requirements.md#req-fo-3-7) |   | 🟩 П |   | 🟩 П |   |   |
| [ФО 4.1](02_Requirements.md#req-fo-4-1) |   |   |   |   |   | 🟨 С |

| ФТ / ФО | [AT-13](03_Test_Plan.md#at-13) | [AT-14](03_Test_Plan.md#at-14) | [AT-15](03_Test_Plan.md#at-15) | [AT-16](03_Test_Plan.md#at-16) | [AT-17](03_Test_Plan.md#at-17) | [AT-18](03_Test_Plan.md#at-18) |
|---|---|---|---|---|---|---|
| [ФТ 6.7](02_Requirements.md#req-ft-6-7) |   |   | 🟩 П |   |   |   |
| [ФТ 6.8](02_Requirements.md#req-ft-6-8) |   |   | 🟩 П |   |   |   |
| [ФТ 7.1](02_Requirements.md#req-ft-7-1) | 🟩 П |   |   |   |   |   |
| [ФТ 7.2](02_Requirements.md#req-ft-7-2) | 🟩 П |   |   |   |   |   |
| [ФТ 7.3](02_Requirements.md#req-ft-7-3) |   |   |   | 🟩 П / 🟨 С |   |   |
| [ФТ 7.4](02_Requirements.md#req-ft-7-4) |   |   |   | 🟩 П / 🟨 С |   |   |
| [ФТ 8.1](02_Requirements.md#req-ft-8-1) | 🟩 П |   |   |   |   |   |
| [ФТ 8.2](02_Requirements.md#req-ft-8-2) | 🟩 П |   |   |   |   |   |
| [ФТ 8.3](02_Requirements.md#req-ft-8-3) |   |   |   |   |   | 🟩 П / 🟨 С |
| [ФТ 8.4](02_Requirements.md#req-ft-8-4) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 8.5](02_Requirements.md#req-ft-8-5) |   |   |   |   | 🟩 П / 🟨 С |   |
| [ФТ 8.6](02_Requirements.md#req-ft-8-6) |   |   |   |   | 🟨 С |   |
| [ФТ 8.7](02_Requirements.md#req-ft-8-7) |   |   |   |   |   | 🟨 С |
| [ФТ 8.8](02_Requirements.md#req-ft-8-8) |   |   |   |   |   | 🟩 П / 🟨 С |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   | 🟥 Н |   |   |   |   |
| [ФО 1.3](02_Requirements.md#req-fo-1-3) |   | 🟥 Н |   |   |   |   |
| [ФО 1.4](02_Requirements.md#req-fo-1-4) |   | 🟥 Н |   |   |   |   |
| [ФО 2.4](02_Requirements.md#req-fo-2-4) | 🟩 П |   |   |   |   |   |
| [ФО 3.5](02_Requirements.md#req-fo-3-5) | 🟩 П |   |   |   |   |   |
| [ФО 3.7](02_Requirements.md#req-fo-3-7) |   |   | 🟩 П |   |   |   |
| [ФО 4.1](02_Requirements.md#req-fo-4-1) | 🟩 П |   |   |   |   |   |
| [ФО 4.2](02_Requirements.md#req-fo-4-2) |   |   |   |   | 🟨 С |   |
| [ФО 4.3](02_Requirements.md#req-fo-4-3) |   |   | 🟩 П |   |   |   |
| [ФО 5.2](02_Requirements.md#req-fo-5-2) |   | 🟥 Н |   |   |   |   |

| ФТ / ФО | [AT-19](03_Test_Plan.md#at-19) | [AT-20](03_Test_Plan.md#at-20) | [AT-21](03_Test_Plan.md#at-21) | [AT-22](03_Test_Plan.md#at-22) | [AT-23](03_Test_Plan.md#at-23) | [AT-24](03_Test_Plan.md#at-24) |
|---|---|---|---|---|---|---|
| [ФТ 3.4](02_Requirements.md#req-ft-3-4) | 🟩 П |   |   |   |   |   |
| [ФТ 3.5](02_Requirements.md#req-ft-3-5) |   |   | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 9.1](02_Requirements.md#req-ft-9-1) | 🟩 П / 🟨 С |   |   |   |   |   |
| [ФТ 9.2](02_Requirements.md#req-ft-9-2) | 🟩 П / 🟨 С |   |   |   |   |   |
| [ФТ 9.3](02_Requirements.md#req-ft-9-3) | 🟨 С |   |   |   |   |   |
| [ФТ 9.4](02_Requirements.md#req-ft-9-4) | 🟨 С |   |   |   |   |   |
| [ФТ 10.1](02_Requirements.md#req-ft-10-1) |   | 🟩 П |   |   |   |   |
| [ФТ 10.2](02_Requirements.md#req-ft-10-2) |   | 🟩 П |   |   |   |   |
| [ФТ 10.3](02_Requirements.md#req-ft-10-3) |   | 🟩 П |   |   |   |   |
| [ФТ 10.4](02_Requirements.md#req-ft-10-4) |   | 🟩 П |   |   |   |   |
| [ФТ 10.5](02_Requirements.md#req-ft-10-5) |   | 🟩 П | 🟩 П / 🟥 Н |   |   |   |
| [ФТ 11.1](02_Requirements.md#req-ft-11-1) |   |   |   |   |   | 🟩 П |
| [ФТ 11.2](02_Requirements.md#req-ft-11-2) |   |   |   |   |   | 🟩 П |
| [ФТ 11.3](02_Requirements.md#req-ft-11-3) |   |   |   |   |   | 🟩 П |
| [ФТ 11.4](02_Requirements.md#req-ft-11-4) |   |   |   |   |   | 🟩 П / 🟥 Н |
| [ФТ 11.5](02_Requirements.md#req-ft-11-5) |   |   |   |   |   | 🟨 С |
| [ФТ 14.1](02_Requirements.md#req-ft-14-1) |   |   |   | 🟩 П |   |   |
| [ФТ 14.2](02_Requirements.md#req-ft-14-2) |   |   |   | 🟩 П / 🟥 Н |   |   |
| [ФТ 14.3](02_Requirements.md#req-ft-14-3) |   |   |   |   | 🟩 П |   |
| [ФТ 14.4](02_Requirements.md#req-ft-14-4) |   |   |   |   | 🟩 П |   |
| [ФТ 14.5](02_Requirements.md#req-ft-14-5) |   |   |   | 🟩 П / 🟥 Н |   |   |
| [ФО 1.1](02_Requirements.md#req-fo-1-1) |   |   |   | 🟥 Н |   |   |
| [ФО 1.5](02_Requirements.md#req-fo-1-5) |   |   |   | 🟥 Н | 🟥 Н |   |
| [ФО 5.1](02_Requirements.md#req-fo-5-1) |   | 🟩 П | 🟩 П / 🟥 Н |   |   |   |
| [ФО 5.3](02_Requirements.md#req-fo-5-3) |   |   | 🟩 П / 🟥 Н |   |   | 🟨 С |

| ФТ / ФО | [AT-25](03_Test_Plan.md#at-25) | [AT-26](03_Test_Plan.md#at-26) | [AT-27](03_Test_Plan.md#at-27) | [AT-28](03_Test_Plan.md#at-28) | [AT-29](03_Test_Plan.md#at-29) | [AT-30](03_Test_Plan.md#at-30) |
|---|---|---|---|---|---|---|
| [ФТ 12.1](02_Requirements.md#req-ft-12-1) | 🟩 П |   |   |   |   |   |
| [ФТ 12.2](02_Requirements.md#req-ft-12-2) | 🟩 П | 🟥 Н / 🟨 С |   |   |   |   |
| [ФТ 12.3](02_Requirements.md#req-ft-12-3) | 🟩 П |   |   |   |   |   |
| [ФТ 12.4](02_Requirements.md#req-ft-12-4) | 🟩 П |   |   |   |   |   |
| [ФТ 13.1](02_Requirements.md#req-ft-13-1) |   |   | 🟩 П |   |   |   |
| [ФТ 13.2](02_Requirements.md#req-ft-13-2) |   |   | 🟩 П |   |   |   |
| [ФТ 15.1](02_Requirements.md#req-ft-15-1) |   |   |   | 🟩 П | 🟨 С |   |
| [ФТ 15.2](02_Requirements.md#req-ft-15-2) |   |   |   |   |   | 🟩 П / 🟨 С |
| [ФТ 15.3](02_Requirements.md#req-ft-15-3) |   |   |   |   |   | 🟥 Н |
| [ФО 6.1](02_Requirements.md#req-fo-6-1) | 🟩 П | 🟨 С |   |   |   |   |
| [ФО 6.2](02_Requirements.md#req-fo-6-2) |   | 🟩 П / 🟨 С |   |   |   |   |
| [ФО 6.3](02_Requirements.md#req-fo-6-3) | 🟩 П |   |   |   |   |   |
| [ФО 6.4](02_Requirements.md#req-fo-6-4) | 🟩 П |   |   |   |   |   |
| [ФО 7.1](02_Requirements.md#req-fo-7-1) |   |   |   | 🟩 П | 🟨 С |   |
| [ФО 7.2](02_Requirements.md#req-fo-7-2) |   |   |   |   | 🟨 С |   |
| [ФО 7.3](02_Requirements.md#req-fo-7-3) |   |   |   |   | 🟨 С |   |

| ФТ / ФО | [AT-31](03_Test_Plan.md#at-31) | [AT-32](03_Test_Plan.md#at-32) | [AT-33](03_Test_Plan.md#at-33) |
|---|---|---|---|
| [ФО 1.1](02_Requirements.md#req-fo-1-1) |   |   | 🟩 П |
| [ФО 1.5](02_Requirements.md#req-fo-1-5) |   |   | 🟥 Н |
| [ФО 2.2](02_Requirements.md#req-fo-2-2) | 🟨 С |   |   |
| [ФО 2.3](02_Requirements.md#req-fo-2-3) | 🟥 Н / 🟨 С |   |   |
| [ФО 6.2](02_Requirements.md#req-fo-6-2) |   |   | 🟩 П / 🟨 С |
| [ФО 6.3](02_Requirements.md#req-fo-6-3) |   |   | 🟩 П / 🟨 С |
| [ФО 6.4](02_Requirements.md#req-fo-6-4) |   |   | 🟩 П / 🟨 С |
| [ФО 7.4](02_Requirements.md#req-fo-7-4) |   | 🟨 С |   |
| [ФО 7.5](02_Requirements.md#req-fo-7-5) |   | 🟨 С |   |
