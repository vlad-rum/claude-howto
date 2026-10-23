#!/bin/bash
# Запуск тестов перед коммитом
# Хук: PreToolUse (matcher: Bash) — проверяет, что команда является git commit
# Примечание: события хука "PreCommit" нет. Используйте PreToolUse с matcher Bash
# и проверьте команду, чтобы распознать операции git commit.
#
# Коды выхода: 2 блокирует вызов инструмента и показывает stderr как причину блокировки.
# Любое другое ненулевое значение — НЕблокирующая ошибка: коммит продолжится.
# Источник: https://code.claude.com/docs/en/hooks

# Читаем JSON хука со stdin; тесты запускаем только для команд git commit
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
if ! echo "$COMMAND" | grep -q 'git commit'; then
  exit 0
fi

echo "🧪 Запускаем тесты перед коммитом..."

# Проверяем, есть ли package.json (проект Node.js)
if [ -f "package.json" ]; then
  if grep -q "\"test\":" package.json; then
    npm test
    if [ $? -ne 0 ]; then
      echo "❌ Тесты не прошли! Коммит заблокирован." >&2
      exit 2
    fi
  fi
fi

# Проверяем, доступен ли pytest (проект Python)
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  if command -v pytest &> /dev/null; then
    pytest
    if [ $? -ne 0 ]; then
      echo "❌ Тесты не прошли! Коммит заблокирован." >&2
      exit 2
    fi
  fi
fi

# Проверяем, есть ли go.mod (проект Go)
if [ -f "go.mod" ]; then
  go test ./...
  if [ $? -ne 0 ]; then
    echo "❌ Тесты не прошли! Коммит заблокирован." >&2
    exit 2
  fi
fi

# Проверяем, есть ли Cargo.toml (проект Rust)
if [ -f "Cargo.toml" ]; then
  cargo test
  if [ $? -ne 0 ]; then
    echo "❌ Тесты не прошли! Коммит заблокирован." >&2
    exit 2
  fi
fi

echo "✅ Все тесты прошли! Продолжаем коммит."
exit 0
