#!/usr/bin/env python3
import re
import sys


def analyze_code_metrics(code):
    """Анализирует код по основным метрикам."""

    # Считаем функции
    functions = len(re.findall(r"^def\s+\w+", code, re.MULTILINE))

    # Считаем классы
    classes = len(re.findall(r"^class\s+\w+", code, re.MULTILINE))

    # Средняя длина строки
    lines = code.split("\n")
    avg_length = sum(len(l) for l in lines) / len(lines) if lines else 0

    # Оценка сложности
    complexity = len(re.findall(r"\b(if|elif|else|for|while|and|or)\b", code))

    return {
        "functions": functions,
        "classes": classes,
        "avg_line_length": avg_length,
        "complexity_score": complexity,
    }


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        code = f.read()
    metrics = analyze_code_metrics(code)
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
