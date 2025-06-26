<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-4">
            <button @click="$router.back()" class="flex items-center text-gray-600 hover:text-gray-900">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
              </svg>
              Volver
            </button>
            <h1 class="text-2xl font-bold text-gray-900">
              <NuxtLink to="/noticias" class="hover:text-blue-600">Noticias</NuxtLink>
              <span class="mx-2 text-gray-400">/</span>
              <NuxtLink :to="`/noticias/${article?.category || 'general'}`" class="hover:text-blue-600">
                {{ getCategoryName(article?.category || 'general') }}
              </NuxtLink>
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium" 
                  :class="getCategoryClass(article?.category || 'general')">
              {{ getCategoryName(article?.category || 'general') }}
            </span>
            <a v-if="article?.url" :href="article.url" target="_blank" 
               class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              Ver Original
            </a>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="loading" class="text-center py-12">
        <div class="flex flex-col items-center justify-center space-y-4">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="text-gray-600">Cargando noticia...</p>
        </div>
      </div>

      <div v-else-if="error" class="bg-red-50 text-red-700 p-6 rounded-lg my-8 text-center">
        <p>{{ error }}</p>
        <button 
          @click="fetchArticle" 
          class="mt-4 px-4 py-2 bg-red-100 text-red-700 rounded-md hover:bg-red-200"
        >
          Reintentar
        </button>
      </div>

      <div v-else class="bg-white rounded-lg shadow-sm overflow-hidden">
        <!-- Imagen destacada (si existe) -->
        <div v-if="article.image" class="h-64 bg-gray-200 overflow-hidden">
          <img :src="article.image" :alt="article.title" class="w-full h-full object-cover">
        </div>
        
        <div class="p-6">
          <!-- Metadatos -->
          <div class="flex items-center justify-between mb-6 pb-4 border-b">
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <span class="inline-flex items-center justify-center h-10 w-10 rounded-full bg-gray-100">
                  <span class="text-gray-600 font-medium">{{ article.source.charAt(0) }}</span>
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ article.source }}</p>
                <div class="flex space-x-1 text-sm text-gray-500">
                  <time :datetime="article.date">{{ formatDate(article.date) }}</time>
                  <span aria-hidden="true">&middot;</span>
                  <span>Tiempo de lectura: {{ readingTime }} min</span>
                </div>
              </div>
            </div>
            <div class="flex items-center">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" 
                    :class="getVerdictClass(article.verdict)">
                {{ getVerdictText(article.verdict) }}
              </span>
            </div>
          </div>
          
          <!-- Título -->
          <h1 class="text-3xl font-bold text-gray-900 mb-6">{{ article.title }}</h1>
          
          <!-- Resumen -->
          <div class="prose max-w-none mb-8">
            <p class="text-lg text-gray-700 leading-relaxed">{{ article.summary }}</p>
          </div>
          
          <!-- Contenido completo -->
          <div class="prose max-w-none mb-8">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">Contenido Completo</h2>
            <div v-if="fullContent" class="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {{ fullContent }}
            </div>
            <div v-else class="flex items-center space-x-2 text-gray-500">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span>Obteniendo contenido completo...</span>
            </div>
          </div>
          
          <!-- Análisis de agentes -->
          <div class="mt-12 pt-8 border-t">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Análisis de Agentes IA</h2>
            
            <div class="space-y-6">
              <div v-for="(agent, key) in agents" :key="key" class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <h3 class="text-lg font-medium text-gray-900 flex items-center">
                    <component :is="agent.icon" class="h-5 w-5 mr-2" :class="getAgentColor(key)" />
                    {{ agent.name }}
                  </h3>
                </div>
                <div class="prose max-w-none text-gray-700">
                  <p v-if="typeof article.agents?.[key] === 'string'">{{ article.agents[key] }}</p>
                  <ul v-else-if="Array.isArray(article.agents?.[key])">
                    <li v-for="(item, i) in article.agents[key]" :key="i" class="mb-1">{{ item }}</li>
                  </ul>
                  <p v-else class="text-gray-500 italic">Análisis no disponible</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Enlace a la fuente -->
          <div class="mt-8 pt-6 border-t">
            <a :href="article.url" target="_blank" 
               class="inline-flex items-center text-blue-600 hover:text-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              Leer artículo completo en {{ article.source }}
            </a>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Estados reactivos
const article = ref(null)
const fullContent = ref('')
const loading = ref(true)
const error = ref(null)

// Agentes disponibles
const agents = {
  logic: { name: 'Análisis Lógico', icon: 'LightBulbIcon' },
  context: { name: 'Contexto', icon: 'BookOpenIcon' },
  expert: { name: 'Análisis Experto', icon: 'UserIcon' },
  synth: { name: 'Síntesis', icon: 'ChartBarIcon' }
}

// Obtener la noticia
const fetchArticle = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Extraer ID de la URL amigable
    const newsId = route.params.id.split('-')[0]
    
    // Obtener la noticia de la API externa
    const response = await $fetch(`http://localhost:8000/news/${newsId}`)
    
    if (response && response.article) {
      article.value = {
        ...response.article,
        // Asegurar que los campos requeridos existan
        id: response.article.id || newsId,
        slug: response.article.slug || response.article.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''),
        category: response.article.category || 'general',
        verdict: response.article.verdict || 'unverified',
        date: response.article.date || new Date().toISOString(),
        source: response.article.source || 'Fuente desconocida'
      }
      
      // Obtener contenido completo si es necesario
      if (response.article.url) {
        fetchFullContent(response.article.url)
      }
      
      // Verificar que la categoría en la URL coincida
      if (route.params.categoria !== article.value.category) {
        router.replace(`/noticias/${article.value.category}/${article.value.id}-${article.value.slug}`)
      }
    } else {
      throw new Error('No se encontró la noticia')
    }
  } catch (err) {
    console.error('Error cargando noticia:', err)
    error.value = 'No se pudo cargar la noticia. Por favor, intente más tarde.'
    router.push('/noticias')
  } finally {
    loading.value = false
  }
}

// Cargar la noticia al montar el componente
onMounted(() => {
  fetchArticle()
})

// Tiempo estimado de lectura
const readingTime = computed(() => {
  if (!article.value) return 2
  const words = (article.value.summary || '').split(/\s+/).length
  return Math.max(1, Math.round(words / 200)) // 200 palabras por minuto
})

// Funciones de utilidad
const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('es-AR', options)
}

const getVerdictClass = (verdict) => {
  switch(verdict) {
    case 'true': return 'bg-green-100 text-green-800'
    case 'false': return 'bg-red-100 text-red-800'
    case 'uncertain': return 'bg-yellow-100 text-yellow-800'
    default: return 'bg-gray-100 text-gray-800'
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

const getAgentColor = (agentKey) => {
  const colors = {
    logic: 'text-yellow-600',
    context: 'text-blue-600',
    expert: 'text-green-600',
    synth: 'text-purple-600'
  }
  return colors[agentKey] || 'text-gray-600'
}

const fetchFullContent = async (url) => {
  try {
    fullContent.value = 'Cargando contenido completo...'
    
    // Si la API ya proporciona el contenido, usarlo
    if (article.value?.content) {
      fullContent.value = article.value.content
      return
    }
    
    // Si no, intentar obtenerlo de la URL
    if (url) {
      // Nota: Necesitarás implementar un endpoint en tu API para extraer contenido
      // o usar una solución del lado del cliente
      const response = await $fetch('http://localhost:8000/content/extract', {
        method: 'POST',
        body: { url }
      })
      
      if (response?.content) {
        fullContent.value = response.content
      } else {
        throw new Error('No se pudo extraer el contenido')
      }
    } else {
      throw new Error('No hay URL disponible para extraer contenido')
    }
  } catch (error) {
    console.error('Error obteniendo contenido:', error)
    fullContent.value = 'No se pudo cargar el contenido completo del artículo. Puedes leer la noticia original haciendo clic en "Ver Original".'
  }
}
</script>

<style scoped>
.prose {
  max-width: 100%;
}

.prose p {
  margin-bottom: 1em;
  line-height: 1.7;
}

.prose ul {
  list-style-type: disc;
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.prose li {
  margin-bottom: 0.5em;
}
</style>
