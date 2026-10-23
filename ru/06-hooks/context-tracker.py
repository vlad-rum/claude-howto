#!/usr/bin/env python3
"""
Трекер использования контекста — считает расход токенов на запрос.

Использует UserPromptSubmit как хук «до сообщения» и Stop как хук «после ответа»,
чтобы посчитать дельту расхода токенов для каждого запроса.

Эта версия оценивает число токенов по символам (без зависимостей).
Для большей точности смотрите context-tracker-tiktoken.py.

Использование:
    Настройте оба хука на один и тот же скрипт:
    - UserPromptSubmit: сохраняет текущее число токенов
    - Stop: считает дельту и сообщает расход
"""
import json
import os
import sys
import tempfile

# Конфигурация
CONTEXT_LIMIT = 1000000  # 1M у Opus 5, Sonnet 5, Opus 4.8 и Sonnet 4.6; 200000 у Haiku 4.5 (подберите под свою модель)


def get_state_file(session_id: str) -> str:
    """Путь к временному файлу с числом токенов до сообщения, отдельно для каждой сессии."""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens_estimate(text: str) -> int:
    """
    Оценивает число токенов по приближению на основе символов.

    Берётся соотношение ~4 символа на токен: точность около 80–90%
    для английского текста. Для кода и текста не на английском точность ниже.
    """
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """Читает файл транскрипта и склеивает всё содержимое."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # Извлекаем текст из разных форматов сообщений
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """Хук до сообщения: сохранить текущее число токенов перед запросом."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens_estimate(transcript_content)

    # Сохраняем во временный файл для последующего сравнения
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """Хук после ответа: посчитать и сообщить дельту токенов."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens_estimate(transcript_content)

    # Загружаем число токенов до сообщения
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # Считаем дельту
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # Сообщаем расход (stderr, чтобы не мешать выводу хука)
    print(
        f"Контекст (оценка): ~{current_tokens:,} токенов "
        f"(использовано {percentage:.1f}%, осталось ~{remaining:,})",
        file=sys.stderr,
    )
    if delta_tokens > 0:
        print(f"Этот запрос: ~{delta_tokens:,} токенов", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
