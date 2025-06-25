<template>
  <article 
    class="bg-white border border-gray-200 hover:border-blue-200 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer group rounded-lg p-6"
    @click="goToDetail"
  >
    <!-- Source -->
    <div class="mb-3">
      <span class="text-xs font-medium text-blue-600 uppercase tracking-wide">
        {{ article.source }}
      </span>
    </div>
    
    <!-- Headline -->
    <h2 class="text-lg font-bold text-gray-900 mb-3 leading-tight group-hover:text-blue-600 transition-colors">
      {{ article.title }}
    </h2>
    
    <!-- Summary -->
    <p class="text-sm text-gray-600 leading-relaxed">
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