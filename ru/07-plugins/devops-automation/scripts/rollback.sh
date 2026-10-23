#!/bin/bash
set -e

echo "⏪ Запуск отката..."

ENV=${1:-staging}
echo "📦 Целевое окружение: $ENV"

# Получение предыдущего деплоя
PREVIOUS=$(kubectl rollout history deployment/app -n $ENV | tail -2 | head -1 | awk '{print $1}')
echo "🔄 Откат к ревизии: $PREVIOUS"

# Выполнение отката
kubectl rollout undo deployment/app -n $ENV

# Ожидание отката
echo "⏳ Ожидание завершения отката..."
kubectl rollout status deployment/app -n $ENV

# Проверка здоровья
echo "🏥 Выполняются проверки здоровья..."
sleep 5
curl -f http://api.$ENV.example.com/health

echo "✅ Откат завершён!"
