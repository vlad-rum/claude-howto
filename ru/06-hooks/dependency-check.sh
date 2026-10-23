#!/bin/bash
# Проверка известных уязвимостей в зависимостях после изменения файлов манифеста.
# Хук: PostToolUse (matcher: Write)
#
# Читает путь к целевому файлу из JSON на stdin (протокол хуков Claude Code).
# Источник: https://code.claude.com/docs/en/hooks

# Читаем JSON со stdin (протокол хуков Claude Code)
INPUT=$(cat)

# Извлекаем file_path через sed (совместимо со всеми платформами)
FILE=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE" ]; then
  exit 0
fi

# Для сопоставления берём basename — file_path может быть абсолютным путём
BASENAME=$(basename "$FILE")

# Запускаем только когда записан манифест зависимостей
case "$BASENAME" in
  package.json|package-lock.json|yarn.lock|pnpm-lock.yaml| \
  requirements.txt|Pipfile|Pipfile.lock|pyproject.toml| \
  go.mod|go.sum| \
  Cargo.toml|Cargo.lock| \
  Gemfile|Gemfile.lock| \
  composer.json|composer.lock| \
  pom.xml|build.gradle|build.gradle.kts)
    echo "📦 Обновлён манифест зависимостей: $FILE — ищем уязвимости..."
    ;;
  *)
    exit 0
    ;;
esac

ISSUES_FOUND=0

# ── npm / yarn / pnpm ────────────────────────────────────────────────────────
if [[ "$BASENAME" == package*.json || "$BASENAME" == yarn.lock || "$BASENAME" == pnpm-lock.yaml ]]; then
  if command -v npm &>/dev/null; then
    echo "🔍 Запускаем npm audit..."
    if ! npm audit --audit-level=high --json 2>/dev/null | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
vulns = data.get('metadata', {}).get('vulnerabilities', {})
high = vulns.get('high', 0) + vulns.get('critical', 0)
if high:
    print(f'  ⚠️  Найдено уязвимостей npm уровня high/critical: {high}. Запустите: npm audit fix')
    sys.exit(1)
" 2>/dev/null; then
      ISSUES_FOUND=1
    else
      echo "  ✅ Уязвимостей npm уровня high/critical нет"
    fi
  fi

  if command -v yarn &>/dev/null && [[ "$BASENAME" == yarn.lock ]]; then
    echo "🔍 Запускаем yarn audit..."
    if ! yarn audit --level high --json 2>/dev/null | \
        grep -q '"type":"auditAdvisory"' 2>/dev/null; then
      echo "  ✅ Уязвимостей yarn уровня high нет"
    else
      echo "  ⚠️  yarn audit нашёл уязвимости. Запустите: yarn audit --level high"
      ISSUES_FOUND=1
    fi
  fi
fi

# ── Python ───────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == requirements.txt || "$BASENAME" == Pipfile* || "$BASENAME" == pyproject.toml ]]; then
  if command -v pip-audit &>/dev/null; then
    echo "🔍 Запускаем pip-audit..."
    if pip-audit --format=json 2>/dev/null | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
vulns = [d for d in data.get('dependencies', []) if d.get('vulns')]
if vulns:
    for dep in vulns:
        for v in dep['vulns']:
            print(f'  ⚠️  {dep[\"name\"]} {dep[\"version\"]}: {v[\"id\"]} — {v[\"fix_versions\"]}')
    sys.exit(1)
" 2>/dev/null; then
      echo "  ✅ Уязвимостей Python не найдено"
    else
      ISSUES_FOUND=1
      echo "  Подробности: запустите pip-audit"
    fi
  elif command -v safety &>/dev/null; then
    echo "🔍 Запускаем safety check..."
    OUTPUT=$(safety check --short-report 2>&1)
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
      echo "  ✅ Уязвимостей Python не найдено"
    elif echo "$OUTPUT" | grep -qiE "vulnerability|CVE|insecure"; then
      echo "$OUTPUT"
      ISSUES_FOUND=1
    else
      echo "  ⚠️  safety check не завершился (ошибка сети или конфигурации)" >&2
    fi
  fi
fi

# ── Go ───────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == go.mod || "$BASENAME" == go.sum ]]; then
  if command -v govulncheck &>/dev/null; then
    echo "🔍 Запускаем govulncheck..."
    OUTPUT=$(govulncheck ./... 2>&1)
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
      echo "  ✅ Уязвимостей Go не найдено"
    elif echo "$OUTPUT" | grep -q "Vulnerability #"; then
      echo "$OUTPUT"
      ISSUES_FOUND=1
    else
      echo "  ⚠️  govulncheck не завершился: $OUTPUT" >&2
    fi
  fi
fi

# ── Rust ─────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == Cargo.toml || "$BASENAME" == Cargo.lock ]]; then
  if command -v cargo-audit &>/dev/null; then
    echo "🔍 Запускаем cargo audit..."
    if ! cargo audit 2>/dev/null; then
      ISSUES_FOUND=1
    else
      echo "  ✅ Уязвимостей Rust не найдено"
    fi
  fi
fi

# ── Ruby ─────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == Gemfile || "$BASENAME" == Gemfile.lock ]]; then
  if command -v bundler-audit &>/dev/null; then
    echo "🔍 Запускаем bundler-audit..."
    bundler-audit check --update 2>/dev/null || ISSUES_FOUND=1
  fi
fi

# ── Общий запасной вариант: trivy ────────────────────────────────────────────
if command -v trivy &>/dev/null; then
  echo "🔍 Запускаем сканирование trivy fs..."
  if ! trivy fs --exit-code 1 --severity HIGH,CRITICAL --quiet . 2>/dev/null; then
    ISSUES_FOUND=1
  else
    echo "  ✅ trivy не нашёл проблем уровня HIGH/CRITICAL"
  fi
fi

if [ "$ISSUES_FOUND" -eq 0 ]; then
  echo "✅ Проверка зависимостей пройдена — уязвимости не обнаружены"
else
  echo ""
  echo "⚠️  Обнаружены уязвимости. Просмотрите и обновите зависимости перед коммитом."
  echo "   Этот хук только предупреждает и не блокирует ваш рабочий процесс."
fi

# Всегда выходим с кодом 0 — хук предупреждает, но не блокирует
exit 0
