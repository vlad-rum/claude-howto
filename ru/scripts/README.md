<!-- i18n-source: scripts/README.md -->
<!-- i18n-source-sha: 0e01159 -->
<!-- i18n-date: 2026-10-23 -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# Скрипты сборки

В этом каталоге два генератора, которые превращают markdown-файлы туториала
в форматы для распространения:

- [**Сборщик EPUB**](#скрипт-сборки-epub) — `build_epub.py`
- [**Сборщик статического сайта**](#сборщик-статического-сайта) — `build_website.py`

Оба считают файлы `.md` единственным источником истины — после правки markdown
запустите нужный скрипт заново, чтобы пересобрать результат.

---

# Скрипт сборки EPUB

Собрать электронную книгу EPUB из markdown-файлов Claude How-To.

## Возможности

- Раскладывает главы по структуре папок (01-slash-commands, 02-memory и т. д.)
- Рисует диаграммы Mermaid как изображения SVG с помощью [Pele](https://github.com/obsidianmd/pele), закреплённого пакета, который запускает Node.js; CSS-переменные сворачиваются в обычные цвета на белом фоне, чтобы их показал любой читатель EPUB
- Кэширует одинаковые диаграммы, так что каждая уникальная диаграмма рисуется только один раз
- Создаёт обложку из логотипа проекта
- Превращает внутренние ссылки markdown в ссылки на главы EPUB
- Строгий режим ошибок: сборка падает, если любую диаграмму не удаётся отрисовать

## Требования

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- Node.js >= 20 в `PATH` для отрисовки диаграмм Mermaid. Закреплённый пакет Pele скачивается при первом запуске (сеть нужна один раз), проверяется по sha256 и кэшируется в `scripts/.vendor-cache/pele/`

## Быстрый старт

```bash
# Самый простой путь — uv делает всё сам
uv run scripts/build_epub.py
```

## Настройка для разработки

```bash
# Создать виртуальное окружение
uv venv

# Активировать и установить зависимости
source .venv/bin/activate
uv pip install -r requirements-dev.txt

# Запустить тесты
pytest scripts/tests/ -v

# Запустить скрипт
python scripts/build_epub.py
```

## Параметры командной строки

```
usage: build_epub.py [-h] [--root ROOT] [--output OUTPUT] [--verbose]
                     [--lang {en,vi,zh,ja}]

параметры:
  -h, --help            показать эту справку и выйти
  --root, -r ROOT       Корневой каталог (по умолчанию: корень репозитория)
  --output, -o OUTPUT   Путь к результату (по умолчанию: claude-howto-guide.epub)
  --verbose, -v         Подробное логирование
  --lang {en,vi,zh,ja}  Язык сборки (по умолчанию: en)
```

## Примеры

```bash
# Сборка с подробным выводом
uv run scripts/build_epub.py --verbose

# Свой путь к результату
uv run scripts/build_epub.py --output ~/Desktop/claude-guide.epub

# Собрать переводное издание
uv run scripts/build_epub.py --lang vi
```

## Результат

Создаёт `claude-howto-guide.epub` в корневом каталоге репозитория.

В EPUB входит:
- Обложка с логотипом проекта
- Оглавление с вложенными разделами
- Всё содержимое markdown, преобразованное в HTML, совместимый с EPUB
- Диаграммы Mermaid, отрисованные как изображения SVG

## Запуск тестов

```bash
# С виртуальным окружением
source .venv/bin/activate
pytest scripts/tests/ -v

# Или напрямую через uv
uv run --with pytest --with pytest-asyncio \
    --with ebooklib --with markdown --with beautifulsoup4 \
    --with pillow \
    pytest scripts/tests/ -v
```

## Зависимости

Управляются встроенными метаданными скрипта PEP 723:

| Пакет | Назначение |
|---------|---------|
| `ebooklib` | Сборка EPUB |
| `markdown` | Преобразование Markdown в HTML |
| `beautifulsoup4` | Разбор HTML |
| `pillow` | Создание обложки |

## Устранение неполадок

**Сборка падает с `Pele is unavailable`**: установите Node.js >= 20 и убедитесь, что `node` есть в `PATH` (`node --version`).

**Сбой загрузки пакета Pele или контрольной суммы**: первая сборка скачивает закреплённый пакет Pele с cdn.jsdelivr.net и проверяет sha256 каждого файла. Офлайн или за прокси сделайте одну сборку с доступом в сеть; следующие сборки берут кэш в `scripts/.vendor-cache/pele/<version>/`. Несовпадение контрольной суммы значит, что загрузка изменена или обрезана: удалите этот каталог и соберите снова.

**Нет логотипа**: скрипт делает обложку только из текста, если не найден `claude-howto-logo.png`.

---

# Сборщик статического сайта

Собрать аккуратный, удобный на телефоне статический сайт из тех же markdown-файлов,
что и сборка EPUB. Сайт — это отрисованный вид; файлы `.md`
остаются единственным источником истины.

## Возможности

- По одной HTML-странице на каждый markdown-источник — внутренние ссылки `.md` переписываются
  на соответствующие страницы сайта
- Ссылки на файлы репозитория не в markdown (шаблоны, скрипты, JSON) становятся
  URL blob на GitHub, которые открывают исходник на github.com
- Диаграммы Mermaid рисуются на клиенте с помощью Pele (`pele.global.js`) и отдаются
  с собранного сайта (без CDN во время работы); они следуют переключателю тёмной темы
- Tailwind CSS собран автономным CLI (бинарник Go, без Node.js) и
  отдаётся с собранного сайта — отзывчивая вёрстка с боковой навигацией, оглавлением
  на странице, переключателем тёмной темы и переходами на предыдущую и следующую страницу
- Шрифты Inter и JetBrains Mono лежат рядом с CSS на том же хосте — при загрузке страницы
  нет запросов к третьим сторонам
- Повторяет порядок учебной программы EPUB (`01-` … `10-` плюс документы верхнего уровня)
- Можно выложить как обычные статические файлы — рассчитано на деплой в GitHub Pages

## Быстрый старт

```bash
# Собрать английский сайт в ./site/
uv run scripts/build_website.py

# Посмотреть локально
python -m http.server --directory site 8080
# затем откройте http://localhost:8080
```

## Параметры командной строки

```
usage: build_website.py [-h] [--root ROOT] [--output OUTPUT]
                        [--lang {en,vi,zh,ja,uk}] [--repo-url REPO_URL]
                        [--branch BRANCH] [--verbose]

параметры:
  --root, -r ROOT       Корень исходников (по умолчанию: корень репозитория)
  --output, -o OUTPUT   Каталог вывода (по умолчанию: <repo>/site)
  --lang LANG           Язык сборки: en | vi | zh | ja | uk
  --repo-url URL        Репозиторий GitHub для blob-ссылок (по умолчанию: luongnv89/claude-howto)
  --branch BRANCH       Ветка для blob-ссылок (по умолчанию: main)
  --verbose, -v         Подробное логирование
```

## Деплой на GitHub Pages

В репозитории есть рабочий процесс `.github/workflows/pages.yml`: он собирает
сайт при каждом push в `main` (если меняется любой файл `.md` или генератор) и
публикует через `actions/deploy-pages`. Чтобы это заработало, включите GitHub Pages в настройках репозитория
и укажите **Source: GitHub Actions**.

## Архитектура

`build_website.py` переиспользует логику порядка глав из `build_epub.py` и
поставляет HTML-шаблоны в `scripts/website_templates/`:

- `page.html.j2` — шаблон Jinja2 страницы с боковой навигацией, оглавлением, предыдущей и следующей
- `tailwind.config.js`, `tailwind.input.css` — конфигурация и входной CSS для
  автономного CLI Tailwind; CLI просматривает собранный HTML и создаёт
  `site/assets/tailwind.css` только с теми утилитами, которые реально используются
- `site.css` — небольшой слой стилей сайта плюс тема Pygments

Бинарник CLI Tailwind, пакет Pele и файлы шрифтов скачиваются при
первой сборке в `scripts/.vendor-cache/` (в gitignore) — см.
`scripts/vendor_assets.py`.

Якоря заголовков строятся тем же алгоритмом, что в
`check_cross_references.heading_to_anchor`, поэтому ссылки `#anchor`, которые проверяет
хук pre-commit, на отрисованном сайте открываются правильно.
