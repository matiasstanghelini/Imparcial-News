<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="mb-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-2">
        Plataforma de Análisis de Noticias con IA
      </h1>
      <p class="text-lg text-gray-600">
        Verificación inteligente de noticias con agentes de inteligencia artificial
      </p>
    </header>

    <!-- Agent Toggle Controls -->
    <div class="mb-6">
      <AgentToggle 
        :visible-agents="visibleAgents" 
        @toggle="toggleAgent" 
      />
    </div>

    <!-- News Feed -->
    <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
      <NewsCard
        v-for="article in newsData"
        :key="article.id"
        :article="article"
        :visible-agents="visibleAgents"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { news } from '~/data/news.js'

// News data
const newsData = ref(news)

// Agent visibility state
const visibleAgents = ref({
  logic: true,
  context: true,
  expert: true,
  synth: true
})

// Toggle agent visibility
const toggleAgent = (agentType) => {
  visibleAgents.value[agentType] = !visibleAgents.value[agentType]
}
</script>
