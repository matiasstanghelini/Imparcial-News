<template>
  <article 
    class="bg-white border border-gray-200 hover:border-gray-300 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer group overflow-hidden"
    @click="goToDetail"
  >
    <!-- News Image Placeholder -->
    <div class="relative">
      <div class="w-full h-40 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center group-hover:from-gray-200 group-hover:to-gray-300 transition-all duration-200">
        <div class="text-center text-gray-500">
          <svg class="w-12 h-12 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
          </svg>
          <p class="text-xs font-medium">Imagen</p>
        </div>
      </div>
      
      <!-- Media Logo Overlay -->
      <div class="absolute top-2 left-2">
        <MediaLogo :source="article.source" />
      </div>
      
      <!-- AI Analysis Badge -->
      <div class="absolute top-2 right-2">
        <div class="bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          AI
        </div>
      </div>
    </div>

    <!-- News Content -->
    <div class="p-4">
      <!-- Source and Time -->
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs font-medium text-blue-600 uppercase tracking-wide">
          {{ article.source }}
        </span>
        <span class="text-xs text-gray-500">
          {{ formatTime(article.date) }}
        </span>
      </div>
      
      <!-- Headline -->
      <h2 class="text-base font-bold text-gray-900 mb-2 leading-tight group-hover:text-blue-600 transition-colors line-clamp-2">
        {{ article.title }}
      </h2>
      
      <!-- Summary -->
      <p class="text-gray-600 text-sm leading-relaxed mb-3 line-clamp-2">
        {{ article.summary }}
      </p>
      
      <!-- AI Analysis Preview -->
      <div class="bg-blue-50 border-l-3 border-blue-400 p-2 rounded-r">
        <div class="flex items-center gap-2 mb-1">
          <svg class="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/>
          </svg>
          <span class="text-xs font-medium text-blue-700">Análisis AI disponible</span>
        </div>
        <p class="text-xs text-blue-600">
          Haz clic para ver análisis completo con verificación de fuentes
        </p>
      </div>
    </div>
  </article>
</template>

<script setup>
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

const formatTime = (dateString) => {
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
    
    if (diffInHours < 1) {
      return 'Hace unos minutos'
    } else if (diffInHours < 24) {
      return `Hace ${diffInHours}h`
    } else {
      return date.toLocaleDateString('es-AR', {
        day: 'numeric',
        month: 'short'
      })
    }
  } catch (e) {
    return 'Reciente'
  }
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

.border-l-3 {
  border-left-width: 3px;
}
</style>