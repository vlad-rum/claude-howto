#!/bin/bash
# Проверка безопасности при записи файла
# Хук: PostToolUse (matcher: Write)
#
# Ищет в файлах захардкоженные секреты, API-ключи и учётные данные.
# При находках выдаёт неблокирующее предупреждение через additionalContext.
#
# Совместимо с: macOS, Linux, Windows (Git Bash)

# Читаем JSON со stdin (протокол хуков Claude Code)
INPUT=$(cat)

# Извлекаем file_path через sed (совместимо со всеми платформами, включая Windows Git Bash)
# Обходимся без grep -P (его нет в Windows Git Bash) и без зависимости от python3
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Пропускаем бинарные файлы, каталоги зависимостей и артефакты сборки
case "$FILE_PATH" in
  *.png|*.jpg|*.jpeg|*.gif|*.svg|*.ico|*.woff|*.woff2|*.ttf|*.eot) exit 0 ;;
  */node_modules/*|*/.git/*|*/dist/*|*/build/*) exit 0 ;;
esac

ISSUES=""

# Ищем захардкоженные пароли
# Подходит и JSON ("password": "value"), и код (password = 'value')
# Разделитель \\n — это допустимый JSON-эскейп перевода строки, printf пропускает его безопасно
if grep -qiE '"password"[[:space:]]*:[[:space:]]*"[^"]+"' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен возможный захардкоженный пароль\\n"
elif grep -qiE '(password|passwd|pwd)[[:space:]]*=[[:space:]]*'"'"'[^'"'"']+'"'"'' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен возможный захардкоженный пароль\\n"
fi

# Ищем захардкоженные API-ключи
if grep -qiE '"(api[_-]?key|apikey|access[_-]?token)"[[:space:]]*:[[:space:]]*"[^"]+"' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен возможный захардкоженный API-ключ\\n"
fi

# Ищем захардкоженные секреты и токены
if grep -qiE '(secret|token)[[:space:]]*=[[:space:]]*['"'"'"][^'"'"'"]+['"'"'"]' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен возможный захардкоженный секрет или токен\\n"
fi

# Ищем закрытые ключи
if grep -q "BEGIN.*PRIVATE KEY" "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен закрытый ключ\\n"
fi

# Ищем ключи AWS
if grep -qE "AKIA[0-9A-Z]{16}" "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- ПРЕДУПРЕЖДЕНИЕ: обнаружен ключ доступа AWS\\n"
fi

# Сканируем semgrep, если он есть (stdout подавлен, чтобы не смешать его с JSON)
if command -v semgrep &> /dev/null; then
  semgrep --config=auto "$FILE_PATH" --quiet >/dev/null 2>/dev/null
fi

# Сканируем trufflehog, если он есть (stdout подавлен, чтобы не смешать его с JSON)
if command -v trufflehog &> /dev/null; then
  trufflehog filesystem "$FILE_PATH" --only-verified --quiet >/dev/null 2>/dev/null
fi

# Если проблемы найдены, выводим их как additionalContext (неблокирующее предупреждение)
# Формат hookSpecificOutput обязателен по протоколу PostToolUse в Claude Code
if [ -n "$ISSUES" ]; then
  # Экранируем путь к файлу для JSON (обратный слэш и двойная кавычка)
  # В ISSUES разделитель уже \\n (допустимый JSON-эскейп) — экранируем только двойные кавычки
  SAFE_PATH=$(printf '%s' "$FILE_PATH" | sed 's/\\/\\\\/g; s/"/\\"/g')
  SAFE_ISSUES=$(printf '%s' "$ISSUES" | sed 's/"/\\"/g')
  printf '{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "Проверка безопасности нашла проблемы в %s:\\n%sПросмотрите их и используйте переменные окружения."}}' "$SAFE_PATH" "$SAFE_ISSUES"
fi

exit 0
