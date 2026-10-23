#!/usr/bin/env python3
"""
Анализатор сложности кода

Считает метрики сложности для файлов Python, JavaScript и TypeScript.
Помогает измерить эффект рефакторинга, сравнивая метрики до и после.

Использование:
    python analyze-complexity.py <file>
    python analyze-complexity.py <before_file> <after_file>  # Режим сравнения
    python analyze-complexity.py --dir <directory>           # Анализ каталога

Метрики:
    - Цикломатическая сложность: точки ветвления в коде
    - Когнитивная сложность: насколько трудно понять код
    - Индекс сопровождаемости: общая оценка сопровождаемости (0–100)
    - Строки кода: общее число строк
    - Число функций: количество функций и методов
    - Средняя длина функции: строк на функцию
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class FunctionMetrics:
    """Метрики одной функции."""
    name: str
    start_line: int
    end_line: int
    lines: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    parameter_count: int


@dataclass
class FileMetrics:
    """Метрики файла."""
    filename: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    avg_function_length: float
    max_function_length: int
    functions: List[FunctionMetrics]


class ComplexityAnalyzer:
    """Анализ сложности кода для нескольких языков."""

    # Шаблоны для разных языков
    PATTERNS = {
        'python': {
            'function': r'^\s*def\s+(\w+)\s*\(',
            'class': r'^\s*class\s+(\w+)',
            'decision': [r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
                        r'\bexcept\b', r'\band\b(?!$)', r'\bor\b(?!$)',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*#',
            'multiline_comment_start': r'^\s*["\'][\"\'][\"\']',
            'multiline_comment_end': r'["\'][\"\'][\"\']',
        },
        'javascript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        },
        'typescript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        }
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.language = self._detect_language()
        self.patterns = self.PATTERNS.get(self.language, self.PATTERNS['python'])

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.code = f.read()
        self.lines = self.code.split('\n')

    def _detect_language(self) -> str:
        """Определить язык программирования по расширению файла."""
        ext = os.path.splitext(self.filepath)[1].lower()
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
        }
        return ext_map.get(ext, 'python')

    def calculate_cyclomatic_complexity(self, code: Optional[str] = None) -> int:
        """
        Вычислить цикломатическую сложность по методу Маккейба (McCabe).
        CC = E - N + 2P, где E — рёбра, N — узлы, P — компоненты связности
        Упрощённо: число точек ветвления + 1
        """
        if code is None:
            code = self.code

        complexity = 1  # Базовая сложность

        for pattern in self.patterns['decision']:
            matches = re.findall(pattern, code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self, code: Optional[str] = None) -> int:
        """
        Вычислить когнитивную сложность.
        Показывает, насколько трудно понять код.
        Учитывает глубину вложенности и разрывы потока управления.
        """
        if code is None:
            code = self.code

        lines = code.split('\n')
        cognitive = 0
        nesting_depth = 0
        in_function = False

        for line in lines:
            stripped = line.strip()

            # Отслеживание границ функций
            if re.search(self.patterns['function'], line):
                in_function = True
                nesting_depth = 0

            # Прирост за конструкции управления потоком
            if re.search(r'\b(if|for|while|switch)\b', stripped):
                nesting_depth += 1
                cognitive += nesting_depth  # Вложенные конструкции дороже

            elif re.search(r'\b(elif|else if|else|catch|finally)\b', stripped):
                cognitive += nesting_depth  # Тот же уровень, что у родителя

            # Отслеживание вложенности по скобкам и отступам
            if self.language in ['javascript', 'typescript']:
                nesting_depth += stripped.count('{') - stripped.count('}')
                nesting_depth = max(0, nesting_depth)

            # Надбавка за разрывы линейного потока
            if re.search(r'\b(break|continue|return|throw)\b', stripped):
                if nesting_depth > 1:
                    cognitive += 1

            # Надбавка за рекурсию
            # (упрощённо: просто ищем вызов функцией самой себя)

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        Вычислить индекс сопровождаемости (0–100).
        На основе объёма Холстеда (Halstead Volume), цикломатической сложности и числа строк кода.

        MI = max(0, (171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)) * 100/171)

        Интерпретация:
        - 85–100: высокая сопровождаемость
        - 65–84: умеренная сопровождаемость
        - 50–64: трудно сопровождать
        - 0–49: очень трудно сопровождать
        """
        import math

        loc = len([l for l in self.lines if l.strip()])
        cc = self.calculate_cyclomatic_complexity()

        # Упрощённое приближение объёма Холстеда (Halstead Volume)
        # Подсчёт уникальных операторов и операндов
        operators = len(re.findall(r'[+\-*/%=<>!&|^~]', self.code))
        operands = len(re.findall(r'\b\w+\b', self.code))
        volume = (operators + operands) * math.log2(max(1, operators + operands))

        # Вычисление MI
        mi = 171 - 5.2 * math.log(max(1, volume)) - 0.23 * cc - 16.2 * math.log(max(1, loc))
        mi = max(0, min(100, mi * 100 / 171))

        return round(mi, 2)

    def count_lines(self) -> Dict[str, int]:
        """Подсчитать разные виды строк."""
        total = len(self.lines)
        blank = 0
        comment = 0
        in_multiline_comment = False

        for line in self.lines:
            stripped = line.strip()

            # Проверка многострочных комментариев
            if re.search(self.patterns['multiline_comment_start'], stripped):
                in_multiline_comment = True
            if re.search(self.patterns['multiline_comment_end'], stripped):
                in_multiline_comment = False
                comment += 1
                continue

            if in_multiline_comment:
                comment += 1
            elif not stripped:
                blank += 1
            elif re.match(self.patterns['comment'], stripped):
                comment += 1

        return {
            'total': total,
            'blank': blank,
            'comment': comment,
            'code': total - blank - comment
        }

    def find_functions(self) -> List[FunctionMetrics]:
        """Найти все функции и посчитать их отдельные метрики."""
        functions = []
        current_function = None
        function_start = 0
        brace_depth = 0

        for i, line in enumerate(self.lines):
            # Проверка определения функции
            match = re.search(self.patterns['function'], line)
            if match:
                # Сохранить предыдущую функцию, если она есть
                if current_function:
                    func_code = '\n'.join(self.lines[function_start:i])
                    functions.append(self._create_function_metrics(
                        current_function, function_start, i - 1, func_code
                    ))

                current_function = match.group(1) or match.group(2) if match.lastindex and match.lastindex > 1 else match.group(1)
                function_start = i
                brace_depth = 0

            # Отслеживание скобок для JS/TS
            if self.language in ['javascript', 'typescript']:
                brace_depth += line.count('{') - line.count('}')

        # Не забыть последнюю функцию
        if current_function:
            func_code = '\n'.join(self.lines[function_start:])
            functions.append(self._create_function_metrics(
                current_function, function_start, len(self.lines) - 1, func_code
            ))

        return functions

    def _create_function_metrics(self, name: str, start: int, end: int, code: str) -> FunctionMetrics:
        """Собрать метрики одной функции."""
        lines = end - start + 1

        # Подсчёт параметров (упрощённо)
        param_match = re.search(r'\(([^)]*)\)', code.split('\n')[0])
        param_count = 0
        if param_match and param_match.group(1).strip():
            param_count = len([p for p in param_match.group(1).split(',') if p.strip()])

        return FunctionMetrics(
            name=name,
            start_line=start + 1,
            end_line=end + 1,
            lines=lines,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(code),
            cognitive_complexity=self.calculate_cognitive_complexity(code),
            parameter_count=param_count
        )

    def analyze(self) -> FileMetrics:
        """Выполнить полный анализ файла."""
        line_counts = self.count_lines()
        functions = self.find_functions()

        # Подсчёт классов
        class_count = len(re.findall(self.patterns['class'], self.code))

        # Вычисление средних
        func_lengths = [f.lines for f in functions] if functions else [0]
        avg_func_length = sum(func_lengths) / len(func_lengths)
        max_func_length = max(func_lengths)

        return FileMetrics(
            filename=self.filename,
            lines_of_code=line_counts['code'],
            blank_lines=line_counts['blank'],
            comment_lines=line_counts['comment'],
            function_count=len(functions),
            class_count=class_count,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(),
            cognitive_complexity=self.calculate_cognitive_complexity(),
            maintainability_index=self.calculate_maintainability_index(),
            avg_function_length=round(avg_func_length, 1),
            max_function_length=max_func_length,
            functions=functions
        )


def print_metrics(metrics: FileMetrics, verbose: bool = False) -> None:
    """Напечатать метрики в читаемом виде."""
    print("=" * 60)
    print(f"АНАЛИЗ СЛОЖНОСТИ КОДА: {metrics.filename}")
    print("=" * 60)

    print("\n📊 ОБЗОР")
    print("-" * 40)
    print(f"  Строк кода:                {metrics.lines_of_code}")
    print(f"  Пустых строк:              {metrics.blank_lines}")
    print(f"  Строк комментариев:        {metrics.comment_lines}")
    print(f"  Функций/методов:           {metrics.function_count}")
    print(f"  Классов:                   {metrics.class_count}")

    print("\n📈 МЕТРИКИ СЛОЖНОСТИ")
    print("-" * 40)
    print(f"  Цикломатическая сложность: {metrics.cyclomatic_complexity}")
    print(f"  Когнитивная сложность:     {metrics.cognitive_complexity}")
    print(f"  Индекс сопровождаемости:   {metrics.maintainability_index}")

    # Интерпретация сопровождаемости
    mi = metrics.maintainability_index
    if mi >= 85:
        mi_label = "Высокая сопровождаемость ✅"
    elif mi >= 65:
        mi_label = "Умеренная сопровождаемость 🔶"
    elif mi >= 50:
        mi_label = "Трудно сопровождать ⚠️"
    else:
        mi_label = "Очень трудно сопровождать ❌"
    print(f"    → {mi_label}")

    print("\n📐 МЕТРИКИ ФУНКЦИЙ")
    print("-" * 40)
    print(f"  Средняя длина функции:     {metrics.avg_function_length} строк")
    print(f"  Макс. длина функции:       {metrics.max_function_length} строк")

    if verbose and metrics.functions:
        print("\n📋 ПОДРОБНОСТИ ПО ФУНКЦИЯМ")
        print("-" * 40)
        for f in sorted(metrics.functions, key=lambda x: x.cyclomatic_complexity, reverse=True):
            flag = " ⚠️" if f.cyclomatic_complexity > 10 or f.lines > 50 else ""
            print(f"  {f.name}() [строки {f.start_line}-{f.end_line}]{flag}")
            print(f"    - Строк: {f.lines}, ЦС: {f.cyclomatic_complexity}, "
                  f"Когнитивная: {f.cognitive_complexity}, Параметров: {f.parameter_count}")

    print("\n" + "=" * 60)


def print_comparison(before: FileMetrics, after: FileMetrics) -> None:
    """Напечатать сравнение двух анализов."""
    print("=" * 70)
    print("СРАВНЕНИЕ СЛОЖНОСТИ КОДА")
    print("=" * 70)

    print(f"\n{'Метрика':<30} {'До':<15} {'После':<15} {'Изменение':<12}")
    print("-" * 70)

    def fmt_change(before_val, after_val, lower_is_better=True):
        diff = after_val - before_val
        if lower_is_better:
            symbol = "✅" if diff < 0 else ("⚠️" if diff > 0 else "➖")
        else:
            symbol = "✅" if diff > 0 else ("⚠️" if diff < 0 else "➖")
        return f"{diff:+.1f} {symbol}" if isinstance(diff, float) else f"{diff:+d} {symbol}"

    metrics = [
        ("Строк кода", before.lines_of_code, after.lines_of_code, True),
        ("Число функций", before.function_count, after.function_count, False),
        ("Число классов", before.class_count, after.class_count, False),
        ("Цикломатическая сложность", before.cyclomatic_complexity, after.cyclomatic_complexity, True),
        ("Когнитивная сложность", before.cognitive_complexity, after.cognitive_complexity, True),
        ("Индекс сопровождаемости", before.maintainability_index, after.maintainability_index, False),
        ("Средняя длина функции", before.avg_function_length, after.avg_function_length, True),
        ("Макс. длина функции", before.max_function_length, after.max_function_length, True),
    ]

    for name, b_val, a_val, lower_better in metrics:
        change = fmt_change(b_val, a_val, lower_better)
        print(f"{name:<30} {b_val:<15} {a_val:<15} {change:<12}")

    print("\n" + "=" * 70)

    # Общая оценка
    print("\n🎯 ОЦЕНКА")
    print("-" * 40)

    improvements = 0
    regressions = 0

    if after.maintainability_index > before.maintainability_index:
        print("  ✅ Сопровождаемость улучшилась")
        improvements += 1
    elif after.maintainability_index < before.maintainability_index:
        print("  ⚠️ Сопровождаемость снизилась")
        regressions += 1

    if after.cyclomatic_complexity < before.cyclomatic_complexity:
        print("  ✅ Сложность снизилась")
        improvements += 1
    elif after.cyclomatic_complexity > before.cyclomatic_complexity:
        print("  ⚠️ Сложность выросла")
        regressions += 1

    if after.avg_function_length < before.avg_function_length:
        print("  ✅ Функции в среднем стали короче")
        improvements += 1
    elif after.avg_function_length > before.avg_function_length:
        print("  ⚠️ Функции в среднем стали длиннее")
        regressions += 1

    print(f"\n  Итог: улучшений — {improvements}, регрессий — {regressions}")
    print("=" * 70)


def analyze_directory(directory: str, verbose: bool = False) -> None:
    """Проанализировать все поддерживаемые файлы в каталоге."""
    supported_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx']
    files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in supported_extensions):
                files.append(os.path.join(root, filename))

    if not files:
        print(f"В {directory} не найдено поддерживаемых файлов")
        return

    print(f"Анализ {len(files)} файлов в {directory}...\n")

    total_loc = 0
    total_cc = 0
    total_functions = 0
    all_metrics = []

    for filepath in sorted(files):
        try:
            analyzer = ComplexityAnalyzer(filepath)
            metrics = analyzer.analyze()
            all_metrics.append(metrics)

            total_loc += metrics.lines_of_code
            total_cc += metrics.cyclomatic_complexity
            total_functions += metrics.function_count

            if verbose:
                print_metrics(metrics, verbose=True)
            else:
                flag = " ⚠️" if metrics.maintainability_index < 65 else ""
                print(f"  {metrics.filename}: LOC={metrics.lines_of_code}, "
                      f"CC={metrics.cyclomatic_complexity}, MI={metrics.maintainability_index}{flag}")
        except Exception as e:
            print(f"  Ошибка анализа {filepath}: {e}")

    print("\n" + "=" * 60)
    print("ИТОГ")
    print("=" * 60)
    print(f"  Файлов проанализировано:  {len(all_metrics)}")
    print(f"  Всего строк кода:         {total_loc}")
    print(f"  Суммарная сложность:      {total_cc}")
    print(f"  Всего функций:            {total_functions}")

    if all_metrics:
        avg_mi = sum(m.maintainability_index for m in all_metrics) / len(all_metrics)
        print(f"  Средняя сопровождаемость: {avg_mi:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description='Анализ метрик сложности кода',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s myfile.py                    Анализ одного файла
  %(prog)s before.py after.py           Сравнение двух версий
  %(prog)s --dir src/                   Анализ каталога
  %(prog)s -v myfile.py                 Подробный вывод с деталями функций
        """
    )
    parser.add_argument('files', nargs='*', help='Файл(ы) для анализа')
    parser.add_argument('--dir', '-d', help='Каталог для анализа')
    parser.add_argument('--verbose', '-v', action='store_true', help='Показать подробные метрики функций')
    parser.add_argument('--json', '-j', action='store_true', help='Вывести в формате JSON')

    args = parser.parse_args()

    if args.dir:
        analyze_directory(args.dir, args.verbose)
    elif len(args.files) == 1:
        analyzer = ComplexityAnalyzer(args.files[0])
        metrics = analyzer.analyze()

        if args.json:
            import json
            print(json.dumps({
                'filename': metrics.filename,
                'lines_of_code': metrics.lines_of_code,
                'cyclomatic_complexity': metrics.cyclomatic_complexity,
                'cognitive_complexity': metrics.cognitive_complexity,
                'maintainability_index': metrics.maintainability_index,
                'function_count': metrics.function_count,
                'avg_function_length': metrics.avg_function_length,
            }, indent=2))
        else:
            print_metrics(metrics, args.verbose)
    elif len(args.files) == 2:
        before_analyzer = ComplexityAnalyzer(args.files[0])
        after_analyzer = ComplexityAnalyzer(args.files[1])
        before_metrics = before_analyzer.analyze()
        after_metrics = after_analyzer.analyze()
        print_comparison(before_metrics, after_metrics)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
