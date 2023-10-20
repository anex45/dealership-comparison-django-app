"""IBM Cloud Function that gets all Watson NLU sentiment
Returns:
    Object: NLU Object
"""
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_watson import ApiException


def main(params):
    """Main Function

    Args:
        param_dict (Dict): 
        IAM_AUTH="<your apikey>"
        URL=<service url>

    Returns:
        _type_: object
    """

    authenticator = IAMAuthenticator(params["IAM_AUTH"])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(params["URL"])

    try:
        response = natural_language_understanding.analyze(
            text=params["text"],
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=1),
                keywords=KeywordsOptions(sentiment=True, limit=1))).get_result()

        print(json.dumps(response, indent=2))
        return {"body": response}
    except ApiException as err:
        print("Method failed with status code " +
              str(err.code) + ": " + err.message)
        return {"error": err}
