<template>
  <article class="bg-white border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
    <!-- News Image Placeholder -->
    <div class="relative">
      <div class="w-full h-48 bg-gray-100 border-b border-gray-200 flex items-center justify-center">
        <div class="text-center text-gray-400">
          <svg class="w-16 h-16 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
          </svg>
          <p class="text-sm font-medium">Imagen no disponible</p>
        </div>
      </div>
      
      <!-- Media Logo Overlay -->
      <div class="absolute top-3 left-3">
        <MediaLogo :source="article.source" />
      </div>
      
      <!-- External Link Button -->
      <div class="absolute top-3 right-3">
        <button 
          @click.stop="openExternalLink" 
          class="bg-white bg-opacity-90 hover:bg-opacity-100 p-2 rounded-full shadow-sm transition-all duration-200"
          title="Ir al artículo original"
        >
          <ExternalLink class="h-4 w-4 text-gray-700" />
        </button>
      </div>
    </div>

    <!-- News Content -->
    <div class="p-5">
      <!-- Publication Date -->
      <div class="text-xs text-gray-500 mb-2 font-serif">
        {{ formatDate(article.date) }}
      </div>
      
      <!-- Headline -->
      <h2 
        class="text-lg font-bold text-gray-900 mb-3 leading-tight cursor-pointer hover:text-red-800 transition-colors font-serif"
        @click="goToDetail"
      >
        {{ article.title }}
      </h2>
      
      <!-- Summary -->
      <p class="text-gray-700 text-sm leading-relaxed mb-4 line-clamp-3 font-serif">
        {{ article.summary }}
      </p>
      
      <!-- Action Button -->
      <div class="flex justify-between items-center pt-3 border-t border-gray-100">
        <button
          @click="goToDetail"
          class="text-red-800 hover:text-red-900 font-medium text-sm transition-colors font-serif"
        >
          Leer artículo completo →
        </button>
        
        <!-- Source Credit -->
        <span class="text-xs text-gray-500 font-serif">
          {{ article.source }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ExternalLink } from 'lucide-vue-next'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  newspaperStyle: {
    type: Boolean,
    default: false
  }
})

const goToDetail = () => {
  if (props.article.id) {
    navigateTo(`/noticia/${props.article.id}`)
  }
}

const openExternalLink = () => {
  if (props.article.url) {
    window.open(props.article.url, '_blank')
  }
}

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-AR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long', 
      day: 'numeric'
    }).replace(/^\w/, (c) => c.toUpperCase())
  } catch (e) {
    return dateString
  }
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>