#!/bin/bash

echo "🏥 Проверка здоровья системы"
echo "===================="

ENV=${1:-production}

# Проверка API
echo -n "API: "
if curl -sf http://api.$ENV.example.com/health > /dev/null; then
  echo "✅ Исправен"
else
  echo "❌ Неисправен"
fi

# Проверка базы данных
echo -n "База данных: "
if pg_isready -h db.$ENV.example.com > /dev/null 2>&1; then
  echo "✅ Исправна"
else
  echo "❌ Неисправна"
fi

# Проверка подов
echo -n "Поды Kubernetes: "
PODS_READY=$(kubectl get pods -n $ENV --no-headers | grep "Running" | wc -l)
PODS_TOTAL=$(kubectl get pods -n $ENV --no-headers | wc -l)
echo "$PODS_READY/$PODS_TOTAL готовы"

echo "===================="
