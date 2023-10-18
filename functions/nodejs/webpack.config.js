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
  target: 'node'
};