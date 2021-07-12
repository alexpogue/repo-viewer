const path = require('path');
const argv = require('optimist').argv;

let config = {};
let command = argv['_'][0];
switch(command) {
  case 'build':
    config = {
      outputDir: '../server/repo_viewer/static/gen',
      assetsDir: './',                             // relative to outputDir
      indexPath: '../../templates/gen/index.html', // relative to outputDir
    };
    break;
  case 'serve':
    config = {
      devServer: {
        proxy: 'http://localhost:8080'
      }
    }
}

module.exports = config
