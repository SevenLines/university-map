module.exports = {
  chainWebpack: (config) => {
    console.log("cool");
    const svgRule = config.module.rule('svg');

    svgRule.uses.clear();

    svgRule
      .use('vue-svg-loader')
      .loader('vue-svg-loader');
  },
  devServer: {
    proxy: 'http://localhost:5000'
  }
};