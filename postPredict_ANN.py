#Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from pprint import pprint
# from sklearn.preprocessing import StandardScaler
# from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split as ttsplit
# from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
# from sklearn.linear_model import LinearRegression as LReg
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import cross_val_score, cross_validate
# from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense


class ANN_predict:
    def __init__(self, time_span):
        self.time_span = time_span
        self.dataset = pd.read_csv(r"C:\Users\shant\Documents\SteemJPython\dataSteemjAuto_v13.csv", encoding="ISO-8859-1")
        self.dataset = self.dataset.query('PPV>20 and PPV<300')
        print(self.dataset.shape)
        index_dict = {"15min": [9, 19, 25, 31], "30min": [10, 20, 26, 32], "1hr": [11, 21, 27, 33],
                      "2hr": [12, 22, 28, 34],
                      "4hr": [13, 23, 29, 35], "6hr": [13, 23, 30, 36]}
        self.index = [4, 5, 6, 7, 8, 15, 16, 17, 18] + index_dict[time_span]
        self.index.sort()
        self.X = self.dataset.iloc[:, self.index].values
        y = self.dataset.loc[:, 'PS 6hr'].values * 6
        self.y = y.reshape(len(y), 1)

        # Splitting dataset into Training set and Test set
        self.X_train, self.X_test, self.y_train, self.y_test = ttsplit(self.X, self.y, test_size=0.35, random_state=0)
        self.y_train = self.y_train.reshape(len(self.y_train), 1)
        self.y_test = self.y_test.reshape(len(self.y_test), 1)

        # Feature Scaling Data
        sc_X = MinMaxScaler()
        # sc_y = MinMaxScaler()
        self.X_train_scale = sc_X.fit_transform(self.X_train)
        self.X_test_scale = sc_X.transform(self.X_test)


    def ANN(self):
        model = Sequential()
        model.add(Dense(units=7, input_dim=13, activation='relu', kernel_initializer='normal'))
        # model.add(Dense(units=8, activation='relu', kernel_initializer='normal'))
        # model.add(Dense(units=6, activation='relu', kernel_initializer='normal'))
        # model.add(Dense(units=8, activation='relu', kernel_initializer='glorot_uniform'))
        model.add(Dense(units=1, activation='linear', kernel_initializer='normal'))
        # model.summary()
        model.compile(loss='mse', optimizer='adamax', metrics=['mse', 'mae'])
        return model

    def trainingANN(self, model, X_train_scale, y_train):
        """Fitting ANN to dataset"""
        regressor = model.fit(X_train_scale, y_train, epochs=1000, verbose=2, batch_size=10)
        # print(regressor.history.keys())
        """Summarising history of loss"""
        f = plt.figure()
        plt.plot(regressor.history['loss'])
        #         plt.plot(regressor.history['mean_absolute_error'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        #         plt.legend(['mse', 'mae'], loc='upper left')
        f.show()
        return model

    def ppv_predict(self):
        self.y_pred = self.model.predict(self.X_test_scale)
        self.errorNN = abs(self.y_test - self.y_pred)
        print(sum(self.errorNN) / len(self.y_test))

    def plot_prediction(self, X_test, y_test, y_pred):
        f = plt.figure()
        ppv = (X_test[:, 11] * 0.5).reshape(len(y_test), 1)
        diff_ppv = abs(y_pred - ppv)
        y_test_pred_diff = np.column_stack((ppv, y_test, y_pred, diff_ppv))
        y_test_pred_diff = y_test_pred_diff[y_test_pred_diff[:, 3] > 15]
        plt.scatter(y_test_pred_diff[:, 1], y_test_pred_diff[:, 2], c=y_test_pred_diff[:, 3], cmap='tab20c')
        plt.plot(y_test, y_test, color='green')
        plt.title('Neural Network (' + self.time_span + ')')
        plt.xlabel('Actual PPV ')
        plt.ylabel('Predicted PPV ')
        plt.colorbar()
        plt.xlim(0, y_test.max())
        plt.ylim(0, y_test.max())
        f.show()

    def driver_fn(self):
        self.model = self.ANN()
        self.model = self.trainingANN(self.model, self.X_train_scale, self.y_train)
        self.ppv_predict()
        self.plot_prediction(self.X_test, self.y_test, self.y_pred)
#obj = ANN_predict()
#obj.driver_fn()
