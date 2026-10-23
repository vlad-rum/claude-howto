#!/usr/bin/env node

/**
 * Хук перед ревью
 * Запускается перед началом ревью PR, чтобы проверить предварительные условия
 */

async function preReview() {
  console.log('Выполняются проверки перед ревью...');

  // Проверка, что это git-репозиторий
  const { execSync } = require('child_process');
  try {
    execSync('git rev-parse --git-dir', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Это не git-репозиторий');
    process.exit(1);
  }

  // Проверка незакоммиченных изменений
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf-8' });
    if (status.trim()) {
      console.warn('⚠️  Предупреждение: обнаружены незакоммиченные изменения');
    }
  } catch (error) {
    console.error('❌ Не удалось проверить статус git');
    process.exit(1);
  }

  console.log('✅ Проверки перед ревью пройдены');
}

preReview().catch(error => {
  console.error('Хук перед ревью завершился ошибкой:', error);
  process.exit(1);
});
