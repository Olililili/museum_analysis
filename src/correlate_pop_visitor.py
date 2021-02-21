import numpy as np

from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from src.log_handler import get_logger

log = get_logger()


def correlate_population_visitors(museum_all_data_df):
    # Split the dataset into traning dataset(70%) and test dataset(30%) randomly
    log.info('Start to prepare training and testing dataset for linear regression model... ')
    log.info('Splitting the dataset into 70% training set and 30% testing set...')
    x_train, x_test, y_train, y_test = prepare_train_test_set(museum_all_data_df)

    # Build the linear regression model
    log.info('Building linear regression model...')
    model = build_linear_reg_model(x_train, y_train)

    # Calculate the model's coefficient(slope) and intercept
    log.info('''Calculating the model's coefficient(slope) and intercept...''')
    linear_reg_coef, linear_reg_intercept = calculate_coefficient_and_intercept(model)
    log.info(f'''The model's linear regression coefficient and intercept are:\n '''
             f'Coefficient: {linear_reg_coef}\n '
             f'Intercept: {linear_reg_intercept}')

    # Calculate Pearson's correlation coefficient from linear regression coefficient
    correlation_coef = calculate_pearson_correlation_coefficient(linear_reg_coef, museum_all_data_df)
    log.info(f'''The model's Pearson's correlation coefficient from linear regression coefficient is:\n '''
             f'''Pearson's correlation coefficient: {correlation_coef}''')

    # Make prediction from the model
    log.info('Predicting testing dataset...')
    predictions = model_prediction(model, x_test)

    # Test the Performance of the Model
    log.info('Calculating performance metrics based on y_test set and prediction results...')
    mean_absolute_error, mean_squared_error, root_mean_squared_error = calculate_performance_metrics(y_test,
                                                                                                     predictions)
    log.info(f'The performance metrics has below values: \n '
             f'Mean absolute error: {mean_absolute_error} \n '
             f'Mean squared error: {mean_squared_error} \n '
             f'Root mean squared error: {root_mean_squared_error}')


def prepare_train_test_set(museum_all_data_df):
    x = museum_all_data_df[['population']]
    y = museum_all_data_df[['visitors']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    return x_train, x_test, y_train, y_test


def build_linear_reg_model(x_train, y_train):
    model = LinearRegression()
    model.fit(x_train, y_train)

    return model


def model_prediction(model, x_test):
    predictions = model.predict(x_test)
    return predictions


def calculate_coefficient_and_intercept(model):
    linear_regression_coefficient = model.coef_[0][0]
    linear_regression_intercept = model.intercept_[0]

    return linear_regression_coefficient, linear_regression_intercept


def calculate_pearson_correlation_coefficient(linear_reg_coef, museum_all_data_df):
    x1 = museum_all_data_df['population']
    y1 = museum_all_data_df['visitors']
    correlation_coefficient = linear_reg_coef * np.std(x1) / np.std(y1)

    return correlation_coefficient


def calculate_performance_metrics(y_test, predictions):
    mean_absolute_error = metrics.mean_absolute_error(y_test, predictions)
    mean_squared_error = metrics.mean_squared_error(y_test, predictions)
    root_mean_squared_error = np.sqrt(metrics.mean_squared_error(y_test, predictions))

    return mean_absolute_error, mean_squared_error, root_mean_squared_error
