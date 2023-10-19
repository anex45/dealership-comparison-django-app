## Steps

```
ibmcloud login
ibmcloud fn property set --namespace 77ec479f-bcfa-4ab2-8b39-03ba98a9125c
npm run build
ibmcloud fn action update getAllDealerships .\dist\getAllDealerships.bundle.js --kind nodejs:20
```