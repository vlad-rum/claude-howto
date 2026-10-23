#!/bin/bash
# Автоформатирование кода после записи
# Хук: PostToolUse (matcher: Write)
#
# Читает путь к целевому файлу из JSON на stdin и запускает подходящий форматтер
# прямо в файле после того, как Claude его записал.
#
# Совместимо с: macOS, Linux, Windows (Git Bash)

# Читаем JSON со stdin (протокол хуков Claude Code)
INPUT=$(cat)

# Извлекаем file_path через sed (совместимо со всеми платформами)
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Определяем тип файла и форматируем соответственно
case "$FILE_PATH" in
  *.js|*.jsx|*.ts|*.tsx)
    if command -v prettier &> /dev/null; then
      prettier --write "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.py)
    if command -v black &> /dev/null; then
      black "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.go)
    if command -v gofmt &> /dev/null; then
      gofmt -w "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.rs)
    if command -v rustfmt &> /dev/null; then
      rustfmt "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.java)
    if command -v google-java-format &> /dev/null; then
      google-java-format -i "$FILE_PATH" 2>/dev/null
    fi
    ;;
esac

exit 0
