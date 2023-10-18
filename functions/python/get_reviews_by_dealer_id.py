"""IBM Cloud Function that gets all reviews by dealer ID
Returns:
    List: List of reviews by Dealer ID
"""
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        fields = [
            'id',
            'name',
            'dealership',
            'review',
            'purchase',
            'purchase_date',
            'car_make',
            'car_model',
            'car_year'
        ]
        client = CloudantV1.new_instance()
        response = client.post_find(
            db='reviews',
            selector={'dealership': {'$eq': param_dict["DEALER_ID"]}},
            fields=fields
        ).get_result()

        return {"dbs": response}
    except ApiException as cloudant_exception:
        if str(cloudant_exception.code) == "404":
            return {"error": "dealerId does not exist"}
        if str(cloudant_exception.code) == "500":
            return {"error": "Something went wrong on the server"}
        return {"error": "status code: " + str(cloudant_exception.code)
        + " error message: " + cloudant_exception.message}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}
