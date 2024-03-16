import yfinance as yf
import csv

def get_ticker_object(symbol):
    try:
        # Tickerオブジェクトを作成して返す
        ticker = yf.Ticker(symbol)
        return ticker
    except Exception as e:
        return f"Error: {e}"

def get_market_cap(ticker):
    try:
        # 企業の情報を取得
        info = ticker.info
        # 時価総額を取得
        market_cap = info.get("marketCap")
        if market_cap is None:
            return f"Ticker {ticker} の時価総額が見つかりませんでした。"
        else:
            return int(market_cap)
    except Exception as e:
        return f"Error: {e}"

def get_stock_price(ticker, date="2024-01-01"):
    try:
        # 指定された日付の株価を取得→とれていない。。
        stock_price = ticker.history(start=date, end=date)["Close"].values[0]
        return int(stock_price)
    except Exception as e:
        return f"Error: {e}"



def main():
    # 銘柄コードを記述したファイルを読み込む
    with open("stock_code.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        rows = list(reader)

    # 時価総額を格納するリスト
    market_caps = []

    # 各銘柄コードについて時価総額を取得し、リストに追加する
    for row in rows:
        symbol = row[0] + ".T"
        company_name = row[1]
        ticker_obj = get_ticker_object(symbol)
        market_cap = get_market_cap(ticker_obj)
        stock_price = get_stock_price(ticker_obj)
        # 単位を億円に変換する
        market_cap_billion = market_cap / 10**8 if market_cap else None

        market_caps.append([symbol, company_name, market_cap_billion,stock_price])


    # 時価総額をCSVファイルに出力する
    with open("market_cap.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["銘柄コード", "企業名", "時価総額[億円]","株価[円]"])
        writer.writerows(market_caps)

if __name__ == "__main__":
    main()
