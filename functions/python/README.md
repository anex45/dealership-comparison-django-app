```
ibmcloud login
ibmcloud target -g Default
ibmcloud fn property set --namespace 77ec479f-bcfa-4ab2-8b39-03ba98a9125c
```
ZIP the files separately. Both py files have to have naming convention as follows: `__main__.py`

Finally
```
ibmcloud fn action update getReviewsByDealerId .\get_reviews_by_dealer_id.zip --kind python:3.11
```