<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">
        Plataforma de Análisis de Noticias con IA
      </h1>
      <p class="text-lg text-gray-600">
        Verificación inteligente de noticias con agentes de inteligencia artificial
      </p>
    </header>

    <!-- Controls -->
    <div class="mb-6 space-y-4">
      <!-- News Source Toggle -->
      <div class="flex items-center gap-4 bg-white p-4 rounded-lg shadow-sm">
        <span class="text-sm font-medium text-gray-700">Fuente de noticias:</span>
        <div class="flex gap-2">
          <button
            @click="setNewsSource('demo')"
            :class="newsSource === 'demo' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            class="px-4 py-2 rounded-lg transition-colors duration-200 font-medium text-sm"
          >
            Noticias de Ejemplo
          </button>
          <button
            @click="setNewsSource('live')"
            :class="newsSource === 'live' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            class="px-4 py-2 rounded-lg transition-colors duration-200 font-medium text-sm"
          >
            Noticias en Vivo
          </button>
          <button
            v-if="newsSource === 'live'"
            @click="refreshNews"
            :disabled="loading"
            class="px-3 py-2 bg-blue-100 text-blue-700 hover:bg-blue-200 disabled:opacity-50 rounded-lg transition-colors duration-200 font-medium text-sm"
          >
            🔄 Actualizar
          </button>
        </div>
        <div v-if="loading" class="flex items-center gap-2 text-sm text-gray-500">
          <div class="w-4 h-4 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
          Cargando...
        </div>
      </div>

      <!-- Agent Toggle Controls -->
      <AgentToggle 
        :visible-agents="visibleAgents" 
        @toggle="toggleAgent" 
      />
    </div>

    <!-- News Feed -->
    <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
      <NewsCard
        v-for="article in newsData"
        :key="article.id"
        :article="article"
        :visible-agents="visibleAgents"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { news } from '~/data/news.js'

// News data and source management
const newsData = ref(news)
const newsSource = ref('demo') // 'demo' or 'live'
const loading = ref(false)

// Agent visibility state
const visibleAgents = ref({
  logic: true,
  context: true,
  expert: true,
  synth: true
})

// Toggle agent visibility
const toggleAgent = (agentType) => {
  visibleAgents.value[agentType] = !visibleAgents.value[agentType]
}

// Set news source
const setNewsSource = async (source) => {
  if (source === newsSource.value) return
  
  loading.value = true
  
  try {
    if (source === 'live') {
      console.log('Fetching live news...')
      const response = await $fetch('/api/news/live')
      console.log('API Response:', response)
      
      if (response && response.success && response.data && response.data.length > 0) {
        newsData.value = response.data
        newsSource.value = 'live'
        console.log(`Loaded ${response.data.length} live news items`)
      } else {
        console.error('API response error:', response)
        newsData.value = news
        newsSource.value = 'demo'
        alert('Error obteniendo noticias en vivo. Mostrando noticias de ejemplo.')
      }
    } else {
      // Use demo news
      newsData.value = news
      newsSource.value = 'demo'
    }
  } catch (error) {
    console.error('Network error:', error)
    newsData.value = news
    newsSource.value = 'demo'
    alert('Error de conexión. Mostrando noticias de ejemplo.')
  } finally {
    loading.value = false
  }
}

// Refresh news function
const refreshNews = () => {
  if (newsSource.value === 'live') {
    setNewsSource('live')
  }
}
</script>
