# Wikipedia Dataset Processing Tools

This directory contains tools for processing Wikipedia dumps for LLM training. The processing pipeline downloads Wikipedia dumps, converts them to a training-ready format, and removes duplicates.

## Directory Structure

```
wikipedia/
├── README.md          # This documentation
├── dedup.py          # Deduplication script
├── scripts/          # Shell scripts for processing
│   ├── english.sh    # English Wikipedia processing
│   └── japanese.sh   # Japanese Wikipedia processing
├── english/
│   └── run.py        # English processing implementation
└── japanese/
    └── run.py        # Japanese processing implementation
```

## Processing Pipeline

### 1. Wikipedia Dump Download and Processing

The `scripts/` directory contains shell scripts that:
1. Download Wikipedia enterprise HTML dumps from Wikimedia
2. Extract the compressed archives
3. Process the raw data into JSONL format suitable for LLM training

**English Wikipedia:**
```bash
bash scripts/english.sh
```

**Japanese Wikipedia:**
```bash
bash scripts/japanese.sh
```

### 2. Deduplication

After processing, the data may contain duplicate entries. Use the deduplication script to remove duplicates based on article titles:

```bash
python dedup.py --input-jsonl <input_file.jsonl> --output-jsonl <output_file.jsonl>
```

## Usage Instructions

1. **Run the processing scripts** to download and process Wikipedia dumps
2. **Apply deduplication** to remove duplicate articles from the processed data
3. The final output will be clean JSONL files ready for LLM training

## Output Format

The processed data is saved in JSONL format, where each line contains a JSON object with Wikipedia article information suitable for language model training.

---

# Wikipedia データセット処理ツール

このディレクトリには、LLM学習用のWikipediaダンプを処理するためのツールが含まれています。処理パイプラインは、Wikipediaダンプをダウンロードし、学習用フォーマットに変換し、重複を除去します。

## ディレクトリ構造

```
wikipedia/
├── README.md          # このドキュメント
├── dedup.py          # 重複除去スクリプト
├── scripts/          # 処理用シェルスクリプト
│   ├── english.sh    # 英語Wikipedia処理
│   └── japanese.sh   # 日本語Wikipedia処理
├── english/
│   └── run.py        # 英語処理実装
└── japanese/
    └── run.py        # 日本語処理実装
```

## 処理パイプライン

### 1. Wikipediaダンプのダウンロードと処理

`scripts/`ディレクトリのシェルスクリプトは以下を実行します：
1. WikimediaからWikipedia enterprise HTMLダンプをダウンロード
2. 圧縮アーカイブを展開
3. 生データをLLM学習に適したJSONL形式に処理

**英語Wikipedia:**
```bash
bash scripts/english.sh
```

**日本語Wikipedia:**
```bash
bash scripts/japanese.sh
```

### 2. 重複除去

処理後のデータには重複エントリが含まれている可能性があります。記事タイトルに基づいて重複を除去するには、重複除去スクリプトを使用してください：

```bash
python dedup.py --input-jsonl <input_file.jsonl> --output-jsonl <output_file.jsonl>
```

## 使用方法

1. **処理スクリプトを実行**してWikipediaダンプをダウンロード・処理
2. **重複除去を適用**して処理済みデータから重複記事を除去
3. 最終出力は、LLM学習の準備が整ったクリーンなJSONLファイルになります

## 出力形式

処理されたデータはJSONL形式で保存され、各行には言語モデル学習に適したWikipedia記事情報を含むJSONオブジェクトが含まれます。