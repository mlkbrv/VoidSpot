# Варианты названий проекта

* **Echo / Echoes** — Анонимный пост как эхо, а комментарии как реальные голоса
* **Masked** — Маски надеты для постов, сняты для комментариев
* **Persona** — Игра со словом: личность скрыта или раскрыта
* **WhisperNet** — Сеть шепотов
* **ShadowChat** — Акцент на чаты и скрытность
* **Incognita** — Стильно и понятно

---

# Архитектура проекта: Анонимная социальная сеть с микросервисами

## 1. Обзор системы (System Overview)

Проект представляет собой социальную сеть с разделением уровней приватности:

- **Посты (Публикации):** строго анонимные для читателей (автор скрыт на уровне API).
- **Комментарии:** публичные (виден профиль автора).
- **Чаты:** real‑time общение (FastAPI).
- **Медиа:** поддержка изображений (png, jpeg) и видео (mp4).

Система построена на микросервисной архитектуре для разделения синхронной бизнес‑логики (Django) и асинхронной логики реального времени (FastAPI).

---

## 2. Инфраструктура и сервисы (Infrastructure)

### API Gateway (Nginx / Traefik)

- `/api/v1/` → маршрутизация на **Django Core**
- `/ws/` и `/api/chat/` → маршрутизация на **FastAPI Chat Service**

### Core Service (Django + DRF)

- Управление пользователями
- Управление контентом (посты, комментарии)
- Работа с медиафайлами
- Генерация JWT‑токенов для авторизации

### Chat Service (FastAPI)

- WebSocket соединения
- Комнаты чатов
- Статусы online/offline

### Databases & Storage

- **PostgreSQL** — основная база данных
- **Redis** — брокер сообщений, кэш, хранение WebSocket‑сессий
- **MinIO / AWS S3** — объектное хранилище медиафайлов

---

## 3. Схема базы данных (Database Schema – Django Core)

Основная идея архитектуры — вынести общие поля в сущность `Content`.

### Аутентификация и пользователи

#### User

- `id` (UUID)
- `email` (unique)
- `password_hash`
- `is_active`
- `is_banned`

#### Profile

- `id` (UUID)
- `user_id` (OneToOne → User)
- `nickname` (unique)
- `avatar_url`

---

### Медиа

#### File

- `id` (UUID)
- `file_url` (ссылка на S3)
- `file_type` (enum: image/png, image/jpeg, video/mp4)
- `size_bytes`
- `uploaded_at`

---

### Контент (ядро)

#### Content

- `id` (UUID)
- `text_body`
- `files` (ManyToMany → File)
- `created_at`
- `updated_at`

#### Post (Анонимный пост)

- `id` (UUID)
- `content_id` (OneToOne → Content)
- `author_id` (ForeignKey → User) — хранится только для модерации
- `likes_count`

⚠️ `author_id` никогда не возвращается в API.

#### Comment (Публичный комментарий)

- `id` (UUID)
- `content_id` (OneToOne → Content)
- `post_id` (ForeignKey → Post)
- `author_id` (ForeignKey → Profile)
- `parent_comment_id` (ForeignKey → Comment, nullable)

Это позволяет делать древовидные ответы.

---

## 4. Архитектура чатов (FastAPI Service)

### ChatRoom

- `id` (UUID)
- `type` (enum: private, group)
- `members` (ManyToMany → User ID из Django)

### ChatMessage

- `id` (UUID)
- `room_id`
- `sender_id`
- `text`
- `file_id` (nullable)
- `created_at`

---

## 5. Авторизация (Flow)

1. Пользователь логинится через Django: `/api/v1/auth/login`
2. Django возвращает `JWT Access Token`
3. Клиент подключается:

```
ws://domain.com/ws/chat/?token=ACCESS_TOKEN
```

4. FastAPI проверяет JWT с тем же `SECRET_KEY`
5. Из токена извлекается `user_id`
6. WebSocket соединение устанавливается

---

## 6. События через Redis (Pub/Sub)

### Сценарий: новый комментарий

1. Django сохраняет комментарий в PostgreSQL
2. Django публикует событие в Redis канал `notifications`
3. FastAPI подписан на канал `notifications`
4. FastAPI отправляет WebSocket‑уведомление автору поста

```
"У вашего поста новый комментарий"
```

---

## Итоговая архитектура

Frontend → API Gateway →

- Django (REST API, Users, Posts, Comments, Media)
- FastAPI (WebSockets, Chat)

Shared Infrastructure:

- PostgreSQL
- Redis
- S3 / MinIO
