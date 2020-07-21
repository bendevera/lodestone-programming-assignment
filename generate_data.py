import random
import sqlite3
from datetime import datetime, date
import sys


def build_database(cursor, data_count=10000):
    # drop table if it exists to allow rerunning of script
    drop_table_query = "DROP TABLE IF EXISTS data_ratings;"
    cursor.execute(drop_table_query)
    # create table
    create_table_query = """
    CREATE TABLE data_ratings (
        task_id INTEGER PRIMARY KEY,
        rater_id CHAR,
        date DATE,
        correct_label_three TEXT,
        rater_label_three TEXT,
        label_three_agreement BOOLEAN,
        correct_label_five TEXT,
        rater_label_five TEXT,
        label_five_agreement BOOLEAN
    );
    """
    cursor.execute(create_table_query)

    rater_ids = ["A", "B", "C", "D", "E"]
    three_labels = ["Low", "Average", "High"]
    five_labels = ["Bad", "Okay", "Intermediate", "Great", "Exceptional"]
    insert_query = """
    INSERT INTO data_ratings 
    (task_id, rater_id, date, correct_label_three, rater_label_three, label_three_agreement, 
    correct_label_five, rater_label_five, label_five_agreement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    def generate_random_date():
        day = random.randint(1, 30)
        return date(2005, 10, day)

    # create 10,000 rows of data to store in the SQLite DB
    for i in range(1, data_count+1):
        # date 10/1/05 – 10/30/05
        current_date = generate_random_date()
        # rater A, B, C, D, E
        rater_id = random.choice(rater_ids)
        # correct 3 label
        correct_three_label = random.choice(three_labels)
        # correct 5 label
        correct_five_label = random.choice(five_labels)
        # rater 3 label
        rater_three_label = random.choice(three_labels)
        # rater 5 label
        rater_five_label = random.choice(five_labels)
        # task ID
        task_id = i
        # 3 label agreement
        three_label_agreement = correct_three_label == rater_three_label
        # 5 label agreement
        five_label_agreement = correct_five_label == rater_five_label

        # add data as row in data_ratings table
        insert_data = (task_id, rater_id, current_date, correct_three_label, rater_three_label,
                       three_label_agreement, correct_five_label, rater_five_label, five_label_agreement)
        cursor.execute(insert_query, insert_data)

    # ensure 10,000 rows were added
    sanity_check = "SELECT COUNT(*) FROM data_ratings;"
    sanity_check_result = cursor.execute(sanity_check).fetchone()[0]
    print(sanity_check_result)


if __name__ == "__main__":
    connection = sqlite3.connect('./db.sqlite')
    cursor = connection.cursor()
    if len(sys.argv) == 1:
        build_database(cursor)
    elif len(sys.argv) == 2:
        build_database(cursor, int(sys.argv[1]))
    else:
        raise ValueError(
            "Run programming by calling: `python3 generate_data.py [data_count]`")
    connection.commit()
    cursor.close()
    connection.close()
