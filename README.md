# Lodestone programming assignment

[live webpage with visualizations and responses](https://bendevera-lodestone.herokuapp.com/)

## Step 1 & 2 "Create Random Data"
completed in `generate_data.py`

## Step 3 "Visualizations/Calculations" 
completed in `visualizations.py`

question: "Given your answer, what approaches do you recommend you need to take to improve your metrics, if the metric has not met engineering standards?"

(live setting) I would improve the instructions/training given to raters (maybe through pre-recorded videos), ensure raters aren't labeling tasks at a rate deemed too quick to be accurate, and add incentives for high agreement %, precision and recall by basing a small bonus or level of pay based on these metrics. 

(random data generation) I would add a higher weight to the correct label (comparitive to other label's weights) to improve the liklihood that correct labels are generated more frequently. 


## Step 4 "Questions to Consider"
answered on live webpage linked above ^

## Step 5 "SQL Query"
done in `sql_query.py` but used table name `data_ratings` rather than `rater_data` because that is the name of the table stored in `db.sqlite` that I stored the randomly generated data in