University: [ITMO University](https://itmo.ru/ru/)\
Faculty: [FICT](https://fict.itmo.ru)\
Course: [Введение в веб технологии](https://itmo-ict-faculty.github.io/introduction-in-web-tech/)\
Year: 2025/2026\
Group: U4225\
Author: Kiriltseva Veronika Sergeevna\
Lab: Lab2\
Date of create: 06.09.2026\
Date of finished: — (будет указана после защиты)

# Лабораторная работа №2. CI/CD для Docker-приложения

## Цель работы

Настроить автоматическую сборку и проверку Docker-образа, его публикацию в Docker Hub и условный учебный деплой в зависимости от ветки GitHub.

## 1. Подготовка проекта

Создан отдельный [репозиторий приложения lab2-cicd-kiriltseva](https://github.com/89620761583veronika-png/lab2-cicd-kiriltseva). Отчёт размещён в папке `lab2` учебного репозитория в соответствии с [правилами оформления](https://itmo-ict-faculty.github.io/introduction-in-web-tech/education/labs2025-2026/reportdesign/).

Из лабораторной №1 без изменения скопированы `app.py`, `requirements.txt`, `Dockerfile` и дополнительный `constraints.txt`. Последний необходим для совместимости Flask 2.0.1 с Werkzeug 2.0.3. Приложение возвращает `Hello from Docker!` по маршруту `/`, слушает `0.0.0.0:5000` и запускается от пользователя `appuser` с UID 1000.

В новом репозитории также созданы `.gitignore`, `.dockerignore`, `LICENSE`, `README.md`, скрипт проверки и workflow:

```text
lab2-cicd-kiriltseva/
├── .github/workflows/docker-build.yml
├── .dockerignore
├── .gitignore
├── app.py
├── requirements.txt
├── constraints.txt
├── Dockerfile
├── scripts/test-image.sh
├── logs/
├── LICENSE
└── README.md
```

`.dockerignore` включает в контекст только файлы сборки. Отчёты, Git-история, логи и возможные локальные секреты не попадают в Docker-контекст.

## 2. Настройка GitHub Actions

[Исходный файл workflow](https://github.com/89620761583veronika-png/lab2-cicd-kiriltseva/blob/main/.github/workflows/docker-build.yml) расположен в корне **репозитория приложения** в `.github/workflows/`, поэтому GitHub обнаруживает его автоматически.

```yaml
name: Docker CI/CD

on:
  push:
    branches: [main, develop]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: docker-${{ github.ref }}
  cancel-in-progress: false

jobs:
  build-test-publish:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build image for testing
        uses: docker/build-push-action@v7
        with:
          context: .
          load: true
          tags: my-flask-app:test

      - name: Test HTTP response, user and dependencies
        run: bash scripts/test-image.sh my-flask-app:test

      - name: Validate registry secrets
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
        run: |
          if [[ -z "$DOCKER_USERNAME" || -z "$DOCKER_PASSWORD" ]]; then
            echo '::error::Configure DOCKER_USERNAME and DOCKER_PASSWORD in repository Actions secrets.'
            exit 1
          fi

      - name: Log in to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Prepare image tags
        id: tags
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
        run: |
          case "$GITHUB_REF" in
            refs/heads/main) channel=latest ;;
            refs/heads/develop) channel=develop ;;
            *) echo 'Unsupported branch'; exit 1 ;;
          esac
          {
            echo 'value<<EOF'
            echo "$DOCKER_USERNAME/my-flask-app:$channel"
            echo "$DOCKER_USERNAME/my-flask-app:sha-$GITHUB_SHA"
            echo 'EOF'
          } >> "$GITHUB_OUTPUT"

      - name: Build and push image
        uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: ${{ steps.tags.outputs.value }}

      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: echo "Deploying to production server..."

      - name: Deploy to development
        if: github.ref == 'refs/heads/develop'
        run: echo "Deploying to development server..."
```

Пайплайн запускается при push в `main` или `develop`. `workflow_dispatch` добавляет ручной запуск для повторной проверки после настройки секретов. Job использует Ubuntu, доступ к содержимому репозитория ограничен чтением. Сборки одной ветки используют общую concurrency-группу.

Checkout получает исходники, Buildx создаёт сборщик. Первая сборка загружает образ в локальный Docker runner (`load: true`), чтобы проверить его до публикации. После успешного теста выполняются проверка секретов, вход в registry и сборка с `push: true`. Повторная сборка использует кэш того же Buildx builder. Подход соответствует [документации Docker о проверке перед публикацией](https://docs.docker.com/build/ci/github-actions/test-before-push/).

Ошибка любого обязательного шага останавливает последующие обычные шаги. Таким образом, сообщение деплоя не должно появляться после неудачного теста, отсутствующих секретов или ошибки публикации.

## 3. Проверка приложения перед публикацией

Скрипт `scripts/test-image.sh` запускает временный контейнер, публикует порт 5000 на случайном свободном порту localhost и проверяет:

1. HTTP-запрос к `/` проходит без ошибки и возвращает точную строку `Hello from Docker!`.
2. Процесс в контейнере запускается с UID 1000.
3. `python -m pip check` не находит несовместимых зависимостей.

Запрос повторяется при старте сервера, поскольку процесс Flask не сразу готов принимать соединения. При выходе скрипт выводит логи и удаляет только созданный им контейнер.

Локально на macOS / Apple Silicon и Docker Engine 29.6.1 выполнено:

```sh
docker build --progress=plain -t lab2-my-flask-app:test .
bash scripts/test-image.sh lab2-my-flask-app:test
```

Сборка и тест завершились с кодом 0. Получено:

```text
HTTP /: 200; response: Hello from Docker!
Container user: UID 1000
No broken requirements found.
```

Первый HTTP-запрос получил `Empty reply from server` во время старта Flask, повторный запрос прошёл. Это зафиксировано в исходном логе; встроенный повтор успешно дождался приложения. Локальный тестовый контейнер удалён автоматически.

Доказательства: [лог сборки](logs/local-build.txt), [лог проверки контейнера](logs/local-test.txt).

`FLASK_ENV=production` сохранён из первой лабораторной. Сам Flask при этом запускается через встроенный сервер разработки; учебное сообщение production не означает настройку промышленного WSGI-сервера.

## 4. Секреты и Docker Hub

Workflow ожидает два Repository secrets в **Settings → Secrets and variables → Actions** репозитория приложения:

| Секрет | Значение |
| --- | --- |
| `DOCKER_USERNAME` | Имя пользователя Docker Hub |
| `DOCKER_PASSWORD` | Персональный токен Docker Hub с правами Read & Write |

Токен не должен храниться в YAML, Git-истории или отчёте. В `docker/login-action` оба значения передаются через контекст `secrets`. Шаг валидации проверяет только наличие значений и не выводит их.

Для публикации требуется репозиторий `my-flask-app` в аккаунте Docker Hub. На момент подготовки проекта вход в Docker Hub отсутствовал; создание registry-репозитория и добавление действительных секретов ещё не подтверждены. Эти действия и успешная публикация не считаются выполненными.

## 5. Задание со звёздочкой: ветки и версии

Созданы и отправлены на GitHub ветки `main` и `develop`. Начальный коммит в `main` содержит проект, в `develop` создан отдельный пустой коммит для проверки запуска.

```sh
git push -u origin main
git switch -c develop
git commit --allow-empty -m "Test development branch pipeline"
git push -u origin develop
git switch main
```

Условия в workflow сравнивают полную ссылку `github.ref`:

| Ветка | Публикуемые теги | Сообщение после успешной публикации |
| --- | --- | --- |
| `main` | `USERNAME/my-flask-app:latest`, `USERNAME/my-flask-app:sha-<полный SHA>` | `Deploying to production server...` |
| `develop` | `USERNAME/my-flask-app:develop`, `USERNAME/my-flask-app:sha-<полный SHA>` | `Deploying to development server...` |

`USERNAME` заменяется значением секрета. Тег `develop` отделяет образ разработки от `latest`. Тег с полным SHA позволяет определить исходный коммит образа; сам по себе он не запрещает перезапись тега в registry.

Согласно заданию деплой реализован как `echo`: фактического обновления удалённого сервера нет. Различие условий настроено в коде; подтверждение обоих сообщений в Actions требует успешного прохождения публикации.

## 6. Фактические запуски GitHub Actions

Push в обе ветки автоматически запустил workflow. Фактические статусы шагов получены через публичный GitHub REST API; исходные ответы сохранены в приложениях.

| Ветка | Коммит и запуск | Результат | Доказательство |
| --- | --- | --- | --- |
| `main` | [`dd736ed`](https://github.com/89620761583veronika-png/lab2-cicd-kiriltseva/actions/runs/34025949002) | Сборка и тесты успешны; ошибка проверки секретов | [JSON](logs/actions-main.json) |
| `develop` | [`40b6990`](https://github.com/89620761583veronika-png/lab2-cicd-kiriltseva/actions/runs/34025959070) | Сборка и тесты успешны; ошибка проверки секретов | [JSON](logs/actions-develop.json) |

В **обоих** запусках успешно выполнены `Checkout code`, `Set up Docker Buildx`, `Build image for testing` и `Test HTTP response, user and dependencies`. Поэтому проверка сборки и HTTP-ответа подтверждена и локально на arm64, и на Ubuntu runner GitHub.

`Validate registry secrets` завершился ошибкой: секреты `DOCKER_USERNAME` и `DOCKER_PASSWORD` ещё не настроены. Шаги входа, публикации и оба деплоя получили статус `skipped`. Итоговый статус запусков — **failure**, а не успешный CI/CD. Сообщения production/development и наличие образа в Docker Hub пока не подтверждены.


## 7. Что осталось для полного завершения

1. Войти в Docker Hub и создать репозиторий `my-flask-app`.
2. Добавить реальные `DOCKER_USERNAME` и `DOCKER_PASSWORD` в секреты репозитория приложения.
3. Повторить запуск через Actions → Docker CI/CD → Run workflow сначала для `main`, затем для `develop` либо отправить новые коммиты в обе ветки.
4. Проверить успешные шаги входа и публикации. В `main` должен выполниться production-шаг, development-шаг — быть пропущен; в `develop` наоборот.
5. Открыть Docker Hub → `my-flask-app` → Tags, убедиться в наличии `latest`, `develop` и SHA-тегов. Сохранить ссылки на успешные запуски и подтверждение тегов в этот отчёт.

## Вывод

Подготовлен и опубликован проект с GitHub Actions для обеих веток, проверкой реального контейнера, публикацией через секреты и условным учебным деплоем. Сборка и функциональные проверки локально выполнены успешно. Для полного завершения лабораторной необходимо подключить Docker Hub и подтвердить успешную публикацию и оба сообщения деплоя. До этого сквозной CI/CD и задание со звёздочкой не считаются полностью проверенными.

## Вопросы для защиты

1. **Что такое CI/CD?** CI автоматизирует интеграцию, сборку и проверки изменений; CD автоматизирует доставку или развёртывание проверенного результата.
2. **Где выполняются команды?** На Ubuntu runner GitHub Actions. Каждый шаг использует окружение текущего job.
3. **Зачем нужен Buildx?** Это расширенный механизм сборки образов на основе BuildKit, поддерживающий кэш и разные платформы.
4. **Чем registry отличается от репозитория Git?** Registry хранит Docker-образы, Git — исходный код и историю изменений.
5. **Почему секреты нельзя записывать в YAML?** Они попадут в Git-историю и станут доступны читателям репозитория. Контекст `secrets` передаёт их при выполнении workflow.
6. **Почему `develop` не публикует `latest`?** Иначе версия разработки могла бы заменить стабильную версию.
7. **Что произойдёт при неудачном HTTP-тесте?** Скрипт завершится ненулевым кодом, публикация и деплой не выполнятся.
8. **Это настоящий деплой на сервер?** Нет, по условиям работы используется учебный `echo`. Для настоящего деплоя нужен дополнительный механизм обновления сервиса.

## Источники

- [Правила оформления отчётов ИТМО](https://itmo-ict-faculty.github.io/introduction-in-web-tech/education/labs2025-2026/reportdesign/).
- [Docker: GitHub Actions](https://docs.docker.com/build/ci/github-actions/).
- [Docker: Test before push](https://docs.docker.com/build/ci/github-actions/test-before-push/).
- [GitHub: Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
