# Персональный сайт на MkDocs

Курсовая работа Кирильцевой Вероники Сергеевны, ИТМО, U4225.

🌐 [Открыть сайт на GitHub Pages](https://89620761583veronika-png.github.io/2025_2026-introduction-in-web-tech-u4225-kiriltseva_v_s/)

## Запуск

Нужен Python 3.9 или новее. Выполняйте команды в папке проекта.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs --version
mkdocs serve --dev-addr 127.0.0.1:8001
```

Windows PowerShell: вместо `source .venv/bin/activate` выполните `.venv\Scripts\Activate.ps1`; вместо `python3` используйте `python`.

Откройте http://127.0.0.1:8001/ в браузере. Остановить сервер: Ctrl+C.

## Сборка

```sh
mkdocs build --strict
```

Результат — папка `site/`. Для проверки статической сборки:

```sh
python -m http.server 8002 --directory site --bind 127.0.0.1
```

Откройте http://127.0.0.1:8002/. Сайт следует открывать через HTTP-сервер: поиск использует веб-ресурсы, которые могут блокироваться при открытии HTML как локального файла.

## Структура

- `mkdocs.yml` — метаданные, Material, навигация, палитры и поиск.
- `docs/*.md` — шесть страниц сайта.
- `docs/images/logo.svg` — локальный логотип-монограмма.
- `docs/stylesheets/extra.css` — оформление и мобильные стили.
- `requirements.txt` — основные зависимости.
- `requirements-lock.txt` — точные версии установленного окружения.
- `report/coursework.md` — отчёт по курсовой работе.
- `report/verification.txt` — результаты проверки.
- `site/` — собранный сайт.

## Редактирование

Тексты меняются в `docs/`, порядок страниц — в `nav` файла `mkdocs.yml`. `mkdocs serve` автоматически обновляет страницы после сохранения. Логотип можно заменить, сохранив пути `logo` и `favicon` в конфигурации.

Биография, образование, работа и увлечения обновлены по сведениям автора от 10.09.2026. Использованы три прикреплённых автором фотографии выдр. Светлая и тёмная темы оформлены в розовой палитре, добавлены эмоджи 🦋.

## Публикация на GitHub Pages

Сайт опубликован из ветки `gh-pages`, папки `/ (root)`. Реальный адрес указан в `site_url` файла `mkdocs.yml`.

После изменения сайта из корня учебного репозитория выполните:

```sh
python -m mkdocs gh-deploy --strict -f coursework/mkdocs.yml
```

Из самой папки `coursework` достаточно `mkdocs gh-deploy --strict`. Нужен настроенный Git-доступ к репозиторию. Обновление GitHub Pages может занять несколько минут.

Документация: [MkDocs](https://www.mkdocs.org/), [Material](https://squidfunk.github.io/mkdocs-material/), [развёртывание MkDocs](https://www.mkdocs.org/user-guide/deploying-your-docs/).
