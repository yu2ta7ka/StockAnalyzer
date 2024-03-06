# StockAnalyzer
株式情報を取得、加工などします。

# yfinanceのインストール
株式情報は[yfinance](https://pypi.org/project/yfinance/)を利用して、取得します。
```
pip install yfinance --upgrade --no-cache-dir
```
# 使い方
1. stock_code.csvに銘柄コードと企業名を記述します。
2. fetch_financial_metrics.pyを実行します。
```
python3 fetch_financial_metrics.py
```
3. market_cap.csvに時価総額が出力されます。

