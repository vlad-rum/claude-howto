<!-- i18n-source: 07-plugins/documentation/README.md -->
<!-- i18n-source-sha: 232591b -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../../resources/logos/claude-howto-logo.svg">
</picture>

# Плагин документации

Полная генерация и сопровождение документации для вашего проекта.

## Возможности

✅ Генерация документации API
✅ Создание и обновление README
✅ Синхронизация документации
✅ Улучшение комментариев в коде
✅ Генерация примеров

## Установка

```bash
claude --plugin-dir ./07-plugins/documentation
```

## Что входит

### Слэш-команды
- `/generate-api-docs` - Сгенерировать документацию API
- `/generate-readme` - Создать или обновить README
- `/sync-docs` - Синхронизировать документацию с изменениями кода
- `/validate-docs` - Проверить документацию

### Субагенты
- `api-documenter` - Специалист по документации API
- `code-commentator` - Улучшение комментариев в коде
- `example-generator` - Создание примеров кода

### Шаблоны
- `api-endpoint.md` - Шаблон документации эндпоинта API
- `function-docs.md` - Шаблон документации функции
- `adr-template.md` - Шаблон записи об архитектурном решении

### MCP-серверы
- Интеграция с GitHub для синхронизации документации

## Использование

### Генерация документации API
```
/generate-api-docs
```

### Создание README
```
/generate-readme
```

### Синхронизация документации
```
/sync-docs
```

### Проверка документации
```
/validate-docs
```

## Требования

- Claude Code 2.1+
- Доступ к GitHub (необязательно)

## Пример рабочего процесса

```
Пользователь: /generate-api-docs

Claude:
1. Сканирует все эндпоинты API в /src/api/
2. Передаёт работу субагенту api-documenter
3. Извлекает сигнатуры функций и JSDoc
4. Группирует по модулю или эндпоинту
5. Использует шаблон api-endpoint.md
6. Генерирует подробную документацию в Markdown
7. Включает примеры на curl, JavaScript и Python

Результат:
✅ Документация API сгенерирована
📄 Созданные файлы:
   - docs/api/users.md
   - docs/api/auth.md
   - docs/api/products.md
📊 Покрытие: задокументировано 23/23 эндпоинта
```

## Использование шаблонов

### Шаблон эндпоинта API
Используйте для документации эндпоинтов REST API с полными примерами.

### Шаблон документации функции
Используйте для документации отдельных функций и методов.

### Шаблон ADR
Используйте для документации архитектурных решений.

## Конфигурация

Задайте токен GitHub для синхронизации документации:
```bash
export GITHUB_TOKEN="your_github_token"
```

## Лучшие практики

- Держите документацию рядом с кодом
- Обновляйте документацию вместе с изменениями кода
- Включайте практические примеры
- Проверяйте регулярно
- Используйте шаблоны для единообразия

---

**Последнее обновление**: 18 октября 2026
**Версия Claude Code**: 2.1.302
**Источники**:
- https://code.claude.com/docs/en/plugins
- https://github.com/anthropics/claude-code/releases/tag/v2.1.131
- https://github.com/anthropics/claude-code/releases/tag/v2.1.138
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/en/plugins/install
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
