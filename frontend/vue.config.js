const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
   transpileDependencies: ['vuetify'],
  outputDir: '../frontend/dist',
  publicPath: './',
});