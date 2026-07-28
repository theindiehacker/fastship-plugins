#!/usr/bin/env python3
"""aws / curl / python3 だけで構成された Bash コマンドを自動承認する PreToolUse フック。

fastmvp.jp の .claude/settings.local.json にあった許可ルールの移植:

    Bash(aws:*) / Bash(aws sts get-caller-identity:*) / Bash(curl:*) / Bash(python3:*)

プラグインは settings の permissions を配布できないため、同じ効果を
PreToolUse フックの permissionDecision: "allow" で再現している。

判定できないコマンドは何も出力せずに終了し、通常の許可フローに委ねる。
"""
import json
import shlex
import sys

ALLOWED_COMMANDS = ("aws", "curl", "python3")

# シェルの制御・リダイレクト演算子。これらでコマンド列を分割し、
# 分割後のすべてのコマンドが許可対象のときだけ承認する。
OPERATOR_CHARS = set("|&;()<>")


def split_segments(line):
    lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    current = []
    for token in lexer:
        if token and set(token) <= OPERATOR_CHARS:
            yield current
            current = []
        else:
            current.append(token)
    yield current


def is_allowed(command):
    # コマンド置換はトークン分割では安全に判定できないので許可フローに委ねる
    if "`" in command or "$(" in command:
        return False
    matched = False
    for line in command.splitlines():
        if not line.strip():
            continue
        try:
            for segment in split_segments(line):
                if not segment:
                    continue
                if segment[0] not in ALLOWED_COMMANDS:
                    return False
                matched = True
        except ValueError:
            return False
    return matched


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if not isinstance(command, str) or not is_allowed(command):
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "fastmvp プラグイン: aws / curl / python3 コマンドは自動承認",
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
