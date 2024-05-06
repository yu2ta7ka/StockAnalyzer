import yfinance as yf
import pandas as pd
import csv

def retrieve_ticker_info(symbol):
    try:
        ticker_info = yf.Ticker(symbol)
        return ticker_info
    except Exception as e:
        print(f"Error fetching ticker info for {symbol}: {e}")
        return None

def calc_debt_ratio(balance_sheet):
    # 負債を取得
    try:
        total_debt = balance_sheet.loc["Total Debt"].values.flatten().tolist()
    except KeyError:
        total_debt = balance_sheet.loc["Total Liabilities Net Minority Interest"].values.flatten().tolist()
    # 純資産を取得
    total_assets = balance_sheet.loc["Total Assets"].values.flatten().tolist()
    # 最新(2023-03-31)の負債比率を計算
    debt_ratio = total_debt[0] / total_assets[0]
    return round(debt_ratio * 100, 1)

def calc_profit_margin(financials):
    # 売上高を取得
    total_revenue = financials.loc["Total Revenue"].values.flatten().tolist()
    # 純利益を取得
    net_income = financials.loc["Net Income"].values.flatten().tolist()
    # 最新(2023-03-31)の純利益率を計算
    profit_margin = net_income[0] / total_revenue[0]
    return round(profit_margin * 100, 1)

def calc_current_ratio(balance_sheet):
    # 流動資産を取得
    cash_and_cash_equivalents = balance_sheet.loc["Current Assets"].values.flatten().tolist()
    # 流動(短期)負債を取得
    total_current_liabilities = balance_sheet.loc["Current Liabilities"].values.flatten().tolist()
    # 最新(2023-03-31)の流動比率を計算
    current_ratio = cash_and_cash_equivalents[0] / total_current_liabilities[0]
    return round(current_ratio, 1)

def main():
    # 銘柄コードを記述したファイルを読み込む
    with open("stock_code.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        rows = list(reader)

    # CSVファイルに出力するデータを格納するリスト
    output_data = []

    for row in rows:
        symbol = row[0] + ".T"
        company_name = row[1]
        
        # 銘柄のバランスシートを取得
        ticker_info = retrieve_ticker_info(symbol)
        
        debt_ratio = calc_debt_ratio(ticker_info.balance_sheet)
        current_ratio = calc_current_ratio(ticker_info.balance_sheet)
        profit_margin = calc_profit_margin(ticker_info.financials)
        output_data.append([symbol, company_name] + [debt_ratio] + [profit_margin] + [current_ratio])

    # CSVファイルに出力する
    with open("financial_soundness.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["銘柄コード","企業名","負債比率[%]","純利益率[%]", "流動比率[%]"])
        writer.writerows(output_data)

if __name__ == "__main__":
    main()
