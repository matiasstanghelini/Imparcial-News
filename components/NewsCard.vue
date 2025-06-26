<template>
  <article 
    class="shadow-sm hover:shadow-lg transition-all duration-200 cursor-pointer group rounded-lg p-4"
    :class="isDarkMode ? 'bg-gray-900 border border-gray-700 hover:border-blue-500' : 'bg-white border border-gray-200 hover:border-blue-200'"
    @click="goToDetail"
  >
    <!-- Media Logo and Source -->
    <div class="mb-3">
      <MediaLogo :source="article.source" />
    </div>
    
    <!-- Headline -->
    <h2 class="text-base font-bold mb-2 leading-tight transition-colors"
      :class="isDarkMode ? 'text-white group-hover:text-blue-400' : 'text-gray-900 group-hover:text-blue-600'"
    >
      {{ article.title }}
    </h2>
    
    <!-- Summary -->
    <p class="text-sm leading-relaxed" :class="isDarkMode ? 'text-gray-300' : 'text-gray-600'">
      {{ article.summary }}
    </p>
  </article>
</template>

<script setup>
import { inject } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

// Inject global dark mode state
const isDarkMode = inject('isDarkMode')

const goToDetail = () => {
  navigateTo(`/noticia/${props.article.id}`)
}
</script>