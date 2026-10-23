<!-- i18n-source: QUICK_REFERENCE.md -->
<!-- i18n-source-sha: ca57ef1 -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Примеры Claude Code — карточка краткого справочника

## 🚀 Краткие команды установки

### Слэш-команды
```bash
# Установить все
cp 01-slash-commands/*.md .claude/commands/

# Установить одну
cp 01-slash-commands/optimize.md .claude/commands/
```

### Память
```bash
# Память проекта
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Личная память
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### Навыки
```bash
# Личные навыки
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Навыки проекта
cp -r 03-skills/code-review-specialist .claude/skills/
```

### Субагенты
```bash
# Установить все
cp 04-subagents/*.md .claude/agents/

# Установить одного
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP
```bash
# Задайте учётные данные
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# Установите конфиг (область проекта)
cp 05-mcp/github-mcp.json .mcp.json

# Или область пользователя: добавьте в ~/.claude.json
```

### Хуки
```bash
# Установите хуки
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# Пропишите в настройках (~/.claude/settings.json)
```

### Плагины
```bash
# Установка из примеров (если опубликованы)
claude --plugin-dir ./07-plugins/pr-review
/plugin install devops-automation
/plugin install documentation
```

### Контрольные точки
```bash
# Контрольные точки создаются сами с каждым промптом пользователя
# Чтобы вернуться, нажмите Esc дважды или используйте:
/rewind

# Затем выберите: восстановить код и разговор, восстановить разговор,
# восстановить код, суммировать отсюда или неважно
```

### Продвинутые функции
```bash
# Настройте в файле настроек (.claude/settings.json)
# См. 09-advanced-features/config-examples.json

# Режим планирования
/plan Описание задачи

# Режимы разрешений (флаг --permission-mode)
# manual         - Спрашивать подтверждение на каждое действие (значение в конфиге "default"; "manual" — его псевдоним с v2.1.200)
# acceptEdits    - Автоматически принимать правки файлов, об остальном спрашивать
# plan           - Анализ только для чтения, без изменений
# auto           - Фоновый классификатор сам решает о разрешениях
# dontAsk        - Выполняются только заранее одобренные инструменты; всё остальное запрещено
# bypassPermissions - Принимать все действия (--permission-mode bypassPermissions; --dangerously-skip-permissions равнозначен)

# Управление сессиями
/resume                # Продолжить предыдущий разговор (без аргументов — выбор из прошлых сессий)
/rename "name"         # Дать имя текущей сессии
/fork [prompt]         # Скопировать разговор в новую фоновую сессию; здесь продолжаете работу
/subtask <task>        # Запустить форкнутого субагента, который наследует разговор и отчитывается
/branch [name]         # Перейти в копию разговора, сохранив оригинал
claude -c              # Продолжить самый свежий разговор
claude -r "session"    # Продолжить сессию по имени или ID
```

---

## 📋 Шпаргалка по функциям

| Функция | Путь установки | Использование |
|---------|-------------|-------|
| **Слэш-команды (60+)** | `.claude/commands/*.md` | `/command-name` |
| **Память** | `./CLAUDE.md` | Загружается сама |
| **Навыки** | `.claude/skills/*/SKILL.md` | Вызываются сами |
| **Субагенты** | `.claude/agents/*.md` | Делегируются сами |
| **MCP** | `.mcp.json` (проект) или `~/.claude.json` (пользователь) | `/mcp__server__action` |
| **Хуки (33 события)** | `~/.claude/hooks/*.sh` | По событию (5 типов) |
| **Плагины** | Через `/plugin install` | Собирает всё |
| **Контрольные точки** | Встроено | `Esc+Esc` или `/rewind` |
| **Режим планирования** | Встроено | `/plan <task>` |
| **Режимы разрешений (6)** | Встроено | `--allowedTools`, `--permission-mode` |
| **Сессии** | Встроено | `/resume`, `/rename`, `/branch`, `/fork` |
| **Фоновые задачи** | Встроено | Запуск в фоне |
| **Remote Control** | Встроено | `claude --remote-control` или `/remote-control` |
| **Веб-сессии** | Встроено | `claude --cloud "task"` |
| **Git worktree** | Встроено | `claude -w <name>` |
| **Автопамять** | Встроено | Само сохраняет в `~/.claude/projects/<project>/memory/` |
| **Список задач** | Встроено | `Ctrl+T` (контрольный список), `/tasks` (фоновая работа) |
| **Встроенные навыки** | Встроено | `/batch`, `/claude-api`, `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` *(Claude тоже может запустить это сам, везде начиная с v2.1.246; если уровень не задан, берётся последний, который вы вводили, v2.1.223)*, `/simplify` *(ревью только на подчистку; снова отличается от `/code-review` начиная с v2.1.154)*, `/debug`, `/fewer-permission-prompts`, `/loop`, `/run` *(v2.1.145+)*, `/run-skill-generator` *(v2.1.145+)*, `/verify` *(v2.1.145+; только явный вызов начиная с v2.1.215 — Claude не запускает это сам)* |

---

## 🎯 Частые сценарии

### Код-ревью
```bash
# Способ 1: слэш-команда
cp 01-slash-commands/optimize.md .claude/commands/
# Использование: /optimize

# Способ 2: субагент
cp 04-subagents/code-reviewer.md .claude/agents/
# Использование: делегируется само

# Способ 3: навык
cp -r 03-skills/code-review-specialist ~/.claude/skills/
# Использование: вызывается само

# Способ 4: плагин (лучший)
claude --plugin-dir ./07-plugins/pr-review
# Использование: /review-pr
```

### Документация
```bash
# Слэш-команда
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# Субагент
cp 04-subagents/documentation-writer.md .claude/agents/

# Навык
cp -r 03-skills/doc-generator ~/.claude/skills/

# Плагин (готовое решение)
/plugin install documentation
```

### DevOps
```bash
# Цельный плагин
/plugin install devops-automation

# Команды: /deploy, /rollback, /status, /incident
```

### Стандарты команды
```bash
# Память проекта
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Отредактируйте под свою команду
vim CLAUDE.md
```

### Автоматизация и хуки
```bash
# Установите хуки (33 события, 5 типов: command, http, mcp_tool, prompt, agent)
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# Примеры:
# - Тесты перед коммитом: pre-commit.sh
# - Автоформатирование кода: format-code.sh
# - Проверка безопасности: security-scan.sh

# Режим Auto для полностью автономных рабочих процессов
claude --permission-mode auto -p "Отрефакторь и протестируй модуль auth"
# Или переключайте режимы в интерактиве через Shift+Tab
```

### Безопасный рефакторинг
```bash
# Контрольные точки создаются сами перед каждым промптом
# Попробуйте рефакторинг
# Если получилось: продолжайте
# Если нет: нажмите Esc+Esc или используйте /rewind, чтобы вернуться
```

### Сложная реализация
```bash
# Используйте режим планирования
/plan Реализовать систему аутентификации пользователей

# Claude составляет подробный план
# Просмотрите и подтвердите
# Claude реализует по шагам
```

### Интеграция CI/CD
```bash
# Запуск в headless-режиме (неинтерактивно)
claude -p "Запусти все тесты и сформируй отчёт"

# С режимом разрешений для CI
claude -p "Запусти тесты" --permission-mode dontAsk

# С режимом Auto для полностью автономных задач CI
claude --permission-mode auto -p "Запусти тесты и исправь падения"

# С хуками для автоматизации
# См. 09-advanced-features/README.md
```

### Обучение и эксперименты
```bash
# Режим plan для безопасного анализа
claude --permission-mode plan

# Экспериментируйте безопасно — контрольные точки создаются сами
# Если нужно вернуться: нажмите Esc+Esc или используйте /rewind
```

### Команды агентов
```bash
# Включите команды агентов
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Или в settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }

# Начните с: «Реализовать функцию X командным подходом»
```

### Запланированные задачи
```bash
# Запускать команду каждые 5 минут
/loop 5m /check-status

# Разовое напоминание: попросите обычным языком (/loop повторяет, пока не отмените)
напомни мне через 30 минут проверить деплой
```

---

## 📁 Где лежат файлы

```text
Ваш проект/
├── .claude/
│   ├── commands/              # Сюда — слэш-команды
│   ├── agents/                # Сюда — субагенты
│   ├── skills/                # Сюда — навыки проекта
│   └── settings.json          # Настройки проекта (хуки и т. д.)
├── .mcp.json                  # Конфигурация MCP (область проекта)
├── CLAUDE.md                  # Память проекта
└── src/
    └── api/
        └── CLAUDE.md          # Память для конкретного каталога

Домашний каталог/
├── .claude/
│   ├── commands/              # Личные команды
│   ├── agents/                # Личные агенты
│   ├── skills/                # Личные навыки
│   ├── hooks/                 # Скрипты хуков
│   ├── settings.json          # Пользовательские настройки
│   └── CLAUDE.md              # Личная память
└── .claude.json               # Личная конфигурация MCP (область пользователя)

Системный каталог/              # macOS /Library/Application Support/ClaudeCode/, Linux /etc/claude-code/, Windows C:\Program Files\ClaudeCode\
├── managed-settings.json      # Управляемые настройки (предприятие/организация)
└── managed-settings.d/        # Подключаемые файлы управляемых настроек
```

---

## 🔍 Где искать примеры

### По категории
- **Слэш-команды**: `01-slash-commands/`
- **Память**: `02-memory/`
- **Навыки**: `03-skills/`
- **Субагенты**: `04-subagents/`
- **MCP**: `05-mcp/`
- **Хуки**: `06-hooks/`
- **Плагины**: `07-plugins/`
- **Контрольные точки**: `08-checkpoints/`
- **Продвинутые функции**: `09-advanced-features/`
- **CLI**: `10-cli/`

### По сценарию
- **Производительность**: `01-slash-commands/optimize.md`
- **Безопасность**: `04-subagents/secure-reviewer.md`
- **Тестирование**: `04-subagents/test-engineer.md`
- **Документация**: `03-skills/doc-generator/`
- **DevOps**: `07-plugins/devops-automation/`

### По сложности
- **Простое**: слэш-команды
- **Среднее**: субагенты, память
- **Продвинутое**: навыки, хуки
- **Полное**: плагины

---

## 🎓 Учебный путь

### День 1
```bash
# Прочитайте обзор
cat README.md

# Установите команду
cp 01-slash-commands/optimize.md .claude/commands/

# Попробуйте её
/optimize
```

### День 2-3
```bash
# Настройте память
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
vim CLAUDE.md

# Установите субагента
cp 04-subagents/code-reviewer.md .claude/agents/
```

### День 4-5
```bash
# Настройте MCP
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
cp 05-mcp/github-mcp.json .mcp.json

# Попробуйте команды MCP
/mcp__github__list_prs
```

### Неделя 2
```bash
# Установите навык
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Пусть он вызывается сам
# Просто скажите: «Проверь этот код на проблемы»
```

### Неделя 3+
```bash
# Установите цельный плагин
claude --plugin-dir ./07-plugins/pr-review

# Пользуйтесь встроенными функциями
/review-pr
/check-security
/check-tests
```

---

## Главное о функциях

| Функция | Описание | Использование |
|---------|-------------|-------|
| **Режим Auto** | Полностью автономная работа с фоновым классификатором; по умолчанию доступен на Bedrock/Vertex/Foundry с v2.1.207 | `Shift+Tab`, чтобы переключать режимы, или `--permission-mode auto` |
| **Каналы** | Интеграция с Discord и Telegram | флаг `--channels`, боты Discord/Telegram |
| **Голосовая диктовка** | Произносите команды и контекст для Claude | команда `/voice` |
| **Стили вывода** | Меняют роль Claude, тон и формат ответа по умолчанию | `/config` → Output style или настройка `outputStyle`. Встроенные: Default, Proactive, Explanatory, Learning, Concise |
| **Строка статуса** | Своя строка внизу сессии, которую выдаёт команда | `/statusline` или настройка `statusLine`; на stdin приходит JSON сессии, модели, стоимости и контекста |
| **Хуки (33 события)** | Расширенная система хуков с 5 типами | типы хуков command, http, mcp_tool, prompt, agent |
| **MCP Elicitation** | MCP-серверы могут запрашивать ввод пользователя во время работы | Запрос появляется сам, когда серверу нужно уточнение |
| **LSP плагинов** | Поддержка Language Server Protocol для плагинов | `userConfig`, переменная `${CLAUDE_PLUGIN_DATA}` |
| **Remote Control** | Управляйте локальной сессией с claude.ai или из приложения Claude | `claude --remote-control` (или `/remote-control` в сессии) |
| **Веб-сессии** | Облачные сессии на claude.ai/code | `claude --cloud "task"`, чтобы запустить из терминала |
| **Приложение для компьютера** | Нативное приложение для компьютера | Скачайте с claude.ai/download |
| **Список задач** | Управление фоновыми задачами | `/tasks` (псевдоним `/bashes`) |
| **Автопамять** | Автоматическое сохранение памяти из разговоров | Claude сохраняет заметки в `~/.claude/projects/<project>/memory/MEMORY.md`; управление через `/memory` |
| **AGENTS.md** *(v2.1.277)* | Файл контекста проекта для разных инструментов; читается как инструкции проекта, если нет `CLAUDE.md` в рабочем каталоге и выше | Переключайте режимы пунктом **Project instructions** в `/config`. См. [AGENTS.md](02-memory/README.md#agentsmd) |
| **Git worktree** | Изолированные рабочие пространства для параллельной разработки | `claude --worktree <name>` (или `-w`) |
| **Выбор модели** | Переключение между Fable 5.1, Fable 5, Opus 5.5, Opus 5, Sonnet 5.5, Sonnet 5, Sonnet 4.6, Opus 4.8, Haiku 5.5 и Haiku 4.5 | `/model` (`sonnet` на Anthropic API соответствует Sonnet 5.5, v2.1.284+) — с v2.1.153 выбор сохраняется как значение по умолчанию для новых сессий; нажмите `s` только для текущей сессии |
| **Команды агентов** | Координация нескольких агентов на задачах | Включите переменной окружения `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (экспериментально) |
| **Динамические Workflows** *(v2.1.154)* | Детерминированная оркестрация нескольких агентов; с v2.1.219 ориентир размера по умолчанию — medium (цель — меньше 10 агентов) | `/workflows`, чтобы смотреть запуски; попросите Claude создать такой; размер меняется пунктом **Dynamic workflow size** в `/config` |
| **Запланированные задачи** | Повторяющиеся задачи через `/loop` | `/loop 5m /command` или инструмент CronCreate |
| **Интеграция с Chrome** | Автоматизация браузера | флаг `--chrome` или команда `/chrome` |
| **Настройка клавиатуры** | Свои сочетания клавиш | команда `/keybindings` |
| **/usage-credits** | Дополнительные лимиты использования (переименовано из `/extra-usage` в v2.1.144; старое имя работает как псевдоним) | `/usage-credits` |
| **/run** *(v2.1.145+)* | Запускает приложение этого проекта, чтобы увидеть изменение в работе | `/run` |
| **/verify** *(v2.1.145+)* | Собрать, запустить и посмотреть приложение, чтобы убедиться, что исправление работает (только явный вызов с v2.1.215 — Claude не запускает это сам) | `/verify` |
| **/run-skill-generator** *(v2.1.145+)* | Учит `/run` и `/verify` работать с конкретным проектом | `/run-skill-generator` |
| **Проверка вывода субагента** *(v2.1.210+)* | Ищет в отчётах субагентов шаблоны внедрения промпта (prompt injection) и обезвреживает их | Включено по умолчанию, отключить нельзя |
| **Лимит WebSearch и ограничения на разветвление субагентов** *(v2.1.212, расширено в v2.1.219)* | 200 вызовов WebSearch за сессию, пополнение по 100 вызовов в час в интерактивных сессиях с v2.1.290; лимит одновременных субагентов (по умолчанию 20) добавлен в v2.1.217; с v2.1.219 субагенты могут порождать вложенных субагентов до **глубины 3 по умолчанию** (в v2.1.217 вложенность была отключена). Лимит в 200 порождений субагентов за сессию **снят в v2.1.224** — общего лимита на число субагентов за сессию больше нет | `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` (по умолчанию 200; `/clear` сбрасывает), `CLAUDE_CODE_WEB_SEARCH_REFILLS_PER_HOUR` (по умолчанию 100 в интерактиве, 0 с `-p`), `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (по умолчанию 20), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (по умолчанию 3; поставьте 1, чтобы отключить) |
| **Режим программы чтения с экрана** *(v2.1.208)* | Текстовый режим отрисовки для программ чтения с экрана | флаг `--ax-screen-reader`, `CLAUDE_AX_SCREEN_READER=1` или `"axScreenReader": true` в настройках |
| **Ограниченный режим** *(v2.1.248+)* | Убирает встроенные инструменты, которые запускают команды или код (такие как Bash и PowerShell), и WebFetch, если `--tools` не называет их по отдельности (не через пресет `default`); игнорирует пользовательские, проектные и локальные настройки (управляемые настройки и `--settings` по-прежнему действуют); ограничивает файловые инструменты рабочими каталогами; отвергает `bypassPermissions` и облачные сессии | `claude --restricted` или `CLAUDE_CODE_RESTRICTED=1` |
| **TTL кэша субагента** *(v2.1.248+)* | Поле frontmatter агента `experimental.cacheTtl` задаёт, как долго живёт кэш промпта субагента | Добавьте `experimental:` с `cacheTtl: "5m"` (или `"1h"`) во frontmatter агента. См. [Субагенты](04-subagents/README.md) |
| **Принудительная модель субагента** *(v2.1.257+)* | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` заставляет `CLAUDE_CODE_SUBAGENT_MODEL` переопределять frontmatter агента. С v2.1.251 переменная окружения по умолчанию больше не побеждает — приоритет у frontmatter (включая `model: inherit`), пока это не задано | `CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude` |

---

## Советы и приёмы

### Настройка под себя
- Начинайте с примеров как есть
- Подстройте под свои задачи
- Проверьте, прежде чем делиться с командой
- Храните конфигурации в системе контроля версий

### Рекомендации
- Память — для стандартов команды
- Плагины — для цельных рабочих процессов
- Субагенты — для сложных задач
- Слэш-команды — для быстрых задач

### Устранение неполадок
```bash
# Проверьте расположение файлов
ls -la .claude/commands/
ls -la .claude/agents/

# Проверьте синтаксис YAML
head -20 .claude/agents/code-reviewer.md

# Проверьте подключение MCP
echo $GITHUB_PERSONAL_ACCESS_TOKEN
```

---

## 📊 Матрица функций

| Нужно | Используйте | Пример |
|------|----------|---------|
| Быстрый ярлык | Слэш-команда (60+) | `01-slash-commands/optimize.md` |
| Стандарты команды | Память | `02-memory/project-CLAUDE.md` |
| Автоматический рабочий процесс | Навык | `03-skills/code-review-specialist/` |
| Специализированная задача | Субагент | `04-subagents/code-reviewer.md` |
| Внешние данные | MCP (+ запрос ввода) | `05-mcp/github-mcp.json` |
| Автоматизация по событиям | Хук (33 события, 5 типов) | `06-hooks/pre-commit.sh` |
| Готовое решение | Плагин (+ поддержка LSP) | `07-plugins/pr-review/` |
| Безопасный эксперимент | Контрольная точка | `08-checkpoints/checkpoint-examples.md` |
| Полная автономия | Режим Auto | `--permission-mode auto` или `Shift+Tab` |
| Интеграции с чатами | Каналы | `--channels` (Discord, Telegram) |
| Пайплайн CI/CD | CLI | `10-cli/README.md` |

---

## 🔗 Быстрые ссылки

- **Основное руководство**: `README.md`
- **Полный указатель**: `INDEX.md`
- **Исходное руководство**: `claude_concepts_guide.md`

---

## 📞 Частые вопросы

**В: Что выбрать?**
О: Начните со слэш-команд, остальные функции добавляйте по мере надобности.

**В: Можно ли смешивать функции?**
О: Да. Они работают вместе. Память + команды + MCP дают сильную связку.

**В: Как поделиться с командой?**
О: Закоммитьте каталог `.claude/` в git.

**В: А секреты?**
О: Используйте переменные окружения, никогда не зашивайте их в код.

**В: Можно ли менять примеры?**
О: Конечно. Это шаблоны, их и нужно подстраивать под себя.

---

## ✅ Контрольный список

Контрольный список для старта:

- [ ] Прочитать `README.md`
- [ ] Установить 1 слэш-команду
- [ ] Попробовать команду
- [ ] Создать проектный `CLAUDE.md`
- [ ] Установить 1 субагента
- [ ] Настроить 1 интеграцию MCP
- [ ] Установить 1 навык
- [ ] Попробовать цельный плагин
- [ ] Подстроить под себя
- [ ] Поделиться с командой

---

**Быстрый старт**: `cat README.md`

**Полный указатель**: `cat INDEX.md`

**Эта карточка**: держите под рукой как краткий справочник.

---

**Обновлено**: 18 октября 2026
**Версия Claude Code**: 2.1.302
**Источники**:
- https://code.claude.com/docs/en/workflows#set-a-size-guideline
- https://code.claude.com/docs/en/memory#agents-md
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/en/cli-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/env-vars
- https://code.claude.com/docs/en/commands
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/agent-teams
- https://code.claude.com/docs/en/memory#storage-location
- https://code.claude.com/docs/en/permission-modes
- https://code.claude.com/docs/en/managed-settings
- https://code.claude.com/docs/en/scheduled-tasks
- https://code.claude.com/docs/en/code-review-local
**Совместимые модели**: Claude Fable 5.1, Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
