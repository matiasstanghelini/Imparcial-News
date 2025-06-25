<template>
  <div class="inline-flex items-center">
    <div 
      :class="logoClasses"
      class="w-6 h-6 rounded-sm flex items-center justify-center text-white text-xs font-bold mr-2"
    >
      {{ logoInitials }}
    </div>
    <span class="text-sm text-gray-600 font-medium">{{ source }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  source: {
    type: String,
    required: true
  }
})

const logoData = {
  'La Nación': {
    initials: 'LN',
    color: 'bg-blue-800'
  },
  'Clarín': {
    initials: 'C',
    color: 'bg-red-600'
  },
  'Página/12': {
    initials: 'P12',
    color: 'bg-green-700'
  },
  'Infobae': {
    initials: 'I',
    color: 'bg-orange-600'
  },
  'Télam': {
    initials: 'T',
    color: 'bg-purple-700'
  },
  'Ámbito': {
    initials: 'A',
    color: 'bg-gray-700'
  },
  'Perfil': {
    initials: 'P',
    color: 'bg-indigo-600'
  },
  'Cronista': {
    initials: 'CR',
    color: 'bg-teal-600'
  }
}

const logoInitials = computed(() => {
  return logoData[props.source]?.initials || props.source.charAt(0).toUpperCase()
})

const logoClasses = computed(() => {
  return logoData[props.source]?.color || 'bg-gray-500'
})
</script>