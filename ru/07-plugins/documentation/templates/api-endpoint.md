<!-- i18n-source: 07-plugins/documentation/templates/api-endpoint.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

# [METHOD] /api/v1/[endpoint]

## Описание
Краткое объяснение, что делает этот эндпоинт.

## Аутентификация
Требуемый способ аутентификации (например, Bearer-токен).

## Параметры

### Параметры пути
| Имя | Тип | Обязательно | Описание |
|------|------|----------|-------------|
| id | string | Да | Идентификатор ресурса |

### Параметры запроса
| Имя | Тип | Обязательно | Описание |
|------|------|----------|-------------|
| page | integer | Нет | Номер страницы (по умолчанию: 1) |
| limit | integer | Нет | Элементов на странице (по умолчанию: 20) |

### Тело запроса
```json
{
  "field": "value"
}
```

## Ответы

### 200 OK
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "Пример"
  }
}
```

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Неверный ввод"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Ресурс не найден"
  }
}
```

## Примеры

### cURL
```bash
curl -X GET "https://api.example.com/api/v1/endpoint" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### JavaScript
```javascript
const response = await fetch('/api/v1/endpoint', {
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.get(
    'https://api.example.com/api/v1/endpoint',
    headers={'Authorization': 'Bearer token'}
)
data = response.json()
```

## Лимиты запросов
- 1000 запросов в час для аутентифицированных пользователей
- 100 запросов в час для публичных эндпоинтов

## Связанные эндпоинты
- [GET /api/v1/related]()
- [POST /api/v1/related]()

---

**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/plugins
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
