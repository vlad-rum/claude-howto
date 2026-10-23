<!-- i18n-source: 07-plugins/pr-review/README.md -->
<!-- i18n-source-sha: 232591b -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../../resources/logos/claude-howto-logo.svg">
</picture>

# Плагин ревью PR

Полный рабочий процесс ревью PR с проверками безопасности, тестов и документации.

## Возможности

✅ Анализ безопасности
✅ Проверка покрытия тестами
✅ Проверка документации
✅ Оценка качества кода
✅ Анализ влияния на производительность

## Установка

```bash
claude --plugin-dir ./07-plugins/pr-review
```

## Что входит

### Слэш-команды
- `/review-pr` - Полное ревью PR
- `/check-security` - Ревью с упором на безопасность
- `/check-tests` - Анализ покрытия тестами

### Субагенты
- `security-reviewer` - Поиск уязвимостей
- `test-checker` - Анализ покрытия тестами
- `performance-analyzer` - Оценка влияния на производительность

### MCP-серверы
- Интеграция с GitHub для данных PR

### Хуки
- `pre-review.js` - Проверка перед ревью

## Использование

### Базовое ревью PR
```
/review-pr
```

### Только проверка безопасности
```
/check-security
```

### Проверка покрытия тестами
```
/check-tests
```

## Требования

- Claude Code 2.1+
- Доступ к GitHub
- Git-репозиторий

## Конфигурация

Задайте токен GitHub:
```bash
export GITHUB_TOKEN="your_github_token"
```

## Пример рабочего процесса

```
Пользователь: /review-pr

Claude:
1. Запускает хук pre-review (проверяет git-репозиторий)
2. Получает данные PR через MCP GitHub
3. Передаёт ревью безопасности субагенту security-reviewer
4. Передаёт тестирование субагенту test-checker
5. Передаёт производительность субагенту performance-analyzer
6. Сводит все находки
7. Даёт полный отчёт ревью

Результат:
✅ Безопасность: критичных проблем не найдено
⚠️  Тесты: покрытие 65%, рекомендуется 80%+
✅ Производительность: заметного влияния нет
📝 Рекомендации: добавить тесты на граничные случаи
```

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
