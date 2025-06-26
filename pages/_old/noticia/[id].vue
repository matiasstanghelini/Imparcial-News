<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-4">
            <button @click="$router.back()" class="flex items-center text-gray-600 hover:text-gray-900">
              <ArrowLeft class="h-5 w-5 mr-2" />
              Volver
            </button>
            <h1 class="text-2xl font-bold text-gray-900">Análisis de Noticia</h1>
          </div>
          <div class="flex items-center space-x-4">
            <MediaLogo v-if="article" :source="article.source" />
            <a v-if="article" :href="article.url" target="_blank" 
               class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
              <ExternalLink class="h-4 w-4 mr-2" />
              Ver Original
            </a>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div v-if="!article" class="text-center py-12">
        <div class="text-gray-500">Cargando noticia...</div>
      </div>
      
      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Contenido de la noticia (izquierda) -->
        <div class="lg:col-span-2">
          <article class="bg-white rounded-lg shadow-sm p-6">
            <!-- Título -->
            <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ article.title }}</h1>
            
            <!-- Metadatos -->
            <div class="flex items-center justify-between mb-6 pb-4 border-b">
              <div class="flex items-center space-x-4">
                <MediaLogo :source="article.source" />
                <span class="text-sm text-gray-600">{{ article.source }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="flex items-center space-x-1">
                  <div :class="getVerdictColor(article.verdict)" class="w-3 h-3 rounded-full"></div>
                  <span class="text-sm font-medium capitalize">{{ getVerdictText(article.verdict) }}</span>
                </div>
              </div>
            </div>

            <!-- Resumen -->
            <div class="mb-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-3">Resumen</h2>
              <p class="text-gray-700 leading-relaxed">{{ article.summary }}</p>
            </div>

            <!-- Contenido completo -->
            <div class="mb-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-3">Contenido Completo</h2>
              <div class="prose max-w-none">
                <div v-if="fullContent" class="text-gray-700 leading-relaxed whitespace-pre-wrap">{{ fullContent }}</div>
                <div v-else class="text-gray-500 italic">
                  <div class="flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                    <span>Obteniendo contenido completo...</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Enlace a la fuente -->
            <div class="pt-4 border-t">
              <a :href="article.url" target="_blank" 
                 class="inline-flex items-center text-blue-600 hover:text-blue-800">
                <ExternalLink class="h-4 w-4 mr-2" />
                Leer artículo completo en {{ article.source }}
              </a>
            </div>
          </article>
        </div>

        <!-- Panel de análisis AI (derecha) -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Análisis de Agentes IA</h2>
            
            <!-- Controles de agentes -->
            <div class="mb-6">
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="(agent, key) in agents"
                  :key="key"
                  @click="toggleAgent(key)"
                  :class="[
                    'flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-colors',
                    visibleAgents[key] 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  <component :is="agent.icon" class="h-4 w-4 mr-2" />
                  {{ agent.name }}
                </button>
              </div>
            </div>

            <!-- Análisis de cada agente -->
            <div class="space-y-4">
              <div v-for="(agent, key) in agents" :key="key" v-show="visibleAgents[key]" 
                   class="border rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center space-x-2">
                    <component :is="agent.icon" class="h-5 w-5 text-gray-700" />
                    <h3 class="font-semibold text-gray-900">{{ agent.name }}</h3>
                  </div>
                  <div class="flex items-center space-x-1">
                    <div :class="getVerdictColor(article.verdict)" class="w-2 h-2 rounded-full"></div>
                    <span class="text-xs text-gray-500">{{ getVerdictText(article.verdict) }}</span>
                  </div>
                </div>
                
                <div class="text-sm text-gray-700">
                  <div v-if="key === 'synth' && Array.isArray(article.agents[key])">
                    <ul class="list-disc list-inside space-y-1">
                      <li v-for="point in article.agents[key]" :key="point">{{ point }}</li>
                    </ul>
                  </div>
                  <div v-else>
                    {{ article.agents[key] }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Botón de actualizar análisis -->
            <div class="mt-6 pt-4 border-t">
              <button 
                @click="refreshAnalysis"
                :disabled="analyzing"
                class="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
              >
                <div v-if="analyzing" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                <RefreshCw v-else class="h-4 w-4 mr-2" />
                {{ analyzing ? 'Analizando...' : 'Actualizar Análisis' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowLeft, ExternalLink, RefreshCw, Brain, BookOpen, UserCheck, BarChart3 } from 'lucide-vue-next'
import MediaLogo from '~/components/MediaLogo.vue'

const route = useRoute()
const router = useRouter()

// Estados reactivos
const article = ref(null)
const fullContent = ref('')
const analyzing = ref(false)

// Agentes disponibles
const agents = {
  logic: { name: 'Lógica', icon: Brain },
  context: { name: 'Contexto', icon: BookOpen },
  expert: { name: 'Experto', icon: UserCheck },
  synth: { name: 'Síntesis', icon: BarChart3 }
}

// Visibilidad de agentes
const visibleAgents = ref({
  logic: true,
  context: true,
  expert: true,
  synth: true
})

// Funciones de utilidad
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
    case 'uncertain': return 'Incierto'
    default: return 'Sin verificar'
  }
}

const toggleAgent = (agentType) => {
  visibleAgents.value[agentType] = !visibleAgents.value[agentType]
}

const refreshAnalysis = async () => {
  analyzing.value = true
  // Simular análisis AI
  await new Promise(resolve => setTimeout(resolve, 2000))
  analyzing.value = false
}

const fetchFullContent = async (url) => {
  try {
    const response = await $fetch('/api/content/extract', {
      method: 'POST',
      body: { url }
    })
    if (response.success) {
      fullContent.value = response.content
    }
  } catch (error) {
    console.error('Error obteniendo contenido:', error)
    fullContent.value = 'No se pudo obtener el contenido completo del artículo.'
  }
}

onMounted(async () => {
  const newsId = parseInt(route.params.id)
  
  // Obtener la noticia desde el estado global o API
  try {
    const newsData = await $fetch('/api/news/live')
    if (newsData.success) {
      article.value = newsData.data.find(item => item.id === newsId)
    }
    
    if (!article.value) {
      // Fallback a noticias demo
      const { news } = await import('~/data/news.js')
      article.value = news.find(item => item.id === newsId)
    }
    
    if (article.value) {
      // Obtener contenido completo
      await fetchFullContent(article.value.url)
    } else {
      router.push('/')
    }
  } catch (error) {
    console.error('Error cargando noticia:', error)
    router.push('/')
  }
})
</script>