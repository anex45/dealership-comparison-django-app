## IBM Cloud functions
Capstone project - Dealership website

To work with these functions, you have to follow the steps below.

1. Login to IBM Cloud in your terminal
```
ibmcloud login -a https://cloud.ibm.com -u passcode -p <passcode>
```
Choose `us-south` from the list
```
ibmcloud target -g Default
ibmcloud fn property set --namespace 77ec479f-bcfa-4ab2-8b39-03ba98a9125c
```

2. ZIP the files separately. Both `.py` files have to have naming convention as follows: `__main__.py` inside ZIP.

3. Update functions on IBM Cloud. Example:
```
ibmcloud fn action update getReviewsByDealerId .\get_reviews_by_dealer_id.zip --kind python:3.11
```
4. Invoke a function from the cloud:
```
ibmcloud fn invoke getReviewsByDealerId --result --param DEALER_ID 15
```
5. Test with Postman or Curl:
```
https://us-south.functions.appdomain.cloud/api/v1/web/77ec479f-bcfa-4ab2-8b39-03ba98a9125c/default/getReviewsByDealerId
```