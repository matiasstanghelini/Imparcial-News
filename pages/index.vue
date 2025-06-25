<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8 border-b-4 border-red-800 pb-6">
      <h1 class="text-5xl font-bold text-gray-900 mb-2 font-serif">
        Noticias Argentina
      </h1>
      <p class="text-lg text-gray-600 font-serif italic">
        Las últimas noticias de los principales medios del país
      </p>
    </header>

    <!-- Controls -->
    <div class="mb-8">
      <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg border-l-4 border-red-800">
        <div class="flex items-center gap-4">
          <span class="text-sm font-medium text-gray-700">Última actualización:</span>
          <span class="text-sm text-gray-600">{{ formatTime(new Date()) }}</span>
        </div>
        <button
          @click="refreshNews"
          :disabled="loading"
          class="px-4 py-2 bg-red-800 text-white hover:bg-red-900 disabled:opacity-50 rounded-lg transition-colors duration-200 font-medium text-sm"
        >
          🔄 Actualizar Noticias
        </button>
        <div v-if="loading" class="flex items-center gap-2 text-sm text-gray-500">
          <div class="w-4 h-4 border-2 border-gray-300 border-t-red-800 rounded-full animate-spin"></div>
          Cargando...
        </div>
      </div>
    </div>

    <!-- News Feed -->
    <div class="grid gap-8 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3">
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

// News data and loading state
const newsData = ref([])
const loading = ref(false)

// Initialize with live news on mount
onMounted(() => {
  fetchLiveNews()
})

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
</script>