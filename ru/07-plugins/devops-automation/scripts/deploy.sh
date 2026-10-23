#!/bin/bash
set -e

echo "🚀 Запуск деплоя..."

# Загрузка окружения
ENV=${1:-staging}
echo "📦 Целевое окружение: $ENV"

# Проверки перед деплоем
echo "✓ Выполняются проверки перед деплоем..."
npm run lint
npm test

# Сборка
echo "🔨 Сборка приложения..."
npm run build

# Деплой
echo "🚢 Деплой в $ENV..."
kubectl apply -f k8s/$ENV/

# Проверка здоровья
echo "🏥 Выполняются проверки здоровья..."
sleep 10
curl -f http://api.$ENV.example.com/health

echo "✅ Деплой завершён!"
