# 動画圧縮スクリプト

FFmpegとSVT-AV1コーデックを使用した動画圧縮用Pythonスクリプト。

## 機能

- **最大解像度**: 4K (3840x2160)
- **コーデック**: SVT-AV1（高速AV1コーデック）
- **CRF（品質）**: デフォルト25（0-63、低い値=高品質、高い値=小さいファイルサイズ）
- **オーディオコーデック**: AAC
- **オーディオビットレート**: 最大320kbps
- **最大FPS**: 120fps
- **進捗表示**: ETA、FPS、速度インジケーター付きのリアルタイムプログレスバー

## 前提条件

このスクリプトを使用するには、以下が必要です：

### FFmpegのインストール

**オプション1: システム全体へのインストール**

**Windows:**

1. [公式ウェブサイト](https://ffmpeg.org/download.html)からFFmpegをダウンロード
2. ディレクトリに展開して配置（例：`C:\ffmpeg`）
3. FFmpegのbinディレクトリをシステムPATHに追加（例：`C:\ffmpeg\bin`）
4. インストール確認: `ffmpeg -version` と `ffprobe -version`

**またはChocolateyを使用:**

```powershell
choco install ffmpeg
```

**またはwingetを使用:**

```powershell
winget install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

**オプション2: ローカルFFmpeg（ポータビリティ推奨）**

FFmpegの実行ファイルをスクリプトと同じディレクトリに配置できます：

- Windows: `ffmpeg.exe` と `ffprobe.exe`
- macOS/Linux: `ffmpeg` と `ffprobe`

スクリプトは、ローカルの実行ファイルが存在する場合、自動的に検出して使用します。

## 使用方法

### 基本的な使い方

```bash
python compress_video.py input_video.mp4
```

出力ファイルは自動的に `input_video_compressed.mp4` として作成されます。

### 出力ファイル名を指定

```bash
python compress_video.py input_video.mp4 -o output_video.mp4
```

### CRF値の変更（品質調整）

```bash
python compress_video.py input_video.mp4 --crf 23
```

- CRF 0-23: 高品質（ファイルサイズ大）
- CRF 25: デフォルト（品質とサイズのバランス）
- CRF 26-40: 中品質
- CRF 40-63: 低品質（ファイルサイズ小）

### オーディオビットレートの変更

```bash
python compress_video.py input_video.mp4 --audio-bitrate 256k
```

### オーディオを無効化

```bash
python compress_video.py input_video.mp4 --no-audio
```

### 解像度を制限

```bash
python compress_video.py input_video.mp4 --resolution 1920x1080
```

### FPSを制限

```bash
python compress_video.py input_video.mp4 --fps 30
```

### 全オプションの組み合わせ

```bash
python compress_video.py input_video.mp4 -o output_video.mp4 --crf 23 --audio-bitrate 256k --resolution 1920x1080 --fps 60
```

## オプション

| オプション | 説明 | デフォルト値 |
| - | - | - |
| `input` | 入力動画ファイルパス（必須） | - |
| `-o`, `--output` | 出力動画ファイルパス | `{入力ファイル名}_compressed.{拡張子}` |
| `--crf` | AV1 CRF値（0-63） | 25 |
| `--audio-bitrate` | オーディオビットレート（最大: 320k） | 192k |
| `--no-audio` | オーディオトラックを無効化 | オーディオ有効 |
| `--fps` | 最大FPS（最大: 120） | 元のFPS |
| `--resolution` | WxH形式の最大解像度（例: 1920x1080） | 3840x2160 |

## ヘルプ

```bash
python compress_video.py --help
```

## 機能詳細

### 解像度制限

- 元の動画が4K（3840x2160）を超える場合、アスペクト比を維持したまま縮小されます
- 解像度が制限内の場合、元の解像度が保持されます
- `--resolution`でカスタム解像度制限を設定できます

### FPS制限

- 元の動画のFPSが指定された最大値を超える場合、削減されます
- デフォルトの最大値は120fpsです
- FPSが制限内の場合、元のFPSが保持されます

### SVT-AV1コーデック

- Intelが開発した高速AV1エンコーダー
- libaom-av1と比較して10-100倍高速なエンコード
- 高い圧縮効率を持つ最新の動画圧縮規格
- CRFモードエンコード（品質ベースの可変ビットレート）
- 自動マルチスレッド対応

### オーディオ処理

- AAC形式に変換
- 最大320kbpsビットレート
- `--no-audio`で無効化可能

### 進捗表示

圧縮中、リアルタイムのプログレスバーが表示されます：

- ビジュアルバー付きの進捗パーセンテージ
- 現在時間 / 合計時間
- ETA（推定残り時間）
- エンコードFPS
- 速度倍率
- フレーム数

## 使用例

### 8K動画を4Kに圧縮

```bash
python compress_video.py 8k_video.mp4 -o compressed_4k.mp4
```

出力: 解像度は3840x2160以下に縮小されます

### Web用に圧縮（1080p、30fps）

```bash
python compress_video.py video.mp4 --resolution 1920x1080 --fps 30
```

### 高品質圧縮

```bash
python compress_video.py video.mp4 --crf 20 --audio-bitrate 320k
```

### ファイルサイズ優先

```bash
python compress_video.py video.mp4 --crf 35 --audio-bitrate 128k
```

### 動画のみ（オーディオなし）

```bash
python compress_video.py video.mp4 --no-audio
```

## 注意事項

- AV1エンコードはCPU負荷が高いため、高解像度動画の処理には時間がかかる場合があります
- エンコード中にCtrl+Cを押すと処理を中断できます
- 出力ファイルが既に存在する場合、上書きされます（`-y`オプション）

## トラブルシューティング

### `FFmpeg not found` エラー

- FFmpegが正しくインストールされていることを確認してください
- FFmpegがシステムPATHに含まれていることを確認してください
- または、`ffmpeg`と`ffprobe`の実行ファイルをスクリプトディレクトリに配置してください
- コマンドラインで `ffmpeg -version` を実行して確認してください

### 動画情報取得エラー

- 入力ファイルが存在することを確認してください
- ファイルが破損していないか確認してください
- ファイルが有効な動画形式であることを確認してください

### プログレスバーが表示されない

- プログレスバーには動画の長さ情報が必要です
- 一部の動画形式では長さのメタデータが提供されない場合があります
- 圧縮は正常に完了します

## ライセンス

このスクリプトは自由に使用、改変、配布できます。
