# 指示書

`README.md`の内容を`README.typ`に、`README.ja.md`の内容を`README.ja.typ`に反映してください。

Markdownファイル側の内容がマスター（正しい）です。Markdownファイルの差分を、対応するTypstファイルに反映してください。

## ヘッダー・フッター（Typstファイルの先頭に固定で配置）

```typst
#import "/.typst/A4-Ame-Serif.typ": *
#show: a4_ame_init
```

## タイトル直後の注記行

英語ファイル（`README.typ`）のタイトル直後の説明文の下に、以下の行を追加してください：

```typst
The latest information is described in the README.md file.
```

日本語ファイル（`README.ja.typ`）のタイトル直後の説明文の下に、以下の行を追加してください：

```typst
最新の内容はREADME.mdファイルに記載されています。
```

## 変換ルール

### ヘッダー

Markdownのヘッダー記号をTypstのヘッダー記号に変換してください。記号の数はそのまま維持します。

- `#` → `=`
- `##` → `==`
- `###` → `===`

（例: `## Features` → `== Features`）

### 太字

Markdownの太字 `**text**` をTypstの太字 `*text*` に変換してください。

（例: `**Maximum Resolution**` → `*Maximum Resolution*`）

### リンク

Markdownのリンク記法をTypstのリンク記法に変換してください。

- `[text](url)` → `#link("url")[text]`

（例: `[official website](https://ffmpeg.org/download.html)` → `#link("https://ffmpeg.org/download.html")[official website]`）

### 引用ブロック（Blockquote）

Markdownの引用ブロック `> text` をTypstの `#quote[...]` に変換してください。

- `> **Note**: text` → `#quote[\n  Note: text\n]`
- `> **注意**: text` → `#quote[\n  注意: text\n]`
- 太字のマーカー `**` は引用内でも `*` に変換してください

### テーブル

MarkdownのパイプテーブルをTypstの `#table(...)` に変換してください。

Markdownのテーブル例：

```markdown
| Option | Description | Default |
| - | - | - |
| `input` | Input file path | - |
```

Typstのテーブル形式：

```typst
#table(
  columns: (4fr, 6fr, 5fr),
  align: (left, left, left),
  stroke: none,
  table.hline(),
  [*Option*], [*Description*], [*Default*],
  table.hline(stroke: 0.5pt),
  [`input`], [Input file path], [-],
  table.hline(),
)
```

変換のポイント：

- ヘッダー行は太字 `*text*` で記述
- 各セルの内容は `[content]` でラップ
- インラインコードはそのままバッククォートを使用（例: `` `input` ``）
- `table.hline()` をテーブルの開始と終了に配置
- ヘッダーの下に `table.hline(stroke: 0.5pt)` を配置

### コードブロック

コードブロック `` ```bash ... ``` `` や `` ```powershell ... ``` `` などは、そのまま維持してください。変換不要です。

### インラインコード

バッククォート `` `code` `` はそのまま維持してください。変換不要です。

### 箇条書き

箇条書きの記号は `-` で統一してください。順序付きリスト（`1.`, `2.`）もそのまま維持してください。

### ページ区切り

主要セクション（`==` レベル）の前に `#pagebreak()` を挿入して、適切にページ分割してください。

ただし、最初のセクション（タイトル）の前には挿入しないでください。

現在のページ区切り位置を維持し、新しい `==` レベルのセクションが追加された場合のみ、適切にページ区切りを追加してください。

## 反映時の注意事項

- Typstファイルの構造（ページ区切り位置、テーブル形式など）は現在の形式を維持してください
- Markdown側で追加・変更・削除された内容のみを反映してください
- Markdownにない内容をTypstに追加しないでください（上記の注記行を除く）
- Typst固有のインポート・設定（`#import`, `#show`）は変更しないでください
- インラインコード内のテキストは変換しないでください
