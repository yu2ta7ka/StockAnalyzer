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

def get_shares_outstanding(ticker):
    try:
        # 企業の情報を取得
        info = ticker.info
        # 発行済株式数を取得
        shares_outstanding = info.get("sharesOutstanding")
        if shares_outstanding is None:
            return f"Ticker {ticker} の発行済株式数(自社株除く)が見つかりませんでした。"
        else:
            return int(shares_outstanding)
    except Exception as e:
        return f"Error: {e}"

def get_recent_stock_price(ticker):
    try:
        # 直近の株価を取得
        stock_price = ticker.history(period="1d")["Close"].values[0]
        
        return int(stock_price)
    except Exception as e:
        return f"Error: {e}"

def get_period_stock_price(ticker, start_date, end_date):
    try:
        # 指定された期間の株価を取得
        stock_price = ticker.history(start=start_date,end = end_date)["Close"].values[0]
        
        return int(stock_price)
    except Exception as e:
        return f"Error: {e}"



def main():
    # 銘柄コードを記述したファイルを読み込む
    with open("stock_code.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        rows = list(reader)

    # 財務指標データを格納するリスト
    financial_metrics = []

    # 各銘柄コードについて財務指標データを取得し、リストに追加する
    for row in rows:
        symbol = row[0] + ".T"
        company_name = row[1]
        ticker_obj = get_ticker_object(symbol)
        market_cap = get_market_cap(ticker_obj)
        stock_price = get_period_stock_price(ticker_obj,"2024-01-04","2024-01-05")
        stock_price_recent = get_recent_stock_price(ticker_obj)
        shares_outstanding = get_shares_outstanding(ticker_obj)

        # 単位を億円に変換する
        market_cap_billion = int((market_cap / 10**8 )) if market_cap else None

        financial_metrics.append([symbol, company_name, market_cap_billion,stock_price,stock_price_recent,round((stock_price_recent / stock_price) * 100, 1),shares_outstanding])

    # 取得データをCSVファイルに出力する
    with open("financial_metrics.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["銘柄コード", "企業名", "時価総額[億円]（自己株除く）","年初株価[円]","直近株価[円]","騰落率[%]","発行済株式数(自己株除く)"])
        writer.writerows(financial_metrics)

if __name__ == "__main__":
    main()
