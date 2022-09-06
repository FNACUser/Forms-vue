const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  //lintOnSave:false
  transpileDependencies: true,

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'es',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
})
