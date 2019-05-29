const {compileTemplate} = require('@vue/component-compiler-utils')

module.exports = function optSvgLoader(source) {
  let r = source.replace(/(rect|path) id="aud-/, 'auditory id="aud-');

  // const compiler = require('vue-template-compiler')
  //
  // const compiled = compileTemplate({
  //   source: r,
  //   compiler,
  //   filename: this.resourcePath,
  //   prettify: false,
  // })
  // const {code} = compiled
  //
  // // finish with ESM exports
  // let out = code + `\nexport { render, staticRenderFns }`
  // console.log(r)
  return r;
}