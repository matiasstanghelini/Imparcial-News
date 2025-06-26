<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8 pb-4 relative" :class="isDarkMode ? 'border-b border-gray-700' : 'border-b border-gray-200'">
      <!-- Left Controls -->
      <div class="absolute left-0 top-1/2 transform -translate-y-1/2 flex items-center gap-3">
        <!-- Categories Menu -->
        <div class="relative">
          <button 
            @click="toggleCategoriesMenu"
            class="p-2 rounded-lg transition-colors"
            :class="isDarkMode ? 'bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-700 hover:text-gray-900'"
          >
            <Menu class="h-5 w-5" />
          </button>
          
          <!-- Categories Dropdown -->
          <div v-if="showCategoriesMenu" class="absolute top-full left-0 mt-2 rounded-lg shadow-lg min-w-[150px] z-10"
            :class="isDarkMode ? 'bg-gray-800 border border-gray-600' : 'bg-white border border-gray-200'"
          >
            <div 
              v-for="category in categories" 
              :key="category.name"
              @click="selectCategory(category.name)"
              class="px-4 py-2 text-sm cursor-pointer transition-colors"
              :class="category.active ? 'bg-blue-600 text-white' : (isDarkMode ? 'text-gray-300 hover:bg-gray-700 hover:text-white' : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900')"
            >
              {{ category.name }}
            </div>
          </div>
        </div>
        
        <!-- Dark Mode Toggle -->
        <button 
          @click="toggleDarkMode"
          class="p-2 rounded-lg transition-colors"
          :class="isDarkMode ? 'bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-700 hover:text-gray-900'"
        >
          <Moon v-if="isDarkMode" class="h-5 w-5" />
          <Sun v-else class="h-5 w-5" />
        </button>
      </div>
      
      <!-- Center Title -->
      <div class="text-center">
        <h1 class="text-4xl font-bold tracking-tight" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
          Imparcial
        </h1>
        <div class="w-16 h-0.5 bg-blue-600 mx-auto mt-2"></div>
      </div>
    </header>

    <!-- Controls -->
    <div class="mb-8">
      <div class="flex items-center justify-between p-4 rounded-md transition-colors"
        :class="isDarkMode ? 'bg-gray-900 border border-gray-700' : 'bg-gray-50 border border-gray-200'"
      >
        <div class="flex items-center gap-4">
          <span class="text-sm font-medium" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Última actualización:</span>
          <span class="text-sm" :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">{{ formatTime(new Date()) }}</span>
        </div>
        <button
          @click="refreshNews"
          :disabled="loading"
          class="px-6 py-2 bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 rounded-md transition-colors duration-200 font-medium text-sm shadow-sm"
        >
          <RefreshCw class="h-4 w-4 inline mr-2" />
          Actualizar Noticias
        </button>
        <div v-if="loading" class="flex items-center gap-2 text-sm" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">
          <div class="w-4 h-4 border-2 rounded-full animate-spin" 
            :class="isDarkMode ? 'border-gray-600 border-t-blue-600' : 'border-gray-300 border-t-blue-600'"
          ></div>
          Cargando...
        </div>
      </div>
    </div>

    <!-- News Feed -->
    <div v-if="newsData.length === 0" class="text-center py-16">
      <div class="mb-4" :class="isDarkMode ? 'text-gray-400' : 'text-gray-500'">
        <svg class="w-16 h-16 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm14 1a1 1 0 11-2 0 1 1 0 012 0zM2 13a2 2 0 012-2h12a2 2 0 012 2v2a2 2 0 01-2 2H4a2 2 0 01-2-2v-2zm14 1a1 1 0 11-2 0 1 1 0 012 0z" clip-rule="evenodd" />
        </svg>
        <h3 class="text-xl font-bold mb-2" :class="isDarkMode ? 'text-gray-300' : 'text-gray-700'">Bienvenido a Imparcial</h3>
        <p :class="isDarkMode ? 'text-gray-400' : 'text-gray-600'">
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
import { ref, onMounted, inject } from 'vue'
import { RefreshCw, Moon, Sun, Menu } from 'lucide-vue-next'

// News data and loading state
const newsData = ref([])
const loading = ref(false)

// Inject global dark mode state
const isDarkMode = inject('isDarkMode')

// Categories menu state
const showCategoriesMenu = ref(false)
const categories = ref([
  { name: 'Todas', active: true },
  { name: 'Política', active: false },
  { name: 'Economía', active: false },
  { name: 'Deportes', active: false },
  { name: 'Internacionales', active: false }
])

const refreshNews = async () => {
  loading.value = true
  await fetchLiveNews()
  loading.value = false
}

// Dark mode toggle
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
}

// Categories menu toggle
const toggleCategoriesMenu = () => {
  showCategoriesMenu.value = !showCategoriesMenu.value
}

// Select category
const selectCategory = (categoryName) => {
  categories.value.forEach(cat => {
    cat.active = cat.name === categoryName
  })
  showCategoriesMenu.value = false
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

// Auto-load news on page mount (only once with flag)
let newsLoaded = false
onMounted(async () => {
  if (!newsLoaded && newsData.value.length === 0) {
    newsLoaded = true
    await fetchLiveNews()
  }
})
</script>