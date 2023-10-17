"""IBM Cloud Function that posts a review
Returns:
    List: List of reviews by Dealer ID
"""
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document
import json
import requests
import sys


def main(review_json):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    review = Document(
        id=review_json[""],
        name="Upkar Lidder",
        dealership=15,
        review="Great service!",
        purchase="false",
        another="field",
        purchase_date="02/16/2021",
        car_make="Audi",
        car_model="Car",
        car_year=2021
    )
    # reviewLoad = json.loads(review_json)
    # review = Document(
    #     id=reviewLoad["id"],
    #     name=reviewLoad["name"],
    #     dealership=reviewLoad["dealership"],
    #     review=reviewLoad["review"],
    #     purchase=reviewLoad["purchase"],
    #     another=reviewLoad["another"],
    #     purchase_date=reviewLoad["purchase_date"],
    #     car_make=reviewLoad["car_make"],
    #     car_model=reviewLoad["car_model"],
    #     car_year=reviewLoad["car_year"],
    # )
    try:
        fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
        client = CloudantV1.new_instance()
        response = client.post_find(
            db='reviews',
            selector={'dealership': {'$eq': param_dict["DEALER_ID"]}},
            fields=fields
        ).get_result()

        print(response)
        return {"dbs": response}
    except ApiException as cloudant_exception:
        if str(cloudant_exception.code) == "404":
            return {"error": "dealerId does not exist"}
        elif str(cloudant_exception.code) == "500":
            return {"error": "Something went wrong on the server"}
        else:
            return {"error": "status code: " + str(cloudant_exception.code) + " error message: " + cloudant_exception.message}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

# python3 main.py main "{"id": 1114,"name": "Upkar Lidder","dealership": 15,"review": "Great service!","purchase": false,"another": "field","purchase_date": "02/16/2021","car_make": "Audi","car_model": "Car","car_year": 2021}"
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])