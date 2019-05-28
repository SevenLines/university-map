module.exports = function optSvgLoader(source) {
  let r = source.replace(/(rect|path) id="aud-/, 'auditory id="aud-');
  return r
}