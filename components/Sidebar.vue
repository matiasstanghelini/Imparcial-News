<template>
  <div>
    <!-- Overlay -->
    <div 
      v-if="isOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
      @click="closeSidebar"
    ></div>
    
    <!-- Sidebar -->
    <aside 
      class="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-900 shadow-lg transform transition-transform duration-300 ease-in-out z-50"
      :class="{ 'translate-x-0': isOpen, '-translate-x-full': !isOpen }"
    >
      <div class="h-full flex flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Categorías</h2>
          <button 
            @click="closeSidebar"
            class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Categories -->
        <nav class="flex-1 overflow-y-auto">
          <ul class="space-y-1 p-2">
            <li v-for="category in categories" :key="category.slug">
              <NuxtLink
                :to="`/noticias/${category.slug}`"
                class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                :class="{ 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400': $route.params.category === category.slug }"
                @click="closeSidebar"
              >
                <span class="w-2 h-2 rounded-full mr-3" :class="getCategoryColor(category.slug)"></span>
                <span class="font-medium">{{ category.name }}</span>
                <span class="ml-auto bg-gray-100 dark:bg-gray-800 text-xs font-medium px-2 py-0.5 rounded-full">
                  {{ getCategoryCount(category.slug) }}
                </span>
              </NuxtLink>
            </li>
          </ul>
        </nav>
        
        <!-- Footer -->
        <div class="p-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ totalArticles }} noticias</span>
            <button 
              @click="toggleDarkMode"
              class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300"
              :aria-label="isDarkMode ? 'Modo claro' : 'Modo oscuro'"
            >
              <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  news: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'toggleDarkMode'])

// Categorías predefinidas
const categories = [
  { slug: 'politica', name: 'Política' },
  { slug: 'economia', name: 'Economía' },
  { slug: 'tecnologia', name: 'Tecnología' },
  { slug: 'deportes', name: 'Deportes' },
  { slug: 'general', name: 'General' }
]

// Contar noticias por categoría
const categoryCounts = computed(() => {
  const counts = {}
  categories.forEach(cat => {
    counts[cat.slug] = props.news.filter(n => 
      n.category === cat.slug || n.categories?.includes(cat.slug)
    ).length
  })
  return counts
})

// Contar total de noticias
const totalArticles = computed(() => props.news.length)

// Cerrar sidebar al cambiar de ruta
watch(() => route.path, () => {
  closeSidebar()
})

// Cerrar con tecla Escape
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.isOpen) {
    closeSidebar()
  }
}

// Agregar/remover event listener
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const closeSidebar = () => {
  emit('close')
}

const toggleDarkMode = () => {
  emit('toggleDarkMode')
}

const getCategoryColor = (category) => {
  const colors = {
    politica: 'bg-red-500',
    economia: 'bg-blue-500',
    tecnologia: 'bg-purple-500',
    deportes: 'bg-green-500',
    general: 'bg-gray-500'
  }
  return colors[category] || 'bg-gray-400'
}

const getCategoryCount = (category) => {
  return categoryCounts.value[category] || 0
}

// Inyectar el estado del modo oscuro
const isDarkMode = inject('isDarkMode', ref(false))
</script>
