"""
Write a SQL query that outputs the following from the table:
Agreement Rates for Each Rater on October 6
"""
import sqlite3

query = """
SELECT AVG(label_three_agreement), AVG(label_five_agreement), rater_id
FROM data_ratings
WHERE date = '2005-10-06'
GROUP BY rater_id;
"""
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

result = cursor.execute(query).fetchall()
print(result)

cursor.close()