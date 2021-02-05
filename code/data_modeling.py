import pandas as pd
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt
from statsmodels.graphics.api import abline_plot
import pprint

from sklearn.compose import make_column_transformer, TransformedTargetRegressor
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

from code.data_wrangling import load_from_db

# load PROFILE for filter_by_offer()
_, PROFILE = load_from_db()


def power_2(x):
    '''
    create inverse of np.sqrt() for normalization
    see build_model()
    '''
    return x**2


def filter_by_offer(df, offer_name: str):
    '''
    Extract data for offer_name only
    Remove offer with no spending
    Convert datetime into timestamp to be used as numerical variable
    ---
    INPUTS
    df - dataframe with amount_viewed for each offer per customer
    offer_name - 'bogo', 'discount' or 'informational'
    ---
    OUTPUTS
    X - features
    y - target
    '''
    Y = df.query('(portfolio_type == @offer_name) & (amount_viewed != 0)')['amount_viewed']
    y = Y.values.ravel()

    X = PROFILE.loc[Y.index, :]
    X['became_member_on'] = X['became_member_on'].apply(lambda x: x.timestamp())

    return X, y


def build_model(CAT_COL, CON_COL, func_name=None):
    '''
    build model by:
    1. encoding the categorical columns with OneHotEncoder
    2. scaling of the numerical columns with RobustScaler (limit outliers effects)
    3. create pipeline testing Ridge regressor
        3.1 normalization of the target variable (None, sqrt, or log10)
    4. create parameters to test through GridSearch
    5. create Grid search with cross-validation
    ---
    INPUTS
    CAT_COL - list of categorical columns
    CON_COL - list of continuous columns
    func_name - nomalization function (str) 'sqrt' or 'log10'
    OUTPUT
    model
    '''

    func_option = ['np.sqrt', 'np.log10']
    func_inv = ['power_2', 'sp.special.exp10']

    if func_name:
        try:
            func_str = 'np.'+func_name
            idx = [x.split('.')[-1] for x in func_option].index(func_name)
            inv_str = func_inv[idx]
        except:
            print(f'{func_name} is not an option')
    else:
        func_str = 'None'
        inv_str = 'None'

    preprocessor = make_column_transformer(
        (OneHotEncoder(drop='if_binary'), CAT_COL),
        (RobustScaler(), CON_COL),
        remainder='passthrough'
    )

    pipe = make_pipeline(
        preprocessor,
        TransformedTargetRegressor(
            regressor=Ridge(alpha=1e-10, fit_intercept=True, solver='auto'),
            func=eval(func_str),
            inverse_func=eval(inv_str)
        )
    )

    params = {
        'transformedtargetregressor__regressor__alpha': [1e-10, 1e-5, 0.1],
        'transformedtargetregressor__regressor__max_iter': [None, 100, 200],
        'transformedtargetregressor__regressor__tol': [0.001, 0.01, 0.1]
    }

    model = GridSearchCV(pipe, params, cv=5)

    return model, func_str


def evaluate_model(model, X_test, y_test):
    '''
    Evaluate the model created by build_model()
    creates prediction for X_test
    computes evaluation metrics:
    ---
    INPUTS
    model - model from build_model
    OUTPUTS
    r2 - variance explained
    Mean_Abs_Perc_Err - mean absolute percentage error
    Mean_Abs_Err - mean absolute error
    RMS_Err - root mean squared error
    y_pred - predictions for X_test
    '''
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    Mean_Abs_Perc_Err = mean_absolute_percentage_error(y_test, y_pred)
    Mean_Abs_Err = mean_absolute_error(y_test, y_pred)
    RMS_Err = np.sqrt(mean_squared_error(y_test, y_pred))

    return r2, Mean_Abs_Perc_Err, Mean_Abs_Err, RMS_Err, y_pred


def run_model(X, y, norm_func=None):

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    CAT_COL = ['gender']
    CON_COL = ['age', 'became_member_on', 'income', 'total_spending', 'total_offers']

    print('Building model...')
    model, func_str = build_model(CAT_COL, CON_COL, func_name=norm_func)

    print('Training model...')
    model.fit(X_train, y_train)
    pprint.pprint(model.best_params_)
    print(f'\nBest Score:{model.best_score_:.2%}', '\n')

    print('Evaluating model...')
    r2, Mean_Abs_Perc_Err, Mean_Abs_Err, RMS_Err, y_pred = evaluate_model(model, X_test, y_test)
    print(f'\nThis model explains {r2:.2%} of the variance of the amount_viewed')
    print(f'Our predictions are wrong by {Mean_Abs_Perc_Err:.2%}')
    print(f'Which represent on average ${Mean_Abs_Err:.2f}')

    if True:
        f, ax = plt.subplots(figsize=[8, 8])
        plt.scatter(y_test, y_pred)
        abline_plot(intercept=0, slope=1, color="red", ax=ax, ls='--', lw=2)
        ax.set_xlabel('Truth')
        ax.set_ylabel('Prediction')
        ax.set_title(f'Transformation: {func_str}', weight='bold', fontsize=16)
        plt.show()
        
        if False:
            ax.set_title("Discount Offer", weight='bold', fontsize=16)
            f.savefig('./docs/assets/truth_vs_preds.png', transparent=True, dpi=150)
