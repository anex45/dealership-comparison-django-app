"""IBM Cloud Function that gets all reviews by dealer ID
Returns:
    List: List of reviews by Dealer ID
"""
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1
import requests


def main(param):
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

        authenticator = IAMAuthenticator(param["IAM_AUTH"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(param["CLOUDANT_URL"])

        response = service.post_find(
            db='reviews',
            selector={'dealership': {'$eq': param["DEALER_ID"]}},
            fields=fields
        ).get_result()

        return {"body": response}
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
