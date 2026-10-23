#!/bin/bash
# Проверка промптов пользователя
# Хук: UserPromptSubmit
#
# Читает промпт пользователя из JSON на stdin и блокирует опасные операции.
#
# Совместимо с: macOS, Linux, Windows (Git Bash)

# Читаем JSON со stdin (протокол хуков Claude Code)
INPUT=$(cat)

# Извлекаем текст промпта из JSON на входе
# Claude Code передаёт текст UserPromptSubmit в поле "prompt"
PROMPT=$(echo "$INPUT" | sed -n 's/.*"prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$PROMPT" ]; then
  exit 0
fi

# Проверяем опасные операции
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "delete database"
  "drop database"
  "format disk"
  "dd if="
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$PROMPT" | grep -qi "$pattern"; then
    printf '{"decision": "block", "reason": "Обнаружена опасная операция: %s"}' "$pattern"
    exit 0
  fi
done

# Проверяем деплой в продакшен
if echo "$PROMPT" | grep -qiE "(deploy|push).*production"; then
  if [ ! -f ".deployment-approved" ]; then
    echo '{"decision": "block", "reason": "Деплой в продакшен требует одобрения. Чтобы продолжить, создайте файл .deployment-approved."}'
    exit 0
  fi
fi

# Проверяем нужный контекст для отдельных операций
if echo "$PROMPT" | grep -qi "refactor"; then
  if [ ! -d "tests" ] && [ ! -d "test" ]; then
    printf '{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "Предупреждение: рефакторинг без тестов может быть рискованным. Сначала лучше написать тесты."}}'
  fi
fi

exit 0
