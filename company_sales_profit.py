import yfinance as yf
import pandas as pd
import csv

def get_financials(symbol):
    try:
        ticker_info = yf.Ticker(symbol)
        balance_sheet_df = ticker_info.financials
        return balance_sheet_df
    except Exception as e:
        print(f"Error fetching financial data for {symbol}: {e}")
        return None

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
        if financials_df is not None:
            # 売上と利益に関するレコードを抽出
            sales_profit_record = financials_df.loc[['Total Revenue', 'Net Income']]
            # 銘柄コード、企業名、売上と利益に関するレコードをリストに追加
            output_data.append([symbol, company_name] + sales_profit_record.values.flatten().tolist())

    # 売上と利益に関するデータをCSVファイルに出力する
    with open("sales_profit_records.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["銘柄コード","企業名","2023-03-31売上","純利益","2022-03-31売上","純利益","2021-03-31売上","純利益","2020-03-31売上","純利益"])
        writer.writerows(output_data)

if __name__ == "__main__":
    main()
