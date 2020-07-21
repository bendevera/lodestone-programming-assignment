from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)
get_data_query = """
SELECT task_id, rater_id, date, correct_label_three, rater_label_three, label_three_agreement, 
correct_label_five, rater_label_five, label_five_agreement
FROM data_ratings
LIMIT 10;
"""


def get_cursor():
    connection = sqlite3.connect('./db.sqlite')
    return connection.cursor()

@app.route('/')
def index():
    cursor = get_cursor()
    data_excerpt = cursor.execute(get_data_query).fetchall()
    cursor.close()
    with open('precision_recall_data.json') as f:
        precision_recall_data = json.load(f)
    return render_template('index.html', data_excerpt=data_excerpt, precision_recall=precision_recall_data)


if __name__ == '__main__':
    app.run()