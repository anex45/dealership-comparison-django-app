const path = require('path');

module.exports = {
  entry: {
    getAllDealerships: './getAllDealerships.js',
    getDealershipByState: './getDealershipByState.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].bundle.js'
  },
  externals: {
    cloudant: '@ibm-cloud/cloudant',
    cloudantSdk: 'ibm-cloud-sdk-core'
  },
  target: 'node',
  mode: 'development'
};