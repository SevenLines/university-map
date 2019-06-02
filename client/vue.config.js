const path = require("path");

module.exports = {
  chainWebpack: (config) => {
    // config.module.rule('opt.svg').uses.clear().end()
    //   .test(/\.opt\.svg$/)
    //     .use("vue-loader").loader("vue-loader").end()
    //     .use('opt-svg-loader').loader(path.resolve(__dirname, 'src/utils/opt_svg_loader.js')).end()
  },
  devServer: {
    proxy: 'http://localhost:8000',
    hot: true
  }
};