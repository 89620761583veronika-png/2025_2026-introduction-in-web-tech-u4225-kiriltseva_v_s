University: [ITMO University](https://itmo.ru/ru/)\
Faculty: [FICT](https://fict.itmo.ru)\
Course: [Введение в веб технологии](https://itmo-ict-faculty.github.io/introduction-in-web-tech/)\
Year: 2025/2026\
Group: U4225\
Author: Kiriltseva Veronika Sergeevna\
Lab: Lab0\
Date of create: 05.09.2026\
Date of finished: — (будет указана после защиты)

# Лабораторная работа №0

## Создание репозитория и настройка рабочего окружения

## Цель работы

Научиться создавать репозитории, настраивать рабочее окружение и использовать Git и GitHub: подключение по SSH, клонирование, ветвление, коммиты, Pull Request и слияние изменений.

## Исходные данные и окружение

Автор: Кирильцева Вероника Сергеевна, группа U4225. Использован существующий аккаунт [89620761583veronika-png](https://github.com/89620761583veronika-png).

- Операционная система: macOS; оболочка: zsh.
- Git: `git version 2.50.1 (Apple Git-155)`.
- Веб-интерфейс GitHub открыт в Яндекс Браузере.
- SSH-ключ: Ed25519.

Учебный год 2025/2026 указан по предоставленным требованиям оформления; фактическая дата выполнения — 05.09.2026. Дата защиты пока не указана.

Для выполнения обоих требований к названиям используются два репозитория: `devops-lab-kiriltseva` для практической части и `2025_2026-introduction-in-web-tech-u4225-kiriltseva_v_s` для отчётов.

## Ход работы

### 1. Проверка Git и настройка SSH

Командой `git --version` проверено наличие Git. При первоначальной проверке каталог `~/.ssh` отсутствовал, а SSH-agent не содержал ключей.

Создан отдельный ключ и добавлен в SSH-agent:

```sh
install -d -m 700 ~/.ssh
ssh-keygen -t ed25519 -C '89620761583veronika-png devops-lab' -f ~/.ssh/id_ed25519_github_veronika -N ''
ssh-add ~/.ssh/id_ed25519_github_veronika
```

Параметр `-N ''` означает отсутствие парольной фразы. Приватный ключ хранится локально вне проекта и не публикуется. Публичная часть с расширением `.pub` добавлена в GitHub через **Settings → SSH and GPG keys → New SSH key**, тип **Authentication Key**, название **Veronika Mac - DevOps**.

Отпечаток ключа: `SHA256:lyY8RLJdsNHCsBe343mdmSEU6Ypl0U0pVxaTx9HkctE`.

Создан файл `~/.ssh/config`:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github_veronika
  IdentitiesOnly yes
  AddKeysToAgent yes
```

Для конфигурации установлены права `600`. Параметр `IdentitiesOnly yes` ограничивает выбор ключей заданной идентичностью.

Проверка соединения:

```sh
ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -T git@github.com
```

Результат:

```text
Hi 89620761583veronika-png! You've successfully authenticated, but GitHub does not provide shell access.
```

Аутентификация успешна. Код возврата `1` в этом случае ожидаем: GitHub поддерживает Git по SSH, но не предоставляет интерактивную оболочку. При первом подключении ключ сервера добавлен в `known_hosts`; режим `accept-new` не разрешает автоматически принимать изменившиеся ключи уже известных серверов.

### 2. Создание и клонирование репозитория

В GitHub создан публичный репозиторий [devops-lab-kiriltseva](https://github.com/89620761583veronika-png/devops-lab-kiriltseva). При создании включён начальный README, чтобы ветка `main` имела начальный коммит и могла служить базой Pull Request.

В каталоге `/Users/veronika/Desktop/ИКТ` выполнено:

```sh
git clone git@github.com:89620761583veronika-png/devops-lab-kiriltseva.git
cd devops-lab-kiriltseva
git config user.name 'Kiriltseva Veronika Sergeevna'
git config user.email '89620761583veronika@gmail.com'
```

Имя и почта автора настроены локально для учебного репозитория. Почта соответствует автору начального коммита, созданного аккаунтом в GitHub.

### 3. Ветка develop и файлы проекта

Создана рабочая ветка:

```sh
git switch -c develop
```

В неё добавлены:

| Файл | Содержание |
| --- | --- |
| `README.md` | Описание проекта, ФИО, группа, ссылка на GitHub, план изучения DevOps и ссылка на отчёты |
| `.gitignore` | Исключения macOS, Windows, временных файлов редакторов и локальных секретов |
| `CONTRIBUTING.md` | Правила работы с ветками, коммитами, Pull Request и документацией |

План изучения включает Git, командную строку и сети, Docker, CI/CD, инфраструктуру как код и мониторинг. Это план дальнейшего обучения, а не перечень уже выполненных лабораторных.

### 4. Коммит и публикация

```sh
git diff --check
git add README.md .gitignore CONTRIBUTING.md
git commit -m 'Initial project setup'
git push -u origin develop
```

Проверка `git diff --check` прошла без ошибок. Создан коммит [`dc2c771`](https://github.com/89620761583veronika-png/devops-lab-kiriltseva/commit/dc2c771c4ec3656ffcc2d79dd590b6b4a0f38654) с сообщением **Initial project setup**: 3 изменённых файла, 81 добавленная и 2 удалённые строки. Ветка опубликована по SSH.

### 5. Pull Request и слияние

Через веб-интерфейс создан [Pull Request №1 — Initial project setup](https://github.com/89620761583veronika-png/devops-lab-kiriltseva/pull/1), направление **develop → main**. Описание содержит назначение изменений, список файлов и проверки.

Слияние выполнено через командную строку с сохранением отдельного коммита слияния:

```sh
git switch main
git merge --no-ff develop -m 'Merge pull request #1 from 89620761583veronika-png/develop'
git push origin main
git push origin --delete develop
git branch -d develop
```

Создан коммит слияния [`6ee0985`](https://github.com/89620761583veronika-png/devops-lab-kiriltseva/commit/6ee098519ea1637a4802b1482e4f9fffefb7e130). После публикации GitHub распознал слияние Pull Request. Проверка через публичный API подтвердила `state: closed`, `merged: true` и соответствующий хеш коммита. Ветка `develop` удалена локально и на сервере.

### 6. Контроль результата

```sh
git status --short --branch
git log --oneline -3
```

После слияния рабочая копия чистая, текущая ветка синхронизирована с сервером:

```text
## main...origin/main
6ee0985 Merge pull request #1 from 89620761583veronika-png/develop
dc2c771 Initial project setup
d9ed83b Initial commit
```

Отчёт размещён в `lab0/lab0_report.md`; в корне репозитория отчётов находятся `README.md`, `.gitignore` и `LICENSE` (MIT).

## Результаты и вывод

Настроено рабочее окружение с Git и SSH-аутентификацией в нужный аккаунт. Создан и клонирован репозиторий, подготовлена документация проекта, выполнены коммит, публикация ветки, создание и слияние Pull Request. Временная ветка удалена, изменения сохранены в `main`.

Освоен цикл совместной работы: отдельная ветка → коммит → публикация → Pull Request → слияние. Git хранит локальную историю изменений, а GitHub предоставляет удалённый репозиторий и интерфейс обсуждения и проверки изменений. SSH позволяет аутентифицировать компьютер при обмене данными с сервером.

## Вопросы для защиты

1. **Чем Git отличается от GitHub?** Git — система контроля версий; GitHub — сервис размещения Git-репозиториев и совместной работы.
2. **Что делает git clone?** Создаёт локальную копию репозитория с историей и настраивает удалённый источник `origin`.
3. **Зачем нужна develop?** Позволяет подготовить изменения отдельно от основной ветки и затем предложить их через Pull Request.
4. **Что сохраняет коммит?** Снимок подготовленных изменений, ссылку на родителя, автора, время и сообщение.
5. **Что делает git push -u?** Публикует ветку и задаёт её связь с удалённой веткой для последующих push/pull.
6. **Зачем .gitignore?** Исключает неотслеживаемые файлы из обычного добавления в Git; уже отслеживаемые файлы автоматически не удаляет.
7. **Что такое Pull Request?** Предложение объединить изменения из одной ветки в другую с возможностью просмотра различий и обсуждения.
8. **Чем публичный SSH-ключ отличается от приватного?** Публичный добавляется на сервер, приватный остаётся на компьютере и доказывает владение ключом.
9. **Что означает --no-ff?** Создаёт отдельный коммит слияния даже при возможности простого перемещения указателя ветки.
10. **Почему после удаления develop изменения остаются?** Коммиты уже входят в историю `main`; удаляется ссылка на ветку, а не объединённые изменения.

## Источники

- [Задание лабораторной №0](https://itmo-ict-faculty.github.io/introduction-in-web-tech/education/labs2025-2026/lab0/lab0/).
- [Правила оформления](https://itmo-ict-faculty.github.io/introduction-in-web-tech/education/labs2025-2026/reportdesign/).
- [Создание SSH-ключа](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
- [Добавление SSH-ключа в GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
