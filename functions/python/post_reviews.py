"""IBM Cloud Function that posts a review
Returns:
    Object: {'ok': True, 'id': '6', 'rev': '3-...'}
"""
import json
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant.cloudant_v1 import CloudantV1, Document
import requests


def main(params):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    json_load = json.loads(params["PAYLOAD"])

    review = Document(
        doc_id=json_load["doc_id"],
        name=json_load["name"],
        dealership=json_load["dealership"],
        review=json_load["review"],
        sentiment=json_load["sentiment"],
        purchase=json_load["purchase"],
        purchase_date=json_load["purchase_date"],
        car_make=json_load["car_make"],
        car_model=json_load["car_model"],
        car_year=json_load["car_year"],
    )
    try:
        authenticator = IAMAuthenticator(params["IAM_AUTH"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(params["CLOUDANT_URL"])

        response = service.post_document(
            db='reviews', document=review).get_result()

        return {"body": response}
    except ApiException as cloudant_exception:
        if str(cloudant_exception.code) == "500":
            return {"error": "Something went wrong on the server"}
        return {"error": "status code: "
                + str(cloudant_exception.code) + " error message: "
                + cloudant_exception.message}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        return {"error": err}
