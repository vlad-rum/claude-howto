#!/usr/bin/env python3
"""
setup-auto-mode-permissions.py

Заполняет ~/.claude/settings.json консервативным базовым набором безопасных
разрешений для Claude Code. Набор по умолчанию рассчитан на чтение и локальный
осмотр; необязательные флаги расширяют список разрешений для правок, запуска
тестов, операций записи git, установки пакетов и записи через GitHub CLI.

Использование:
    python3 setup-auto-mode-permissions.py
    python3 setup-auto-mode-permissions.py --dry-run
    python3 setup-auto-mode-permissions.py --include-edits --include-tests
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Iterable

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

# Базовый набор: осмотр только для чтения и локальные команды оболочки с низким риском.
CORE_PERMISSIONS = [
    "Read(*)",
    "Grep(*)",
    "Agent(*)",
    "Skill(*)",
    "WebSearch(*)",
    "WebFetch(*)",
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(which:*)",
    "Bash(echo:*)",
    "Bash(cat:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(sort:*)",
    "Bash(uniq:*)",
    "Bash(find:*)",
    "Bash(dirname:*)",
    "Bash(basename:*)",
    "Bash(realpath:*)",
    "Bash(file:*)",
    "Bash(stat:*)",
    "Bash(diff:*)",
    "Bash(md5sum:*)",
    "Bash(sha256sum:*)",
    "Bash(date:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git branch:*)",
    "Bash(git show:*)",
    "Bash(git rev-parse:*)",
    "Bash(git remote -v:*)",
    "Bash(git remote get-url:*)",
    "Bash(git stash list:*)",
]

# Необязательно, но всё ещё локально: правки файлов и учёт задач.
EDITING_PERMISSIONS = [
    "Edit(*)",
    "TaskCreate(*)",
    "TaskUpdate(*)",
]

# Необязательные команды разработки и тестов. Они всё ещё могут выполнить произвольные
# скрипты проекта, поэтому оставьте их включаемыми явно, а не частью базового набора.
TEST_AND_BUILD_PERMISSIONS = [
    "Bash(npm test:*)",
    "Bash(cargo test:*)",
    "Bash(go test:*)",
    "Bash(pytest:*)",
    "Bash(python3 -m pytest:*)",
    "Bash(make:*)",
    "Bash(cmake:*)",
]

# Необязательные локальные операции записи git. Команды, переписывающие историю, не входят
# в базовый набор: ими легко злоупотребить.
GIT_WRITE_PERMISSIONS = [
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git switch:*)",
    "Bash(git stash:*)",
    "Bash(git tag:*)",
]

# Необязательные команды зависимостей и пакетов. Их намеренно нет в базовом наборе:
# они могут выполнить хуки проекта или скачать код.
PACKAGE_MANAGER_PERMISSIONS = [
    "Bash(npm ci:*)",
    "Bash(npm install:*)",
    "Bash(pip install:*)",
    "Bash(pip3 install:*)",
]

# Необязательный доступ на запись через GitHub CLI.
GITHUB_WRITE_PERMISSIONS = [
    "Bash(gh pr create:*)",
]

# Необязательный дополнительный доступ на чтение через GitHub CLI.
GITHUB_READ_PERMISSIONS = [
    "Bash(gh pr view:*)",
    "Bash(gh pr list:*)",
    "Bash(gh issue view:*)",
    "Bash(gh issue list:*)",
    "Bash(gh repo view:*)",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Заполнить настройки Claude Code консервативным базовым набором разрешений."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать правила, которые будут добавлены, не записывая settings.json",
    )
    parser.add_argument(
        "--include-edits",
        action="store_true",
        help="Добавить разрешения на правку файлов (Edit/TaskCreate/TaskUpdate)",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Добавить локальные команды сборки и тестов, например pytest, cargo test и make",
    )
    parser.add_argument(
        "--include-git-write",
        action="store_true",
        help="Добавить локальные команды изменения git, например add, commit, checkout и stash",
    )
    parser.add_argument(
        "--include-packages",
        action="store_true",
        help="Добавить команды установки пакетов, например npm ci, npm install и pip install",
    )
    parser.add_argument(
        "--include-gh-write",
        action="store_true",
        help="Добавить разрешения на запись GitHub CLI, например gh pr create",
    )
    parser.add_argument(
        "--include-gh-read",
        action="store_true",
        help="Добавить разрешения на чтение GitHub CLI, например gh pr view и gh repo view",
    )
    return parser.parse_args()


def load_settings(path: Path) -> dict:
    if not path.exists():
        return {}

    try:
        with path.open() as f:
            settings = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Некорректный JSON в {path}: {exc}") from exc

    if not isinstance(settings, dict):
        raise SystemExit(f"Ожидалось, что {path} содержит объект JSON.")

    return settings


def build_permissions(args: argparse.Namespace) -> list[str]:
    permissions = list(CORE_PERMISSIONS)

    if args.include_edits:
        permissions.extend(EDITING_PERMISSIONS)

    if args.include_tests:
        permissions.extend(TEST_AND_BUILD_PERMISSIONS)

    if args.include_git_write:
        permissions.extend(GIT_WRITE_PERMISSIONS)

    if args.include_packages:
        permissions.extend(PACKAGE_MANAGER_PERMISSIONS)

    if args.include_gh_write:
        permissions.extend(GITHUB_WRITE_PERMISSIONS)

    if args.include_gh_read:
        permissions.extend(GITHUB_READ_PERMISSIONS)

    return permissions


def append_unique(existing: list, new_items: Iterable[str]) -> list[str]:
    seen = set(existing)
    added: list[str] = []
    for item in new_items:
        if item not in seen:
            existing.append(item)
            seen.add(item)
            added.append(item)
    return added


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        delete=False,
    ) as tmp:
        json.dump(payload, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)

    tmp_path.replace(path)


def main() -> None:
    args = parse_args()
    permissions_to_add = build_permissions(args)

    settings = load_settings(SETTINGS_PATH)
    permissions = settings.setdefault("permissions", {})

    if not isinstance(permissions, dict):
        raise SystemExit("Ожидалось, что permissions — объект JSON.")

    allow = permissions.setdefault("allow", [])
    if not isinstance(allow, list):
        raise SystemExit("Ожидалось, что permissions.allow — массив JSON.")

    added = append_unique(allow, permissions_to_add)

    if not added:
        print("Добавлять нечего — все выбранные правила уже есть.")
        return

    print(f"{'Будет добавлено' if args.dry_run else 'Добавляется'} {len(added)} правил:")
    for rule in added:
        print(f"  + {rule}")

    if args.dry_run:
        print("\nПробный запуск — изменения не записаны.")
        return

    atomic_write_json(SETTINGS_PATH, settings)
    print(f"\nГотово. В {SETTINGS_PATH} добавлено правил: {len(added)}")


if __name__ == "__main__":
    main()
