<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8 border-b border-gray-200 pb-4 text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-1 tracking-tight">
        Imparcial
      </h1>
      <div class="w-16 h-0.5 bg-blue-600 mx-auto mb-2"></div>
      <p class="text-base text-gray-600 font-medium">
        news powered by AI
      </p>
    </header>

    <!-- Controls -->
    <div class="mb-8">
      <div class="flex items-center justify-between bg-gray-50 p-4 rounded-md border border-gray-200">
        <div class="flex items-center gap-4">
          <span class="text-sm font-medium text-gray-700">Última actualización:</span>
          <span class="text-sm text-gray-600">{{ formatTime(new Date()) }}</span>
        </div>
        <button
          @click="refreshNews"
          :disabled="loading"
          class="px-6 py-2 bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 rounded-md transition-colors duration-200 font-medium text-sm shadow-sm"
        >
          <RefreshCw class="h-4 w-4 inline mr-2" />
          Actualizar Noticias
        </button>
        <div v-if="loading" class="flex items-center gap-2 text-sm text-gray-500">
          <div class="w-4 h-4 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin"></div>
          Cargando...
        </div>
      </div>
    </div>

    <!-- News Feed -->
    <div v-if="newsData.length === 0" class="text-center py-16">
      <div class="text-gray-500 mb-4">
        <svg class="w-16 h-16 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm14 1a1 1 0 11-2 0 1 1 0 012 0zM2 13a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 01-2 2H4a2 2 0 01-2-2v-2zm14 1a1 1 0 11-2 0 1 1 0 012 0z" clip-rule="evenodd" />
        </svg>
        <h3 class="text-xl font-bold text-gray-700 mb-2">Bienvenido a Imparcial</h3>
        <p class="text-gray-600">
          Haga clic en "Actualizar Noticias" para cargar las últimas noticias de los principales medios argentinos
        </p>
      </div>
    </div>
    
    <div v-else class="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <NewsCard
        v-for="article in newsData"
        :key="article.id"
        :article="article"
        :newspaper-style="true"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RefreshCw } from 'lucide-vue-next'

// News data and loading state
const newsData = ref([])
const loading = ref(false)

const refreshNews = async () => {
  loading.value = true
  await fetchLiveNews()
  loading.value = false
}

const fetchLiveNews = async () => {
  try {
    console.log('Fetching live news...')
    const response = await $fetch('/api/news/live')
    console.log('API Response:', response)
    
    if (response.success && response.data) {
      newsData.value = response.data
      console.log(`Loaded ${response.data.length} live news items`)
    } else {
      console.error('Failed to fetch live news:', response.error)
    }
  } catch (error) {
    console.error('Error fetching live news:', error)
  }
}

const formatTime = (date) => {
  return date.toLocaleTimeString('es-AR', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Auto-load news on page mount
onMounted(() => {
  fetchLiveNews()
})
</script>