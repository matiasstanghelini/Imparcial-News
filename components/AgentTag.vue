<template>
  <div 
    v-if="visible"
    class="inline-flex items-center px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm transition-colors duration-200"
  >
    <span class="mr-1">{{ agentIcon }}</span>
    <span class="font-medium text-gray-700">{{ agentName }}</span>
    <span class="ml-1 text-gray-500">{{ previewText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  agentType: {
    type: String,
    required: true
  },
  analysis: {
    type: [String, Array],
    required: true
  },
  visible: {
    type: Boolean,
    default: true
  }
})

// Agent configuration
const agentConfig = {
  logic: {
    name: 'Lógico',
    icon: '🧠'
  },
  context: {
    name: 'Contexto',
    icon: '📚'
  },
  expert: {
    name: 'Experto',
    icon: '👨‍🔬'
  },
  synth: {
    name: 'Síntesis',
    icon: '📊'
  }
}

const agentName = computed(() => agentConfig[props.agentType]?.name || 'Unknown')
const agentIcon = computed(() => agentConfig[props.agentType]?.icon || '🤖')

// Generate preview text
const previewText = computed(() => {
  if (props.agentType === 'synth' && Array.isArray(props.analysis)) {
    return `(${props.analysis.length} points)`
  } else if (typeof props.analysis === 'string') {
    return props.analysis.length > 30 
      ? `(${props.analysis.substring(0, 30)}...)`
      : `(${props.analysis})`
  }
  return '(Analysis available)'
})
</script>
