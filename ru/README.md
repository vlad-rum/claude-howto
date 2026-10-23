<!-- i18n-source: README.md -->
<!-- i18n-source-sha: 232591b -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

<p align="center">
  <a href="https://github.com/trending">
    <img src="https://img.shields.io/badge/GitHub-🔥%20%231%20Trending-purple?style=for-the-badge&logo=github"/>
  </a>
</p>

[![Звёзды GitHub](https://img.shields.io/github/stars/luongnv89/claude-howto?style=flat&color=gold)](https://github.com/luongnv89/claude-howto/stargazers)
[![Форки GitHub](https://img.shields.io/github/forks/luongnv89/claude-howto?style=flat)](https://github.com/luongnv89/claude-howto/network/members)
[![Лицензия: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Версия](https://img.shields.io/badge/version-2.1.302-brightgreen)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-2.1+-purple)](https://code.claude.com)

🌐 **Language / Ngôn ngữ / 语言 / Мова / 言語 / Язык:** [English](../README.md) | [Tiếng Việt](../vi/README.md) | [中文](../zh/README.md) | [Українська](../uk/README.md) | [日本語](../ja/README.md) | [Русский](README.md)

# Освойте Claude Code за выходные

От ввода `claude` до оркестрации агентов, хуков, навыков и MCP-серверов — с наглядными туториалами, шаблонами, которые можно скопировать, и учебным путём.

**[Начните за 15 минут](#начните-за-15-минут)** | **[Найдите свой уровень](#не-знаете-с-чего-начать)** | **[Откройте каталог функций](CATALOG.md)**

---

## Содержание

- [Проблема](#проблема)
- [Как Claude How To это решает](#как-claude-how-to-это-решает)
- [Как это работает](#как-это-работает)
- [Не знаете, с чего начать?](#не-знаете-с-чего-начать)
- [Начните за 15 минут](#начните-за-15-минут)
- [Что можно собрать с этим?](#что-можно-собрать-с-этим)
- [Частые вопросы](#частые-вопросы)
- [Участие в разработке](#участие-в-разработке)
- [Лицензия](#лицензия)

---

## Проблема

Вы установили Claude Code. Запустили несколько промптов. Что дальше?

- **Официальная документация описывает функции — но не показывает, как их сочетать.** Вы знаете, что слэш-команды есть, но не знаете, как связать их с хуками, памятью и субагентами в рабочий процесс, который реально экономит часы.
- **Нет ясного учебного пути.** Учить MCP раньше хуков? Навыки раньше субагентов? В итоге вы просматриваете всё и не осваиваете ничего.
- **Примеры слишком простые.** Слэш-команда «hello world» не поможет собрать продакшен-пайплайн код-ревью, который использует память, делегирует работу специализированным агентам и сам запускает проверки безопасности.

Вы оставляете 90% возможностей Claude Code нетронутыми — и не знаете, чего именно не знаете.

---

## Как Claude How To это решает

Это не очередной справочник функций. Это **структурированное наглядное руководство на примерах**: оно учит пользоваться каждой функцией Claude Code и даёт реальные шаблоны, которые можно скопировать в проект сегодня.

| | Официальная документация | Это руководство |
|--|---------------|------------|
| **Формат** | Справочная документация | Наглядные туториалы с диаграммами Mermaid |
| **Глубина** | Описания функций | Как это устроено под капотом |
| **Примеры** | Простые фрагменты | Готовые к продакшену шаблоны, которые можно использовать сразу |
| **Структура** | По функциям | Последовательный учебный путь (от начинающего до продвинутого) |
| **Онбординг** | Самостоятельный | Дорожная карта с оценкой времени |
| **Самооценка** | Нет | Интерактивные тесты, чтобы найти пробелы и собрать персональный путь |

### Что вы получаете:

- **10 модулей туториала** по каждой функции Claude Code — от слэш-команд до своих команд агентов
- **Конфиги, которые можно скопировать** — слэш-команды, шаблоны CLAUDE.md, скрипты хуков, конфиги MCP, описания субагентов и полные наборы плагинов
- **Диаграммы Mermaid**, которые показывают, как каждая функция устроена внутри, чтобы вы понимали *почему*, а не только *как*
- **Учебный путь**, который ведёт от начинающего до опытного пользователя за 11-13 часов
- **Встроенная самооценка** — запустите `/self-assessment` или `/lesson-quiz hooks` прямо в Claude Code, чтобы найти пробелы

**[Начните учебный путь ->](LEARNING-ROADMAP.md)**

---

## Как это работает

### 1. Определите свой уровень

Пройдите [квиз самооценки](LEARNING-ROADMAP.md#-найдите-свой-уровень) или запустите `/self-assessment` в Claude Code. Вы получите персональную дорожную карту по тому, что уже знаете.

### 2. Идите по учебному пути

Пройдите 10 модулей по порядку — каждый опирается на предыдущий. По ходу копируйте шаблоны прямо в свой проект.

### 3. Собирайте функции в рабочие процессы

Настоящая сила — в сочетании функций. Научитесь связывать слэш-команды + память + субагентов + хуки в автоматические пайплайны для код-ревью, деплоя и генерации документации.

### 4. Проверьте понимание

После каждого модуля запускайте `/lesson-quiz [topic]`. Квиз покажет, что вы пропустили, и пробелы закроются быстро.

**[Начните за 15 минут](#начните-за-15-минут)**

---

## Нам доверяют разработчики

- **Звёзды GitHub** от разработчиков, которые пользуются Claude Code каждый день
- **Форки** от команд, которые адаптируют это руководство под свои рабочие процессы
- **Активно поддерживается** — синхронизируется с каждым релизом Claude Code (последний: v2.1.302, октябрь 2026)
- **Силами сообщества** — вклад разработчиков, которые делятся реальными конфигурациями

[![График истории звёзд](https://api.star-history.com/svg?repos=luongnv89/claude-howto&type=Date)](https://star-history.com/#luongnv89/claude-howto&Date)

---

## Не знаете, с чего начать?

Пройдите самооценку или выберите уровень:

| Уровень | Вы умеете... | Начните здесь | Время |
|-------|-----------|------------|------|
| **Начинающий** | Запустить Claude Code и общаться | [Слэш-команды](01-slash-commands) | ~2,5 часа |
| **Средний** | Пользоваться CLAUDE.md и своими командами | [Навыки](03-skills) | ~3,5 часа |
| **Продвинутый** | Настраивать MCP-серверы и хуки | [Продвинутые функции](09-advanced-features) | ~5 часов |

**Полный учебный путь, все 10 модулей:**

| Порядок | Модуль | Уровень | Время |
|-------|--------|-------|------|
| 1 | [Слэш-команды](01-slash-commands) | Начинающий | 30 мин |
| 2 | [Память](02-memory) | Начинающий+ | 45 мин |
| 3 | [Контрольные точки](08-checkpoints) | Средний | 45 мин |
| 4 | [Основы CLI](10-cli) | Начинающий+ | 30 мин |
| 5 | [Навыки](03-skills) | Средний | 1 час |
| 6 | [Хуки](06-hooks) | Средний | 1 час |
| 7 | [MCP](05-mcp) | Средний+ | 1 час |
| 8 | [Субагенты](04-subagents) | Средний+ | 1,5 часа |
| 9 | [Продвинутые функции](09-advanced-features) | Продвинутый | 2-3 часа |
| 10 | [Плагины](07-plugins) | Продвинутый | 2 часа |

**[Полная дорожная карта обучения ->](LEARNING-ROADMAP.md)**

---

## Начните за 15 минут

> **Примечание об установке**: начиная с v2.1.113 Claude Code поставляется как нативный бинарный файл под каждую платформу (macOS/Linux/Windows). Рекомендуемая установка — нативный установщик (`curl -fsSL https://claude.ai/install.sh | bash`); установка через npm помечена как устаревшая в официальном README; предпочтительны нативный установщик, Homebrew (`brew install --cask claude-code`) или WinGet (`winget install Anthropic.ClaudeCode`). Для справки: `npm install -g @anthropic-ai/claude-code` при установке скачивает тот же нативный бинарник через необязательную зависимость для конкретной платформы. Начиная с v2.1.116 загрузки идут с `https://downloads.claude.ai/claude-code-releases` — корпоративным прокси нужно разрешить этот хост.

```bash
# 1. Клонируйте руководство
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# 2. Скопируйте первую слэш-команду
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 3. Попробуйте — в Claude Code введите:
# /optimize

# 4. Нужно больше? Настройте память проекта:
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md

# 5. Установите навык:
cp -r 03-skills/code-review-specialist ~/.claude/skills/
```

Нужна полная настройка? Вот **базовая настройка на 1 час**:

```bash
# Слэш-команды (15 мин)
cp 01-slash-commands/*.md .claude/commands/

# Память проекта (15 мин)
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Установите навык (15 мин)
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Цель на выходные: добавьте хуки, субагентов, MCP и плагины
# Дальше идите по учебному пути — настройка с пояснениями
```

**[Полная справка по установке](#начните-за-15-минут)**

---

## Что можно собрать с этим?

| Сценарий | Какие функции сочетать |
|----------|------------------------|
| **Автоматическое код-ревью** | Слэш-команды + субагенты + память + MCP |
| **Онбординг команды** | Память + слэш-команды + плагины |
| **Автоматизация CI/CD** | Справочник CLI + хуки + фоновые задачи |
| **Генерация документации** | Навыки + субагенты + плагины |
| **Аудит безопасности** | Субагенты + навыки + хуки (режим только для чтения) |
| **DevOps-пайплайны** | Плагины + MCP + хуки + фоновые задачи |
| **Сложный рефакторинг** | Контрольные точки + режим планирования + хуки |

---

## Частые вопросы

**Это бесплатно?**
Да. Лицензия MIT, бесплатно навсегда. Используйте в личных проектах, на работе, в команде — единственное условие: сохранить текст лицензии.

**Руководство поддерживается?**
Да, активно. Оно синхронизируется с каждым релизом Claude Code. Текущая версия: v2.1.302 (октябрь 2026), совместимо с Claude Code 2.1+.

**Чем это отличается от официальной документации?**
Официальная документация — справочник функций. Это руководство — туториал с диаграммами, готовыми к продакшену шаблонами и последовательным учебным путём. Они дополняют друг друга — начните здесь, чтобы разобраться, и открывайте документацию, когда нужны подробности.

**Сколько времени уйдёт на всё?**
11-13 часов на полный путь. Но пользу вы получите уже за 15 минут — скопируйте шаблон слэш-команды и попробуйте её.

**Можно ли использовать это с Claude Sonnet / Haiku / Opus?**
Да. Все шаблоны работают с Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 5.5 и Claude Haiku 4.5.

**Можно ли помочь проекту?**
Конечно. См. [CONTRIBUTING.md](CONTRIBUTING.md) — правила. Мы рады новым примерам, исправлениям ошибок, улучшению документации и шаблонам сообщества.

**Можно ли читать это офлайн?**
Да. Запустите `uv run scripts/build_epub.py`, чтобы собрать EPUB со всем содержимым и отрисованными диаграммами.

---

## Начните осваивать Claude Code сегодня

Claude Code у вас уже установлен. От продуктивности в 10 раз вас отделяет только умение им пользоваться. Это руководство даёт структурный путь, наглядные объяснения и шаблоны, которые можно скопировать.

Лицензия MIT. Бесплатно навсегда. Клонируйте, делайте форк, делайте своим.

**[Начните учебный путь ->](LEARNING-ROADMAP.md)** | **[Откройте каталог функций](CATALOG.md)** | **[Начните за 15 минут](#начните-за-15-минут)**

---

<details>
<summary>Быстрая навигация — все функции</summary>

| Функция | Описание | Папка |
|---------|-------------|--------|
| **Каталог функций** | Полный справочник с командами установки | [CATALOG.md](CATALOG.md) |
| **Слэш-команды** | Ярлыки, которые вызывает пользователь | [01-slash-commands/](01-slash-commands) |
| **Память** | Постоянный контекст | [02-memory/](02-memory) |
| **Навыки** | Повторно используемые возможности | [03-skills/](03-skills) |
| **Субагенты** | Специализированные ИИ-помощники | [04-subagents/](04-subagents) |
| **Протокол MCP** | Доступ к внешним инструментам | [05-mcp/](05-mcp) |
| **Хуки** | Автоматизация по событиям | [06-hooks/](06-hooks) |
| **Плагины** | Собранные в пакет функции | [07-plugins/](07-plugins) |
| **Контрольные точки** | Снимки сессии и возврат | [08-checkpoints/](08-checkpoints) |
| **Продвинутые функции** | Планирование, мышление, фоновые задачи | [09-advanced-features/](09-advanced-features) |
| **Справочник CLI** | Команды, флаги и параметры | [10-cli/](10-cli) |
| **Записи в блоге** | Примеры из реальной работы | [Записи в блоге](https://medium.com/@luongnv89) |

</details>

<details>
<summary>Сравнение функций</summary>

| Функция | Вызов | Что сохраняется | Лучше всего для |
|---------|-----------|------------|----------|
| **Слэш-команды** | Вручную (`/cmd`) | Только сессия | Быстрые ярлыки |
| **Память** | Загружается сама | Между сессиями | Долгосрочное обучение |
| **Навыки** | Вызываются сами | Файловая система | Автоматические рабочие процессы |
| **Субагенты** | Делегируются сами | Изолированный контекст | Распределение задач |
| **Протокол MCP** | Запросы сами | В реальном времени | Доступ к живым данным |
| **Хуки** | По событию | Настраивается | Автоматизация и проверка |
| **Плагины** | Одна команда | Все функции | Готовые решения |
| **Контрольные точки** | Вручную/авто | В рамках сессии | Безопасные эксперименты |
| **Режим планирования** | Вручную/авто | Фаза плана | Сложные реализации |
| **Фоновые задачи** | Вручную | На время задачи | Долгие операции |
| **Справочник CLI** | Команды терминала | Сессия/скрипт | Автоматизация и скрипты |

</details>

<details>
<summary>Краткая справка по установке</summary>

```bash
# Слэш-команды
cp 01-slash-commands/*.md .claude/commands/

# Память
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# Навыки
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Субагенты
cp 04-subagents/*.md .claude/agents/

# MCP
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# Хуки
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# Плагины (загрузить локальный плагин из корня репозитория)
claude --plugin-dir ./07-plugins/pr-review

# Контрольные точки (включены сами, настраиваются в settings)
# См. 08-checkpoints/README.md

# Продвинутые функции (настраиваются в settings)
# См. 09-advanced-features/config-examples.json

# Справочник CLI (установка не нужна)
# См. 10-cli/README.md — примеры использования
```

</details>

<details>
<summary>01. Слэш-команды</summary>

**Расположение**: [01-slash-commands/](01-slash-commands)

**Что**: ярлыки, которые вызывает пользователь; хранятся как файлы Markdown

**Примеры**:
- `optimize.md` - анализ оптимизации кода
- `pr.md` - подготовка pull request
- `generate-api-docs.md` - генератор документации API

**Установка**:
```bash
cp 01-slash-commands/*.md /path/to/project/.claude/commands/
```

**Использование**:
```
/optimize
/pr
/generate-api-docs
```

**Подробнее**: [Знакомство со слэш-командами Claude Code](https://medium.com/@luongnv89/discovering-claude-code-slash-commands-cdc17f0dfb29)

</details>

<details>
<summary>02. Память</summary>

**Расположение**: [02-memory/](02-memory)

**Что**: постоянный контекст между сессиями

**Примеры**:
- `project-CLAUDE.md` - стандарты проекта для всей команды
- `directory-api-CLAUDE.md` - правила для конкретного каталога
- `personal-CLAUDE.md` - личные предпочтения

**Установка**:
```bash
# Память проекта
cp 02-memory/project-CLAUDE.md /path/to/project/CLAUDE.md

# Память каталога
cp 02-memory/directory-api-CLAUDE.md /path/to/project/src/api/CLAUDE.md

# Личная память
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

**Использование**: Claude загружает автоматически

</details>

<details>
<summary>03. Навыки</summary>

**Расположение**: [03-skills/](03-skills)

**Что**: повторно используемые возможности с инструкциями и скриптами, вызываются сами

**Примеры**:
- `code-review-specialist/` - всестороннее код-ревью со скриптами
- `brand-voice/` - проверка единства голоса бренда
- `doc-generator/` - генератор документации API

**Установка**:
```bash
# Личные навыки
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# Навыки проекта
cp -r 03-skills/code-review-specialist /path/to/project/.claude/skills/
```

**Использование**: вызывается само, когда это уместно

</details>

<details>
<summary>04. Субагенты</summary>

**Расположение**: [04-subagents/](04-subagents)

**Что**: специализированные ИИ-помощники с изолированным контекстом и своими промптами

**Примеры**:
- `code-reviewer.md` - всесторонний анализ качества кода
- `test-engineer.md` - стратегия тестирования и покрытие
- `documentation-writer.md` - техническая документация
- `secure-reviewer.md` - ревью с упором на безопасность (только чтение)
- `implementation-agent.md` - полная реализация функции

**Установка**:
```bash
cp 04-subagents/*.md /path/to/project/.claude/agents/
```

**Использование**: основной агент делегирует сам

</details>

<details>
<summary>05. Протокол MCP</summary>

**Расположение**: [05-mcp/](05-mcp)

**Что**: Model Context Protocol для доступа к внешним инструментам и API

**Примеры**:
- `github-mcp.json` - интеграция с GitHub
- `database-mcp.json` - запросы к базе данных
- `filesystem-mcp.json` - операции с файлами
- `multi-mcp.json` - несколько MCP-серверов

**Установка**:
```bash
# Задайте переменные окружения
export DATABASE_URL="postgresql://..."

# Добавьте MCP-сервер через CLI
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# Или добавьте в .mcp.json проекта вручную (примеры см. в 05-mcp/)
```

**Использование**: после настройки инструменты MCP автоматически доступны Claude

</details>

<details>
<summary>06. Хуки</summary>

**Расположение**: [06-hooks/](06-hooks)

**Что**: команды оболочки по событиям, которые выполняются сами в ответ на события Claude Code

**Примеры**:
- `format-code.sh` - автоформатирование кода после записи
- `pre-commit.sh` - тесты перед коммитами
- `security-scan.sh` - поиск проблем безопасности
- `log-bash.sh` - журнал всех команд bash
- `validate-prompt.sh` - проверка промптов пользователя
- `notify-team.sh` - уведомления по событиям

**Установка**:
```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

Пропишите хуки в `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/format-code.sh" },
          { "type": "command", "command": "~/.claude/hooks/security-scan.sh" }
        ]
      }
    ]
  }
}
```

**Использование**: хуки выполняются сами по событиям

**Типы хуков** (5): `command`, `http`, `prompt`, `mcp_tool`, `agent` — как хук запускается.

**События хуков** (33, в 4 категориях) — когда он запускается:
- **Хуки инструментов**: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionRequest`, `PermissionDenied`
- **Хуки сессии**: `SessionStart`, `Setup`, `SessionEnd`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`
- **Хуки задач**: `UserPromptSubmit`, `UserPromptExpansion`, `MessageDisplay`, `TaskCompleted`, `TaskCreated`, `TeammateIdle` — `TaskCompleted` и `TaskCreated` срабатывают, только когда включены инструменты todo; по умолчанию они доступны лишь на моделях Claude 3.x, Opus с 4 по 4.7, Sonnet с 4 по 4.6 и Haiku 4.5 (`CLAUDE_CODE_ENABLE_TODO_TOOLS=1` возвращает их)
- **Хуки жизненного цикла**: `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `WorktreeCreate`, `WorktreeRemove`, `Notification`, `InstructionsLoaded`, `Elicitation`, `ElicitationResult`

</details>

<details>
<summary>07. Плагины</summary>

**Расположение**: [07-plugins/](07-plugins)

**Что**: собранные наборы команд, агентов, MCP и хуков

**Примеры**:
- `pr-review/` - полный рабочий процесс ревью PR
- `devops-automation/` - деплой и мониторинг
- `documentation/` - генерация документации

**Установка**:
```bash
# Из корня репозитория (в этом репозитории нет маркетплейса, поэтому /plugin install не подходит)
claude --plugin-dir ./07-plugins/pr-review
claude --plugin-dir ./07-plugins/devops-automation
claude --plugin-dir ./07-plugins/documentation
```

**Использование**: пользуйтесь встроенными слэш-командами и функциями

</details>

<details>
<summary>08. Контрольные точки и возврат</summary>

**Расположение**: [08-checkpoints/](08-checkpoints)

**Что**: сохраняйте состояние разговора и возвращайтесь к предыдущим точкам, чтобы пробовать разные подходы

**Ключевые понятия**:
- **Контрольная точка**: снимок состояния разговора
- **Возврат**: вернуться к предыдущей контрольной точке
- **Точка ветвления**: пробовать несколько подходов от одной контрольной точки

**Использование**:
```
# Контрольные точки создаются сами с каждым промптом пользователя
# Чтобы вернуться, нажмите Esc дважды или используйте:
/rewind

# Затем выберите один из шести вариантов:
# 1. Восстановить код и разговор
# 2. Восстановить разговор
# 3. Восстановить код
# 4. Суммировать отсюда
# 5. Суммировать до этого места
# 6. Неважно
```

**Сценарии**:
- Пробовать разные подходы к реализации
- Восстанавливаться после ошибок
- Безопасные эксперименты
- Сравнивать альтернативные решения
- A/B-тестирование разных дизайнов

</details>

<details>
<summary>09. Продвинутые функции</summary>

**Расположение**: [09-advanced-features/](09-advanced-features)

**Что**: продвинутые возможности для сложных рабочих процессов и автоматизации

**Включает**:
- **Режим планирования** — подробный план реализации до написания кода
- **Расширенное мышление** — глубокие рассуждения для сложных задач (переключение `Alt+T` / `Option+T`)
- **Фоновые задачи** — долгие операции без блокировки
- **Режимы разрешений** — `manual` (значение в конфиге `default`), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`
- **Headless-режим** — запуск Claude Code в CI/CD: `claude -p "Запусти тесты и сформируй отчёт"`
- **Управление сессиями** — `/resume`, `/rename`, `/fork`, `/branch`, `claude -c`, `claude -r`
- **Настройка** — поведение задаётся в `~/.claude/settings.json`

Полные конфигурации см. в [config-examples.json](09-advanced-features/config-examples.json).

</details>

<details>
<summary>10. Справочник CLI</summary>

**Расположение**: [10-cli/](10-cli)

**Что**: полный справочник интерфейса командной строки Claude Code

**Быстрые примеры**:
```bash
# Интерактивный режим
claude "объясни этот проект"

# Режим print (неинтерактивный)
claude -p "проверь этот код"

# Обработайте содержимое файла
cat error.log | claude -p "объясни эту ошибку"

# JSON-вывод для скриптов
claude -p --output-format json "перечисли функции"

# Продолжить сессию
claude -r "feature-auth" "продолжи реализацию"
```

**Сценарии**: интеграция в пайплайн CI/CD, автоматизация скриптами, пакетная обработка, рабочие процессы с несколькими сессиями, свои конфигурации агентов

</details>

<details>
<summary>Примеры рабочих процессов</summary>

### Полный рабочий процесс код-ревью

```markdown
# Использует: слэш-команды + субагенты + память + MCP

Пользователь: /review-pr

Claude:
1. Загружает память проекта (стандарты кода)
2. Получает PR через GitHub MCP
3. Делегирует субагенту code-reviewer
4. Делегирует субагенту test-engineer
5. Сводит выводы
6. Даёт развёрнутое ревью
```

### Автоматическая документация

```markdown
# Использует: навыки + субагенты + память

Пользователь: «Сгенерируй документацию API для модуля auth»

Claude:
1. Загружает память проекта (стандарты документации)
2. Распознаёт запрос на генерацию документации
3. Сам вызывает навык doc-generator
4. Делегирует субагенту api-documenter
5. Создаёт подробную документацию с примерами
```

### Деплой DevOps

```markdown
# Использует: плагины + MCP + хуки

Пользователь: /deploy production

Claude:
1. Запускает хук перед деплоем (проверяет окружение)
2. Делегирует субагенту deployment-specialist
3. Выполняет деплой через Kubernetes MCP
4. Следит за прогрессом
5. Запускает хук после деплоя (проверки здоровья)
6. Сообщает статус
```

</details>

<details>
<summary>Структура каталогов</summary>

```
├── 01-slash-commands/
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   └── README.md
├── 02-memory/
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   └── README.md
├── 03-skills/
│   ├── code-review-specialist/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── templates/
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   └── README.md
├── 04-subagents/
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   └── README.md
├── 05-mcp/
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
├── 06-hooks/
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   └── README.md
├── 07-plugins/
│   ├── pr-review/
│   ├── devops-automation/
│   ├── documentation/
│   └── README.md
├── 08-checkpoints/
│   ├── checkpoint-examples.md
│   └── README.md
├── 09-advanced-features/
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
├── 10-cli/
│   └── README.md
└── README.md (этот файл)
```

</details>

<details>
<summary>Рекомендации</summary>

### Делайте
- Начните с простого: со слэш-команд
- Добавляйте функции постепенно
- Храните стандарты команды в памяти
- Сначала проверяйте настройки локально
- Документируйте свои реализации
- Храните настройки проекта в системе контроля версий
- Делитесь плагинами с командой

### Не делайте
- Не создавайте дублирующие функции
- Не зашивайте учётные данные в код
- Не пропускайте документацию
- Не усложняйте простые задачи
- Не игнорируйте рекомендации по безопасности
- Не коммитьте чувствительные данные

</details>

<details>
<summary>Устранение неполадок</summary>

### Функция не загружается
1. Проверьте расположение и имя файла
2. Проверьте синтаксис frontmatter YAML
3. Проверьте права на файл
4. Проверьте совместимость версии Claude Code

### Не удалось подключиться к MCP
1. Проверьте переменные окружения
2. Проверьте установку MCP-сервера
3. Проверьте учётные данные
4. Проверьте сеть

### Субагент не получает задачи
1. Проверьте разрешения инструментов
2. Проверьте ясность описания агента
3. Оцените сложность задачи
4. Проверьте агента отдельно

</details>

<details>
<summary>Тестирование</summary>

В проекте есть подробные автоматические тесты:

- **Модульные тесты**: тесты на Python с pytest (Python 3.10, 3.11, 3.12)
- **Качество кода**: линтинг и форматирование с Ruff
- **Безопасность**: поиск уязвимостей с Bandit
- **Проверка типов**: статический анализ типов с mypy
- **Проверка сборки**: тестирование генерации EPUB
- **Учёт покрытия**: интеграция с Codecov

```bash
# Установите зависимости для разработки
uv pip install -r scripts/requirements-dev.txt

# Запустите все модульные тесты
pytest scripts/tests/ -v

# Запустите тесты с отчётом о покрытии
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# Запустите проверки качества кода
ruff check scripts/
ruff format --check scripts/

# Запустите проверку безопасности
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/

# Запустите проверку типов
mypy scripts/ --ignore-missing-imports
```

Тесты запускаются автоматически при каждом push в `main`/`develop` и каждом PR в `main`. Подробности см. в [TESTING.md](.github/TESTING.md).

</details>

<details>
<summary>Сборка EPUB</summary>

Хотите читать это руководство офлайн? Соберите книгу EPUB:

```bash
uv run scripts/build_epub.py
```

Так создаётся `claude-howto-guide.epub` со всем содержимым, включая отрисованные диаграммы Mermaid.

Дополнительные параметры см. в [scripts/README.md](scripts/README.md).

</details>

<details>
<summary>Участие в разработке</summary>

Нашли проблему или хотите прислать пример? Будем рады помощи.

**Прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) — там подробно:**
- Типы вклада (примеры, документация, функции, ошибки, отзывы)
- Как настроить окружение разработки
- Структура каталогов и как добавлять материалы
- Правила написания и рекомендации
- Процесс коммита и PR

**Нормы нашего сообщества:**
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - как мы относимся друг к другу
- [SECURITY.md](SECURITY.md) - политика безопасности и сообщения об уязвимостях

### Сообщение об уязвимостях

Если вы нашли уязвимость, сообщите о ней ответственно:

1. **Используйте GitHub Private Vulnerability Reporting**: https://github.com/luongnv89/claude-howto/security/advisories
2. **Или прочитайте** [.github/SECURITY_REPORTING.md](.github/SECURITY_REPORTING.md) — подробные инструкции
3. **НЕ** открывайте публичный issue об уязвимостях

Быстрый старт:
1. Сделайте форк и клонируйте репозиторий
2. Создайте понятную ветку (`add/feature-name`, `fix/bug`, `docs/improvement`)
3. Внесите изменения по правилам
4. Откройте pull request с ясным описанием

**Нужна помощь?** Откройте issue или обсуждение, и мы проведём вас по процессу.

</details>

<details>
<summary>Дополнительные материалы</summary>

- [Документация Claude Code](https://code.claude.com/docs/en/overview)
- [Спецификация протокола MCP](https://modelcontextprotocol.io)
- [Репозиторий навыков](https://github.com/luongnv89/skills) - набор готовых навыков
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Рабочий процесс Claude Code от Boris Cherny](https://x.com/bcherny/status/2007179832300581177) - создатель Claude Code делится своим систематизированным рабочим процессом: параллельные агенты, общий CLAUDE.md, режим планирования, слэш-команды, субагенты и проверочные хуки для автономных долгих сессий.

</details>

---

## Участие в разработке

Мы рады вкладу. Как начать, см. в [руководстве по участию](CONTRIBUTING.md).

---

## Лицензия

Лицензия MIT — см. [LICENSE](LICENSE). Можно свободно использовать, изменять и распространять. Единственное требование — сохранить текст лицензии.

---

**Обновлено**: 18 октября 2026
**Версия Claude Code**: 2.1.302
**Источники**:
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/en/permission-modes
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://github.com/anthropics/claude-code/releases
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://code.claude.com/docs/en/model-config
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://github.com/anthropics/claude-code/releases/tag/v2.1.296
- https://code.claude.com/docs/en/setup
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/en/checkpointing
- https://github.com/anthropics/claude-code
- https://code.claude.com/docs/en/changelog#2-1-302
**Совместимые модели**: Claude Fable 5.1, Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
