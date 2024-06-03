import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

from datetime import date


def show_graph(data, name_graph: str, name_for_x_label: str, name_for_y_label: str,
               new_data: list, new_color: list):
    plt.figure(figsize=(12, 6))
    plt.plot(data)
    # for parameter, data_params in zip(new_parameters, data_for_parameters):
    for new_data_object, color in zip(new_data, new_color):
        plt.plot(new_data_object, color)
    plt.title(name_graph)
    plt.xlabel(name_for_x_label)
    plt.ylabel(name_for_y_label)
    plt.grid(True)
    plt.show()


def load_data(ticker: str, start_date: str, today_date: date = date.today().strftime("%Y-%m-%d")):
    data = yf.download(ticker, start_date, today_date)
    data.reset_index(inplace=True)
    return data


def create_test_data(data):
    return pd.DataFrame(data[int(len(data)*0.70): int(len(data))])


def create_train_data(data):
    return pd.DataFrame(data[0:int(len(data)*0.70)])


def create_training_array(data):
    x_train = []
    y_train = []
    for i in range(100, data.shape[0]):
        x_train.append(data[i - 100: i])
        y_train.append(data[i, 0])
    return np.array(x_train), np.array(y_train)


def add_new_value_for_predict(x, y, z, number_of_values):
    z = [[z[i]] for i in range(0, number_of_values) if number_of_values != 0]
    z = z + [[0]]
    return pd.concat([x, y, pd.DataFrame(np.array(z))], ignore_index=True)
