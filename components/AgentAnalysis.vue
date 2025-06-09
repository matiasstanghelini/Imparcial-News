<template>
  <div v-if="visible" class="bg-gray-50 rounded-lg p-4">
    <div class="flex items-center mb-3">
      <div class="flex items-center">
        <component 
          :is="agentIcon" 
          class="mr-2 w-5 h-5 text-gray-600" 
        />
        <h3 class="font-semibold text-gray-900 capitalize">{{ agentName }}</h3>
      </div>
    </div>
    
    <div class="text-sm text-gray-700">
      <!-- For synthesis agent, show bullet points -->
      <div v-if="agentType === 'synth'" class="space-y-1">
        <div 
          v-for="point in analysis" 
          :key="point"
          class="flex items-start"
        >
          <span class="mr-2">•</span>
          <span>{{ point }}</span>
        </div>
      </div>
      
      <!-- For other agents, show text analysis -->
      <p v-else>{{ analysis }}</p>
    </div>
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
    name: 'Agente Lógico',
    icon: Brain
  },
  context: {
    name: 'Agente de Contexto',
    icon: BookOpen
  },
  expert: {
    name: 'Agente Experto',
    icon: UserCheck
  },
  synth: {
    name: 'Agente de Síntesis',
    icon: BarChart3
  }
}

const agentName = computed(() => agentConfig[props.agentType]?.name || 'Agente Desconocido')
const agentIcon = computed(() => agentConfig[props.agentType]?.icon || Bot)
</script>
