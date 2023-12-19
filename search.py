# SEARCH SERVICE

import requests
import psycopg2
import json
from decouple import config


def get_item_info(item):
    url = f'https://trackapi.nutritionix.com/v2/search/instant/?query={item}'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': config('X_APP_ID'),
        'x-app-key': config('X_APP_KEY')
    }
    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    return response


def get_nutrition_info(food_name):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-app-id': config('X_APP_ID'),
        'x-app-key': config('X_APP_KEY')
    }
    query = {'query' : food_name}
    response = requests.request("POST", url, headers=headers, data=query)
    # print(response.text)
    return response


def response_into_dictionary(common):
    fields = ["tag_id", "food_name", "serving_unit", "serving_qty", "photo", "locale"]
    reduced_common = [{} for i in range(len(common))]
    for i in range(len(common)):
        for k, v in common[i].items():
            if k in fields:
                reduced_common[i].update({k: v})

    return reduced_common


def get_formatted_response(item):
    common = json.loads(item.text)  # turns json into python dict
    common = common['common']  # list of dictionary items; each item a food; only common not brands
    reduced_common = response_into_dictionary(common)

    first_food = reduced_common[0]
    nutrition_response = get_nutrition_info(first_food['food_name']).json()
    nutrition_dict = nutrition_response['foods'][0]

    nutrition_info = (f'{first_food["serving_qty"]} {first_food["serving_unit"]} contains: '
                      f'CALORIES: {nutrition_dict["nf_calories"]}\n'
                      f'CARBS: {nutrition_dict["nf_total_carbohydrate"]}\n'
                      f'FATS: {nutrition_dict["nf_total_fat"]}\n'
                      f'PROTEIN: {nutrition_dict["nf_protein"]}\n')

    return first_food['photo'], nutrition_info

# for testing
# get_formatted_response(get_response('mozzarella cheese'))

def item_in_db(curr, tag_id):
    curr.execute('SELECT nix.foods.tag_id FROM nix.foods')
    tag_ids = curr.fetchall()
    for i in range(len(tag_ids)):
        tag_ids[i] = tag_ids[i][0]
    # print("Tag_ids: ", tag_ids)
    for t_id in tag_ids:
        if tag_id == t_id:
            return True # 'Food item already in db.'
    return False


def add_item_to_db(item):
    # runs whenever user searches, so every new search adds to the postgres db, almost like a cache

    ## CALL REST API TO GET DATA
    response = get_item_info(item)

    ## STRUCTURE RESPONSE FOR DB
    common = json.loads(response.text) # turns json into python dict
    common = common['common'] # list of dictionary items; each item a food; only common not brands

    try:
        conn = psycopg2.connect(
            database="postgres",
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host='localhost',
            # port=5432
        )
    except Exception as e:
        print(e)
        raise e

    # check to see if item already in db, don't add if so
    curr = conn.cursor()
    if item_in_db(curr, int(common[0]['tag_id'])):
        return 'Food item already in db.'

    reduced_common = response_into_dictionary(common)

    ## PUT ITEM IN DB
    for i in range(len(reduced_common)):
        food_dict = reduced_common[i]
        exists = item_in_db(curr, int(food_dict['tag_id']))
        # print(exists)
        if not exists:
            # print(f"adding... {food_dict['tag_id']}")
            tag_id, name, serving_unit, serving_qty, photo, locale = int(food_dict['tag_id']), food_dict['food_name'], food_dict['serving_unit'], int(food_dict['serving_qty']), food_dict['photo']['thumb'], food_dict['locale']
            curr.execute('INSERT INTO nix.foods(tag_id, name, serving_unit, serving_qty, photo, locale) VALUES (%s, %s, %s, %s, %s, %s)',
                         (tag_id, name, serving_unit, serving_qty, photo, locale))
            curr.execute('SELECT * FROM nix.foods')
            print("1. ", curr.fetchmany())

    conn.commit()
    curr.close()
    conn.close()


# for testing...
# add_item_to_db('pizza')
