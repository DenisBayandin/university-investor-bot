from tinkoff.invest import Client, InstrumentIdType, CandleInterval
from tinkoff.invest.schemas import CandleSource
from tinkoff.invest.utils import now
from datetime import datetime, timedelta


class TinkoffHandler:
    def __init__(self, client: Client):
        self.client = client

    def get_stocks(self, use_convenient_format_output: bool, show_all_info: bool = True):
        if use_convenient_format_output:
            from pprint import pprint
            pprint(self.client.instruments.shares())
        return self.client.instruments.shares()

    def get_data_by_stock(self, id_stock: str, class_code: str):
        return self.client.instruments.share_by(id=id_stock, class_code=class_code, id_type=InstrumentIdType(1))

    def get_candles(self,
                    figi: str,
                    interval: CandleInterval = CandleInterval.CANDLE_INTERVAL_DAY,
                    begin_date: datetime = now() - timedelta(days=20),
                    candle_source: CandleSource = CandleSource.CANDLE_SOURCE_UNSPECIFIED):
        return self.client.get_all_candles(figi="BBG004730N88",
                                           from_=begin_date,
                                           interval=interval,
                                           candle_source_type=candle_source)
