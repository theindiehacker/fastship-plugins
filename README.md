# claude-plugins

theindiehacker プロジェクト群で使う Claude Code プラグインのマーケットプレイスです。

## 使い方

```
/plugin marketplace add theindiehacker/claude-plugins
/plugin install <plugin-name>@theindiehacker
```

## プラグイン一覧

| プラグイン | 説明 |
| --- | --- |
| [fastmvp](plugins/fastmvp/) | fastmvp.jp の Claude Code 設定を移植。`aws` / `curl` / `python3` コマンドを自動承認する PreToolUse フックを提供する。 |

## リポジトリ構成

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json   # マーケットプレイスカタログ
└── plugins/
    └── fastmvp/           # 各プラグイン本体
```
