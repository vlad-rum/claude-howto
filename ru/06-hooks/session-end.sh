#!/usr/bin/env bash
# Хук SessionEnd: записывает пройденные модули, затем дописывает запись сессии
# в ~/.claude-howto-progress.json для постоянного учёта прогресса обучения.
#
# Срабатывает один раз, когда сессия Claude Code завершается, — не после каждого ответа.
# Хуки работают без управляющего терминала (/dev/tty недоступен), поэтому модули и
# заметки берутся из переменных окружения CLAUDE_HOWTO_MODULES / CLAUDE_HOWTO_NOTES.
#
# Установка: добавьте в .claude/settings.json на событие "SessionEnd" (см. ниже).

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# Защита: запускать только внутри этого репозитория
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

# Создаём файл прогресса, если его ещё нет
if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Claude Code — конец учебной сессии"
echo " $DATE $TIME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
# Пройденные модули, например запуск: CLAUDE_HOWTO_MODULES=06,07 claude
# 01=Слэш  02=Память  03=Навыки  04=Субагенты  05=MCP
# 06=Хуки  07=Плагины 08=Контрольные точки 09=Продвинутое 10=CLI
INPUT="${CLAUDE_HOWTO_MODULES:-}"

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  echo " Пропущено — сессия не записана."
  echo ""
  exit 0
fi

# Короткие номера сопоставляем с именами модулей (for вместо pipeline+while: bash 3.2 такое не разбирает)
IFS=',' read -ra PARTS <<< "$INPUT"
MODULES_JSON=""
for m in "${PARTS[@]}"; do
  m="${m// /}"  # убираем пробелы
  case "$m" in
    01) label='"01-slash-commands"' ;;
    02) label='"02-memory"' ;;
    03) label='"03-skills"' ;;
    04) label='"04-subagents"' ;;
    05) label='"05-mcp"' ;;
    06) label='"06-hooks"' ;;
    07) label='"07-plugins"' ;;
    08) label='"08-checkpoints"' ;;
    09) label='"09-advanced-features"' ;;
    10) label='"10-cli"' ;;
    *)  label="\"$m\"" ;;
  esac
  MODULES_JSON="${MODULES_JSON:+$MODULES_JSON,}$label"
done

# Необязательные заметки, например CLAUDE_HOWTO_NOTES="попробовал пример pre-commit"
NOTES="${CLAUDE_HOWTO_NOTES:-}"

# Передаём NOTES отдельным аргументом, чтобы Python экранировал JSON —
# так JSON не ломается, если в заметках есть кавычки или обратные слэши.
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo ""
echo " Сохранено в $PROGRESS_FILE"
[ -n "$NOTES" ] && echo " Заметки: $NOTES"
echo ""

exit 0
