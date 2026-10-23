#!/usr/bin/env node

/**
 * Хук после деплоя
 * Запускается после завершения деплоя
 */

async function postDeploy() {
  console.log('Выполняются задачи после деплоя...');

  const { execSync } = require('child_process');

  // Ждём, пока поды станут готовы
  console.log('Ожидание готовности подов...');
  try {
    execSync('kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s', {
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('❌ Поды не перешли в состояние готовности');
    process.exit(1);
  }

  // Запуск дымовых тестов
  console.log('Запуск дымовых тестов...');
  // Добавьте сюда команды дымовых тестов

  console.log('✅ Задачи после деплоя выполнены');
}

postDeploy().catch(error => {
  console.error('Хук после деплоя завершился ошибкой:', error);
  process.exit(1);
});
