import pandas as pds
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, recall_score, classification_report, roc_auc_score, roc_curve, confusion_matrix

def make_survey_weight_df(
        df: pds.DataFrame, 
        group_field='SEQN',
        survey_weight_field='WTMEC2YR',
        adj_weight_field='adj_weight',
        weight_divisor=1000
    ):
    """duplicates the rows in df by survey_weight_field divided by the weight_divisor"""
    # create adjusted weight based on the survey weight value
    for idx in df.index:
        weight_value = df.loc[idx, survey_weight_field]

        if weight_divisor > 0:
            adj_weight = round(weight_value/weight_divisor, 0)
        else:
            adj_weight = round(weight_value, 0)

        df.loc[idx, adj_weight_field] = adj_weight 

    # convert adj weight field to ints
    df[adj_weight_field] = df[adj_weight_field].astype(int)

    # find index position of adj_weight_field; needed for use with iloc below
    adj_weight_field_index = len(df.columns) - 1 

    # create list of dataframes in which the each dataframe is
    # duplicated by the value of the adj_weight
    dfs = []
    for idx, mydf in df.groupby(group_field):
        adj_weight = mydf.iloc[0, adj_weight_field_index]

        # append copies of dataframe to list
        for i in range(adj_weight):
            dfs.append(mydf.copy())
    
    # return concatenated dataframes
    return pds.concat(dfs)


def make_machine_learning_df(
        train_cols=['SEQN', 'female', 'ridageyr', 'pct_teeth_gt_3', 'pct_teeth_gt_4', 'pct_teeth_gt_5', 'pct_teeth_gt_6'],
        test_col='low_global_re',
        index='SEQN',
        use_survey_weight=True,
        survey_weight_field='WTMEC2YR',
        adj_weight_field='adj_weight',
        weight_divisor=1000
    ):
    """automate process of creating the dataset used by machine learning methods"""
    # add test col
    if type(test_col) == str:
        train_cols.append(test_col)
    else:
        train_cols.extend(test_col)

    # add survey weight field to train_cols
    if use_survey_weight:
        train_cols.append(survey_weight_field) 

    if train_cols is not None and len(train_cols) > 0:
        merge_df = pds.read_table('../refined_data/merged_data.tsv', usecols=train_cols)
    else:
        merge_df = pds.read_table('../refined_data/merged_data.tsv')
    
    
    if use_survey_weight:
        merge_df = \
            make_survey_weight_df(
                merge_df, 
                group_field=index,
                survey_weight_field=survey_weight_field, 
                adj_weight_field=adj_weight_field, 
                weight_divisor=weight_divisor
            )

        # drop weighting info
        merge_df = merge_df.drop([survey_weight_field, adj_weight_field], axis=1)

    if len(index) > 0:
        merge_df = merge_df.set_index(index)
        merge_df.index = merge_df.index.astype(int)
    
    # rename age field
    if 'ridageyr' in merge_df.columns:
        merge_df = merge_df.rename(columns={'ridageyr': 'age'})
    
    # print(merge_df.head()) # testing
    
    return merge_df


def make_pd_cog_contingency_table(df, pd_field, cog_score_field):
    """build contingency table based on the dataframe and periodontal disease field (pd_field)"""
    table = pds.DataFrame (
        {
            'pd': [1.0 if val > 0.0 else 0 for val in df[pd_field]],
            'low_score': df[cog_score_field].values
        }
    )
    ctg_table = pds.crosstab(table['pd'], table['low_score'])

    return ctg_table


def test_count_df(
        df: pds.DataFrame, 
        group_field='SEQN',
        survey_weight_field='WTMEC2YR',
        adj_weight_field='adj_weight',
        weight_divisor=1000
    ):
    """tests the number of dataframes created"""
    # create adjusted weight based on the survey weight value
    for idx in df.index:
        weight_value = df.loc[idx, survey_weight_field]

        if weight_divisor > 0:
            adj_weight = round(weight_value/weight_divisor, 0)
        else:
            adj_weight = round(weight_value, 0)

        df.loc[idx, adj_weight_field] = adj_weight 

    # convert adj weight field to ints
    df[adj_weight_field] = df[adj_weight_field].astype(int)
    
    # count number of dataframes created
    df_count = 0
    for idx, mydf in df.groupby(group_field):
        adj_weight = df.loc[idx, adj_weight_field]
        df_count += adj_weight
        # print(idx, adj_weight, df_count) # print for testing
        
    return df_count


def plot_roc_curve(
        y_test, 
        y_pred, 
        y_proba, 
        figsize=(2,2), 
        title="", 
        text_x=-0.5, 
        text_y=-1.25,
        text_size='x-small',
        legend_loc=4, 
        plot_report=True,
        return_scores=False
    ):
    # calc false positive rate, true positive rate, and thresholds
    fpr, tpr, _ = roc_curve(y_test,  y_proba)
    
    # calc classification report and auc score
    report = classification_report(y_test, y_pred, zero_division=0)
    auc_score = round(roc_auc_score(y_test, y_proba), 5)

    #create ROC curve
    plt.figure(figsize=figsize)
    
    if len(title) > 0:
        plt.title(title, fontsize=15, color='black')

    plt.plot(fpr, tpr, label="AUC="+str(auc_score))
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.legend(loc=legend_loc)
    
        
    if plot_report:
        plt.text(x=-0.5, y=-1.25, s=report, size=text_size)
    
    if return_scores:
        return plt, report, auc_score # return the classification report and the auc
    else:
        return plt


def plot_model_score_results(
        score_results,
        figsize=(14,3), 
        title="",
        text_x=-0.2, 
        text_y=0.8, 
        legend_loc=4, 
        plot_report=True,
        text_size='x-small'
    ):
    
    fig, axs = plt.subplots(1, 4, figsize=figsize)
    
    # grab test, pred, and probability for each model
    axs_count = 0
    for key, results in score_results.items():
        ax = axs[axs_count]
        
        y_test, y_pred, y_proba, title = results.values()
        
        # print(model_name, y_test)
        # calc false positive rate, true positive rate, and thresholds
        fpr, tpr, _ = roc_curve(y_test,  y_proba)

        # calc classification report and auc score
        report = classification_report(y_test, y_pred, zero_division=0)
        auc_score = round(roc_auc_score(y_test, y_proba), 5)
        
        #create ROC curve
        #fig, ax = plt.figure(figsize=figsize)
        
        if title == "": # default title is the key
            ax.title.set_text(key)
        else:
            ax.title.set_text(title)

        ax.plot(fpr, tpr, label="AUC="+str(auc_score))
        ax.set_ylabel('True Positive Rate')
        ax.set_xlabel('False Positive Rate')
        ax.legend(loc=legend_loc)
        
        if plot_report:
            ax.text(x=text_x, y=-text_y, s=report, size=text_size)
        
        axs_count += 1

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
        
    return plt


def plot_train_test_counts(y_train, y_test):
    plot_data = {
        'data': [
            'train - not low', 
            'train - low', 
            'test - not low', 
            'test - low'
        ], 
        'count': [
            len(y_train[y_train == 0]), 
            len(y_train[y_train == 1]), 
            len(y_test[y_test == 0]), 
            len(y_test[y_test == 1])
        ]
    }
    plot_df = pds.DataFrame(plot_data)

    
    plt.figure(figsize=(5,3))
    sns.barplot(data=plot_df, x='data', y='count')

    return plot


def feature_imp(df,model):
    fi = pds.DataFrame()
    fi["feature"] = df.columns
    fi["importance"] = model.feature_importances_
    return fi.sort_values(by="importance", ascending=False)


def plot_feature_importances(df, models):
    fig, axs = plt.subplots(1, 4, figsize=(14,3))
    kind='bar'
    
    axs_count = 0
    for model in models:
        ax = axs[axs_count]
        ax.set_ylabel('Importance')
        ax.set_xlabel('Feature')
        
        try:
            plot_df = feature_imp(df, model)
            #ax.plot( plot_df.feature, plot_df.importance, kind, legend=False)
            # ax.xticks(rotation=30)
            # ax.set_xticklabels(plot_df.feature, rotation=30)
            ax.bar(plot_df.feature, plot_df.importance, width=0.5)
            ax.set_xticks([0,1,2,3]) # hack to supress FixedLocator warning
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        except Exception as e:
            # ax.text(x=0, y=0, s=str(e))
            pass
        finally:
            axs_count += 1
    
    for ax in axs.flat:
        ax.label_outer()
        
    return plt


def plot_patient_age_gender(df, figsize=(12,2)):
    # plt.figure(figsize=(10,2))
    fig, axs = plt.subplots(1, 3, figsize=figsize)

    # gender counts
    sns.barplot(
        ax=axs[0],
        data=df.female.value_counts().reset_index().rename(columns={'index': 'female', 'female': 'count'}),
        x='female', 
        y='count',
        width=0.5
    )


    # total age counts
    axs[1].hist(df[['age']])
    axs[1].set_xlabel('age')

    # age counts by gender
    axs[2].hist(
            [
                df.loc[df['female'] == 0, 'age'],
                df.loc[df['female'] == 1, 'age']
            ],
            label=['male', 'female']
         )
    axs[2].set_xlabel('age by gender')

    plt.legend()

    # for ax in axs.flat: ax.label_outer() # share y axis
    return plt


def plot_hist_row(dataframes, x, titles=[], figsize=(12,2), kde=True):
    """plots a row of histograms"""
    # plt.figure(figsize=(10,2))

    num_hist = len(dataframes) # number of histograms to plot
    if num_hist == 1: # if one hist then create list with one ax
        fig, ax = plt.subplots(1, num_hist, figsize=figsize)
        axs = [ax]
    else:
        fig, axs = plt.subplots(1, num_hist, figsize=figsize)

    for n in range(num_hist):
        h = sns.histplot(
            data=dataframes[n], ax=axs[n], x=x, kde=kde
        )

        if n == 0:
            h.set(ylabel="count")
        else:
            h.set(ylabel="")

        if len(titles) == num_hist:
            h.set(title=titles[n])

    return plt


def plot_countplot_row(dataframes, x, titles=[], figsize=(8,2), hues=[]):
    """plots a row of bar charts"""
    # plt.figure(figsize=(10,2))

    num_plot = len(dataframes) # number of countplots to plot
    if num_plot == 1: # if one hist then create list with one ax
        fig, ax = plt.subplots(1, num_plot, figsize=figsize)
        axs = [ax]
    else:
        fig, axs = plt.subplots(1, num_plot, figsize=figsize)

    for n in range(num_plot):
        if len(hues) == num_plot:
            p = sns.countplot(data=dataframes[n], ax=axs[n], x=x, hue=hues[n])
        else:
            p = sns.countplot(data=dataframes[n], ax=axs[n], x=x)

        if n == 0:
            p.set(ylabel="count")
        else:
            p.set(ylabel="")

        if len(titles) == num_plot:
            p.set(title=titles[n])

    return plt


def add_cal_class(df: pds.DataFrame):
    """
    add class of CAL according to highest level found:
    - CAL>3
    - CAL>4
    - CAL>5
    - CAL>6
    """
    def get_value(val):
        # some values are sereis with the same index, so use the first one
        if type(val) == pds.Series:
            return val.values[0]
        else:
            return val

    df['cal_class'] = 'NA' # default value

    for idx in df.index:
        if get_value(df.loc[idx, 'pct_teeth_gt_3']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>3'
        
        if get_value(df.loc[idx, 'pct_teeth_gt_4']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>4'
        
        if get_value(df.loc[idx, 'pct_teeth_gt_5']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>5'

        if get_value(df.loc[idx, 'pct_teeth_gt_6']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>6'
    
    return df

def add_age_class(df: pds.DataFrame):
    """
    adds age class to dataframe:
    - <60
    - 60-69
    - 70-79
    - 80+
    """
    def get_value(val):
        # some values are sereis with the same index, so use the first one
        if type(val) == pds.Series:
            return val.values[0]
        else:
            return val

    df['age_class'] = '<60' # default value
    
    for idx in df.index:
        age = get_value(df.loc[idx, 'age'])

        if age < 60:
            df.loc[idx, 'age_class'] = '<60'

        if age > 59 and age < 70:
            df.loc[idx, 'age_class'] = '60-69'

        if age > 69 and age < 80:
            df.loc[idx, 'age_class'] = '70-79'

        if age > 79:
            df.loc[idx, 'age_class'] = '80+'

    return df


def add_age_cal_class(df: pds.DataFrame):
    """
    adds age and cal classes to dataframe:
    age classes:
    - <60
    - 60-69
    - 70-79
    - 80+

    cal classes:
    - CAL>3
    - CAL>4
    - CAL>5
    - CAL>6
    """
    def get_value(val):
         # some values are sereis with the same index, so use the first one
        if type(val) == pds.Series:
            return val.values[0]
        else:
            return val

    # default values
    df['age_class'] = '<60' 
    df['cal_class'] = 'NA' 

    for idx in df.index:
        # add age class
        age = get_value(df.loc[idx, 'age'])

        if age < 60:
            df.loc[idx, 'age_class'] = '<60'

        if age > 59 and age < 70:
            df.loc[idx, 'age_class'] = '60-69'

        if age > 69 and age < 80:
            df.loc[idx, 'age_class'] = '70-79'

        if age > 79:
            df.loc[idx, 'age_class'] = '80+'

        # add cal class
        if get_value(df.loc[idx, 'pct_teeth_gt_3']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>3'
        
        if get_value(df.loc[idx, 'pct_teeth_gt_4']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>4'
        
        if get_value(df.loc[idx, 'pct_teeth_gt_5']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>5'

        if get_value(df.loc[idx, 'pct_teeth_gt_6']) > 0:
            df.loc[idx, 'cal_class'] = 'CAL>6'

    return df


def make_lmplot_df(df: pds.DataFrame):
    "melts data in form need by lmplot"

    # melt cal pct data into single column
    temp_df = ( 
        df.reset_index().
        melt(
            id_vars=['SEQN', 'female', 'age', 'age_cat', 'cerad_sum', 'digit_symbol', 'animal_fluency'], 
            value_vars=['pct_teeth_gt_3', 'pct_teeth_gt_4', 'pct_teeth_gt_5', 'pct_teeth_gt_6'],
            var_name='pct_cal',
            value_name='pct_value'
        )
    )

    # melt cog scores into single column
    plot_df = (
        temp_df.melt(
            id_vars=['SEQN', 'female', 'age', 'age_cat', 'pct_cal', 'pct_value'],
            value_vars=['cerad_sum', 'digit_symbol', 'animal_fluency'],
            var_name='cog_test',
            value_name='cog_score'
        )
    )

    return plot_df