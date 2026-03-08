# Video Compression Script

FFmpegを使用した動画圧縮Pythonスクリプト

## 機能

- **最大解像度**: 2K (2560x1440) に制限
- **コーデック**: SVT-AV1 (高速AV1コーデック)
- **CRF (品質設定)**: デフォルト25 (0-63、低いほど高品質、高いほどファイルサイズ小)
- **音声コーデック**: MP3 (libmp3lame)
- **音声ビットレート**: 最大192kbps

## 前提条件

このスクリプトを使用するには、以下がインストールされている必要があります：

### FFmpegのインストール

**Windows:**

1. [FFmpeg公式サイト](https://ffmpeg.org/download.html)からFFmpegをダウンロード
2. 解凍して任意のディレクトリに配置（例: `C:\ffmpeg`）
3. システム環境変数のPATHにFFmpegのbinディレクトリを追加（例: `C:\ffmpeg\bin`）
4. インストールを確認: `ffmpeg -version` および `ffprobe -version`

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

## 使い方

### 基本的な使い方

```bash
python compress_video.py 入力動画.mp4
```

出力ファイルは `入力動画_compressed.mp4` として自動的に作成されます。

### 出力ファイル名を指定

```bash
python compress_video.py 入力動画.mp4 -o 出力動画.mp4
```

### CRF値を変更（品質調整）

```bash
python compress_video.py 入力動画.mp4 --crf 23
```

- CRF 0-23: 高品質（ファイルサイズ大）
- CRF 25: デフォルト（品質とサイズのバランス）
- CRF 26-40: 中程度の品質
- CRF 40-63: 低品質（ファイルサイズ小）

### 音声ビットレートを変更

```bash
python compress_video.py 入力動画.mp4 --audio-bitrate 256k
```

### 全てのオプションを指定

```bash
python compress_video.py 入力動画.mp4 -o 出力動画.mp4 --crf 23 --audio-bitrate 256k
```

## オプション

| オプション | 説明 | デフォルト値 |
| - | - | - |
| `input` | 入力動画ファイルのパス（必須） | - |
| `-o`, `--output` | 出力動画ファイルのパス | `{入力ファイル名}_compressed.{拡張子}` |
| `--crf` | AV1のCRF値 (0-63) | 25 |
| `--audio-bitrate` | 音声ビットレート | 192k |

## ヘルプ

```bash
python compress_video.py --help
```

## 機能の詳細

### 解像度制限

- 元動画の解像度が2K (2560x1440) を超えている場合、アスペクト比を維持したまま2K以下に縮小されます
- 解像度が2K以下の場合は、元の解像度が維持されます

### SVT-AV1コーデック

- Intelが開発した高速なAV1エンコーダー
- libaom-av1に比べて10-100倍の高速エンコードを実現
- 最新のビデオ圧縮規格で、高い圧縮率を維持
- CRFモードでエンコード（品質ベースの可変ビットレート）
- 自動マルチスレッド対応

### 音声処理

- MP3形式に変換（libmp3lameエンコーダー）
- 最大192kbpsまで設定可能

## 例

### 4K動画を圧縮

```bash
python compress_video.py 4k_video.mp4 -o compressed_2k.mp4
```

出力: 解像度が2560x1440以下に縮小されます

### 高品質圧縮

```bash
python compress_video.py video.mp4 --crf 20 --audio-bitrate 320k
```

### 小サイズ優先

```bash
python compress_video.py video.mp4 --crf 35 --audio-bitrate 192k
```

## 注意点

- AV1エンコードはCPU集約型のため、高解像度の動画では処理に時間がかかる場合があります
- エンコード中にCtrl+Cを押すと処理を中断できます
- 出力ファイルが既存の場合は、上書きされます（`-y`オプション）

## エラー対処

### `FFmpeg not found` エラー

- FFmpegが正しくインストールされているか確認してください
- システムのPATH環境変数にFFmpegが含まれているか確認してください
- コマンドラインで `ffmpeg -version` を実行して確認してください

### 動画情報の取得エラー

- 入力ファイルが存在するか確認してください
- ファイルが破損していないか確認してください

## ライセンス

このスクリプトは自由に使用、修正、配布できます。
