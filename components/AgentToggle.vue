<template>
  <div class="bg-white rounded-lg shadow-sm p-4 mb-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-3">Filter Analysis Agents</h3>
    
    <div class="flex flex-wrap gap-4">
      <label 
        v-for="(config, agentType) in agentConfig" 
        :key="agentType"
        class="flex items-center cursor-pointer hover:bg-gray-50 rounded-lg p-2 transition-colors duration-200"
      >
        <input
          type="checkbox"
          :checked="visibleAgents[agentType]"
          @change="$emit('toggle', agentType)"
          class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
        >
        <span class="ml-2 mr-1">{{ config.icon }}</span>
        <span class="text-sm font-medium text-gray-700">{{ config.name }}</span>
      </label>
    </div>
    
    <!-- Quick Actions -->
    <div class="mt-4 pt-3 border-t border-gray-200">
      <div class="flex gap-2">
        <button
          @click="selectAll"
          class="px-3 py-1 text-xs bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-md transition-colors duration-200"
        >
          Select All
        </button>
        <button
          @click="deselectAll"
          class="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md transition-colors duration-200"
        >
          Deselect All
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visibleAgents: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggle'])

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

// Quick action methods
const selectAll = () => {
  Object.keys(agentConfig).forEach(agentType => {
    if (!props.visibleAgents[agentType]) {
      emit('toggle', agentType)
    }
  })
}

const deselectAll = () => {
  Object.keys(agentConfig).forEach(agentType => {
    if (props.visibleAgents[agentType]) {
      emit('toggle', agentType)
    }
  })
}
</script>
