#!/usr/bin/env python3
"""
Сравнивает цикломатическую сложность кода до и после изменений.
Помогает понять, действительно ли рефакторинг упрощает структуру кода.
"""

import re
import sys


class ComplexityAnalyzer:
    """Анализирует метрики сложности кода."""

    def __init__(self, code: str):
        self.code = code
        self.lines = code.split("\n")

    def calculate_cyclomatic_complexity(self) -> int:
        """
        Считает цикломатическую сложность по методу Маккейба.
        Считает точки решения: if, elif, else, for, while, except, and, or
        """
        complexity = 1  # Базовая сложность

        # Считаем точки решения
        decision_patterns = [
            r"\bif\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bexcept\b",
            r"\band\b(?!$)",
            r"\bor\b(?!$)",
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, self.code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self) -> int:
        """
        Считает когнитивную сложность: насколько трудно понять код.
        Опирается на глубину вложенности и поток управления.
        """
        cognitive = 0
        nesting_depth = 0

        for line in self.lines:
            # Отслеживаем глубину вложенности
            if re.search(r"^\s*(if|for|while|def|class|try)\b", line):
                nesting_depth += 1
                cognitive += nesting_depth
            elif re.search(r"^\s*(elif|else|except|finally)\b", line):
                cognitive += nesting_depth

            # Уменьшаем вложенность при возврате к нулевому отступу
            if line and not line[0].isspace():
                nesting_depth = 0

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        Индекс сопровождаемости от 0 до 100.
        > 85: отлично
        > 65: хорошо
        > 50: удовлетворительно
        < 50: плохо
        """
        lines = len(self.lines)
        cyclomatic = self.calculate_cyclomatic_complexity()
        cognitive = self.calculate_cognitive_complexity()

        # Упрощённый расчёт индекса сопровождаемости (MI)
        mi = (
            171
            - 5.2 * (cyclomatic / lines)
            - 0.23 * (cognitive)
            - 16.2 * (lines / 1000)
        )

        return max(0, min(100, mi))

    def get_complexity_report(self) -> dict:
        """Формирует полный отчёт о сложности."""
        return {
            "cyclomatic_complexity": self.calculate_cyclomatic_complexity(),
            "cognitive_complexity": self.calculate_cognitive_complexity(),
            "maintainability_index": round(self.calculate_maintainability_index(), 2),
            "lines_of_code": len(self.lines),
            "avg_line_length": round(
                sum(len(l) for l in self.lines) / len(self.lines), 2
            )
            if self.lines
            else 0,
        }


def compare_files(before_file: str, after_file: str) -> None:
    """Сравнивает метрики сложности двух версий кода."""

    with open(before_file) as f:
        before_code = f.read()

    with open(after_file) as f:
        after_code = f.read()

    before_analyzer = ComplexityAnalyzer(before_code)
    after_analyzer = ComplexityAnalyzer(after_code)

    before_metrics = before_analyzer.get_complexity_report()
    after_metrics = after_analyzer.get_complexity_report()

    print("=" * 60)
    print("СРАВНЕНИЕ СЛОЖНОСТИ КОДА")
    print("=" * 60)

    print("\nДО:")
    print(f"  Цикломатическая сложность: {before_metrics['cyclomatic_complexity']}")
    print(f"  Когнитивная сложность:     {before_metrics['cognitive_complexity']}")
    print(f"  Индекс сопровождаемости:   {before_metrics['maintainability_index']}")
    print(f"  Строк кода:                {before_metrics['lines_of_code']}")
    print(f"  Средняя длина строки:      {before_metrics['avg_line_length']}")

    print("\nПОСЛЕ:")
    print(f"  Цикломатическая сложность: {after_metrics['cyclomatic_complexity']}")
    print(f"  Когнитивная сложность:     {after_metrics['cognitive_complexity']}")
    print(f"  Индекс сопровождаемости:   {after_metrics['maintainability_index']}")
    print(f"  Строк кода:                {after_metrics['lines_of_code']}")
    print(f"  Средняя длина строки:      {after_metrics['avg_line_length']}")

    print("\nИЗМЕНЕНИЯ:")
    cyclomatic_change = (
        after_metrics["cyclomatic_complexity"] - before_metrics["cyclomatic_complexity"]
    )
    cognitive_change = (
        after_metrics["cognitive_complexity"] - before_metrics["cognitive_complexity"]
    )
    mi_change = (
        after_metrics["maintainability_index"] - before_metrics["maintainability_index"]
    )
    loc_change = after_metrics["lines_of_code"] - before_metrics["lines_of_code"]

    print(f"  Цикломатическая сложность: {cyclomatic_change:+d}")
    print(f"  Когнитивная сложность:     {cognitive_change:+d}")
    print(f"  Индекс сопровождаемости:   {mi_change:+.2f}")
    print(f"  Строк кода:                {loc_change:+d}")

    print("\nОЦЕНКА:")
    if mi_change > 0:
        print("  ✅ Код СТАЛ более сопровождаемым")
    elif mi_change < 0:
        print("  ⚠️  Код СТАЛ менее сопровождаемым")
    else:
        print("  ➡️  Сопровождаемость не изменилась")

    if cyclomatic_change < 0:
        print("  ✅ Сложность СНИЗИЛАСЬ")
    elif cyclomatic_change > 0:
        print("  ⚠️  Сложность ВЫРОСЛА")
    else:
        print("  ➡️  Сложность не изменилась")

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python compare-complexity.py <before_file> <after_file>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
