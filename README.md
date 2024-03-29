
# MealGen

MealGen is a web application to provide tailored meal recommendations based on user preferences.

This app is a work in progress meant to develop and showcase skills in Python, web development, Postgres, utilizing APIs, and creating ETL pipelines. Future work will be done to accomplish user authentication/authorization, scheduled data pulls via Apache Airflow, and recommendations.

Feature(s) in progress: testing with Selenium, web scraping, and Python scripting. 

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file.

Information for connecting to Postgres Database:

DB_USER

DB_PASSWORD

Information for connecting to [NutritionIX API](https://www.nutritionix.com/business/api "@embed"):

X_APP_ID

X_APP_KEY


## Deployment

To deploy this project locally run

```bash 
  flask run
```
