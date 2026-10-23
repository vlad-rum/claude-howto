<!-- i18n-source: 01-slash-commands/commit.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [сообщение]
description: Создать git-коммит с контекстом
---

## Контекст

- Текущий статус git: !`git status`
- Текущий diff git: !`git diff HEAD`
- Текущая ветка: !`git branch --show-current`
- Недавние коммиты: !`git log --oneline -10`

## Ваша задача

На основе изменений выше создайте один git-коммит.

Если сообщение передано аргументами, используйте его: `$ARGUMENTS`

Иначе проанализируйте изменения и составьте подходящее сообщение коммита в формате conventional commits:
- `feat:` для новых функций
- `fix:` для исправления ошибок
- `docs:` для изменений документации
- `refactor:` для рефакторинга кода
- `test:` для добавления тестов
- `chore:` для задач сопровождения

---
**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/commands
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
