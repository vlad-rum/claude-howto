<!-- i18n-source: 07-plugins/devops-automation/README.md -->
<!-- i18n-source-sha: 232591b -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../../resources/logos/claude-howto-logo.svg">
</picture>

# Плагин автоматизации DevOps

Полная автоматизация DevOps для деплоя, мониторинга и реагирования на инциденты.

## Возможности

✅ Автоматические деплои
✅ Процедуры отката
✅ Мониторинг здоровья системы
✅ Рабочие процессы реагирования на инциденты
✅ Интеграция с Kubernetes

## Установка

```bash
claude --plugin-dir ./07-plugins/devops-automation
```

## Что входит

### Слэш-команды
- `/deploy` - Деплой в продакшен или staging
- `/rollback` - Откат к предыдущей версии
- `/status` - Проверка здоровья системы
- `/incident` - Разбор продакшен-инцидентов

### Субагенты
- `deployment-specialist` - Операции деплоя
- `incident-commander` - Координация инцидентов
- `alert-analyzer` - Анализ здоровья системы

### MCP-серверы
- Интеграция с Kubernetes

### Скрипты
- `deploy.sh` - Автоматизация деплоя
- `rollback.sh` - Автоматизация отката
- `health-check.sh` - Утилиты проверки здоровья

### Хуки
- `pre-deploy.js` - Проверка перед деплоем
- `post-deploy.js` - Задачи после деплоя

## Использование

### Деплой в staging
```
/deploy staging
```

### Деплой в продакшен
```
/deploy production
```

### Откат
```
/rollback production
```

### Проверка статуса
```
/status
```

### Разбор инцидента
```
/incident
```

## Требования

- Claude Code 2.1+
- CLI Kubernetes (kubectl)
- Настроенный доступ к кластеру

## Конфигурация

Настройте конфигурацию Kubernetes:
```bash
export KUBECONFIG=~/.kube/config
```

## Пример рабочего процесса

```
Пользователь: /deploy production

Claude:
1. Запускает хук pre-deploy (проверяет kubectl и подключение к кластеру)
2. Передаёт работу субагенту deployment-specialist
3. Запускает скрипт deploy.sh
4. Следит за ходом деплоя через MCP Kubernetes
5. Запускает хук post-deploy (ждёт поды, дымовые тесты)
6. Даёт сводку деплоя

Результат:
✅ Деплой завершён
📦 Версия: v2.1.0
🚀 Поды: 3/3 готовы
⏱️  Время: 2 мин 34 с
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
