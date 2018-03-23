import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style


def load_data(filename, sequence_length):
    style.use('ggplot')

    # Read the data file
    df = pd.read_csv(filename, index_col=0)
    print(df.head())
    df.index = pd.to_datetime(df.index.values, unit='s')
    # idx, Timestamp,Open,High,Low,Close,Volume_(BTC),Volume_(Currency),Weighted_Price
    print(df.index[0], df.index[-1])
#    df = df[-15000:]
#    df.to_csv('last15000.csv')
    df['500ma'] = df['Weighted_Price'].rolling(window=500, min_periods=0).mean()
    df['1200ma'] = df['Weighted_Price'].rolling(window=1200, min_periods=0).mean()
    df['buy'] = df['500ma'] - df['1200ma']

    ax1 = plt.subplot2grid((7, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((7, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['Weighted_Price'])
    ax1.plot(df.index, df['500ma'])
    ax1.plot(df.index, df['1200ma'])
    ax2.plot(df.index, df['buy'])

    plt.show()



    # Convert the file to a list
#    print('Replacing N/A and Zeroes')
    #raw_data = raw_data[['Timestamp', 'Weighted_Price']]
#    raw_data[["Open","High","Low","Close","Volume_(BTC)","Volume_(Currency)","Weighted_Price"]].fillna(method='ffill', inplace=True)
#    raw_data[["Open","High","Low","Close","Volume_(BTC)","Volume_(Currency)","Weighted_Price"]].replace(to_replace=0, method='ffill', inplace=True)
#    print(raw_data.head())
#    raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], unit='s')
#    print(raw_data['Timestamp'].head())
#    print(raw_data['Timestamp'].tail())

"""
    data = raw_data.values

    print('replacement done')

    # Convert the data to a 3D array (a x b x c)
    # Where a is the number of days, b is the window size, and c is the number of features in the data file
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    # Normalizing data by going through each window
    # Every value in the window is divided by the first value in the window, and then 1 is subtracted
    d0 = np.array(result)
    dr = np.zeros_like(d0)
    dr[1:, 1:, :] = d0[1:, 1:, :] / d0[1:, 0:1, :] - 1

    # Keeping the unnormalized prices for Y_test
    # Useful when graphing bitcoin price over time later
    start = 2400
    end = int(dr.shape[0] + 1)
    print("d0.shape", d0.shape, start, end)
#    unnormalized_bases = d0[start:end, 0:1, 20]
    unnormalized_bases = d0[start:end, 0:1, price_idx]

    # Splitting data set into training (First 90% of data points) and testing data (last 10% of data points)
    split_line = round(0.9 * dr.shape[0])
    training_data = dr[:int(split_line), :]

    # Shuffle the data
    np.random.shuffle(training_data)

    # Training Data
    X_train = training_data[:, :-1]
    Y_train = training_data[:, -1]
    Y_train = Y_train[:, price_idx]

    # Testing data
    X_test = dr[int(split_line):, :-1]
    Y_test = dr[int(split_line):, 49, :]
    Y_test = Y_test[:, price_idx]

    # Get the day before Y_test's price
    Y_daybefore = dr[int(split_line):, 48, :]
    Y_daybefore = Y_daybefore[:, price_idx]

    # Get window size and sequence length
    sequence_length = sequence_length
    window_size = sequence_length - 1  # because the last value is reserved as the y value
    return X_train, Y_train, X_test, Y_test, Y_daybefore, unnormalized_bases, window_size
"""

#X_train, Y_train, X_test, Y_test, Y_daybefore, unnormalized_bases, window_size = \
#load_data('last15000.csv', 50)
load_data('bitcoin.csv', 50)