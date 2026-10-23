<!-- i18n-source: 03-skills/doc-generator/SKILL.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

---
name: doc-generator
description: Создаёт полную и точную документацию API по исходному коду. Используйте при создании или обновлении документации API, генерации спецификаций OpenAPI или когда пользователь упоминает документацию API, эндпоинты или документацию.
---

# Навык генератора документации API

## Что создаёт

- Спецификации OpenAPI/Swagger
- Документацию эндпоинтов API
- Примеры использования SDK
- Руководства по интеграции
- Справочники кодов ошибок
- Руководства по аутентификации

## Структура документации

### Для каждого эндпоинта

````markdown
## GET /api/v1/users/:id

### Описание
Кратко, что делает этот эндпоинт

### Параметры

| Имя | Тип | Обязательно | Описание |
|------|------|----------|-------------|
| id | string | Да | Идентификатор пользователя |

### Ответ

**200 Успех**
```json
{
  "id": "usr_123",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**404 Не найдено**
```json
{
  "error": "USER_NOT_FOUND",
  "message": "Пользователь не существует"
}
```

### Примеры

**cURL**
```bash
curl -X GET "https://api.example.com/api/v1/users/usr_123" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**JavaScript**
```javascript
const user = await fetch('/api/v1/users/usr_123', {
  headers: { 'Authorization': 'Bearer token' }
}).then(r => r.json());
```

**Python**
```python
response = requests.get(
    'https://api.example.com/api/v1/users/usr_123',
    headers={'Authorization': 'Bearer token'}
)
user = response.json()
```
````

---

**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/skills
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
