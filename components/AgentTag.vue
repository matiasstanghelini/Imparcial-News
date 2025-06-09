<template>
  <div 
    v-if="visible"
    class="inline-flex items-center px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm transition-colors duration-200"
  >
    <component 
      :is="agentIcon" 
      class="mr-1 w-3 h-3 text-gray-600" 
    />
    <span class="font-medium text-gray-700">{{ agentName }}</span>
    <span class="ml-1 text-gray-500">{{ previewText }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Brain, BookOpen, UserCheck, BarChart3, Bot } from 'lucide-vue-next'

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
    icon: Brain
  },
  context: {
    name: 'Contexto',
    icon: BookOpen
  },
  expert: {
    name: 'Experto',
    icon: UserCheck
  },
  synth: {
    name: 'Síntesis',
    icon: BarChart3
  }
}

const agentName = computed(() => agentConfig[props.agentType]?.name || 'Desconocido')
const agentIcon = computed(() => agentConfig[props.agentType]?.icon || Bot)

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
