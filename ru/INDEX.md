<!-- i18n-source: INDEX.md -->
<!-- i18n-source-sha: 232591b -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Примеры Claude Code — полный указатель

Этот документ — полный указатель всех файлов-примеров, сгруппированных по типу функции.

## Сводная статистика

- **Всего файлов**: 100+ файлов
- **Категории**: 10 категорий функций
- **Плагины**: 3 полных плагина
- **Навыки**: 6 полных навыков
- **Хуки**: 11 примеров хуков
- **Готово к использованию**: все примеры

---

## 01. Слэш-команды (10 файлов)

Сокращения, которые вызывает пользователь, для типовых рабочих процессов.

| Файл | Описание | Сценарий |
|------|-------------|----------|
| `optimize.md` | Анализатор оптимизации кода | Поиск проблем производительности |
| `pr.md` | Подготовка pull request | Автоматизация рабочего процесса PR |
| `generate-api-docs.md` | Генератор документации API | Генерация документации API |
| `commit.md` | Помощник сообщений коммита | Стандартизированные коммиты |
| `setup-ci-cd.md` | Настройка пайплайна CI/CD | Автоматизация DevOps |
| `push-all.md` | Отправка всех изменений | Быстрый рабочий процесс отправки |
| `unit-test-expand.md` | Расширение покрытия модульными тестами | Автоматизация тестов |
| `doc-refactor.md` | Рефакторинг документации | Улучшение документации |
| `pr-slash-command.png` | Пример снимка экрана | Визуальный ориентир |
| `README.md` | Документация | Руководство по установке и использованию |

**Путь установки**: `.claude/commands/`

**Использование**: `/optimize`, `/pr`, `/generate-api-docs`, `/commit`, `/setup-ci-cd`, `/push-all`, `/unit-test-expand`, `/doc-refactor`

---

## 02. Память (6 файлов)

Постоянный контекст и стандарты проекта.

| Файл | Описание | Область | Расположение |
|------|-------------|-------|----------|
| `project-CLAUDE.md` | Стандарты командного проекта | Весь проект | `./CLAUDE.md` |
| `directory-api-CLAUDE.md` | Правила для API | Каталог | `./src/api/CLAUDE.md` |
| `personal-CLAUDE.md` | Личные предпочтения | Пользователь | `~/.claude/CLAUDE.md` |
| `memory-saved.png` | Снимок экрана: память сохранена | - | Визуальный ориентир |
| `memory-ask-claude.png` | Снимок экрана: вопрос к Claude | - | Визуальный ориентир |
| `README.md` | Документация | - | Справочник |

**Установка**: скопируйте в нужное место

**Использование**: Claude загружает автоматически

**AGENTS.md** (v2.1.277): читается как инструкции проекта, если на уровне рабочего каталога или выше нет `CLAUDE.md`, `.claude/CLAUDE.md` или `CLAUDE.local.md` — см. `02-memory/README.md#agentsmd`

---

## 03. Навыки (23 файла)

Возможности с автоматическим вызовом, со скриптами и шаблонами.

### Навык код-ревью (5 файлов)
```
code-review-specialist/
├── SKILL.md                          # Определение навыка
├── scripts/
│   ├── analyze-metrics.py            # Анализатор метрик кода
│   └── compare-complexity.py         # Сравнение сложности
└── templates/
    ├── review-checklist.md           # Чек-лист ревью
    └── finding-template.md           # Документирование находки
```

**Назначение**: всестороннее код-ревью с анализом безопасности, производительности и качества

**Вызывается автоматически**: при ревью кода

---

### Навык голоса бренда (4 файла)
```
brand-voice/
├── SKILL.md                          # Определение навыка
├── templates/
│   ├── email-template.txt            # Формат письма
│   └── social-post-template.txt      # Формат для соцсетей
└── tone-examples.md                  # Примеры сообщений
```

**Назначение**: единый голос бренда в коммуникациях

**Вызывается автоматически**: при создании маркетинговых текстов

---

### Навык генератора документации (2 файла)
```
doc-generator/
├── SKILL.md                          # Определение навыка
└── generate-docs.py                  # Извлечение документации на Python
```

**Назначение**: полная документация API по исходному коду

**Вызывается автоматически**: при создании или обновлении документации API

---

### Навык рефакторинга (5 файлов)
```
refactor/
├── SKILL.md                          # Определение навыка
├── scripts/
│   ├── analyze-complexity.py         # Анализатор сложности
│   └── detect-smells.py              # Детектор запахов кода
├── references/
│   ├── code-smells.md                # Каталог запахов кода
│   └── refactoring-catalog.md        # Паттерны рефакторинга
└── templates/
    └── refactoring-plan.md           # Шаблон плана рефакторинга
```

**Назначение**: системный рефакторинг кода с анализом сложности

**Вызывается автоматически**: при рефакторинге кода

---

### Навык Claude MD (1 файл)
```
claude-md/
└── SKILL.md                          # Определение навыка
```

**Назначение**: управление файлами CLAUDE.md и их оптимизация

---

### Навык черновика блога (3 файла)
```
blog-draft/
├── SKILL.md                          # Определение навыка
└── templates/
    ├── draft-template.md             # Шаблон черновика блога
    └── outline-template.md           # Шаблон плана статьи
```

**Назначение**: черновики статей блога с единой структурой

**Плюс**: `README.md` — обзор навыков и руководство по использованию

**Путь установки**: `~/.claude/skills/` или `.claude/skills/`

---

## 04. Субагенты (10 файлов)

Специализированные ИИ-помощники со своими возможностями.

| Файл | Описание | Инструменты | Сценарий |
|------|-------------|-------|----------|
| `code-reviewer.md` | Анализ качества кода | Read, Grep, Glob, Bash | Всесторонние ревью |
| `test-engineer.md` | Анализ покрытия тестами | Read, Write, Bash, Grep | Автоматизация тестов |
| `documentation-writer.md` | Создание документации | Read, Write, Grep | Генерация документации |
| `secure-reviewer.md` | Ревью безопасности (только чтение) | Read, Grep | Аудиты безопасности |
| `implementation-agent.md` | Полная реализация | Read, Write, Edit, Bash, Grep, Glob | Разработка функций |
| `debugger.md` | Специалист по отладке | Read, Edit, Bash, Grep, Glob | Расследование багов |
| `data-scientist.md` | Специалист по анализу данных | Bash, Read, Write | Рабочие процессы с данными |
| `clean-code-reviewer.md` | Стандарты чистого кода | Read, Grep, Glob, Bash | Качество кода |
| `performance-optimizer.md` | Анализ узких мест производительности | Read, Edit, Bash, Grep, Glob | Работа по оптимизации |
| `README.md` | Документация | - | Руководство по установке и использованию |

**Путь установки**: `.claude/agents/`

**Использование**: основной агент делегирует автоматически

---

## 05. Протокол MCP (5 файлов)

Интеграции с внешними инструментами и API.

| Файл | Описание | Интеграция с | Сценарий |
|------|-------------|-----------------|----------|
| `github-mcp.json` | Интеграция с GitHub | GitHub API | Управление PR и issue |
| `database-mcp.json` | Запросы к базе данных | PostgreSQL/MySQL | Запросы к актуальным данным |
| `filesystem-mcp.json` | Операции с файлами | Локальная файловая система | Управление файлами |
| `multi-mcp.json` | Несколько серверов | GitHub + БД + Slack | Полная интеграция |
| `README.md` | Документация | - | Руководство по установке и использованию |

**Путь установки**: `.mcp.json` (область проекта) или `~/.claude.json` (область пользователя)

**Использование**: `/mcp__github__list_prs` и другие

---

## 06. Хуки (12 файлов)

Скрипты событийной автоматизации, которые выполняются сами.

| Файл | Описание | Событие | Сценарий |
|------|-------------|-------|----------|
| `format-code.sh` | Автоформатирование кода | PostToolUse (matcher: Write) | Форматирование кода |
| `pre-commit.sh` | Запуск тестов перед коммитом | PreToolUse (matcher: Bash) | Автоматизация тестов |
| `pre-tool-check.sh` | Проверка и аудит команд до запуска | PreToolUse (matcher: Bash) | Защитные ограничения, журнал аудита |
| `security-scan.sh` | Сканирование безопасности | PostToolUse (matcher: Write) | Проверки безопасности |
| `dependency-check.sh` | Сканирование манифестов зависимостей на уязвимости | PostToolUse (matcher: Write) | Проверки цепочки поставок |
| `log-bash.sh` | Журналирование команд bash | PostToolUse (matcher: Bash) | Журналирование команд |
| `notify-team.sh` | Отправка уведомлений | PostToolUse (matcher: Bash) | Уведомления команде |
| `validate-prompt.sh` | Проверка промптов | UserPromptSubmit | Проверка ввода |
| `session-end.sh` | Фиксация прогресса при завершении сессии | SessionEnd | Отслеживание прогресса |
| `context-tracker.py` | Отслеживание использования контекстного окна | UserPromptSubmit, Stop | Наблюдение за контекстом |
| `context-tracker-tiktoken.py` | Отслеживание контекста по токенам | UserPromptSubmit, Stop | Точный подсчёт токенов |
| `README.md` | Документация | - | Руководство по установке и использованию |

**Путь установки**: настройте в `~/.claude/settings.json`

**Использование**: задаются в настройках и выполняются автоматически

**Типы хуков** (5): `command`, `http`, `prompt`, `mcp_tool`, `agent` — как хук запускается.

**События хуков** (33, в 4 категориях) — когда он срабатывает:
- Хуки инструментов: PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, PermissionRequest, PermissionDenied
- Хуки сессии: SessionStart, Setup, SessionEnd, Stop, StopFailure, SubagentStart, SubagentStop
- Хуки задач: UserPromptSubmit, UserPromptExpansion, MessageDisplay, TaskCompleted, TaskCreated, TeammateIdle (TaskCompleted и TaskCreated срабатывают, только когда инструменты todo включены — по умолчанию они доступны только на моделях Claude 3.x, Opus 4–4.7, Sonnet 4–4.6 и Haiku 4.5)
- Хуки жизненного цикла: ConfigChange, CwdChanged, DirectoryAdded, FileChanged, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, WorktreeCreate, WorktreeRemove, Notification, InstructionsLoaded, Elicitation, ElicitationResult

---

## 07. Плагины (3 полных плагина, 39 файлов)

Собранные вместе наборы функций.

### Плагин ревью PR (10 файлов)
```
pr-review/
├── .claude-plugin/
│   └── plugin.json                   # Манифест плагина
├── commands/
│   ├── review-pr.md                  # Всестороннее ревью
│   ├── check-security.md             # Проверка безопасности
│   └── check-tests.md                # Проверка покрытия тестами
├── agents/
│   ├── security-reviewer.md          # Специалист по безопасности
│   ├── test-checker.md               # Специалист по тестам
│   └── performance-analyzer.md       # Специалист по производительности
├── mcp/
│   └── github-config.json            # Интеграция с GitHub
├── hooks/
│   └── pre-review.js                 # Проверка перед ревью
└── README.md                         # Документация плагина
```

**Функции**: анализ безопасности, покрытие тестами, влияние на производительность

**Команды**: `/review-pr`, `/check-security`, `/check-tests`

**Установка**: `claude --plugin-dir ./07-plugins/pr-review` (из корня репозитория)

---

### Плагин автоматизации DevOps (15 файлов)
```
devops-automation/
├── .claude-plugin/
│   └── plugin.json                   # Манифест плагина
├── commands/
│   ├── deploy.md                     # Деплой
│   ├── rollback.md                   # Откат
│   ├── status.md                     # Состояние системы
│   └── incident.md                   # Реагирование на инцидент
├── agents/
│   ├── deployment-specialist.md      # Эксперт по деплою
│   ├── incident-commander.md         # Координатор инцидентов
│   └── alert-analyzer.md             # Анализатор оповещений
├── mcp/
│   └── kubernetes-config.json        # Интеграция с Kubernetes
├── hooks/
│   ├── pre-deploy.js                 # Проверки перед деплоем
│   └── post-deploy.js                # Задачи после деплоя
├── scripts/
│   ├── deploy.sh                     # Автоматизация деплоя
│   ├── rollback.sh                   # Автоматизация отката
│   └── health-check.sh               # Проверки работоспособности
└── README.md                         # Документация плагина
```

**Функции**: деплой в Kubernetes, откат, мониторинг, реагирование на инциденты

**Команды**: `/deploy`, `/rollback`, `/status`, `/incident`

**Установка**: `claude --plugin-dir ./07-plugins/devops-automation` (из корня репозитория)

---

### Плагин документации (14 файлов)
```
documentation/
├── .claude-plugin/
│   └── plugin.json                   # Манифест плагина
├── commands/
│   ├── generate-api-docs.md          # Генерация документации API
│   ├── generate-readme.md            # Создание README
│   ├── sync-docs.md                  # Синхронизация документации
│   └── validate-docs.md              # Проверка документации
├── agents/
│   ├── api-documenter.md             # Специалист по документации API
│   ├── code-commentator.md           # Специалист по комментариям в коде
│   └── example-generator.md          # Генератор примеров
├── mcp/
│   └── github-docs-config.json       # Интеграция с GitHub
├── templates/
│   ├── api-endpoint.md               # Шаблон эндпоинта API
│   ├── function-docs.md              # Шаблон документации функции
│   └── adr-template.md               # Шаблон ADR
└── README.md                         # Документация плагина
```

**Функции**: документация API, генерация README, синхронизация документации, проверка

**Команды**: `/generate-api-docs`, `/generate-readme`, `/sync-docs`, `/validate-docs`

**Установка**: `claude --plugin-dir ./07-plugins/documentation` (из корня репозитория)

**Плюс**: `README.md` — обзор плагинов и руководство по использованию

---

## 08. Контрольные точки и перемотка (2 файла)

Сохраняйте состояние разговора и пробуйте альтернативные подходы.

| Файл | Описание | Содержание |
|------|-------------|---------|
| `README.md` | Документация | Подробное руководство по контрольным точкам |
| `checkpoint-examples.md` | Реальные примеры | Миграция базы данных, оптимизация производительности, итерации UI, отладка |
| | | |

**Ключевые понятия**:
- **Контрольная точка**: снимок состояния разговора
- **Перемотка**: возврат к предыдущей контрольной точке
- **Точка ветвления**: пробовать несколько подходов

**Использование**:
```
# Контрольные точки создаются автоматически с каждым промптом пользователя
# Чтобы перемотать, нажмите Esc дважды или выполните:
/rewind
# Затем выберите: восстановить код и разговор, восстановить разговор,
# восстановить код, суммировать отсюда, суммировать до этого места или не надо
```

**Сценарии использования**:
- Пробовать разные реализации
- Восстанавливаться после ошибок
- Безопасные эксперименты
- Сравнивать решения
- A/B-тестирование

---

## 09. Продвинутые функции (4 файла)

Продвинутые возможности для сложных рабочих процессов.

| Файл | Описание | Функции |
|------|-------------|----------|
| `README.md` | Полное руководство | Документация по всем продвинутым функциям |
| `config-examples.json` | Примеры конфигурации | 10+ конфигураций под конкретные сценарии |
| `planning-mode-examples.md` | Примеры планирования | REST API, миграция базы данных, рефакторинг |
| `setup-auto-mode-permissions.py` | Заполняет `permissions.allow` для режима Auto | Идемпотентный скрипт, флаги `--dry-run` и явного включения |
| Динамические Workflows | Детерминированная оркестрация множества агентов через `/workflows` (v2.1.154) | Всесторонние аудиты, миграции, масштабирование |
| Запланированные задачи | Повторяющиеся задачи с `/loop` и инструментами cron | Автоматизированные повторяющиеся рабочие процессы |
| Интеграция с Chrome | Автоматизация браузера в вашем Chrome через расширение Claude in Chrome | Веб-тестирование и сбор данных со страниц |
| Remote Control (расширено) | Способы подключения, безопасность, сравнительная таблица, карточки устройств | Удалённое управление сессиями (больше не исследовательская предварительная версия) |
| Обмен сообщениями между сессиями | `SendMessage` / `ListAgents`, включая `notify_when_idle` (v2.1.236) | Координация сессий на одной машине |
| Настройка клавиатуры | Свои сочетания клавиш, поддержка аккордов, контексты | Персональные сочетания |
| Десктоп-приложение (расширено) | Коннекторы, launch.json, корпоративные функции | Интеграция с рабочим столом |
| | | |

**Рассмотренные продвинутые функции**:

### Режим планирования
- Подробные планы реализации
- Оценки времени и рисков
- Системная разбивка задач

### Расширенное мышление
- Глубокие рассуждения для сложных задач
- Анализ архитектурных решений
- Оценка компромиссов

### Фоновые задачи
- Долгие операции без блокировки
- Параллельные рабочие процессы разработки
- Управление задачами и наблюдение за ними

### Динамические Workflows (v2.1.154)
- Детерминированная оркестрация от десятков до сотен фоновых субагентов
- Веерное распределение (fan-out) / пайплайн / параллельные этапы для полного охвата
- Смотрите запуски через `/workflows`; переключатель Ultracode в `/effort` (`/effort ultracode [on\|off]`) включает его на сессию, не меняя уровень усилий (v2.1.284); настройка `ultracode` делает это постоянным
- Ориентир размера по умолчанию — medium (стремитесь к менее чем 10 агентам) с v2.1.219 — измените его пунктом **Dynamic workflow size** в `/config`

### Режимы разрешений
- **manual**: спрашивать перед всем, кроме чтения (с v2.1.200 отображается как Manual; значение в конфигурации по-прежнему `default`)
- **acceptEdits**: автоматически принимать правки файлов, об остальных спрашивать
- **plan**: анализ только для чтения, без изменений
- **auto**: всё, с фоновыми проверками безопасности — классификатор проверяет команды и запись в защищённые каталоги (настраивается объектом настроек `autoMode`)
- **dontAsk**: только заранее одобренные инструменты — автоматически отклоняет каждый вызов, который иначе вызвал бы запрос. Claude выполняет только совпадения с `permissions.allow`, команды Bash только для чтения и вызовы, одобренные хуком `PreToolUse`
- **bypassPermissions**: принимать всё (включите через `--permission-mode bypassPermissions` или равнозначный `--dangerously-skip-permissions`)

### Режим headless (`claude -p`)
- Интеграция с CI/CD
- Автоматическое выполнение задач
- Пакетная обработка

### Управление сессиями
- Несколько рабочих сессий
- Переключение и сохранение сессий
- Сохранение сессий между запусками

### Интерактивные функции
- Сочетания клавиш
- История команд
- Дополнение по Tab
- Многострочный ввод

### Конфигурация
- Полноценное управление настройками
- Конфигурации под окружение
- Настройка для каждого проекта

### Запланированные задачи
- Повторяющиеся задачи командой `/loop`
- Инструменты cron: CronCreate, CronList, CronDelete
- Автоматизированные повторяющиеся рабочие процессы

### Интеграция с Chrome
- Автоматизация браузера в вашем Chrome через расширение Claude in Chrome
- Веб-тестирование и сбор данных со страниц
- Взаимодействие со страницей и извлечение данных

### Remote Control (расширено)
- Способы и протоколы подключения
- Соображения безопасности и лучшие практики
- Сравнительная таблица вариантов удалённого доступа
- Вышел из исследовательской предварительной версии — машина, на которой запущен `claude remote-control`, появляется карточкой устройства на вкладке Code в приложении Claude

### Обмен сообщениями между сессиями
- `SendMessage` между сессиями на одной машине
- `notify_when_idle` — одно уведомление по явному включению, когда другая сессия в следующий раз перейдёт в простой (v2.1.236)
- `ListAgents` сообщает собственное имя сессии и перечисляет активных участников (v2.1.239)

### Настройка клавиатуры
- Настройка своих сочетаний клавиш
- Поддержка аккордов для многоклавишных сочетаний
- Включение сочетаний с учётом контекста

### Десктоп-приложение (расширено)
- Коннекторы для интеграции с IDE
- Конфигурация launch.json
- Корпоративные функции и деплой

---

## 10. Использование CLI (1 файл)

Шаблоны использования интерфейса командной строки (CLI) и справочник.

| Файл | Описание | Содержание |
|------|-------------|---------|
| `README.md` | Документация CLI | Флаги, параметры и шаблоны использования |

**Ключевые возможности CLI**:
- `claude` — запустить интерактивную сессию
- `claude -p "prompt"` — режим headless / неинтерактивный режим
- `claude --cloud "task"` — запустить облачную (веб) сессию
- `claude --model` — выбрать модель (Opus 5.5, Sonnet 5.5, Opus 5, Sonnet 5, Sonnet 4.6, Opus 4.8, Haiku 5.5, Haiku 4.5)
- `claude --permission-mode` — задать режим разрешений
- `claude --remote-control` — запустить сессию, которой можно управлять также с claude.ai или из приложения Claude

---

## Файлы документации (13 файлов)

| Файл | Расположение | Описание |
|------|----------|-------------|
| `README.md` | `/` | Главный обзор примеров |
| `INDEX.md` | `/` | Этот полный указатель |
| `QUICK_REFERENCE.md` | `/` | Карточка краткого справочника |
| `README.md` | `/01-slash-commands/` | Руководство по слэш-командам |
| `README.md` | `/02-memory/` | Руководство по памяти |
| `README.md` | `/03-skills/` | Руководство по навыкам |
| `README.md` | `/04-subagents/` | Руководство по субагентам |
| `README.md` | `/05-mcp/` | Руководство по MCP |
| `README.md` | `/06-hooks/` | Руководство по хукам |
| `README.md` | `/07-plugins/` | Руководство по плагинам |
| `README.md` | `/08-checkpoints/` | Руководство по контрольным точкам |
| `README.md` | `/09-advanced-features/` | Руководство по продвинутым функциям |
| `README.md` | `/10-cli/` | Руководство по CLI |

---

## Полное дерево файлов

```
claude-howto/
├── README.md                                    # Главный обзор
├── INDEX.md                                     # Этот файл
├── QUICK_REFERENCE.md                           # Карточка краткого справочника
├── claude_concepts_guide.md                     # Исходное руководство
│
├── 01-slash-commands/                           # Слэш-команды
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   ├── commit.md
│   ├── setup-ci-cd.md
│   ├── push-all.md
│   ├── unit-test-expand.md
│   ├── doc-refactor.md
│   ├── pr-slash-command.png
│   └── README.md
│
├── 02-memory/                                   # Память
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   ├── memory-saved.png
│   ├── memory-ask-claude.png
│   └── README.md
│
├── 03-skills/                                   # Навыки
│   ├── code-review-specialist/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── analyze-metrics.py
│   │   │   └── compare-complexity.py
│   │   └── templates/
│   │       ├── review-checklist.md
│   │       └── finding-template.md
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   ├── templates/
│   │   │   ├── email-template.txt
│   │   │   └── social-post-template.txt
│   │   └── tone-examples.md
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   ├── refactor/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── analyze-complexity.py
│   │   │   └── detect-smells.py
│   │   ├── references/
│   │   │   ├── code-smells.md
│   │   │   └── refactoring-catalog.md
│   │   └── templates/
│   │       └── refactoring-plan.md
│   ├── claude-md/
│   │   └── SKILL.md
│   ├── blog-draft/
│   │   ├── SKILL.md
│   │   └── templates/
│   │       ├── draft-template.md
│   │       └── outline-template.md
│   └── README.md
│
├── 04-subagents/                                # Субагенты
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   ├── debugger.md
│   ├── data-scientist.md
│   ├── clean-code-reviewer.md
│   └── README.md
│
├── 05-mcp/                                      # Протокол MCP
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
│
├── 06-hooks/                                    # Хуки
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   ├── context-tracker.py
│   ├── context-tracker-tiktoken.py
│   └── README.md
│
├── 07-plugins/                                  # Плагины
│   ├── pr-review/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── review-pr.md
│   │   │   ├── check-security.md
│   │   │   └── check-tests.md
│   │   ├── agents/
│   │   │   ├── security-reviewer.md
│   │   │   ├── test-checker.md
│   │   │   └── performance-analyzer.md
│   │   ├── mcp/
│   │   │   └── github-config.json
│   │   ├── hooks/
│   │   │   └── pre-review.js
│   │   └── README.md
│   ├── devops-automation/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── deploy.md
│   │   │   ├── rollback.md
│   │   │   ├── status.md
│   │   │   └── incident.md
│   │   ├── agents/
│   │   │   ├── deployment-specialist.md
│   │   │   ├── incident-commander.md
│   │   │   └── alert-analyzer.md
│   │   ├── mcp/
│   │   │   └── kubernetes-config.json
│   │   ├── hooks/
│   │   │   ├── pre-deploy.js
│   │   │   └── post-deploy.js
│   │   ├── scripts/
│   │   │   ├── deploy.sh
│   │   │   ├── rollback.sh
│   │   │   └── health-check.sh
│   │   └── README.md
│   ├── documentation/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── generate-api-docs.md
│   │   │   ├── generate-readme.md
│   │   │   ├── sync-docs.md
│   │   │   └── validate-docs.md
│   │   ├── agents/
│   │   │   ├── api-documenter.md
│   │   │   ├── code-commentator.md
│   │   │   └── example-generator.md
│   │   ├── mcp/
│   │   │   └── github-docs-config.json
│   │   ├── templates/
│   │   │   ├── api-endpoint.md
│   │   │   ├── function-docs.md
│   │   │   └── adr-template.md
│   │   └── README.md
│   └── README.md
│
├── 08-checkpoints/                              # Контрольные точки
│   ├── checkpoint-examples.md
│   └── README.md
│
├── 09-advanced-features/                        # Продвинутые функции
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
│
└── 10-cli/                                      # Использование CLI
    └── README.md
```

---

## Быстрый старт по сценарию

### Качество кода и ревью
```bash
# Установите слэш-команду
cp 01-slash-commands/optimize.md .claude/commands/

# Установите субагента
cp 04-subagents/code-reviewer.md .claude/agents/

# Установите навык
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Или установите полный плагин
claude --plugin-dir ./07-plugins/pr-review
```

### DevOps и деплой
```bash
# Установите плагин (в нём есть всё)
claude --plugin-dir ./07-plugins/devops-automation
```

### Документация
```bash
# Установите слэш-команду
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# Установите субагента
cp 04-subagents/documentation-writer.md .claude/agents/

# Установите навык
cp -r 03-skills/doc-generator ~/.claude/skills/

# Или установите полный плагин
claude --plugin-dir ./07-plugins/documentation
```

### Стандарты команды
```bash
# Настройте память проекта
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Отредактируйте под стандарты вашей команды
```

### Внешние интеграции
```bash
# Задайте переменные окружения
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
export DATABASE_URL="postgresql://..."
export SLACK_BOT_TOKEN="your-slack-bot-token"
export SLACK_TEAM_ID="T0000000000"

# Установите конфигурацию MCP (область проекта)
cp 05-mcp/multi-mcp.json .mcp.json
```

### Автоматизация и проверка
```bash
# Установите хуки
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# Настройте хуки в настройках (~/.claude/settings.json)
# См. 06-hooks/README.md
```

### Безопасные эксперименты
```bash
# Контрольные точки создаются автоматически с каждым промптом пользователя
# Чтобы перемотать: нажмите Esc+Esc или выполните /rewind
# Затем выберите, что восстановить, в меню перемотки

# См. примеры в 08-checkpoints/README.md
```

### Продвинутые рабочие процессы
```bash
# Настройте продвинутые функции
# См. 09-advanced-features/config-examples.json

# Используйте режим планирования
/plan Implement feature X

# Используйте режимы разрешений
claude --permission-mode plan          # Для код-ревью (только чтение)
claude --permission-mode acceptEdits   # Автоматически принимать правки
claude --permission-mode auto          # Автоматически одобрять безопасные действия

# Запустите в режиме headless для CI/CD
claude -p "Run tests and report results"

# Запустите фоновые задачи
Запусти тесты в фоне

# См. полное руководство в 09-advanced-features/README.md
```

---

## Матрица покрытия функций

| Категория | Команды | Агенты | MCP | Хуки | Скрипты | Шаблоны | Документы | Изображения | Всего |
|----------|----------|--------|-----|-------|---------|-----------|------|--------|-------|
| **01 Слэш-команды** | 8 | - | - | - | - | - | 1 | 1 | **10** |
| **02 Память** | - | - | - | - | - | 3 | 1 | 2 | **6** |
| **03 Навыки** | - | - | - | - | 5 | 7 | 11 | - | **23** |
| **04 Субагенты** | - | 9 | - | - | - | - | 1 | - | **10** |
| **05 MCP** | - | - | 4 | - | - | - | 1 | - | **5** |
| **06 Хуки** | - | - | - | 11 | - | - | 1 | - | **12** |
| **07 Плагины** | 11 | 9 | 3 | 3 | 3 | 3 | 7 | - | **39** |
| **08 Контрольные точки** | - | - | - | - | - | - | 1 | 1 | **2** |
| **09 Продвинутые** | - | - | - | - | 1 | 1 | 2 | - | **4** |
| **10 CLI** | - | - | - | - | - | - | 1 | - | **1** |

---

## Учебный путь

### Начинающий (неделя 1)
1. ✅ Прочитайте `README.md`
2. ✅ Установите 1–2 слэш-команды
3. ✅ Создайте файл памяти проекта
4. ✅ Попробуйте базовые команды

### Средний уровень (недели 2–3)
1. ✅ Настройте GitHub MCP
2. ✅ Установите субагента
3. ✅ Попробуйте делегировать задачи
4. ✅ Установите навык

### Продвинутый (неделя 4+)
1. ✅ Установите полный плагин
2. ✅ Создайте свои слэш-команды
3. ✅ Создайте своего субагента
4. ✅ Создайте свой навык
5. ✅ Соберите свой плагин

### Эксперт (неделя 5+)
1. ✅ Настройте хуки для автоматизации
2. ✅ Используйте контрольные точки для экспериментов
3. ✅ Настройте режим планирования
4. ✅ Эффективно используйте режимы разрешений
5. ✅ Настройте режим headless для CI/CD
6. ✅ Освойте управление сессиями

---

## Поиск по ключевому слову

### Производительность
- `01-slash-commands/optimize.md` — анализ производительности
- `04-subagents/code-reviewer.md` — ревью производительности
- `03-skills/code-review-specialist/` — метрики производительности
- `07-plugins/pr-review/agents/performance-analyzer.md` — специалист по производительности

### Безопасность
- `04-subagents/secure-reviewer.md` — ревью безопасности
- `03-skills/code-review-specialist/` — анализ безопасности
- `07-plugins/pr-review/` — проверки безопасности

### Тестирование
- `04-subagents/test-engineer.md` — инженер по тестам
- `07-plugins/pr-review/commands/check-tests.md` — покрытие тестами

### Документация
- `01-slash-commands/generate-api-docs.md` — команда документации API
- `04-subagents/documentation-writer.md` — агент-автор документации
- `03-skills/doc-generator/` — навык генератора документации
- `07-plugins/documentation/` — полный плагин документации

### Деплой
- `07-plugins/devops-automation/` — полное решение DevOps

### Автоматизация
- `06-hooks/` — событийная автоматизация
- `06-hooks/pre-commit.sh` — автоматизация перед коммитом
- `06-hooks/format-code.sh` — автоформатирование
- `09-advanced-features/` — режим headless для CI/CD

### Проверка
- `06-hooks/security-scan.sh` — проверка безопасности
- `06-hooks/validate-prompt.sh` — проверка промптов

### Эксперименты
- `08-checkpoints/` — безопасные эксперименты с перемоткой
- `08-checkpoints/checkpoint-examples.md` — реальные примеры

### Планирование
- `09-advanced-features/planning-mode-examples.md` — примеры режима планирования
- `09-advanced-features/README.md` — расширенное мышление

### Конфигурация
- `09-advanced-features/config-examples.json` — примеры конфигурации

---

## Примечания

- Все примеры готовы к использованию
- Измените их под свои задачи
- Примеры следуют лучшим практикам Claude Code
- У каждой категории свой README с подробными инструкциями
- В скриптах есть нормальная обработка ошибок
- Шаблоны можно настраивать

---

## Участие в разработке

Хотите добавить ещё примеры? Следуйте структуре:
1. Создайте подходящий подкаталог
2. Добавьте README.md с описанием использования
3. Соблюдайте соглашения об именах
4. Тщательно протестируйте
5. Обновите этот указатель

---

**Последнее обновление**: 18 октября 2026
**Версия Claude Code**: 2.1.302
**Источники**:
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/en/workflows#set-a-size-guideline
- https://code.claude.com/docs/en/memory#agents-md
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/permission-modes
- https://github.com/anthropics/claude-code/releases/tag/v2.1.153
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/workflows#let-claude-decide-with-ultracode
- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/chrome
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
**Всего примеров**: 100+ файлов
**Категории**: 10 функций
**Хуки**: 11 скриптов автоматизации
**Примеры конфигурации**: 10+ сценариев
**Готово к использованию**: все примеры
