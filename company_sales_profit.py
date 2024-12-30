import yfinance as yf
import pandas as pd
import csv
from datetime import datetime

def get_financials(symbol):
    try:
        ticker_info = yf.Ticker(symbol)
        balance_sheet_df = ticker_info.financials
        return balance_sheet_df
    except Exception as e:
        print(f"Error fetching financial data for {symbol}: {e}")
        return None

def generate_headers(years, suffix):
    return [f"{year}-03-31{suffix}" for year in years]

# ヘッダー行の生成
def create_header_sales_profit_records():
    header = ["銘柄コード", "企業名"]
    # 現在の年から過去3年分の年リストを生成
    years = [datetime.now().year - i for i in range(3)]
    header += generate_headers(years, "売上")
    header += generate_headers(years, "純利益")

    return header

def main():
    # 銘柄コードを記述したファイルを読み込む
    with open("stock_code.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        rows = list(reader)

    # CSVファイルに出力するデータを格納するリスト
    output_data = []

    # 各銘柄コードについて売上と利益に関するレコードを取得し、リストに追加する
    for row in rows:
        symbol = row[0] + ".T"
        company_name = row[1]
        
        # 銘柄に関する売上と利益に関するレコードを取得
        print(symbol)
        financials_df = get_financials(symbol)
        #print(financials_df)
        if financials_df is not None:
            # 売上と利益に関する3年分のレコードを抽出
            sales_profit_record = financials_df.loc[['Total Revenue', 'Net Income']].iloc[:, :3]
            # NaN列を削除
            #sales_profit_record = sales_profit_record.dropna(axis=1, how='all')
            # 売上と利益の単位を「円」から「百万円」に変換
            sales_profit_record = sales_profit_record / 1000000
            #print(sales_profit_record)
            # 銘柄コード、企業名、売上と利益に関するレコードをリストに追加
            output_data.append([symbol, company_name] + sales_profit_record.values.flatten().tolist())

    # 売上と利益に関するデータをCSVファイルに出力する
    with open("sales_profit_records.csv", "w", newline="") as file:
        writer = csv.writer(file)
        header = create_header_sales_profit_records()

        writer.writerow(header)
        writer.writerows(output_data)


if __name__ == "__main__":
    main()
