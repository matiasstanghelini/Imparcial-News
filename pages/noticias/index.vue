<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Mostrar estado de carga -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Cargando noticias...</p>
    </div>
    
    <!-- Mostrar mensaje de error -->
    <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg mb-6">
      {{ error }}
    </div>
    <h1 class="text-3xl font-bold mb-8">Últimas Noticias</h1>
    
    <!-- Navegación por categorías -->
    <div class="mb-8">
      <div class="flex flex-wrap gap-2">
        <NuxtLink 
          v-for="category in categories" 
          :key="category.slug"
          :to="`/noticias/${category.slug}`"
          class="px-4 py-2 rounded-full text-sm font-medium"
          :class="{
            'bg-blue-600 text-white': $route.params.category === category.slug,
            'bg-gray-100 text-gray-700 hover:bg-gray-200': $route.params.category !== category.slug
          }"
        >
          {{ category.name }}
        </NuxtLink>
      </div>
    </div>
    
    <!-- Lista de noticias -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="article in filteredNews" 
        :key="article.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
      >
        <NuxtLink :to="`/noticias/${article.category}/${article.id}-${article.slug}`">
          <div class="p-6">
            <div class="flex justify-between items-center mb-2">
              <span class="text-sm text-gray-500">{{ article.source }}</span>
              <span class="inline-block px-2 py-1 text-xs rounded-full" 
                    :class="getCategoryClass(article.category)">
                {{ getCategoryName(article.category) }}
              </span>
            </div>
            <h2 class="text-xl font-semibold mb-2 line-clamp-2">{{ article.title }}</h2>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">{{ article.summary }}</p>
            <div class="flex justify-between items-center text-sm text-gray-500">
              <span>{{ formatDate(article.date) }}</span>
              <span class="inline-flex items-center">
                <span class="w-2 h-2 rounded-full mr-1" 
                      :class="getVerdictColor(article.verdict)"></span>
                {{ getVerdictText(article.verdict) }}
              </span>
            </div>
          </div>
        </NuxtLink>
      </div>
    </div>
    
    <!-- Mensaje si no hay noticias -->
    <div v-if="filteredNews.length === 0" class="text-center py-12">
      <p class="text-gray-500">No se encontraron noticias en esta categoría.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const news = ref([])

// Categorías disponibles (se cargarán desde la API)
const categories = ref([])

// Obtener categorías de la API
const fetchCategories = async () => {
  try {
    const categoriesData = await $fetch('http://localhost:8000/categories')
    if (categoriesData && Array.isArray(categoriesData)) {
      categories.value = categoriesData.map(cat => ({
        slug: cat.slug || cat.name.toLowerCase(),
        name: cat.name
      }))
    }
  } catch (err) {
    console.error('Error cargando categorías:', err)
    // Valores por defecto en caso de error
    categories.value = [
      { slug: 'politica', name: 'Política' },
      { slug: 'economia', name: 'Economía' },
      { slug: 'tecnologia', name: 'Tecnología' },
      { slug: 'deportes', name: 'Deportes' },
      { slug: 'general', name: 'General' }
    ]
  }
}

// Cargar categorías al montar el componente
onMounted(() => {
  fetchNews()
  fetchCategories()
})

// Obtener noticias y categorías
const loading = ref(true)
const error = ref(null)

const fetchNews = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Obtener noticias de la API externa
    const newsData = await $fetch('http://localhost:8000/news?limit=100')
    
    if (newsData && Array.isArray(newsData.articles)) {
      news.value = newsData.articles.map(article => ({
        ...article,
        // Mapear campos si es necesario para mantener compatibilidad
        id: article.id || article._id,
        slug: article.slug || article.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
      }))
    } else {
      throw new Error('Formato de datos inválido')
    }
  } catch (err) {
    console.error('Error cargando noticias:', err)
    error.value = 'No se pudieron cargar las noticias. Por favor, intente más tarde.'
  } finally {
    loading.value = false
  }
}

// Cargar datos al montar el componente
onMounted(() => {
  fetchNews()
})

// Filtrar noticias por categoría
const filteredNews = computed(() => {
  if (!route.params.category) return news.value
  return news.value.filter(article => 
    article.category === route.params.category || 
    article.categories?.includes(route.params.category)
  )
})

// Funciones de utilidad
const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-AR', options)
}

const getVerdictColor = (verdict) => {
  switch(verdict) {
    case 'true': return 'bg-green-500'
    case 'false': return 'bg-red-500'
    case 'uncertain': return 'bg-yellow-500'
    default: return 'bg-gray-400'
  }
}

const getVerdictText = (verdict) => {
  switch(verdict) {
    case 'true': return 'Verificado'
    case 'false': return 'Falso'
    case 'uncertain': return 'En verificación'
    default: return 'No verificado'
  }
}

const getCategoryClass = (category) => {
  const classes = {
    politica: 'bg-red-100 text-red-800',
    economia: 'bg-blue-100 text-blue-800',
    tecnologia: 'bg-purple-100 text-purple-800',
    deportes: 'bg-green-100 text-green-800',
    general: 'bg-gray-100 text-gray-800'
  }
  return classes[category] || 'bg-gray-100 text-gray-800'
}

const getCategoryName = (category) => {
  const names = {
    politica: 'Política',
    economia: 'Economía',
    tecnologia: 'Tecnología',
    deportes: 'Deportes',
    general: 'General'
  }
  return names[category] || category
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
