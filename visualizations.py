import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sqlite3

connection = sqlite3.connect('./db.sqlite')
df = pd.read_sql('SELECT * FROM data_ratings', con=connection)


"""
What is the agreement rate between the engineer and all the raters for each day?
"""

dates = df.sort_values(by='date')['date'].unique()
agreement_rates = []

for day in dates:
    rows_for_day = df[df['date'] == day]
    label_three_agreement = rows_for_day['label_three_agreement'].value_counts()[1]
    label_five_agreement = rows_for_day['label_five_agreement'].value_counts()[1]
    agreement_rate = (label_five_agreement + label_three_agreement) / (rows_for_day.shape[0]*2)
    agreement_rates.append(agreement_rate)

plt.title('Agreement Rates by Day')
plt.bar([date[-2:] for date in dates], agreement_rates)
plt.savefig('agreement_rates_by_day.png')
plt.clf()

"""
Identify raters that have the highest agreement rates with the engineer. -> E (~27.1%)
Identify raters that have the lowest agreement rates with the engineer. -> C (~25.9%)
Identify raters that have completed the most Task IDs. -> E (2053 tasks)
Identify raters that have completed the least Task IDs. -> A (1966 tasks)
"""

rater_data = df.groupby("rater_id")
rater_agreement_rates = []
task_counts = []
rater_ids = []

for rater_id, rater in rater_data:
    three_agreement_rate = rater['label_three_agreement'].mean()
    five_agreement_rate = rater['label_five_agreement'].mean()
    # same number of three labels as five labels so can add and divide by 2
    rater_agreement_rate = (three_agreement_rate + five_agreement_rate) / 2

    rater_agreement_rates.append(rater_agreement_rate)
    task_counts.append(rater.shape[0])
    rater_ids.append(rater_id)
    print(rater_id, rater.shape[0], rater_agreement_rate)

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(rater_ids)) # the x locations for the groups
ax.barh(ind, rater_agreement_rates, width)
ax.set_yticks(ind+width/2)
ax.set_yticklabels(rater_ids, minor=False)
ax.set_xticks([value/100 for value in range(0, 30, 5)])
ax.set_xticklabels([str(value)+"%" for value in range(0, 30, 5)])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis=u'y', which=u'both',length=0)
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
# plt.savefig('agreement_rates_by_rater.png')
# plt.show()
plt.clf()

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(rater_ids)) # the x locations for the groups
ax.barh(ind, task_counts, width)
ax.set_yticks(ind+width/2)
ax.set_yticklabels(rater_ids, minor=False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis=u'y', which=u'both',length=0)
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
# plt.savefig('completed_tasks_by_rater.png')
# plt.show()
plt.clf()


"""
What is the precision/recall for each of the 5 labels?
Great precision: 0.19328993490235352
Great recall: 0.20135628586332813 

Bad precision: 0.19528619528619529
Bad recall: 0.20049382716049383 

Intermediate precision: 0.2025518341307815
Intermediate recall: 0.19136112506278252 

Exceptional precision: 0.20875912408759123
Exceptional recall: 0.2100881488736533 

Okay precision: 0.1891348088531187
Okay recall: 0.18567901234567902 

What is the precision/recall for each of the 3 labels?
Low precision: 0.3400602409638554
Low recall: 0.3385307346326837 

Average precision: 0.33065236818588023
Average recall: 0.3291814946619217 

High precision: 0.33192897983749625
High recall: 0.33495293045854846 

What is the overall agreement rate considering that the raters have to be in agreement with both the
engineer's 3-label answer and the engineer's 5-label answer.
Overall agreement rate: 6.72%
"""

five_labels = df['correct_label_five'].unique()

for label in five_labels:
    true_positives = df[(df['label_five_agreement'] == 1) & (df['correct_label_five'] == label)].shape[0]
    precision = true_positives / df[df['rater_label_five'] == label].shape[0]
    print(f"{label} precision: {precision}")
    recall = true_positives / df[df['correct_label_five'] == label].shape[0]
    print(f"{label} recall: {recall} \n")

three_labels = df['correct_label_three'].unique()

for label in three_labels:
    true_positives = df[(df['label_three_agreement'] == 1) & (df['correct_label_three'] == label)].shape[0]
    precision = true_positives / df[df['rater_label_three'] == label].shape[0]
    print(f"{label} precision: {precision}")
    recall = true_positives / df[df['correct_label_three'] == label].shape[0]
    print(f"{label} recall: {recall} \n")

agreement_rate = df[(df['label_three_agreement'] == 1) & (df['label_five_agreement'] == 1)].shape[0] / df.shape[0]
print(f"Overall agreement rate: {round(agreement_rate*100, 2)}%")