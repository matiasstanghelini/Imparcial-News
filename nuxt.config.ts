// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxtjs/tailwindcss'],
  ssr: false,
  compatibilityDate: '2025-06-08',
  app: {
    head: {
      title: 'AI News Analysis Platform',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: 'AI-powered news analysis platform' }
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
