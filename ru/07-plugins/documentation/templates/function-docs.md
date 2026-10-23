<!-- i18n-source: 07-plugins/documentation/templates/function-docs.md -->
<!-- i18n-source-sha: b9a973b -->
<!-- i18n-date: 2026-10-23 -->

# Функция: `functionName`

## Описание
Краткое описание того, что делает функция.

## Сигнатура
```typescript
function functionName(param1: Type1, param2: Type2): ReturnType
```

## Параметры

| Параметр | Тип | Обязательно | Описание |
|-----------|------|----------|-------------|
| param1 | Type1 | Да | Описание param1 |
| param2 | Type2 | Нет | Описание param2 |

## Возвращает
**Тип**: `ReturnType`

Описание того, что возвращается.

## Исключения
- `Error`: Когда передан неверный ввод
- `TypeError`: Когда передан неверный тип

## Примеры

### Базовое использование
```typescript
const result = functionName('value1', 'value2');
console.log(result);
```

### Продвинутое использование
```typescript
const result = functionName(
  complexParam1,
  { option: true }
);
```

## Заметки
- Дополнительные заметки или предупреждения
- Соображения о производительности
- Лучшие практики

## См. также
- [Связанная функция]()
- [Документация API]()

---

**Последнее обновление**: 4 августа 2026
**Версия Claude Code**: 2.1.220
**Источники**:
- https://code.claude.com/docs/en/plugins
**Совместимые модели**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
