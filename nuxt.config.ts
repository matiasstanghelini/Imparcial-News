// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxtjs/tailwindcss'],
  ssr: false,
  compatibilityDate: '2025-06-08',
  app: {
    head: {
      title: 'Imparcial - News Powered by AI',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: 'Imparcial - Noticias argentinas con análisis AI en tiempo real' }
      ]
    }
  },
  nitro: {
    preset: 'node-server'
  },
  devServer: {
    host: '0.0.0.0',
    port: 5000
  }
})
