<!-- i18n-source: 05-mcp/README.md -->
<!-- i18n-source-sha: 188f468 -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# MCP (Model Context Protocol)

В этой папке — подробная документация и примеры конфигурации MCP-серверов и работы с ними в Claude Code.

## Обзор

MCP (Model Context Protocol) — стандартный способ дать Claude доступ к внешним инструментам, API и источникам данных в реальном времени. В отличие от памяти, MCP даёт живой доступ к данным, которые меняются.

Основные свойства:

- Доступ к внешним сервисам в реальном времени
- Живая синхронизация данных
- Расширяемая архитектура
- Безопасная аутентификация
- Взаимодействие через инструменты

## Архитектура MCP

```mermaid
graph TB
    A["Claude"]
    B["MCP-сервер"]
    C["Внешний сервис"]

    A -->|"Запрос: list_issues"| B
    B -->|Запрос| C
    C -->|Данные| B
    B -->|Ответ| A

    A -->|"Запрос: create_issue"| B
    B -->|Действие| C
    C -->|Результат| B
    B -->|Ответ| A

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#e8f5e9,stroke:#333,color:#333
```

## Экосистема MCP

```mermaid
graph TB
    A["Claude"] -->|MCP| B["Filesystem<br/>MCP-сервер"]
    A -->|MCP| C["GitHub<br/>MCP-сервер"]
    A -->|MCP| D["Database<br/>MCP-сервер"]
    A -->|MCP| E["Slack<br/>MCP-сервер"]
    A -->|MCP| F["Google Docs<br/>MCP-сервер"]

    B -->|"Ввод-вывод файлов"| G["Локальные файлы"]
    C -->|API| H["Репозитории GitHub"]
    D -->|Запрос| I["PostgreSQL/MySQL"]
    E -->|Сообщения| J["Рабочее пространство Slack"]
    F -->|Документы| K["Google Drive"]

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#f3e5f5,stroke:#333,color:#333
    style F fill:#f3e5f5,stroke:#333,color:#333
    style G fill:#e8f5e9,stroke:#333,color:#333
    style H fill:#e8f5e9,stroke:#333,color:#333
    style I fill:#e8f5e9,stroke:#333,color:#333
    style J fill:#e8f5e9,stroke:#333,color:#333
    style K fill:#e8f5e9,stroke:#333,color:#333
```

## Способы подключения MCP

Claude Code поддерживает несколько транспортных протоколов для подключения MCP-серверов.

### HTTP-транспорт (рекомендуется)

```bash
# Обычное HTTP-соединение
claude mcp add --transport http notion https://mcp.notion.com/mcp

# HTTP с заголовком аутентификации
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Транспорт stdio (локальный)

Для MCP-серверов, которые работают локально:

```bash
# Локальный сервер Node.js
claude mcp add --transport stdio myserver -- npx @myorg/mcp-server

# С переменными окружения
claude mcp add --transport stdio myserver --env KEY=value -- npx server
```

#### `CLAUDE_PROJECT_DIR` для stdio-серверов (v2.1.139+)

Каждый MCP-сервер на stdio запускается с уже заданной в окружении переменной `CLAUDE_PROJECT_DIR=<абсолютный путь к корню репозитория>` — то же соглашение, что и у хуков. В файлах `.mcp.json` плагина и проекта можно ссылаться на `${CLAUDE_PROJECT_DIR}` в значениях `command`, `args` и `env`, и подстановка происходит до `execve()`:

```json
{
  "mcpServers": {
    "repo-tools": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp/repo-tools.js"],
      "env": {
        "REPO_ROOT": "${CLAUDE_PROJECT_DIR:-.}"
      }
    }
  }
}
```

> **Примечание**: В конфигурациях проекта, локальной и пользователя пишите `${CLAUDE_PROJECT_DIR:-.}` со значением по умолчанию: переменная задаётся в окружении сервера, а не в собственном окружении Claude Code. Только конфигурации MCP плагина подставляют `${CLAUDE_PROJECT_DIR}` напрямую.

Используйте это, когда stdio-серверу нужно читать файлы относительно корня проекта независимо от того, откуда запущен Claude Code.

Stdio MCP-серверы также получают `CLAUDE_CODE_SESSION_ID` (то же значение, что передаётся хукам и Bash), в том числе когда сессия возобновляется через `--resume` (v2.1.163+).

### Транспорт SSE (устарел)

Транспорт Server-Sent Events устарел в пользу `http`, но по-прежнему поддерживается:

```bash
claude mcp add --transport sse legacy-server https://example.com/sse
```

### Транспорт WebSocket (`ws`)

Серверы WebSocket держат постоянное двустороннее соединение. Это подходит удалённым MCP-серверам, которые сами присылают Claude события, без запроса с его стороны. Используйте HTTP, если сервер только отвечает на запросы: HTTP поддерживает OAuth и флаг `claude mcp add --transport`, а WebSocket не поддерживает ни то ни другое.

Поскольку `--transport` не принимает `ws`, задайте его в `.mcp.json` или через `claude mcp add-json`:

```json
{
  "type": "ws",
  "url": "wss://mcp.example.com/socket",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  }
}
```

Запись `type: "ws"` принимает те же поля `url`, `headers`, `headersHelper`, `timeout` и `alwaysLoad`, что и `http`. Аутентификация **только через заголовки** — потока OAuth для серверов WebSocket нет.

> **Примечание**: С v2.1.285 `claude mcp list` показывает серверы WebSocket (`ws`) вместе с URL и статусом работоспособности (в более ранних версиях они не попадали в список). Их также можно проверить через `claude mcp get <name>` или панель `/mcp`.

Как HTTP и SSE, соединения WebSocket используют 5-минутное окно простоя; у stdio и WebSocket нет отдельного таймера на каждый запрос. Запись `url` без `type` — ошибка. Допустимые значения: `"http"`, `"sse"` и `"ws"`.

### Рабочие каталоги сессии (roots/list)

MCP-серверы могут узнать рабочие каталоги сессии: каталог запуска плюс все записи `--add-dir` и `additionalDirectories` возвращаются запросом MCP `roots/list`, а при изменении набора отправляется уведомление `notifications/roots/list_changed` (v2.1.203). Таймаут простоя теперь действует и на stdio-серверы (30 минут), а поле `timeout` конкретного сервера задаёт нижнюю границу простоя (v2.1.203).

### Замечание для Windows

В нативном Windows (не WSL) для команд npx используйте `cmd /c`:

```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### Аутентификация OAuth 2.0

Claude Code поддерживает OAuth 2.0 для MCP-серверов, которым он нужен. При подключении к серверу с OAuth Claude Code проводит весь поток аутентификации:

```bash
# Подключение к MCP-серверу с OAuth (интерактивный поток)
claude mcp add --transport http my-service https://my-service.example.com/mcp

# Заранее задать учётные данные OAuth для неинтерактивной настройки
claude mcp add --transport http my-service https://my-service.example.com/mcp \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --callback-port 8080
```

| Функция | Описание |
|---------|-------------|
| **Интерактивный OAuth** | Команда `/mcp` запускает поток OAuth в браузере |
| **Предустановленные OAuth-клиенты** | Встроенные OAuth-клиенты для распространённых сервисов, таких как Notion, Stripe и других (v2.1.30+) |
| **Заранее заданные учётные данные** | Флаги `--client-id`, `--client-secret`, `--callback-port` для автоматической настройки |
| **Хранение токенов** | Токены надёжно хранятся в системной связке ключей |
| **Повышенная аутентификация** | Поддерживается повышенная аутентификация (step-up) для привилегированных операций |
| **Кэш обнаружения** | Метаданные обнаружения OAuth кэшируются, чтобы быстрее подключаться снова |
| **Переопределение метаданных** | `oauth.authServerMetadataUrl` в `.mcp.json` переопределяет обнаружение метаданных OAuth по умолчанию |

#### Переопределение обнаружения метаданных OAuth

Если MCP-сервер возвращает ошибки на стандартной конечной точке метаданных OAuth (`/.well-known/oauth-authorization-server`), но открывает рабочую конечную точку OIDC, можно указать Claude Code, откуда забирать метаданные OAuth. Задайте `authServerMetadataUrl` в объекте `oauth` конфигурации сервера:

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL должен начинаться с `https://`. Параметр требует Claude Code v2.1.64 или новее.

#### Уведомление об аутентификации при запуске и обновление динамических заголовков (v2.1.193)

- **Уведомление об аутентификации при запуске (v2.1.193+)**: при старте Claude Code показывает список MCP-серверов, которым ещё нужна аутентификация, чтобы сервер, ожидающий входа, не оставался молча нерабочим.
- **Автообновление `headersHelper` (v2.1.193+)**: если собственная аутентификация задана через `headersHelper`, помощник вызывается снова сам, когда сервер возвращает HTTP 401 или 403. Учётные данные обновляются на лету, без ручного переподключения. См. [Динамические заголовки для собственной аутентификации](https://code.claude.com/docs/en/mcp).

> **Предупреждение** (v2.1.238): `headersHelper` в проектном `.mcp.json`, а также встроенные MCP-серверы в файлах агентов проекта или каталогов `--add-dir`, теперь требуют, чтобы диалог доверия для этой папки был принят — в том числе при `claude -p`. Такие помощники ещё и запускаются **без унаследованных переменных окружения с учётными данными**; помощники областей user, managed и claude.ai запускаются из каталога конфигурации Claude. Проектная конфигурация, которая полагалась на унаследованные учётные данные или на запуск без доверия, перестанет работать, пока вы не примете диалог доверия и не передадите учётные данные другим способом.

### Коннекторы MCP в Claude.ai

MCP-серверы, настроенные в учётной записи Claude.ai, автоматически доступны в Claude Code. Соединения MCP, которые вы создали в веб-интерфейсе Claude.ai, работают без дополнительной настройки.

Коннекторы MCP Claude.ai доступны и в режиме `--print` (v2.1.83+), поэтому ими можно пользоваться неинтерактивно и из скриптов.

> **Заметка о запуске (v2.1.117+):** параллельное подключение включено по умолчанию, когда настроены и локальные MCP-серверы, и серверы claude.ai (раньше подключение было последовательным). Так меньше задержка старта, если серверов несколько.

Чтобы отключить MCP-серверы Claude.ai в Claude Code, задайте переменную окружения `ENABLE_CLAUDEAI_MCP_SERVERS` значением `false`:

```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

> **Примечание:** эта функция доступна только пользователям, вошедшим через учётную запись Claude.ai.

## Процесс настройки MCP

```mermaid
sequenceDiagram
    participant User as Пользователь
    participant Claude as Claude Code
    participant Config as Файл конфигурации
    participant Service as Внешний сервис

    User->>Claude: Вводит /mcp
    Claude->>Claude: Перечисляет доступные MCP-серверы
    Claude->>User: Показывает варианты
    User->>Claude: Выбирает GitHub MCP
    Claude->>Config: Обновляет конфигурацию
    Config->>Claude: Активирует соединение
    Claude->>Service: Проверяет соединение
    Service-->>Claude: Аутентификация успешна
    Claude->>User: ✅ MCP подключён!
```

### Команда `/mcp`

Введите `/mcp` внутри сессии, чтобы увидеть подключённые серверы, запустить потоки OAuth и проверить состояние соединения.

- С **v2.1.121** MCP повторяет первую попытку соединения до 3 раз при временных ошибках.
- С **v2.1.128** `/mcp` показывает **число инструментов** каждого подключённого сервера и визуально помечает серверы с **0 инструментов**, чтобы неверно настроенные серверы были видны сразу.

## Поиск инструментов MCP

Поиск инструментов включён по умолчанию: инструменты MCP откладываются и обнаруживаются по требованию, поэтому их описания не заполняют контекст модели. Claude Code выключает поиск, когда `ANTHROPIC_BASE_URL` указывает на хост не первой стороны: большинство прокси не передают блоки, которые для этого нужны.

| Настройка | Значение | Описание |
|---------|-------|-------------|
| `ENABLE_TOOL_SEARCH` | (не задано — по умолчанию) | Все инструменты MCP откладываются и загружаются по требованию |
| `ENABLE_TOOL_SEARCH` | `auto` | Пороговый режим: инструменты загружаются сразу, пока их описания не достигнут 10% контекстного окна, затем все откладываются |
| `ENABLE_TOOL_SEARCH` | `auto:<N>` | Пороговый режим со своим процентом (0–100) — например, `auto:5` означает 5% |
| `ENABLE_TOOL_SEARCH` | `true` | Все инструменты MCP откладываются |
| `ENABLE_TOOL_SEARCH` | `false` | Выключено; все описания инструментов отправляются целиком |

> **Примечание:** поиск инструментов требует модели с поддержкой блоков `tool_reference`: Claude Opus 4, Claude Sonnet 4, Claude Haiku 4.5 и более новые модели (Opus 4.5, Sonnet 4.5, Haiku 4.5 и новее на Google Cloud's Agent Platform).

### Обход поиска инструментов для отдельного сервера (v2.1.121+)

Если инструменты конкретного MCP-сервера нужны на каждом шаге, пометьте его конфигурацию `"alwaysLoad": true`, чтобы не откладывать их через поиск инструментов и держать всегда доступными:

```json
{
  "mcpServers": {
    "always-on-tool": {
      "command": "node",
      "args": ["./tools/always.js"],
      "alwaysLoad": true
    }
  }
}
```

Используйте это редко: каждый всегда загруженный инструмент занимает контекст, который поиск инструментов мог бы потратить на более подходящий инструмент.

Чтобы все инструменты сервера оставались за поиском, задайте `"alwaysLoad": false` в записи этого сервера (v2.1.287+). Это касается и инструментов, которые автор сервера пометил для немедленной загрузки; если `alwaysLoad` не указывать, такие помеченные инструменты загружаются сразу. Автор сервера помечает отдельный инструмент ключом `"anthropic/alwaysLoad"` в объекте `_meta` этого инструмента, а настройка `alwaysLoad` на уровне сервера в вашей конфигурации может её перекрыть.

## Динамические обновления инструментов

Claude Code поддерживает уведомления MCP `list_changed`. Когда MCP-сервер динамически добавляет, удаляет или меняет доступные инструменты, Claude Code получает обновление и сам поправляет список инструментов — переподключение и перезапуск не нужны.

## MCP Apps

MCP Apps — первое официальное расширение MCP: вызовы инструментов MCP могут возвращать интерактивные компоненты интерфейса, которые рисуются прямо в чате. Вместо обычного текста MCP-серверы могут отдавать насыщенные панели, формы, визуализации данных и многошаговые рабочие процессы — всё это показывается в разговоре, без перехода в другое окно.

## Элицитация MCP

MCP-серверы могут запрашивать у пользователя структурированный ввод через интерактивные диалоги (v2.1.49+). Так сервер может попросить дополнительные сведения посреди рабочего процесса — например подтверждение, выбор из списка или заполнение обязательных полей — и сделать взаимодействие с MCP-сервером интерактивным.

## Лимит описаний инструментов и инструкций

Claude Code обрезает описание каждого инструмента MCP и инструкции каждого сервера, чтобы многословные серверы не раздували контекст. По умолчанию лимит — **4 096 символов** для инструкций сервера и для описаний инструментов, которые загружаются сразу (v2.1.296; с v2.1.84 до этого было 2 048), и **16 384 символа** для описаний, которые Claude загружает через поиск инструментов (v2.1.295). С v2.1.280 переменная `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` перекрывает оба лимита: заданное число заменяет **оба** порога (`8192` поднимает меньший и опускает больший). С v2.1.299 описания и инструкции собственных MCP-серверов Anthropic на `api.anthropic.com` доходят до Claude целиком. Важные детали ставьте в начало описания.

## Промпты MCP как слэш-команды

MCP-серверы могут открывать промпты, которые в Claude Code появляются как слэш-команды. К промптам обращаются по такому шаблону имени:

```
/mcp__<server>__<prompt>
```

Например, если сервер с именем `github` открывает промпт `review`, его вызывают как `/mcp__github__review`.

## Дедупликация серверов

Если один и тот же MCP-сервер задан в нескольких областях (`local`, `project`, `user`), приоритет у локальной конфигурации. Так можно перекрыть настройки MCP уровня проекта или пользователя локальными правками, без конфликтов.

## Недавние исправления жизненного цикла (v2.1.136)

Два давних бага жизненного цикла MCP исправлены в v2.1.136 — имеет смысл обновиться, если у вас несколько серверов:

- **MCP-серверы сохраняются после `/clear`**: серверы из `.mcp.json`, плагинов или коннекторов claude.ai больше не пропадают после `/clear` в VS Code, JetBrains или Agent SDK. В более ранних версиях они тихо отключались, и нужен был перезапуск.
- **Исправление одновременного обновления refresh-токена OAuth**: при нескольких серверах с OAuth refresh-токены больше не теряются, когда серверы обновляют их одновременно. Это убирает ситуацию «каждое утро приходится входить заново», которая возникала в настройках с несколькими MCP-серверами под защитой OAuth.

## Ресурсы MCP через упоминания @

На ресурсы MCP можно ссылаться прямо в промптах через упоминание `@`:

```
@server-name:protocol://resource/path
```

Например, чтобы сослаться на конкретный ресурс базы данных:

```
@database:postgres://mydb/users
```

Так Claude получает содержимое ресурса MCP и вставляет его в контекст разговора.

## Области MCP

Конфигурации MCP хранятся в разных областях, и общий доступ у них разный:

| Область | Флаг | Расположение | Описание | Общий доступ | Нужно подтверждение |
|-------|------|----------|-------------|-------------|------------------|
| **Локальная** (по умолчанию) | `--scope local` | `~/.claude.json` (в пути проекта) | Только для текущего пользователя и только в текущем проекте (в старых версиях называлась `project`) | Только вы | Нет |
| **Проект** | `--scope project` | `.mcp.json` | Коммитится в git-репозиторий | Участники команды | Да (при первом использовании) |
| **Пользователь** | `--scope user` | `~/.claude.json` | Доступна во всех проектах (в старых версиях называлась `global`) | Только вы | Нет |

Область выбирают при добавлении сервера флагом `--scope` (краткая форма `-s`). Если флаг опустить, Claude Code берёт `local`:

```bash
# Проектная область — запись в .mcp.json, чтобы команда пользовалась им вместе
claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# Пользовательская область — доступен в каждом проекте
claude mcp add --scope user --transport stdio memory -- npx @modelcontextprotocol/server-memory
```

### Использование проектной области

Храните проектные конфигурации MCP в `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

При первом использовании проектных MCP участники команды увидят запрос на подтверждение. В недоверенном рабочем пространстве серверы, которые репозиторий сам одобрил через закоммиченный `.claude/settings.json`, **не** запускаются автоматически командами `claude mcp list` и `get` — они показывают `⏸ Pending approval`, пока вы не примете диалог доверия, а `enableAllProjectMcpServers` в недоверенной папке игнорируется (v2.1.196).

## Управление конфигурацией MCP

### Добавление MCP-серверов

```bash
# Добавить сервер на HTTP
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# Добавить локальный stdio-сервер
claude mcp add --transport stdio database -- npx @company/db-server

# Список всех MCP-серверов
claude mcp list

# Подробности конкретного сервера
claude mcp get github

# Удалить MCP-сервер
claude mcp remove github

# Сбросить проектные решения о подтверждении
claude mcp reset-project-choices

# Аутентификация MCP-сервера из CLI (v2.1.186+)
claude mcp login github

# Выйти из MCP-сервера (v2.1.186+)
claude mcp logout github

# Импорт из Claude Desktop
claude mcp add-from-claude-desktop

# Добавить сервер из JSON-фрагмента (удобно для настройки скриптом)
claude mcp add-json events-server '{"type":"stdio","command":"npx","args":["@modelcontextprotocol/server-events"]}'
```

> **Примечание**: В JSON-конфигурациях — `.mcp.json`, `~/.claude.json` или `claude mcp add-json` — поле `type` принимает `streamable-http` как псевдоним `http`. В спецификации MCP этот транспорт называется `streamable-http`, поэтому конфигурации, скопированные из документации самого сервера, работают без правок.

С v2.1.238 `claude mcp list` и `claude mcp get` показывают отключённые серверы как `⊘ Disabled` и не подключаются к ним для проверки работоспособности.

`claude mcp login <name>` и `claude mcp logout <name>` — неинтерактивный эквивалент потока OAuth в меню `/mcp`: войти или выйти, не открывая его. Добавьте к `login` флаг `--no-browser`, чтобы пройти OAuth по SSH или в headless-сессии (поток идёт через stdin).

## Таблица доступных MCP-серверов

| MCP-сервер | Назначение | Типичные инструменты | Аутентификация | В реальном времени |
|------------|---------|--------------|------|-----------|
| **Filesystem** | Операции с файлами | read, write, delete | Разрешения ОС | ✅ Да |
| **GitHub** | Управление репозиторием | list_prs, create_issue, push | OAuth | ✅ Да |
| **Slack** | Общение в команде | send_message, list_channels | Токен | ✅ Да |
| **Database** | SQL-запросы | query, insert, update | Учётные данные | ✅ Да |
| **Google Docs** | Доступ к документам | read, write, share | OAuth | ✅ Да |
| **Asana** | Управление проектами | create_task, update_status | API-ключ | ✅ Да |
| **Stripe** | Платёжные данные | list_charges, create_invoice | API-ключ | ✅ Да |
| **Memory** | Постоянная память | store, retrieve, delete | Локально | ❌ Нет |

## Практические примеры

### Пример 1: конфигурация GitHub MCP

**Файл:** `.mcp.json` (корень проекта)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Доступные инструменты GitHub MCP:**

#### Управление pull request

- `list_prs` — список всех PR в репозитории
- `get_pr` — подробности PR, включая diff
- `create_pr` — создать новый PR
- `update_pr` — обновить описание или заголовок PR
- `merge_pr` — слить PR в ветку main
- `review_pr` — добавить комментарии к ревью

**Пример запроса:**

```
/mcp__github__get_pr 456

# Возвращает:
Заголовок: Добавлена поддержка тёмной темы
Автор: @alice
Описание: Тёмная тема через CSS-переменные
Статус: OPEN
Ревьюеры: @bob, @charlie
```

#### Управление issue

- `list_issues` — список всех issue
- `get_issue` — подробности issue
- `create_issue` — создать новый issue
- `close_issue` — закрыть issue
- `add_comment` — добавить комментарий к issue

#### Сведения о репозитории

- `get_repo_info` — сведения о репозитории
- `list_files` — дерево файлов
- `get_file_content` — прочитать содержимое файла
- `search_code` — поиск по кодовой базе

#### Операции с коммитами

- `list_commits` — история коммитов
- `get_commit` — подробности конкретного коммита
- `create_commit` — создать новый коммит

**Настройка**:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token"
# Или добавить сразу через CLI:
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

### Подстановка переменных окружения в конфигурации

Конфигурации MCP поддерживают подстановку переменных окружения со значениями по умолчанию. Синтаксис `${VAR}` и `${VAR:-default}` работает в полях `command`, `args`, `env`, `url` и `headers`.

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}",
        "X-Custom-Header": "${CUSTOM_HEADER:-default-value}"
      }
    },
    "local-server": {
      "command": "${MCP_BIN_PATH:-npx}",
      "args": ["${MCP_PACKAGE:-@company/mcp-server}"],
      "env": {
        "DB_URL": "${DATABASE_URL:-postgresql://localhost/dev}"
      }
    }
  }
}
```

Переменные раскрываются во время выполнения:

- `${VAR}` — берётся переменная окружения; если она не задана (и нет значения по умолчанию), сервер всё равно загружается с буквальным `${VAR}`, а `claude mcp list` и `/mcp` предупреждают о недостающей переменной
- `${VAR:-default}` — берётся переменная окружения, а если она не задана — значение по умолчанию

### Пример 2: настройка Database MCP

**Конфигурация:**

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"]
    }
  }
}
```

**Пример использования:**

```markdown
Пользователь: Получи всех пользователей, у которых больше 10 заказов

Claude: Запрошу вашу базу данных и найду это.

# Инструмент MCP для базы данных:
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 10
ORDER BY order_count DESC;

# Результаты:
- Alice: 15 заказов
- Bob: 12 заказов
- Charlie: 11 заказов
```

**Настройка**:

```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
claude mcp add --transport stdio database -- npx -y @bytebase/dbhub \
  --dsn "$DATABASE_URL"
```

> **Предупреждение**: Эта настройка даёт Claude доступ на запись. Инструмент `execute_sql` в DBHub выполняет любой полученный SQL, включая `UPDATE`, `DELETE` и `DROP`, пока вы не включите режим только для чтения. Используйте локальную или одноразовую базу, но не продакшен.

**Настройка только для чтения (рекомендуется):**

Создайте пользователя базы, который может выполнять только `SELECT` (пример для PostgreSQL):

```sql
CREATE ROLE claude_readonly LOGIN PASSWORD 'change-me';
GRANT CONNECT ON DATABASE mydb TO claude_readonly;
GRANT USAGE ON SCHEMA public TO claude_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly;
```

Включите режим только для чтения в `dbhub.toml`. Старый флаг `--readonly` больше не работает. DBHub подставляет `${DATABASE_URL}` из вашего окружения, поэтому учётные данные в файл не попадают:

```toml
[[sources]]
id = "default"
dsn = "${DATABASE_URL}"

[[tools]]
name = "execute_sql"
source = "default"
readonly = true
```

Затем укажите DBHub на файл, а не передавайте `--dsn`. Сначала удалите сервер `database` с доступом на запись, который вы добавили выше: Claude Code не добавит второй сервер с тем же именем:

```bash
# Заменить добавленный выше сервер с доступом на запись
claude mcp remove database
export DATABASE_URL="postgresql://claude_readonly:change-me@localhost/mydb"
claude mcp add --transport stdio database -- npx -y @bytebase/dbhub \
  --config "$PWD/dbhub.toml"
```

Режим только для чтения фильтрует текст SQL, и раньше его обходили (исправлено в DBHub 0.22.6), поэтому данные по-настоящему защищает пользователь только с `SELECT`. См. [Режим только для чтения DBHub](https://dbhub.ai/tools/execute-sql#read-only-mode).

### Пример 3: рабочий процесс с несколькими MCP

**Сценарий: ежедневный отчёт**

```markdown
# Рабочий процесс ежедневного отчёта на нескольких MCP

## Настройка
1. GitHub MCP — метрики PR
2. Database MCP — запрос данных о продажах
3. Slack MCP — публикация отчёта
4. Filesystem MCP — сохранение отчёта

## Рабочий процесс

### Шаг 1: Получить данные GitHub
/mcp__github__list_prs completed:true last:7days

Вывод:
- Всего PR: 42
- Среднее время слияния: 2,3 часа
- Время до ревью: 1,1 часа

### Шаг 2: Запрос к базе данных
SELECT COUNT(*) as sales, SUM(amount) as revenue
FROM orders
WHERE created_at > NOW() - INTERVAL '1 day'

Вывод:
- Продажи: 247
- Выручка: $12 450

### Шаг 3: Сформировать отчёт
Собрать данные в HTML-отчёт

### Шаг 4: Сохранить в файловую систему
Записать report.html в /reports/

### Шаг 5: Опубликовать в Slack
Отправить сводку в канал #daily-reports

Итог:
✅ Отчёт сформирован и опубликован
📊 На этой неделе слито 47 PR
💰 $12 450 дневных продаж
```

**Настройка**:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_BOT_TOKEN="your_slack_bot_token"
export SLACK_TEAM_ID="your_slack_team_id"
# Добавьте каждый MCP-сервер через CLI или опишите их в .mcp.json
```

### Пример 4: операции Filesystem MCP

**Конфигурация:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

**Доступные операции:**

| Операция | Команда | Назначение |
|-----------|---------|---------|
| Список файлов | `ls ~/projects` | Показать содержимое каталога |
| Чтение файла | `cat src/main.ts` | Прочитать содержимое файла |
| Запись файла | `create docs/api.md` | Создать новый файл |
| Правка файла | `edit src/app.ts` | Изменить файл |
| Поиск | `grep "async function"` | Поиск в файлах |
| Удаление | `rm old-file.js` | Удалить файл |

**Настройка**:

```bash
# Добавить сразу через CLI:
claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem /home/user/projects
```

## MCP и память: матрица выбора

```mermaid
graph TD
    A["Нужны внешние данные?"]
    A -->|Нет| B["Использовать память"]
    A -->|Да| C["Данные часто меняются?"]
    C -->|"Нет/редко"| B
    C -->|"Да/часто"| D["Использовать MCP"]

    B -->|Хранит| E["Предпочтения<br/>Контекст<br/>История"]
    D -->|Обращается| F["Живые API<br/>Базы данных<br/>Сервисы"]

    style A fill:#fff3e0,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#fff3e0,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#e8f5e9,stroke:#333,color:#333
    style F fill:#e8f5e9,stroke:#333,color:#333
```

## Шаблон запроса и ответа

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP-сервер
    participant DB as База данных

    App->>MCP: Запрос: "SELECT * FROM users WHERE id=1"
    MCP->>DB: Выполняет запрос
    DB-->>MCP: Набор результатов
    MCP-->>App: Возвращает разобранные данные
    App->>App: Обрабатывает результат
    App->>App: Продолжает задачу

    Note over MCP,DB: Доступ в реальном времени<br/>Без кэширования
```

## Переменные окружения

Храните чувствительные учётные данные в переменных окружения:

```bash
# ~/.bashrc или ~/.zshrc
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxxxxxxxxxxxx"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_BOT_TOKEN="your-slack-bot-token"
export SLACK_TEAM_ID="T0000000000"
```

Затем ссылайтесь на них в конфигурации MCP:

```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}
```

## Claude как MCP-сервер (`claude mcp serve`)

Сам Claude Code может быть MCP-сервером для других приложений. Тогда внешние инструменты, редакторы и системы автоматизации используют возможности Claude через стандартный протокол MCP.

```bash
# Запустить Claude Code как MCP-сервер на stdio
claude mcp serve
```

Другие приложения подключаются к этому серверу так же, как к любому MCP-серверу на stdio. Например, чтобы добавить Claude Code как MCP-сервер в другой экземпляр Claude Code:

```bash
claude mcp add --transport stdio claude-agent -- claude mcp serve
```

Это удобно для многоагентных рабочих процессов, где один экземпляр Claude управляет другим.

## Управляемая конфигурация MCP (для организаций)

В корпоративных деплоях IT-администраторы задают политику MCP-серверов двумя отдельными механизмами: файл `managed-mcp.json` разворачивает фиксированный набор серверов и единолично ими управляет, а ключи настроек `allowedMcpServers` и `deniedMcpServers` фильтруют, какие из настроенных серверов можно загружать.

**Расположение:**

- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux и WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

`managed-mcp.json` использует тот же формат, что и проектный `.mcp.json` — карта `mcpServers` верхнего уровня. Файл разворачивает серверы, а не фильтрует их:

```json
{
  "mcpServers": {
    "example-remote": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"]
    }
  }
}
```

Этот файл может прочитать любой пользователь машины, поэтому никогда не кладите учётные данные в блок `env`. Используйте подстановку `${VAR}`, OAuth или `headersHelper`.

**Фильтрация: списки разрешённых и запрещённых**

`allowedMcpServers`, `deniedMcpServers` и `allowAllClaudeAiMcps` — это **ключи настроек, а не поля `managed-mcp.json`**. Чтобы они применялись принудительно, поместите их в управляемый источник настроек: настройки, управляемые сервером, `managed-settings.json`, профиль MDM или реестр.

- `allowedMcpServers` — список разрешённых серверов. Рядом, в том же управляемом источнике, задайте `allowManagedMcpServersOnly: true`, иначе списки разрешённых сливаются из каждой области, и пользователь может расширить ваш список.
- `deniedMcpServers` — список запрещённых серверов. Сливается из каждой области в любом случае.
- `allowAllClaudeAiMcps` — загружает облачные коннекторы claude.ai вместе с развёрнутым `managed-mcp.json` (v2.1.149+). Читается только из уровней политики, которыми управляет администратор.

Каждая запись — объект с **одним** ключом:

| Ключ | С чем совпадает |
|-----|---------|
| `serverUrl` | URL удалённого сервера, точный или с подстановочными знаками `*` |
| `serverCommand` | Точная команда и аргументы запуска stdio-сервера в виде массива — каждый аргумент по порядку |
| `serverName` | Метка, заданная пользователем. **Только точное совпадение; подстановочные знаки не раскрываются** |

**Пример конфигурации:**

```json
{
  "allowedMcpServers": [
    { "serverUrl": "https://mcp.example.com/*" },
    { "serverCommand": ["/usr/local/bin/company-mcp-server", "--config", "/etc/company/mcp-config.json"] }
  ],
  "deniedMcpServers": [
    { "serverName": "untrusted-server" },
    { "serverUrl": "http://*" }
  ],
  "allowManagedMcpServersOnly": true
}
```

Третья управляемая настройка, `managedMcpServers` (v2.1.259+), позволяет организации выдать каждому пользователю MCP-серверы HTTP и SSE. Записи имеют ту же форму, что и в `.mcp.json`; записи, которые называют команду для запуска, пропускаются.

> **Примечание:** Если серверу соответствуют и `allowedMcpServers`, и `deniedMcpServers`, приоритет у правила запрета.

## MCP-серверы из плагинов

Плагины могут поставлять собственные MCP-серверы: они становятся доступны сами, когда плагин установлен. Такие серверы задают двумя способами:

1. **Отдельный `.mcp.json`** — положите файл `.mcp.json` в корневой каталог плагина
2. **Прямо в `plugin.json`** — опишите MCP-серверы в манифесте плагина

Переменная `${CLAUDE_PLUGIN_ROOT}` указывает пути относительно каталога установки плагина:

```json
{
  "mcpServers": {
    "plugin-tools": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/dist/mcp-server.js"],
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## MCP в области субагента

MCP-серверы можно описать прямо во frontmatter агента ключом `mcpServers:`, и тогда они относятся к конкретному субагенту, а не ко всему проекту. Это полезно, когда агенту нужен определённый MCP-сервер, а остальным агентам рабочего процесса он не нужен.

```yaml
---
name: my-tool-agent
description: Использует my-tool для специализированных операций
mcpServers:
  my-tool:
    type: http
    url: https://my-tool.example.com/mcp
---

Вы — агент с доступом к my-tool для специализированных операций.
```

MCP-серверы в области субагента доступны только в контексте выполнения этого агента и не передаются родительскому агенту и соседним агентам.

## Лимиты вывода MCP

Claude Code ограничивает вывод инструментов MCP, чтобы контекст не переполнялся:

| Предел | Порог | Поведение |
|-------|-----------|----------|
| **Предупреждение** | 10 000 токенов | Показывается предупреждение, что вывод большой |
| **Максимум по умолчанию** | 25 000 токенов | Более крупный вывод сохраняется в файл, а в разговор попадает путь к файлу |
| **Сохранение на диск** | 50 000 символов | Результаты инструмента длиннее 50 000 символов записываются на диск |

Максимальный лимит вывода настраивается переменной окружения `MAX_MCP_OUTPUT_TOKENS`:

```bash
# Поднять максимальный вывод до 50 000 токенов
export MAX_MCP_OUTPUT_TOKENS=50000
```

## Автоматический уход долгих вызовов инструментов в фон (v2.1.212)

Вызовы инструментов MCP, которые длятся дольше 2 минут, теперь сами уходят в фон, и сессия остаётся рабочей, а не блокируется на медленном инструменте. Порог настраивается, а поведение можно изменить или отключить через `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`:

```bash
# Изменить порог автоматического ухода в фон на 5 минут (300 000 мс)
export CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=300000
```

## Как выполнение кода снимает раздувание контекста

Когда MCP используют всё шире, подключение к десяткам серверов с сотнями или тысячами инструментов создаёт серьёзную проблему: **раздувание контекста**. На масштабе это, пожалуй, главная проблема MCP, и инженерная команда Anthropic предложила изящное решение — выполнять код вместо прямых вызовов инструментов.

> **Источник**: [Выполнение кода с MCP: как создавать более эффективных агентов](https://www.anthropic.com/engineering/code-execution-with-mcp) — блог Anthropic Engineering

### Проблема: два источника лишних токенов

**1. Описания инструментов перегружают контекстное окно**

Большинство клиентов MCP загружают все описания инструментов сразу. При подключении к тысячам инструментов модель должна обработать сотни тысяч токенов ещё до того, как прочитает запрос пользователя.

**2. Промежуточные результаты съедают дополнительные токены**

Каждый промежуточный результат инструмента проходит через контекст модели. Представьте перенос расшифровки встречи из Google Drive в Salesforce: полный текст проходит через контекст **дважды** — когда его читают и когда записывают в назначение. Расшифровка двухчасовой встречи может означать 50 000+ лишних токенов.

```mermaid
graph LR
    A["Модель"] -->|"Вызов инструмента: getDocument"| B["MCP-сервер"]
    B -->|"Полная расшифровка (50 тыс. токенов)"| A
    A -->|"Вызов инструмента: updateRecord<br/>(снова отправляет полную расшифровку)"| B
    B -->|Подтверждение| A

    style A fill:#ffcdd2,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
```

### Решение: инструменты MCP как программные API

Вместо того чтобы пропускать описания инструментов и результаты через контекстное окно, агент **пишет код**, который вызывает инструменты MCP как API. Код выполняется в песочнице, и в модель возвращается только итоговый результат.

```mermaid
graph LR
    A["Модель"] -->|"Пишет код"| B["Среда выполнения<br/>кода"]
    B -->|"Вызывает инструменты напрямую"| C["MCP-серверы"]
    C -->|"Данные остаются<br/>в среде выполнения"| B
    B -->|"Только итоговый результат<br/>(минимум токенов)"| A

    style A fill:#c8e6c9,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
```

#### Как это устроено

Инструменты MCP представлены как дерево файлов с типизированными функциями:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
└── ...
```

В каждом файле инструмента — типизированная обёртка:

```typescript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>(
    'google_drive__get_document', input
  );
}
```

Затем агент пишет код, который координирует инструменты:

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

// Данные идут напрямую между инструментами — не через модель
const transcript = (
  await gdrive.getDocument({ documentId: 'abc123' })
).content;

await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**Результат: расход токенов падает с ~150 000 до ~2 000 — снижение на 98,7%.**

### Ключевые преимущества

| Преимущество | Описание |
|---------|-------------|
| **Постепенное раскрытие** | Агент обходит файловую систему и загружает только нужные описания инструментов, а не все сразу |
| **Экономные по контексту результаты** | Данные фильтруются и преобразуются в среде выполнения до возврата в модель |
| **Гибкое управление потоком** | Циклы, условия и обработка ошибок выполняются в коде, без лишних кругов через модель |
| **Сохранение приватности** | Промежуточные данные (PII, чувствительные записи) остаются в среде выполнения и не попадают в контекст модели |
| **Сохранение состояния** | Агенты могут сохранять промежуточные результаты в файлы и собирать переиспользуемые функции навыков |

#### Пример: фильтрация больших наборов данных

```typescript
// Без выполнения кода — все 10 000 строк проходят через контекст
// ВЫЗОВ ИНСТРУМЕНТА: gdrive.getSheet(sheetId: 'abc123')
//   -> в контекст возвращаются 10 000 строк

// С выполнением кода — фильтр в среде выполнения
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(
  row => row["Status"] === 'pending'
);
console.log(`Найдено ожидающих заказов: ${pendingOrders.length}`);
console.log(pendingOrders.slice(0, 5)); // До модели доходят только 5 строк
```

#### Пример: цикл без лишних кругов

```typescript
// Опрос уведомления о деплое — целиком выполняется в коде
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({
    channel: 'C123456'
  });
  found = messages.some(
    m => m.text.includes('deployment complete')
  );
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Получено уведомление о деплое');
```

### На что обратить внимание

У выполнения кода есть своя сложность. Запуск кода, который сгенерировал агент, требует следующего:

- **Безопасной среды выполнения в песочнице** с подходящими лимитами ресурсов
- **Наблюдения и журналирования** выполняемого кода
- Дополнительных **затрат на инфраструктуру** по сравнению с прямыми вызовами инструментов

Эту выгоду — меньше трат на токены, ниже задержка, лучше композиция инструментов — стоит сопоставить с этими затратами на внедрение. Для агента с несколькими MCP-серверами прямые вызовы инструментов могут быть проще. Для агента на масштабе (десятки серверов, сотни инструментов) выполнение кода даёт заметный выигрыш.

### MCPorter: среда выполнения для композиции инструментов MCP

[MCPorter](https://github.com/steipete/mcporter) — среда выполнения и набор CLI на TypeScript. Он делает вызов MCP-серверов практичным без шаблонного кода и помогает уменьшить раздувание контекста за счёт выборочного показа инструментов и типизированных обёрток.

**Что это решает:** вместо загрузки всех описаний инструментов со всех MCP-серверов сразу MCPorter позволяет обнаруживать, изучать и вызывать конкретные инструменты по требованию — контекст остаётся компактным.

**Ключевые функции:**

| Функция | Описание |
|---------|-------------|
| **Обнаружение без настройки** | Сам находит MCP-серверы из Cursor, Claude, Codex или локальных конфигов |
| **Типизированные клиенты инструментов** | `mcporter emit-ts` генерирует интерфейсы `.d.ts` и готовые к запуску обёртки |
| **Компонуемый API** | `createServerProxy()` открывает инструменты как методы в camelCase с помощниками `.text()`, `.json()`, `.markdown()` |
| **Генерация CLI** | `mcporter generate-cli` превращает любой MCP-сервер в отдельный CLI с фильтрами `--include-tools` / `--exclude-tools` |
| **Скрытие параметров** | Необязательные параметры по умолчанию скрыты, и схема менее многословна |

**Установка:**

```bash
npx mcporter list          # Установка не нужна — серверы находятся сразу
pnpm add mcporter          # Добавить в проект
brew install steipete/tap/mcporter  # macOS через Homebrew
```

**Пример — композиция инструментов на TypeScript:**

```typescript
import { createRuntime, createServerProxy } from "mcporter";

const runtime = await createRuntime();
const gdrive = createServerProxy(runtime, "google-drive");
const salesforce = createServerProxy(runtime, "salesforce");

// Данные идут между инструментами, не проходя через контекст модели
const doc = await gdrive.getDocument({ documentId: "abc123" });
await salesforce.updateRecord({
  objectType: "SalesMeeting",
  recordId: "00Q5f000001abcXYZ",
  data: { Notes: doc.text() }
});
```

**Пример — вызов инструмента из CLI:**

```bash
# Вызвать конкретный инструмент напрямую
npx mcporter call linear.create_comment issueId:ENG-123 body:'Выглядит хорошо!'

# Список доступных серверов и инструментов
npx mcporter list
```

MCPorter дополняет описанный выше подход с выполнением кода: даёт среду, в которой инструменты MCP вызываются как типизированные API, и промежуточные данные легко не пускать в контекст модели.

## Рекомендации

### Вопросы безопасности

#### Что делать ✅

- Храните все учётные данные в переменных окружения
- Регулярно меняйте токены и API-ключи (рекомендуется раз в месяц)
- По возможности используйте токены только для чтения
- Ограничивайте доступ MCP-сервера необходимым минимумом
- Следите за использованием MCP-сервера и журналами доступа
- Для внешних сервисов используйте OAuth, если он доступен
- Вводите лимит запросов на обращения к MCP
- Проверяйте соединения MCP до использования в продакшене
- Документируйте все активные соединения MCP
- Обновляйте пакеты MCP-серверов

#### Чего не делать ❌

- Не прописывайте учётные данные в файлах конфигурации
- Не коммитьте токены и секреты в git
- Не пересылайте токены в командных чатах и письмах
- Не используйте личные токены для командных проектов
- Не выдавайте лишние разрешения
- Не игнорируйте ошибки аутентификации
- Не открывайте конечные точки MCP публично
- Не запускайте MCP-серверы с правами root или администратора
- Не кэшируйте чувствительные данные в журналах
- Не отключайте механизмы аутентификации

### Рекомендации по конфигурации

1. **Контроль версий**: держите `.mcp.json` в git, а секреты — в переменных окружения
2. **Минимум привилегий**: выдавайте каждому MCP-серверу только нужные разрешения
3. **Изоляция**: по возможности запускайте разные MCP-серверы в отдельных процессах
4. **Наблюдение**: журналируйте все запросы MCP и ошибки для аудита
5. **Проверка**: проверяйте все конфигурации MCP до деплоя в продакшен

### Советы по производительности

- Кэшируйте часто используемые данные на уровне приложения
- Делайте запросы MCP конкретными, чтобы передавать меньше данных
- Следите за временем ответа операций MCP
- Учитывайте лимит запросов внешних API
- Группируйте операции, когда их несколько

## Инструкции по установке

### Что нужно заранее

- Установлены Node.js и npm
- Установлен Claude Code CLI
- Есть API-токены и учётные данные внешних сервисов

### Пошаговая настройка

1. **Добавьте первый MCP-сервер** через CLI (пример: GitHub):

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

   Или создайте файл `.mcp.json` в корне проекта:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

2. **Задайте переменные окружения:**

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_personal_access_token"
```

3. **Проверьте соединение:**

```bash
claude /mcp
```

4. **Используйте инструменты MCP:**

```bash
/mcp__github__list_prs
/mcp__github__create_issue "Title" "Description"
```

### Установка для отдельных сервисов

**GitHub MCP:**

```bash
npm install -g @modelcontextprotocol/server-github
```

**Database MCP:**

```bash
npm install -g @bytebase/dbhub
```

**Filesystem MCP:**

```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Slack MCP (устаревший пакет):**

```bash
npm install -g @modelcontextprotocol/server-slack
```

## Устранение неполадок

### Начните с текста ошибки (v2.1.219+)

Если сервер не подключается, до любых правок запустите `claude mcp list` (или `/mcp` внутри сессии). Claude Code теперь печатает **HTTP-код статуса и текст ошибки сервера** рядом с проблемным сервером, поэтому вы видите `401 Unauthorized` или `404 Not Found`, а не общее `failed to connect`:

```bash
# Статус соединения, а при сбое ещё HTTP-статус и текст ошибки
claude mcp list
```

Сначала прочитайте статус — по нему понятно, какое исправление подходит:

- `401` / `403` → неверные или просроченные учётные данные; войдите снова через `claude mcp login <name>`
- `404` → неверный URL (обычно не хватает суффикса пути `/mcp` или `/sse`)
- `5xx` или таймаут → удалённый сервер недоступен; см. [Таймаут соединения](#таймаут-соединения)

### Скрытые пробелы в значениях конфигурации (v2.1.219+)

Claude Code предупреждает, если в значении конфигурации MCP есть **пробелы в начале или в конце**. Это частая и труднозаметная причина сбоев аутентификации: токен, скопированный из браузера или сообщения в чате, часто несёт пробел или перевод строки в конце. Он уходит в заголовок `Authorization` как есть и отвергается как неверные учётные данные.

Если вы видите это предупреждение, перепроверьте значение в `.mcp.json` (или переменную окружения, из которой оно раскрывается) и обрежьте пробелы:

```bash
# Показывает скрытые пробелы в начале и в конце между разделителями
printf '[%s]\n' "$GITHUB_PERSONAL_ACCESS_TOKEN"
```

### Пропущенные серверы в headless-запусках (v2.1.219+)

Серверы, переданные через `--mcp-config`, которые не проходят проверку конфигурации, **пропускаются**, а не прерывают запуск. Из-за этого headless-скрипт может выглядеть рабочим, хотя половины инструментов нет. Claude Code теперь сообщает, какие серверы отброшены:

- **Headless-запуски и `-p`**: в событии `init` потока stream-json есть поле `mcp_server_errors` со всеми пропущенными записями. Проверьте его, прежде чем доверять выводу запуска.
- **Интерактивный терминал**: та же проблема печатается предупреждением при старте сессии.

```bash
# Просмотреть пропущенные записи --mcp-config в headless-запуске
claude -p "list my tools" --mcp-config ./servers.json \
  --output-format stream-json --verbose \
  | jq -r 'select(.type == "system" and .subtype == "init") | .mcp_server_errors'
```

### MCP-сервер не найден

```bash
# Проверить, что MCP-сервер установлен
npm list -g @modelcontextprotocol/server-github

# Установить, если его нет
npm install -g @modelcontextprotocol/server-github
```

### Сбой аутентификации

```bash
# Проверить, что переменная окружения задана
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# Экспортировать заново, если нужно
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"

# Проверить, что у токена нужные разрешения
# Области доступа токена GitHub: https://github.com/settings/tokens
```

### Таймаут соединения

- Проверьте сеть: `ping api.github.com`
- Убедитесь, что конечная точка API доступна
- Проверьте лимиты запросов API
- Попробуйте увеличить таймаут в конфигурации
- Проверьте файрвол и прокси

### Падения MCP-сервера

- Журналы MCP-сервера: `~/.claude/logs/`
- Проверьте, что все переменные окружения заданы
- Проверьте права на файлы
- Попробуйте переустановить пакет MCP-сервера
- Проверьте, не занят ли тот же порт другим процессом

## Связанные понятия

### Память и MCP

- **Память**: хранит постоянные, не меняющиеся данные (предпочтения, контекст, история)
- **MCP**: обращается к живым, меняющимся данным (API, базы данных, сервисы реального времени)

### Когда что использовать

- **Память** — для предпочтений пользователя, истории разговора, усвоенного контекста
- **MCP** — для текущих issue GitHub, запросов к живой базе, данных в реальном времени

### Связка с другими функциями Claude

- Сочетайте MCP с памятью, чтобы контекст был богаче
- Используйте инструменты MCP в промптах, чтобы рассуждения были точнее
- Подключайте несколько MCP для сложных рабочих процессов

## Дополнительные материалы

- [Официальная документация MCP](https://code.claude.com/docs/en/mcp)
- [Спецификация протокола MCP](https://modelcontextprotocol.io/specification)
- [Репозиторий MCP на GitHub](https://github.com/modelcontextprotocol/servers)
- [Доступные MCP-серверы](https://github.com/modelcontextprotocol/servers)
- [MCPorter](https://github.com/steipete/mcporter) — среда выполнения и CLI на TypeScript для вызова MCP-серверов без шаблонного кода
- [Выполнение кода с MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — инженерный блог Anthropic о том, как снять раздувание контекста
- [Справочник CLI Claude Code](https://code.claude.com/docs/en/cli-reference)
- [Документация Claude API](https://docs.anthropic.com)

---

**Последнее обновление**: 18 октября 2026
**Версия Claude Code**: 2.1.302
**Источники**:

- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/managed-mcp
- https://code.claude.com/docs/en/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.117
- https://github.com/anthropics/claude-code/releases/tag/v2.1.139
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/mcp#configure-tool-search
- https://code.claude.com/docs/en/env-vars
- https://github.com/anthropics/claude-code/releases/tag/v2.1.285
- https://github.com/anthropics/claude-code/releases/tag/v2.1.296
- https://code.claude.com/docs/en/mcp#tool-search-for-mcp-server-authors
- https://code.claude.com/docs/en/mcp#environment-variable-expansion-in-mcp-json
- https://code.claude.com/docs/en/sub-agents

**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
