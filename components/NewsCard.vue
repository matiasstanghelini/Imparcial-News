<template>
  <article 
    class="bg-gray-900 border border-gray-700 hover:border-blue-500 shadow-sm hover:shadow-lg transition-all duration-200 cursor-pointer group rounded-lg p-4"
    @click="goToDetail"
  >
    <!-- Media Logo and Source -->
    <div class="mb-3">
      <MediaLogo :source="article.source" />
    </div>
    
    <!-- Headline -->
    <h2 class="text-base font-bold text-white mb-2 leading-tight group-hover:text-blue-400 transition-colors">
      {{ article.title }}
    </h2>
    
    <!-- Summary -->
    <p class="text-sm text-gray-300 leading-relaxed">
      {{ article.summary }}
    </p>
  </article>
</template>

<script setup>
const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const goToDetail = () => {
  navigateTo(`/noticia/${props.article.id}`)
}
</script>