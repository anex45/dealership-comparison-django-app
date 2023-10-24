## IBM Cloud functions
Capstone project - Node.js functions

To work with these functions, you have to follow the steps below.

1. Log in to IBM Cloud in your terminal:
```
ibmcloud login -a https://cloud.ibm.com -u passcode -p <passcode>
```
Choose `us-south` from the list
```
ibmcloud target -g Default
ibmcloud fn property set --namespace 77ec479f-bcfa-4ab2-8b39-03ba98a9125c
```
2. Bundle the code:
```
npm run build
```
3. Update the cloud functions:
```
ibmcloud fn action update getAllDealerships .\dist\getAllDealerships.bundle.js --kind nodejs:20
```
4. Invoke a function from the cloud:
```
ibmcloud fn invoke getAllDealerships --result
```
5. Test with Postman or Curl:
```
https://us-south.functions.appdomain.cloud/api/v1/web/77ec479f-bcfa-4ab2-8b39-03ba98a9125c/default/getAllDealerships
```