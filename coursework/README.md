# Персональный сайт на MkDocs

Курсовая работа Кирильцевой Вероники Сергеевны, ИТМО, U4225.

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

Образование, имя, группа и ссылки взяты из существующих учебных отчётов. Хобби, почта, коммерческий опыт и сертификаты не выдумывались. При необходимости дополните `about.md`, `resume.md`, `contacts.md` собственными сведениями.

## Публикация на GitHub Pages — по желанию

1. Создайте репозиторий для этого проекта и загрузите исходники без `.venv/` и `site/`.
2. Добавьте в `mkdocs.yml` строку `site_url: https://ВАШ-ЛОГИН.github.io/ИМЯ-РЕПОЗИТОРИЯ/`, заменив обе части настоящими значениями.
3. Из локального Git-репозитория с настроенным `origin` выполните `mkdocs gh-deploy`.
4. В Settings → Pages выберите публикацию из ветки `gh-pages`, папки `/ (root)`.
5. Откройте выданный GitHub адрес и проверьте навигацию и поиск.

Публикация пока не выполнялась. `site_url` намеренно не содержит вымышленного адреса.

Документация: [MkDocs](https://www.mkdocs.org/), [Material](https://squidfunk.github.io/mkdocs-material/), [развёртывание MkDocs](https://www.mkdocs.org/user-guide/deploying-your-docs/).
