#!/bin/bash
# Отправка уведомлений о событиях
# Хук: PostToolUse (matcher: Bash) — запускается после каждого вызова Bash; скрипт выходит, если команда не git push
# Примечание: у Claude Code нет встроенного события PostPush. Чтобы сработать на git push, проверьте строку
# команды bash на "git push" через matcher или условие внутри этого скрипта.

# Читаем вход хука и выходим, если команда Bash — не git push
INPUT=$(cat)
# Извлекаем команду (экранированные кавычки вроде \"msg\" сохраняются) и ищем "git push" как слово команды в любом месте
COMMAND=$(echo "$INPUT" | sed -nE 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/p' | head -1)
printf '%s\n' "$COMMAND" | grep -qE '(^|[^[:alnum:]_-]|\\n)git[[:space:]]+push([^[:alnum:]_-]|$)' || exit 0

REPO_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null)
COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null)
AUTHOR=$(git log -1 --pretty=%an 2>/dev/null)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

echo "📢 Отправляем уведомление команде..."

# Пример вебхука Slack (подставьте свой URL вебхука)
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"

if [ -n "$SLACK_WEBHOOK" ]; then
  curl -X POST "$SLACK_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"Новый push в *$REPO_NAME*\",
      \"attachments\": [{
        \"color\": \"good\",
        \"fields\": [
          {\"title\": \"Ветка\", \"value\": \"$BRANCH\", \"short\": true},
          {\"title\": \"Автор\", \"value\": \"$AUTHOR\", \"short\": true},
          {\"title\": \"Коммит\", \"value\": \"$COMMIT_MSG\"}
        ]
      }]
    }" \
    --silent --output /dev/null

  echo "✅ Уведомление в Slack отправлено"
fi

# Пример вебхука Discord (подставьте свой URL вебхука)
DISCORD_WEBHOOK="${DISCORD_WEBHOOK_URL:-}"

if [ -n "$DISCORD_WEBHOOK" ]; then
  curl -X POST "$DISCORD_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{
      \"content\": \"**Новый push в $REPO_NAME**\",
      \"embeds\": [{
        \"title\": \"$COMMIT_MSG\",
        \"color\": 3066993,
        \"fields\": [
          {\"name\": \"Ветка\", \"value\": \"$BRANCH\", \"inline\": true},
          {\"name\": \"Автор\", \"value\": \"$AUTHOR\", \"inline\": true}
        ]
      }]
    }" \
    --silent --output /dev/null

  echo "✅ Уведомление в Discord отправлено"
fi

# Пример уведомления по электронной почте
EMAIL_TO="${TEAM_EMAIL:-}"

if [ -n "$EMAIL_TO" ]; then
  echo "Новый push в $REPO_NAME от $AUTHOR" | \
    mail -s "Git push: $BRANCH" "$EMAIL_TO"

  echo "✅ Уведомление по почте отправлено"
fi

exit 0
