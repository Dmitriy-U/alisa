# Тестирование Яндекс Алисы

---

## Запуск

Запуск в тестовом режиме на порту **7777** из виртуального окружения: `flask --app app run --port=7777`

---

## Привязка к Яндекс

### 1. Предоставление прав

#### 1.1 Отправка пользователя на страницу привязки

> Яндекс Умный дом -> Сервис авторизации

На странице предоставления прав авторизационного сервиса пользователю нужно авторизоваться если не авторизован и
предоставить права.

GET `<auth_service_authorization_grant_url>`

**Query parameters**:

|  Наименование | Тип    | Обязательный | Описание                                                                                                                                                                   |
|--------------:|:-------|:------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  redirect_uri | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) адрес отправки пользователя после предоставления прав                        |
| response_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `code` что требуется отдать клиенту пользователя                             |
|     client_id | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) идентификатор клиента                                                        |
|         scope | string |     Нет      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `yandex_smart_home:lights` список разрешений для запрашиваемых OAuth-токенов |
|         state | string |      Да      | служебное поле для проверки состояния прав                                                                                                                                 |

#### 1.2 Создание кода авторизации

Любым способом создать в сервисе авторизации код авторизации

#### 1.3 Отправка пользователя обратно к клиенту (Яндекс Умный Дом)

> Сервис авторизации -> Яндекс Умный дом

Нужно отправить код авторизации на обратный url адрес

GET `<redirect_uri>`

**Query parameters**:

|  Наименование | Тип    | Обязательный | Описание                                                                                                                                                                   |
|--------------:|:-------|:------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          code | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код авторизации                                                              |
| response_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `code` что требуется отдать клиенту пользователя                             |
|     client_id | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) идентификатор клиента                                                        |
|         scope | string |     Нет      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `yandex_smart_home:lights` список разрешений для запрашиваемых OAuth-токенов |
|         state | string |      Да      | служебное поле для проверки состояния авторизации                                                                                                                          |

### 2. Получение токена по коду авторизации

> Яндекс Умный дом -> Сервис авторизации

#### 2.1 Обработать запрос

POST `<auth_service_token_url>`

**Headers:**

- Content-Type: application/x-www-form-urlencoded

**Payload:**

|  Наименование | Тип    | Обязательный | Описание                                                                                                                                            |
|--------------:|:-------|:------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------|
|          code | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код авторизации                                       |
| client_secret | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) секретный код клиента                                 |
|  redirect_uri | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) адрес отправки пользователя после предоставления прав |
|    grant_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `authorization_code` тип прав                         |
|     client_id | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) идентификатор клиента                                 |

#### 2.2 Проверка

Проверить на сервере авторизации *code*, *client_secret*, *client_id* и создать пару токенов для клиента пользователя.

#### 2.3 Отдать ответ

**Headers:**

- Content-Type: application/json

**Payload:**

|   Наименование | Тип    | Обязательный | Описание                                                                                                                                                                   |
|---------------:|:-------|:------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     token_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `bearer` код авторизации                                                     |
|     expires_in | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) время жизни токена (секунд)                                                  |
|   access_token | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код доступа                                                                  |
|  refresh_token | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код обновления                                                               |
|          scope | string |     Нет      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `yandex_smart_home:lights` список разрешений для запрашиваемых OAuth-токенов |

### 3. Перевыпуск токенов

> Яндекс Умный дом -> Сервис авторизации

#### 2.1 Обработать запрос

POST `<auth_service_refresh_token_url>`

**Headers:**

- Content-Type: application/x-www-form-urlencoded

**Payload:**

|   Наименование | Тип    | Обязательный | Описание                                                                                                                                            |
|---------------:|:-------|:------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------|
|  refresh_token | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код обновления                                        |
|  client_secret | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) секретный код клиента                                 |
|   redirect_uri | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) адрес отправки пользователя после предоставления прав |
|     grant_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `authorization_code` тип прав                         |
|      client_id | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) идентификатор клиента                                 |

#### 2.2 Проверка

Проверить на сервере авторизации *refresh_token*, *client_secret*, *client_id* и создать пару токенов для клиента пользователя, а предыдущий пометить, как использованный или удалить.

#### 2.3 Отдать ответ

**Headers:**

- Content-Type: application/json

**Payload:**

|   Наименование | Тип    | Обязательный | Описание                                                                                                                                                                   |
|---------------:|:-------|:------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     token_type | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `bearer` код авторизации                                                     |
|     expires_in | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) время жизни токена (секунд)                                                  |
|   access_token | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код доступа                                                                  |
|  refresh_token | string |      Да      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) код обновления                                                               |
|          scope | string |     Нет      | ![OAuth 2.0](https://img.shields.io/static/v1?label=OAuth&message=2.0&style=flat&color=white) `yandex_smart_home:lights` список разрешений для запрашиваемых OAuth-токенов |
