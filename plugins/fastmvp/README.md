# FastMVP プラグイン

[fastmvp.jp](https://github.com/theindiehacker/fastmvp.jp) プロジェクトの `.claude/settings.local.json` にあった Claude Code 設定を、他のプロジェクトでも再利用できるようにプラグイン化したものです。

## 提供する機能

### コマンド自動承認フック(PreToolUse)

元の設定は以下の許可ルールでした。

```json
{
  "permissions": {
    "allow": [
      "Bash(aws:*)",
      "Bash(aws sts get-caller-identity:*)",
      "Bash(curl:*)",
      "Bash(python3:*)"
    ]
  }
}
```

Claude Code のプラグインは `permissions` 設定そのものを配布できないため、このプラグインでは同じ効果を **PreToolUse フック** で再現しています。Bash コマンドが `aws` / `curl` / `python3` **だけ** で構成されている場合に自動承認します。

## 安全側に倒す判定

`hooks/auto_approve.py` は以下のケースでは自動承認せず、通常の許可フロー(確認プロンプト)に委ねます。

- `&&` `||` `;` `|` などで連結された複合コマンドに、許可対象以外のコマンドが 1 つでも含まれる場合
- コマンド置換(`` ` `` や `$(...)`)を含む場合
- リダイレクトを含むなど、トークン分割で安全に判定できない場合

## インストール

```
/plugin marketplace add theindiehacker/claude-plugins
/plugin install fastmvp@theindiehacker
```

## 注意

このプラグインを有効にすると、有効化したすべてのプロジェクトで `aws` / `curl` / `python3` コマンドが確認なしで実行されます。信頼できるプロジェクトでのみ有効化してください。
