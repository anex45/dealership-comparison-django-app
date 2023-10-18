## Steps

```
ibmcloud login
npm run build
ibmcloud fn action update my-action dist/my-action.bundle.js --kind nodejs:18
```