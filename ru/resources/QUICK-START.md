<!-- i18n-source: resources/QUICK-START.md -->
<!-- i18n-source-sha: 20779db -->
<!-- i18n-date: 2026-10-23 -->

# Быстрый старт — бренд-материалы

## Скопируйте материалы в проект

```bash
# Скопировать все материалы в веб-проект
cp -r resources/ /path/to/your/website/

# Или только фавиконки для веба
cp resources/favicons/* /path/to/your/website/public/
```

## Добавьте в HTML (скопируйте)

```html
<!-- Фавиконки -->
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-32.svg" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-16.svg" sizes="16x16">
<link rel="apple-touch-icon" href="/resources/favicons/favicon-128.svg">
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-256.svg" sizes="256x256">
<meta name="theme-color" content="#000000">
```

## Используйте в Markdown и документации

```markdown
# Claude How To

![Логотип Claude How To](resources/logos/claude-howto-logo.svg)

![Значок](resources/icons/claude-howto-icon.svg)
```

## Рекомендуемые размеры

| Назначение | Размер | Файл |
|---------|------|------|
| Шапка сайта | 520×120 | `logos/claude-howto-logo.svg` |
| Значок приложения | 256×256 | `icons/claude-howto-icon.svg` |
| Вкладка браузера | 32×32 | `favicons/favicon-32.svg` |
| Домашний экран телефона | 128×128 | `favicons/favicon-128.svg` |
| Настольное приложение | 256×256 | `favicons/favicon-256.svg` |
| Маленький аватар | 64×64 | `favicons/favicon-64.svg` |

## Значения цветов

```css
/* Используйте это в своём CSS */
--color-primary: #000000;
--color-secondary: #6B7280;
--color-accent: #22C55E;
--color-bg-light: #FFFFFF;
--color-bg-dark: #0A0A0A;
```

## Смысл знака

**Компас со скобкой кода**:
- Кольцо компаса = навигация, структурированный учебный путь
- Зелёная северная стрелка = направление, прогресс, проводник
- Чёрная южная стрелка = опора, твёрдое основание
- Скобка `>` = приглашение терминала, код, контекст CLI
- Засечки = точность, структурированные шаги

Это символ «найти путь в коде с ясным проводником».

## Что куда ставить

### Сайт
- **Шапка**: логотип (`logos/claude-howto-logo.svg`)
- **Фавиконка**: 32px (`favicons/favicon-32.svg`)
- **Превью для соцсетей**: значок (`icons/claude-howto-icon.svg`)

### GitHub
- **Значок README**: значок (`icons/claude-howto-icon.svg`) при 64–128px
- **Аватар репозитория**: значок (`icons/claude-howto-icon.svg`)

### Социальные сети
- **Фото профиля**: значок (`icons/claude-howto-icon.svg`)
- **Баннер**: логотип (`logos/claude-howto-logo.svg`)
- **Миниатюра**: значок 256×256px

### Документация
- **Заголовки глав**: логотип или значок (масштаб по месту)
- **Значки навигации**: фавиконка (32–64px)

---

Полная документация — в [README.md](README.md).
