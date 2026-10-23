<!-- i18n-source: .github/TESTING.md -->
<!-- i18n-source-sha: 728bd50 -->
<!-- i18n-date: 2026-10-23 -->

# Руководство по тестированию

Этот документ описывает инфраструктуру тестирования Claude How To.

## Обзор

Проект использует GitHub Actions, чтобы автоматически запускать тесты при каждом push и pull request. Тесты охватывают:

- **Модульные тесты**: тесты Python на pytest
- **Качество кода**: линтинг и форматирование с помощью Ruff
- **Безопасность**: поиск уязвимостей с помощью Bandit
- **Проверка типов**: статический анализ типов с помощью mypy
- **Проверка сборки**: тест генерации EPUB

## Локальный запуск тестов

### Что нужно заранее

```bash
# Установить uv (быстрый менеджер пакетов Python)
pip install uv

# Или на macOS через Homebrew
brew install uv
```

### Настройка окружения

```bash
# Клонировать репозиторий
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# Создать виртуальное окружение
uv venv

# Активировать его
source .venv/bin/activate  # macOS/Linux
# или
.venv\Scripts\activate     # Windows

# Установить зависимости для разработки
uv pip install -r requirements-dev.txt
```

### Запуск тестов

```bash
# Запустить все модульные тесты
pytest scripts/tests/ -v

# Запустить тесты с покрытием
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# Запустить конкретный файл тестов
pytest scripts/tests/test_build_epub.py -v

# Запустить конкретную тестовую функцию
pytest scripts/tests/test_build_epub.py::test_function_name -v

# Запустить тесты в режиме наблюдения (нужен pytest-watch)
ptw scripts/tests/
```

### Запуск линтинга

```bash
# Проверить форматирование кода
ruff format --check scripts/

# Автоматически исправить форматирование
ruff format scripts/

# Запустить линтер
ruff check scripts/

# Автоматически исправить замечания линтера
ruff check --fix scripts/
```

### Запуск проверки безопасности

```bash
# Запустить проверку безопасности Bandit
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/

# Собрать отчёт в JSON
bandit -c pyproject.toml -r scripts/ --exclude scripts/tests/ -f json -o bandit-report.json
```

### Запуск проверки типов

```bash
# Проверить типы с помощью mypy
mypy scripts/ --ignore-missing-imports --no-implicit-optional
```

## Рабочий процесс GitHub Actions

### Когда запускается

- **Push** в ветки `main` или `develop` (когда меняются скрипты)
- **Pull request** в `main` (когда меняются скрипты)
- Ручной запуск рабочего процесса

### Задачи

#### 1. Модульные тесты (pytest)

- **Где выполняется**: Ubuntu latest
- **Версии Python**: 3.10, 3.11, 3.12
- **Что делает**:
  - Ставит зависимости из `requirements-dev.txt`
  - Запускает pytest с отчётом о покрытии
  - Загружает покрытие в Codecov
  - Сохраняет результаты тестов и HTML покрытия

**Итог**: если любой тест падает, рабочий процесс падает (критично)

#### 2. Качество кода (Ruff)

- **Где выполняется**: Ubuntu latest
- **Версия Python**: 3.11
- **Что делает**:
  - Проверяет форматирование через `ruff format`
  - Запускает линтер через `ruff check`
  - Сообщает о проблемах, но не роняет рабочий процесс

**Итог**: не блокирует (только предупреждение)

#### 3. Проверка безопасности (Bandit)

- **Где выполняется**: Ubuntu latest
- **Версия Python**: 3.11
- **Что делает**:
  - Ищет уязвимости безопасности
  - Собирает отчёт в JSON
  - Загружает отчёт как артефакт

**Итог**: не блокирует (только предупреждение)

#### 4. Проверка типов (mypy)

- **Где выполняется**: Ubuntu latest
- **Версия Python**: 3.11
- **Что делает**:
  - Выполняет статический анализ типов
  - Сообщает о несовпадениях типов
  - Помогает ловить ошибки рано

**Итог**: не блокирует (только предупреждение)

#### 5. Сборка EPUB

- **Где выполняется**: Ubuntu latest
- **Зависит от**: pytest, lint, security (все должны пройти)
- **Что делает**:
  - Собирает файл EPUB через `scripts/build_epub.py`
  - Проверяет, что EPUB успешно создан
  - Загружает EPUB как артефакт

**Итог**: если сборка падает, рабочий процесс падает (критично)

#### 6. Сводка

- **Где выполняется**: Ubuntu latest
- **Зависит от**: всех остальных задач
- **Что делает**:
  - Собирает сводку рабочего процесса
  - Перечисляет все артефакты
  - Сообщает общий статус

## Как писать тесты

### Структура тестов

Тесты кладите в `scripts/tests/` с именами вида `test_*.py`:

```python
# scripts/tests/test_example.py
import pytest
from scripts.example_module import some_function

def test_basic_functionality():
    """Проверяет, что some_function работает правильно."""
    result = some_function("input")
    assert result == "expected_output"

def test_error_handling():
    """Проверяет, что some_function аккуратно обрабатывает ошибки."""
    with pytest.raises(ValueError):
        some_function("invalid_input")

@pytest.mark.asyncio
async def test_async_function():
    """Проверяет асинхронные функции."""
    result = await async_function()
    assert result is not None
```

### Удачные практики тестов

- **Говорящие имена**: `test_function_returns_correct_value()`
- **Одно утверждение на тест** (когда можно): так проще разбирать падения
- **Фикстуры** для повторяемой подготовки: см. `scripts/tests/conftest.py`
- **Подменяйте внешние сервисы**: используйте `unittest.mock` или `pytest-mock`
- **Проверяйте граничные случаи**: пустой ввод, значения None, ошибки
- **Держите тесты быстрыми**: избегайте sleep() и внешнего ввода-вывода
- **Используйте маркеры pytest**: `@pytest.mark.slow` для медленных тестов

### Фикстуры

Общие фикстуры определены в `scripts/tests/conftest.py`:

```python
# Используйте фикстуры в тестах
def test_something(tmp_path):
    """Фикстура tmp_path даёт временный каталог."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

## Отчёты о покрытии

### Локальное покрытие

```bash
# Собрать отчёт о покрытии
pytest scripts/tests/ --cov=scripts --cov-report=html

# Открыть отчёт о покрытии в браузере
open htmlcov/index.html
```

### Цели по покрытию

- **Минимальное покрытие**: 80%
- **Покрытие ветвей**: включено
- **На чём сосредоточиться**: основная функциональность и пути ошибок

## Хуки pre-commit

Проект использует хуки pre-commit, чтобы автоматически запускать проверки перед коммитами:

```bash
# Установить хуки pre-commit
pre-commit install

# Запустить хуки вручную
pre-commit run --all-files

# Пропустить хуки для коммита (не рекомендуется)
git commit --no-verify
```

Хуки в `.pre-commit-config.yaml`:
- Форматировщик Ruff
- Линтер Ruff
- Сканер безопасности Bandit
- Проверка YAML
- Проверка размера файлов
- Поиск конфликтов слияния

## Устранение неполадок

### Тесты проходят локально, но падают в CI

Типичные причины:
1. **Разная версия Python**: CI использует 3.10, 3.11, 3.12
2. **Не хватает зависимостей**: обновите `requirements-dev.txt`
3. **Различия платформ**: разделители путей, переменные окружения
4. **Нестабильные тесты**: тесты, которые зависят от времени или порядка

Решение:
```bash
# Проверить на тех же версиях Python
uv python install 3.10 3.11 3.12

# Проверить в чистом окружении
rm -rf .venv
uv venv
uv pip install -r requirements-dev.txt
pytest scripts/tests/
```

### Bandit сообщает о ложных срабатываниях

Некоторые предупреждения безопасности могут быть ложными. Настройте в `pyproject.toml`:

```toml
[tool.bandit]
exclude_dirs = ["scripts/tests"]
skips = ["B101"]  # Пропустить предупреждение assert_used
```

### Проверка типов слишком строгая

Ослабьте проверку типов для отдельных файлов:

```python
# Добавьте в начало файла
# type: ignore

# Или для отдельных строк
some_dynamic_code()  # type: ignore
```

## Удачные практики непрерывной интеграции

1. **Держите тесты быстрыми**: каждый тест должен заканчиваться меньше чем за 1 секунду
2. **Не тестируйте внешние API**: подменяйте внешние сервисы
3. **Тестируйте изолированно**: каждый тест должен быть независим
4. **Ясные утверждения**: `assert x == 5`, а не `assert x`
5. **Асинхронные тесты**: используйте `@pytest.mark.asyncio`
6. **Собирайте отчёты**: покрытие, безопасность, проверка типов

## Материалы

- [Документация pytest](https://docs.pytest.org/)
- [Документация Ruff](https://docs.astral.sh/ruff/)
- [Документация Bandit](https://bandit.readthedocs.io/)
- [Документация mypy](https://mypy.readthedocs.io/)
- [Документация GitHub Actions](https://docs.github.com/en/actions)

## Тесты в материалах участников

Когда отправляете PR:

1. **Пишите тесты** для новой функциональности
2. **Запускайте тесты локально**: `pytest scripts/tests/ -v`
3. **Проверяйте покрытие**: `pytest scripts/tests/ --cov=scripts`
4. **Запускайте линтинг**: `ruff check scripts/`
5. **Проверка безопасности**: `bandit -r scripts/ --exclude scripts/tests/`
6. **Обновляйте документацию**, если тесты меняются

Тесты обязательны для всех PR! 🧪

---

По вопросам и проблемам тестирования откройте GitHub Issue или обсуждение.
