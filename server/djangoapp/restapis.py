import json
import requests
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    '''GET
    e.g., response = requests.get(
        url,
        params=params,
        headers={'Content-Type': 'application/json'},
        auth=HTTPBasicAuth('apikey', api_key))
    '''

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    return json_data


def post_request(url, payload, **kwargs):
    '''
    make HTTP POST requests
    e.g., response = requests.post(url, params=kwargs, json=payload)
    '''

    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, headers={
                                 'Content-Type': 'application/json'}, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    '''GET dealers
    - Call get_request() with specified arguments
    - Parse JSON results into a CarDealer object list
    '''
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url)
    if dealers:
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in dealer object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealerId):
    '''
    get reviews by dealer id from a cloud function
    - Call post_request() with specified arguments
    - Parse JSON results into a DealerView object list
    '''
    results = []
    json_result = post_request(url, {'DEALER_ID': dealerId})

    if json_result:
        docs = json_result["docs"]
        for rev in docs:
            review_obj = DealerReview(dealership=rev["dealership"], name=rev["name"], purchase=rev["purchase"],
                                      review=rev["review"], purchase_date=rev["purchase_date"], car_make=rev["car_make"],
                                      car_model=rev["car_model"], car_year=rev["car_year"], sentiment="", id=rev["id"])

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    '''
    call Watson NLU and analyze text
    Call post_request() with specified arguments
    Get the returned sentiment label such as Positive or Negative
    Value from Watson NLU - positive, neutral, negative
    '''
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/77ec479f-bcfa-4ab2-8b39-03ba98a9125c/default/getWatsonSentiment"
    json_result = post_request(url, {'text': text})
    if json_result:
        keywords = json_result["keywords"]
        result = ""
        for keyword in keywords:
            sentiment = keyword["sentiment"]
            result = sentiment["label"]
        return result
