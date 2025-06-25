<template>
  <div class="bg-white rounded-2xl shadow-lg p-6 hover:bg-gray-50 transition-colors duration-200">
    <!-- News Header -->
    <div class="mb-4">
      <div class="flex items-center justify-between mb-2">
        <MediaLogo :source="article.source" />
        <span class="text-sm text-gray-400">{{ formatDate(article.date) }}</span>
      </div>
      
      <h2 class="text-xl font-semibold text-gray-900 mb-3 leading-tight">
        {{ article.title }}
      </h2>
      
      <p class="text-gray-700 mb-4 line-clamp-2">
        {{ article.summary }}
      </p>
    </div>

    <!-- Verdict Badge -->
    <div class="mb-4">
      <span 
        :class="verdictClasses"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
      >
        <span :class="verdictIcon" class="w-2 h-2 rounded-full mr-2"></span>
        {{ verdictText }}
      </span>
    </div>

    <!-- Agent Tags Preview -->
    <div class="mb-4 flex flex-wrap gap-2">
      <AgentTag
        v-for="(analysis, agentType) in article.agents"
        :key="agentType"
        :agent-type="agentType"
        :analysis="analysis"
        :visible="visibleAgents[agentType]"
      />
    </div>

    <!-- Analysis Mode Toggle -->
    <div class="flex gap-2 mb-4">
      <button
        @click="setAnalysisMode('standard')"
        :class="analysisMode === 'standard' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        class="px-3 py-2 rounded-lg transition-colors duration-200 font-medium text-sm"
      >
        Vista Estándar
      </button>
      <button
        @click="setAnalysisMode('sequential')"
        :class="analysisMode === 'sequential' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        class="px-3 py-2 rounded-lg transition-colors duration-200 font-medium text-sm"
      >
        Vista Proceso IA
      </button>
    </div>

    <!-- Expand Button -->
    <button
      @click="toggleExpanded"
      class="w-full py-2 px-4 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition-colors duration-200 font-medium"
    >
      {{ isExpanded ? 'Ocultar Análisis' : 'Mostrar Análisis' }}
      <svg 
        :class="{ 'rotate-180': isExpanded }"
        class="inline-block ml-2 w-5 h-5 transition-transform duration-200" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>

    <!-- Expanded Analysis -->
    <div v-if="isExpanded" class="mt-4">
      <!-- Standard Analysis View -->
      <div v-if="analysisMode === 'standard'" class="space-y-4">
        <AgentAnalysis
          v-for="(analysis, agentType) in article.agents"
          :key="agentType"
          :agent-type="agentType"
          :analysis="analysis"
          :visible="visibleAgents[agentType]"
        />
      </div>

      <!-- Sequential Analysis View -->
      <div v-else-if="analysisMode === 'sequential'">
        <SequentialAnalysis :article="article" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  article: {
    type: Object,
    required: true
  },
  visibleAgents: {
    type: Object,
    required: true
  }
})

const isExpanded = ref(false)
const analysisMode = ref('standard')

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const setAnalysisMode = (mode) => {
  analysisMode.value = mode
}

// Verdict styling
const verdictClasses = computed(() => {
  switch (props.article.verdict) {
    case 'true':
      return 'bg-green-100 text-green-800'
    case 'false':
      return 'bg-red-100 text-red-800'
    case 'uncertain':
      return 'bg-yellow-100 text-yellow-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})

const verdictIcon = computed(() => {
  switch (props.article.verdict) {
    case 'true':
      return 'bg-green-500'
    case 'false':
      return 'bg-red-500'
    case 'uncertain':
      return 'bg-yellow-500'
    default:
      return 'bg-gray-400'
  }
})

const verdictText = computed(() => {
  switch (props.article.verdict) {
    case 'true':
      return 'Verificado'
    case 'false':
      return 'Falso'
    case 'uncertain':
      return 'Incierto'
    default:
      return 'Desconocido'
  }
})

// Date formatting
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
