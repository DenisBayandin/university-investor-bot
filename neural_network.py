import tensorflow as tf
import numpy as np
import pandas as pd

from tensorflow import keras
from sklearn.metrics import mean_absolute_error, r2_score
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

from utils import create_training_array, plt, add_new_value_for_predict


def create_new_model(x_train):
    model = Sequential()  # Выбираем последовательную модель.

    model.add(LSTM(units=100, activation='tanh', return_sequences=True,
                   input_shape=(x_train.shape[1], 1)))  # Задаем архитектуру
    model.add(Dropout(0.2))

    model.add(LSTM(units=80, activation='tanh', return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=60, activation='tanh'))  # delete return_sequences parameter
    model.add(Dropout(0.2))

    model.add(Dense(units=1))  # layer output
    return model


def training_model(model, x_train, y_train, stock_abbreviature, epochs: int = 10):
    model.compile(optimizer='adam', loss='mean_absolute_error', metrics=[tf.keras.metrics.MeanAbsoluteError()])
    model.fit(x_train, y_train, epochs=epochs)
    model.save(f'models/{stock_abbreviature}_keras_model.keras')


def final_data(train_close, test_close, scaler):
    past_100_days = pd.DataFrame(train_close[-100:])
    test_df = pd.DataFrame(test_close)
    final_df = pd.concat([past_100_days, test_df], ignore_index=True)
    return scaler.fit_transform(final_df)


def data_for_training_model(data):
    return create_training_array(data)


def testing_predict_data(model, scaler):
    x_test, y_test = data_for_training_model(final_data())
    y_pred = model.predict(x_test)
    scale_factor = 1 / scaler.scale_[0]
    return y_pred * scale_factor, y_test * scale_factor


def graph_for_test_and_predict_data(data_for_graph=None, model=None):  # График тестовых данных и предикта
    y_pred, y_test = testing_predict_data(model) if model else data_for_graph
    plt.figure(figsize=(12, 6))
    plt.plot(y_test, 'b', label="Original Price")
    plt.plot(y_pred, 'r', label="Predicted Price")
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()


def calculation_r2(data_for_graph=None, model=None):  # Расчет оценки R2
    y_pred, y_test = testing_predict_data(model) if model else data_for_graph
    actual = y_test
    predicted = y_pred
    r2 = r2_score(actual, predicted)
    plt.scatter(actual, predicted)
    plt.plot([min(actual), max(actual)], [min(predicted), max(predicted)], 'r--')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(f'R2 Score: {r2:.2f}')
    plt.show()


def predict_value(model, train_close, test_close, scaler, number_of_values: int, values_pre_prediction: list = [0]):
    past_100_days = pd.DataFrame(train_close[-100:])
    test_df = pd.DataFrame(test_close)
    final_data = add_new_value_for_predict(past_100_days, test_df, values_pre_prediction, number_of_values)
    input_data = scaler.fit_transform(final_data)
    x_data_for_predict, y_test = create_training_array(input_data)
    predict = model.predict(x_data_for_predict)
    scale_factor = 1 / scaler.scale_[0]
    x_data_for_predict_after_scale = predict * scale_factor
    # calculation_r2(data_for_graph=(x_data_for_predict_after_scale, y_test * scale_factor))
    # graph_for_test_and_predict_data(data_for_graph=(x_data_for_predict_after_scale, y_test * scale_factor))
    return x_data_for_predict_after_scale[len(x_data_for_predict_after_scale) - 1][0]


def load_custom_model(path):
    return keras.models.load_model(path)


def create_and_testing_model():
    model = create_new_model()
    training_model(model, epochs=15)
    graph_for_test_and_predict_data(model=model)
    calculation_r2(model=model)


def get_preidict_by_ready_model(stock_abbreviation, train_close, test_close, scaler, number_of_values: int):
    if number_of_values == 1:
        model = load_custom_model(f"models/{stock_abbreviation}_keras_model.keras")
        return predict_value(model, train_close, test_close, scaler, number_of_values=number_of_values)
    else:
        predict_values = []
        for value in range(0, number_of_values):
            model = load_custom_model(f"models/{stock_abbreviation}_keras_model.keras")
            predict_values.append(predict_value(model, train_close, test_close, scaler,
                                                number_of_values=value,
                                                values_pre_prediction=predict_values))
        return predict_values




# from tinkoff_data import x_train, y_train, STOCK
# model = create_new_model(x_train=x_train)
# training_model(model=model, x_train=x_train, y_train=y_train, stock_abbreviature=STOCK)
