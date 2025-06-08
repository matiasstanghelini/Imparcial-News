<template>
  <div v-if="visible" class="bg-gray-50 rounded-lg p-4">
    <div class="flex items-center mb-3">
      <div class="flex items-center">
        <span class="text-lg mr-2">{{ agentIcon }}</span>
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
    name: 'Logic Agent',
    icon: '🧠'
  },
  context: {
    name: 'Context Agent',
    icon: '📚'
  },
  expert: {
    name: 'Expert Agent',
    icon: '👨‍🔬'
  },
  synth: {
    name: 'Synthesis Agent',
    icon: '📊'
  }
}

const agentName = computed(() => agentConfig[props.agentType]?.name || 'Unknown Agent')
const agentIcon = computed(() => agentConfig[props.agentType]?.icon || '🤖')
</script>
