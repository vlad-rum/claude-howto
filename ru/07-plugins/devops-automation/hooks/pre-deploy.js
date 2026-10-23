#!/usr/bin/env node

/**
 * Хук перед деплоем
 * Проверяет окружение и предварительные условия перед деплоем
 */

async function preDeploy() {
  console.log('Выполняются проверки перед деплоем...');

  const { execSync } = require('child_process');

  // Проверка, установлен ли kubectl
  try {
    execSync('which kubectl', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ kubectl не найден. Установите CLI Kubernetes.');
    process.exit(1);
  }

  // Проверка подключения к кластеру
  try {
    execSync('kubectl cluster-info', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Нет подключения к кластеру Kubernetes');
    process.exit(1);
  }

  console.log('✅ Проверки перед деплоем пройдены');
}

preDeploy().catch(error => {
  console.error('Хук перед деплоем завершился ошибкой:', error);
  process.exit(1);
});
