import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from sqlalchemy import create_engine


def load_data(data_path):
    '''
    load, filter and format portfolio, profile and transcript data

    INPUT
    data_path - path to folder containing portfolio, profile, and transcript files

    OUTPUT
    PORTFOLIO - DataFrame of offers details
    PROFILE - DataFrame of customers demographics
    TRANSCRIPT - DataFrame of app interactions
    '''

    # read in the json files
    portfolio = pd.read_json(data_path+'portfolio.json', orient='records', lines=True)
    profile = pd.read_json(data_path+'/profile.json', orient='records', lines=True)
    transcript = pd.read_json(data_path+'transcript.json', orient='records', lines=True)

    # PORTFOLIO
    PORTFOLIO = portfolio.set_index('id')  # set id as index
    # create readable code for each offer (first letter.duration.difficulty)
    PORTFOLIO['code'] = PORTFOLIO.apply(
        lambda x: x['offer_type'][0].
        capitalize()+'.'+str(x['duration']).zfill(2) + '.' + str(x['difficulty']).zfill(2),
        axis=1
    )
    # create dummy variable for each channels (except 'email' found in all offer)
    for col in ['web', 'mobile', 'social']:
        PORTFOLIO['chann_'+col] = PORTFOLIO['channels'].apply(lambda x: int(col in x))

    PORTFOLIO.drop('channels', axis=1, inplace=True)

    # PROFILE
    PROFILE = profile.query('age != 118')  # filtering out age == 118 (see README)
    PROFILE['became_member_on'] = pd.to_datetime(
        PROFILE.loc[:, 'became_member_on'], format='%Y%m%d')
    PROFILE.set_index('id', inplace=True)

    # TRANSCRIPT
    # keep only participants from PROFILE with "offer received" and "transaction"
    user_list = set(PROFILE.index)  # remove customers with no offers
    user_received = set(transcript.query('event == "offer received"')['person'])
    user_transaction = set(transcript.query('event == "transaction"')['person'])
    user_list.intersection_update(user_received, user_transaction)

    TRANSCRIPT = expand_transcript(transcript.query('person in @user_list').reset_index(drop=True))

    return PORTFOLIO, PROFILE, TRANSCRIPT


def expand_transcript(df):
    '''
    expand json formated data (in column called 'value') into pandas DataFrame

    INPUT
    df - DataFrame containg transcript(app interactions)

    OUTPUT
    n_trans - df['value'] expanded into ['offer_id', 'amount', 'reward']

    '''
    # change 'offer id' in 'offer_id'
    value = df['value'].\
        apply(lambda x: {('offer_id' if k == 'offer id' else k): v for k, v in x.items()})

    # expand dictionary into 3 columns and add to transcript
    n_trans = df.join(pd.json_normalize(value))

    return n_trans.drop(columns=['value'])  # drop obsolete columns


def create_features(PROFILE):
    '''
    Creates bracketed features for 'age', 'became_member_on', and 'income'.
    Brackets are based on scatterplot visualizations (see devStarbucks.ipynb)

    INPUT
    PROFILE - DataFrame containing customer profile demographics

    OUTPUT
    feat_profile - bracketed demographics
    '''

    feat_profile = pd.DataFrame()

    # age brackets
    bins_age = [0, 36, 48, 75, float('inf')]
    lab_age = ['<36', '36-47', '48-74', '>75']
    feat_profile['age_brackets'] = pd.cut(
        PROFILE['age'], bins=bins_age, labels=lab_age, right=False)

    # membership brackets
    date_breaks = [
        datetime(year=2015, month=8, day=1),
        datetime(year=2017, month=8, day=1)
    ]
    bins_date = PROFILE['became_member_on'].agg({'min': min, 'max': max}).to_list()
    bins_date.extend(pd.to_datetime(date_breaks).to_list())
    bins_date.sort()

    str_lab = [str(x.month)+'-'+str(x.year) for x in bins_date]
    lab_date = []
    for i in range(len(str_lab)-1):
        lab_date.append(str_lab[i] + ' to ' + str_lab[i+1])
#     lab_date = ['to '+str(x.date()) for x in bins_date[1:]]

    feat_profile['membership'] = pd.cut(PROFILE.became_member_on, bins=bins_date, labels=lab_date)
    feat_profile['membership'] = feat_profile['membership'].astype('category')

    # income brackets
    bins_income = [0, 50000, 75000, 100000, float("inf")]
    lab_income = ['<50k', '50k-74k', '75k-99k', '>100k']
    feat_profile['income_brackets'] = pd.cut(
        PROFILE['income'], bins=bins_income, labels=lab_income, right=False)

    if False:
        # total_spending brackets
        bins_spending = [0, 50, 100, 150, 200, 250, 300, float('inf')]
        lab_spending = ['<50', '50-99', '100-149', '150-199', '200-249', '250-299', '>300']
        feat_profile['spending_brackets'] = pd.cut(
            PROFILE['total_spending'], bins=bins_spending, labels=lab_spending, right=False)

    return feat_profile.join(PROFILE['gender'])


def find_best_offer(res_table, age=None, member=None, income=None, gender=None):
    '''
    INPUTS
    age - age to find in age brackets (integer)
    member - date of mambership (string "Year-Month-Day")
    income - income to find in income brackets (integer)
    gender - 'F', 'M', 'O'
    res_table - DataFrame with completion rate per brackets

    OUTPUT
    pandas DataFrame
    '''
    age_list = list(res_table['age_brackets'].unique())
    member_list = list(res_table['membership'].unique())
    income_list = list(res_table['income_brackets'].unique())
    gender_list = ['M', 'F', 'O']

    # default query would return all res_table
    str_query = '(age_brackets != "118")'

    # find age bracket
    if age:
        test_age = dict()
        for k in age_list:
            number = re.findall('\d+', k)
            test_age[k] = min([np.abs(age-int(x)) for x in number])
        age_br = min(test_age.keys(), key=(lambda k: test_age[k]))
        str_query = '(age_brackets == @age_br)'

    # find membership bracket
    if member:
        test_member = dict()
        for k in member_list:
            dates = re.findall('\d+', k)
            dt = datetime(year=int(dates[-1]), month=int(dates[-2]), day=1)
            test_member[k] = dt-datetime.fromisoformat(member)
        test_member = {k: v for k, v in test_member.items() if v >= timedelta(0)}
        member_br = min(test_member.keys(), key=(lambda k: test_member[k]))
        str_query = str_query + ' & (membership == @member_br)'

    # find income bracket
    if income:
        test_income = dict()
        for k in income_list:
            inc = re.findall('\d+', k)
            test_income[k] = min([np.abs(income-int(x)*1000) for x in inc])
        income_br = min(test_income.keys(), key=(lambda k: test_income[k]))
        str_query = str_query + ' & (income_brackets == @income_br)'

    if gender:
        str_query = str_query + ' & (gender == @gender)'

    df_out = res_table.query(str_query)

    return df_out


def load_from_db():
    '''
    open database and load results and profile tables into DataFrames
    '''
    database_filename = './data/db_results.db'
    engine = create_engine('sqlite:///'+database_filename)

    RES = pd.read_sql_table('Variables', con=engine)
    PROFILE = pd.read_sql_table('Profile', con=engine, index_col='id',
                                parse_dates=['became_member_on'])

    return RES, PROFILE
