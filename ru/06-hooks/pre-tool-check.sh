#!/bin/bash
# Предварительная проверка безопасности команд Bash
# Хук: PreToolUse (matcher: Bash)
#
# Этот хук запускается перед каждым выполнением инструмента Bash и блокирует
# или предупреждает о потенциально разрушительных и рискованных командах оболочки.
#
# Установка:
#   cp 06-hooks/pre-tool-check.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/pre-tool-check.sh
#
# Настройте в ~/.claude/settings.json:
#   {
#     "hooks": {
#       "PreToolUse": [
#         {
#           "matcher": "Bash",
#           "hooks": [
#             {
#               "type": "command",
#               "command": "~/.claude/hooks/pre-tool-check.sh"
#             }
#           ]
#         }
#       ]
#     }
#   }
#
# Вход: JSON через stdin такой формы:
#   { "tool_name": "Bash", "tool_input": { "command": "..." } }
#
# Соглашение о выходе (по протоколу хуков Claude Code):
#   - код 0 → разрешить. stdout может содержать JSON (hookSpecificOutput); stderr
#     молча отбрасывается, поэтому предупреждения на stderr НЕ видны.
#     Чтобы наблюдать за разрешёнными командами, пишите в файл журнала аудита.
#   - код 2 → блокировать. stderr возвращается Claude как причина блокировки.
#     Любой echo с объяснением, *почему* команда заблокирована, ОБЯЗАТЕЛЬНО
#     перенаправляйте в stderr через `>&2`, иначе Claude Code сообщит "No stderr output".
#
# Журнал аудита: каждый запуск записывается в
#   $CLAUDE_PROJECT_DIR/.claude/hooks/audit.log
# с решением (BLOCK/WARN/ALLOW), чтобы видеть совпадения уровня WARN,
# даже когда Claude Code отбрасывает их вывод в stderr.

# Читаем весь JSON со stdin
INPUT=$(cat)

# Извлекаем команду переносимым sed (совместимо с macOS и Linux)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# Если извлечь не удалось, берём сырой вход
if [ -z "$COMMAND" ]; then
  COMMAND="$INPUT"
fi

# ── Журнал аудита ─────────────────────────────────────────────────────────────
# Записывает каждый запуск с итоговым решением. Это единственный надёжный
# способ увидеть уровень WARN: Claude Code молча отбрасывает stderr
# при коде выхода 0. Если хук вызван вне Claude Code, берётся $(pwd)
# (например, при локальной проверке).
LOG_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/hooks"
LOG_FILE="$LOG_DIR/audit.log"
mkdir -p "$LOG_DIR" 2>/dev/null
log_decision() {
  echo "$(date -u +%FT%TZ) [$1] $COMMAND" >> "$LOG_FILE"
}

# ── Заблокированные шаблоны ───────────────────────────────────────────────────
# Эти команды блокируются безусловно: они почти всегда разрушительны
# и редко бывают намеренными в автоматическом контексте.

BLOCKED_PATTERNS=(
  # Якорим `rm -rf /`, чтобы после `/` был пробел или конец строки,
  # иначе поиск по подстроке ложно сработает, например, на `rm -rf /tmp/foo`.
  "rm -rf /([[:space:]]|$)"
  "rm -rf \*"
  "dd if=/dev/zero"
  "dd if=/dev/random"
  ":\(\)\{:\|:&\};:"  # Форк-бомба (метасимволы регулярного выражения экранированы)
  "mkfs\."           # Форматирование файловой системы
  "format c:"        # Форматирование диска Windows
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    log_decision "BLOCK:$pattern"
    # Эти echo ОБЯЗАТЕЛЬНО идут в stderr — Claude Code показывает stderr
    # как причину блокировки при коде 2. Запись в stdout даст "No stderr output".
    echo "❌ Заблокировано: обнаружена потенциально разрушительная команда: $pattern" >&2
    echo "   Команда: $COMMAND" >&2
    exit 2
  fi
done

# ── Шаблоны предупреждений ────────────────────────────────────────────────────
# Эти шаблоны рискованны, но могут быть намеренными. Пишем предупреждение и разрешаем.

WARNING_PATTERNS=(
  "rm -rf"
  "git push --force"
  "git reset --hard"
  "git clean -f"
  "chmod -R 777"
  "sudo rm"
  "DROP TABLE"
  "DROP DATABASE"
  "truncate"
)

MATCHED_WARNINGS=""
for pattern in "${WARNING_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    MATCHED_WARNINGS="${MATCHED_WARNINGS:+$MATCHED_WARNINGS,}$pattern"
    # Дублируем предупреждение в stderr для тех, кто запускает хук вручную.
    # Claude Code отбрасывает его при коде выхода 0 — надёжная запись
    # в журнале аудита (смотрите записи WARN).
    echo "⚠️  Предупреждение: обнаружена рискованная операция: $pattern" >&2
  fi
done

if [ -n "$MATCHED_WARNINGS" ]; then
  log_decision "WARN:$MATCHED_WARNINGS"
  echo "   Команда: $COMMAND" >&2
  echo "   Продолжаем — просмотрите предупреждения выше, прежде чем идти дальше." >&2
else
  log_decision "ALLOW"
fi

# ── Разрешить ─────────────────────────────────────────────────────────────────
exit 0
