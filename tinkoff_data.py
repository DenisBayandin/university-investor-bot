import numpy as np

from datetime import timedelta, date
from sklearn.preprocessing import MinMaxScaler

from utils import *
from tinkoff_handler import *
from config import tinkoff_token
from neural_network import get_preidict_by_ready_model, create_and_testing_model


START = "2010-01-01"
STOCKS_NAME = {
    "Global Payments": "GPN",  # figi='BBG000CX0P89', ticker='GPN', class_code='SPBXM', isin='US37940X1028',
    "TPI Composites Inc": "TPIC",  # figi='BBG0016MQ7C5', ticker='TPIC', class_code='SPBXM', isin='US87266J1043',
    "Vuzix Corp": "VUZI"  # figi='BBG000QKVV49', ticker='VUZI', class_code='SPBXM', isin='US92921W3007',
}
STOCKS_DATA = {
    "GPN": {"isin": "US37940X1028", "class_code": "SPBXM"},
    "TPIC": {"isin": "US87266J1043", "class_code": "SPBXM"},
    "VUZI": {"isin": "US92921W3007", "class_code": "SPBXM"}
}


def get_prediction(stock_abbreviation, number_of_values: int):
    with Client(tinkoff_token) as client:
        info_about_stock = TinkoffHandler(client=client).get_data_by_stock(id_stock=STOCKS_DATA[stock_abbreviation]["isin"],
                                                                           class_code=STOCKS_DATA[stock_abbreviation]["class_code"])
        stock_abbreviature = STOCKS_NAME[info_about_stock.instrument.name]
        data = load_data(stock_abbreviature, start_date=START)
        #  Разделение датасета на данные для обучения и теста модели
        train = create_train_data(data)
        test = create_test_data(data)

        #  Применяем MinMaxScaler для нормализации данных
        scaler = MinMaxScaler(feature_range=(0, 1))
        train_close = train.iloc[:, 4:5].values  # Взять все данные, и взять один лишь столбец - 'Close'
        test_close = test.iloc[:, 4:5].values  # Взять все данные, и взять один лишь столбец - 'Close'
        training_array = scaler.fit_transform(train_close)

        # Подготовка данных для тренировки
        x_train, y_train = create_training_array(training_array)
        return get_preidict_by_ready_model(stock_abbreviation, train_close,
                                           test_close, scaler, number_of_values=number_of_values)


# STOCK = "VUZI"
# with Client(tinkoff_token) as client:
#     info_about_stock = TinkoffHandler(client=client).get_data_by_stock(id_stock=STOCKS_DATA[STOCK]["isin"],
#                                                                        class_code=STOCKS_DATA[STOCK]["class_code"])
#
# #  Визуализируем цену закрытия
# stock_abbreviature = STOCKS_NAME[info_about_stock.instrument.name]
# data = load_data(stock_abbreviature, start_date=START)
#
# #  Рисуем 100 дневную скользящую среднюю
# ma100 = data.Close.rolling(100).mean()
# # show_graph(
# #     data=data['Close'],
# #     name_graph="Global Payments Stock Price",
# #     name_for_x_label="Date",
# #     name_for_y_label=f"Price ({info_about_stock.instrument.currency.upper()})",
# #     new_data=[ma100],
# #     new_color=["r"]
# # )
# ma200 = data.Close.rolling(200).mean()
# # show_graph(
# #     data=data['Close'],
# #     name_graph="Global Payments Stock Price",
# #     name_for_x_label="Date",
# #     name_for_y_label=f"Price ({info_about_stock.instrument.currency.upper()})",
# #     new_data=[ma100, ma200],
# #     new_color=["r", "g"]
# # )
#
# #  Разделение датасета на данные для обучения и теста модели
# train = create_train_data(data)
# test = create_test_data(data)
#
# #  Применяем MinMaxScaler для нормализации данных
# scaler = MinMaxScaler(feature_range=(0, 1))
# train_close = train.iloc[:, 4:5].values  # Взять все данные, и взять один лишь столбец - 'Close'
# test_close = test.iloc[:, 4:5].values  # Взять все данные, и взять один лишь столбец - 'Close'
# training_array = scaler.fit_transform(train_close)
#
#
# # Подготовка данных для тренировки
# x_train, y_train = create_training_array(training_array)



