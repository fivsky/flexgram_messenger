# Flexgram — real-time messenger

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green)](https://djangoproject.com)
[![WebSocket](https://img.shields.io/badge/WebSocket-✅-purple)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
[![PWA](https://img.shields.io/badge/PWA-ready-orange)](https://web.dev/progressive-web-apps/)

Современный мессенджер. Реалтайм-чат, передача файлов, фото и видео. Устанавливается на iPhone как нативное приложение.

## ✨ Возможности
- 🔐 Регистрация/аутентификация (Django Auth)
- 💬 Обмен сообщениями в реальном времени (WebSocket)
- 📎 Отправка фото, видео, файлов (автоопределение формата)
- 📱 PWA-установка на iOS/Android (иконка, полноэкранный режим)
- 🎨 Уникальный дизайн: шрифт Unbounded, серо-зеленая гамма, акценты
- 🌐 Деплой на Render (Daphne ASGI, PostgreSQL, автосборка)

## 🛠 Стек
| Технология | Назначение |
|-----------|------------|
| Django 6.0 | Бэкенд, ORM, аутентификация |
| Django Channels | WebSocket-сервер |
| Daphne | ASGI-продакшен-сервер |
| PostgreSQL | База данных |
| Channels Layers | Группы комнат (InMemory) |
| MediaRecorder API | Запись аудио/видео в браузере |
| WhiteNoise | Отдача статики в продакшене |
| Render | Хостинг (ASGI + PostgreSQL) |

## 🚀 Быстрый старт
```bash
git clone https://github.com/fivsky/flexgram_messenger.git
cd flexgram_messenger
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
