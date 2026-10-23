<!-- i18n-source: 01-slash-commands/generate-api-docs.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

---
description: Создать полную документацию API по исходному коду
---

# Генератор документации API

Сгенерируйте документацию API так:

1. Просканируйте все файлы в `/src/api/`
2. Извлеките сигнатуры функций и комментарии JSDoc
3. Сгруппируйте по эндпоинту или модулю
4. Создайте Markdown с примерами
5. Включите схемы запроса и ответа
6. Добавьте документацию ошибок

Формат вывода:
- Файл Markdown в `/docs/api.md`
- Примеры curl для всех эндпоинтов
- Типы TypeScript

---
**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/commands
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
