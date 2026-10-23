<!-- i18n-source: 01-slash-commands/pr.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

---
description: Привести код в порядок, проиндексировать изменения и подготовить pull request
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(npm test:*), Bash(npm run lint:*)
---

# Чеклист подготовки pull request

Перед созданием PR выполните эти шаги:

1. Запустите линтинг: `prettier --write .`
2. Запустите тесты: `npm test`
3. Просмотрите git diff: `git diff HEAD`
4. Добавьте изменения в индекс: `git add .`
5. Составьте сообщение коммита в формате conventional commits:
   - `fix:` для исправления ошибок
   - `feat:` для новых функций
   - `docs:` для документации
   - `refactor:` для перестройки кода
   - `test:` для добавления тестов
   - `chore:` для сопровождения

6. Сформируйте сводку PR, включив:
   - Что изменилось
   - Почему это изменилось
   - Какое тестирование проведено
   - Возможные последствия

---
**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/commands
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
