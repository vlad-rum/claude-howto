#!/bin/bash
# Журнал всех команд bash
# Хук: PostToolUse (matcher: Bash)
#
# Читает выполненную команду из JSON на stdin и пишет её в файл.
#
# Совместимо с: macOS, Linux, Windows (Git Bash)

# Читаем JSON со stdin (протокол хуков Claude Code)
INPUT=$(cat)

# Извлекаем команду bash из tool_input
# Примечание: sed [^"]* останавливается на экранированных кавычках в JSON; у команд
# со строками в двойных кавычках захватывается только часть до первого \" — это
# известное ограничение разбора JSON через sed, для журнала оно приёмлемо.
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$COMMAND" ]; then
  exit 0
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOGFILE="$HOME/.claude/bash-commands.log"

# Создаём каталог журнала, если его ещё нет
mkdir -p "$(dirname "$LOGFILE")"

# Пишем команду в журнал
echo "[$TIMESTAMP] $COMMAND" >> "$LOGFILE"

exit 0
