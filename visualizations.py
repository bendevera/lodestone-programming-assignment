import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3
import sys


""" creates agreement rate by day graph """
def by_day_graph(df, show=True, save=False):
    dates = df.sort_values(by='date')['date'].unique()
    agreement_rates = []

    for day in dates:
        rows_for_day = df[df['date'] == day]
        label_three_agreement = rows_for_day['label_three_agreement'].value_counts()[
            1]
        label_five_agreement = rows_for_day['label_five_agreement'].value_counts()[
            1]
        agreement_rate = (label_five_agreement +
                          label_three_agreement) / (rows_for_day.shape[0]*2)
        agreement_rates.append(agreement_rate)

    fig, ax = plt.subplots(figsize=(10, 3))
    ind = np.arange(len(agreement_rates))  # the x locations for the groups
    plt.bar([date[-2:] for date in dates],
            agreement_rates, align='edge', width=0.3)
    ax.set_yticks([value/100 for value in range(0, 35, 5)])
    ax.set_yticklabels(
        [str(value)+"%" for value in range(0, 31, 5)], minor=False)
    ax.set_xticks([value for value in range(0, 30)])
    ax.set_xticklabels([str(value) for value in range(1, 31)])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.ylabel('Agreement Rate')
    plt.xlabel('Day')
    plt.title('Agreement Rates by Day')

    if save:
        plt.savefig('agreement_rates_by_day.png')
    if show:
        plt.show()
    plt.clf()


""" gets data for by rater graph and total tasks graph """
def get_by_rater_data(df, verbose=False):
    rater_data = df.groupby("rater_id")
    rater_agreement_rates = []
    task_counts = []
    rater_ids = []

    if verbose:
        print("By rater data")

    for rater_id, rater in rater_data:
        three_agreement_rate = rater['label_three_agreement'].mean()
        five_agreement_rate = rater['label_five_agreement'].mean()
        # same number of three labels as five labels so can add and divide by 2
        rater_agreement_rate = (three_agreement_rate + five_agreement_rate) / 2

        rater_agreement_rates.append(rater_agreement_rate)
        task_counts.append(rater.shape[0])
        rater_ids.append(rater_id)
        if verbose:
            print(rater_id, rater.shape[0], rater_agreement_rate)
    return rater_agreement_rates, task_counts, rater_ids


""" creates agreement rates by rater graph """
def agreement_by_rater_graph(rater_ids, rater_agreement_rates, show=True, save=False):
    fig, ax = plt.subplots()
    width = 0.75  # the width of the bars
    ind = np.arange(len(rater_ids))  # the x locations for the groups
    ax.barh(ind, rater_agreement_rates, width)
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(rater_ids, minor=False)
    ax.set_xticks([value/100 for value in range(0, 30, 5)])
    ax.set_xticklabels([str(value)+"%" for value in range(0, 30, 5)])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis=u'y', which=u'both', length=0)
    for index, value in enumerate(rater_agreement_rates):
        if value == max(rater_agreement_rates):
            plt.text(value, index, str(round(value*100, 1))+"%", color="green")
        elif value == min(rater_agreement_rates):
            plt.text(value, index, str(round(value*100, 1))+"%", color="red")
        else:
            plt.text(value, index, str(round(value*100, 1))+"%")

    plt.xlabel('Agreement Rate')
    plt.ylabel('Raters')
    plt.title('Agreement Rates by Rater')
    if save:
        plt.savefig('agreement_rates_by_rater.png')
    if show:
        plt.show()
    plt.clf()


""" creates completed tasks by rater graph """
def tasks_by_rater_graph(rater_ids, task_counts, show=True, save=False):
    fig, ax = plt.subplots()
    width = 0.75  # the width of the bars
    ind = np.arange(len(rater_ids))  # the x locations for the groups
    ax.barh(ind, task_counts, width)
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(rater_ids, minor=False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis=u'y', which=u'both', length=0)
    for index, value in enumerate(task_counts):
        if value == max(task_counts):
            plt.text(value, index, str(value), color="green")
        elif value == min(task_counts):
            plt.text(value, index, str(value), color="red")
        else:
            plt.text(value, index, str(value))

    plt.xlabel('Completed Tasks')
    plt.ylabel('Raters')
    plt.title('Completed Tasks by Rater')
    if save:
        plt.savefig('completed_tasks_by_rater.png')
    if show:
        plt.show()
    plt.clf()


""" precision and recall calculations """
def precision_recall(df, verbose=False):
    result = []

    five_labels = df['correct_label_five'].unique()

    for label in five_labels:
        true_positives = df[(df['label_five_agreement'] == 1) & (
            df['correct_label_five'] == label)].shape[0]
        precision = true_positives / \
            df[df['rater_label_five'] == label].shape[0]
        recall = true_positives / \
            df[df['correct_label_five'] == label].shape[0]
        if verbose:
            print(f"{label} precision: {precision}")
            print(f"{label} recall: {recall} \n")
        result.append({
            "label": label,
            "precision": precision,
            "recall": recall
        })

    three_labels = df['correct_label_three'].unique()

    for label in three_labels:
        true_positives = df[(df['label_three_agreement'] == 1) & (
            df['correct_label_three'] == label)].shape[0]
        precision = true_positives / \
            df[df['rater_label_three'] == label].shape[0]
        recall = true_positives / \
            df[df['correct_label_three'] == label].shape[0]
        if verbose:
            print(f"{label} precision: {precision}")
            print(f"{label} recall: {recall} \n")
        result.append({
            "label": label,
            "precision": precision,
            "recall": recall
        })
    return result


""" overall agreement rate calculation """
def overall_agreement(df, verbose=False):
    agreement_rate = df[(df['label_three_agreement'] == 1) & (
        df['label_five_agreement'] == 1)].shape[0] / df.shape[0]
    if verbose:
        print(f"Overall agreement rate: {round(agreement_rate*100, 2)}%")
    return agreement_rate


if __name__ == "__main__":
    connection = sqlite3.connect('./db.sqlite')
    df = pd.read_sql('SELECT * FROM data_ratings', con=connection)
    if "--save" in sys.argv:
        save = True
    else:
        save = False
    if "--no-show" in sys.argv:
        show = False
    else:
        show = True
    if "--verbose" in sys.argv:
        verbose = True
    else:
        verbose = False
    by_day_graph(df, show, save)
    rater_agreement_rates, task_counts, rater_ids = get_by_rater_data(
        df, verbose)
    agreement_by_rater_graph(rater_ids, rater_agreement_rates, show, save)
    tasks_by_rater_graph(rater_ids, task_counts, show, save)
    precision_recall_data = precision_recall(df, verbose)
    overall_agreement_data = overall_agreement(df, verbose)
