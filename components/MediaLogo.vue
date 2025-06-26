<template>
  <div class="inline-flex items-center">
    <div 
      :class="logoClasses"
      class="w-8 h-8 rounded-md flex items-center justify-center text-white text-xs font-bold mr-3 shadow-sm"
    >
      <component :is="logoSvg" v-if="logoSvg" class="w-5 h-5" />
      <span v-else>{{ logoInitials }}</span>
    </div>
    <span class="text-sm font-medium text-gray-300">{{ source }}</span>
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

// Componente SVG para logos de periódicos
const NewspaperIcon = {
  template: `
    <svg fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clip-rule="evenodd" />
      <path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z" />
    </svg>
  `
}

const logoData = {
  'La Nación': {
    initials: 'LN',
    color: 'bg-blue-900',
    svg: NewspaperIcon
  },
  'Clarín': {
    initials: 'C',
    color: 'bg-red-700',
    svg: NewspaperIcon
  },
  'Página/12': {
    initials: 'P12',
    color: 'bg-green-700',
    svg: NewspaperIcon
  },
  'Infobae': {
    initials: 'I',
    color: 'bg-orange-600',
    svg: NewspaperIcon
  },
  'Télam': {
    initials: 'T',
    color: 'bg-purple-700',
    svg: NewspaperIcon
  },
  'Ámbito': {
    initials: 'A',
    color: 'bg-indigo-700',
    svg: NewspaperIcon
  },
  'Cronista': {
    initials: 'CR',
    color: 'bg-blue-600',
    svg: NewspaperIcon
  },
  'TN': {
    initials: 'TN',
    color: 'bg-red-600',
    svg: NewspaperIcon
  },
  'Perfil': {
    initials: 'P',
    color: 'bg-indigo-600',
    svg: NewspaperIcon
  },
  'iProfesional': {
    initials: 'iP',
    color: 'bg-teal-600',
    svg: NewspaperIcon
  },
  'Chequeado': {
    initials: 'CH',
    color: 'bg-green-600',
    svg: NewspaperIcon
  },
  'Filo News': {
    initials: 'FN',
    color: 'bg-purple-600',
    svg: NewspaperIcon
  },
  'Minuto Uno': {
    initials: 'M1',
    color: 'bg-orange-600',
    svg: NewspaperIcon
  },
  'El Destape Web': {
    initials: 'ED',
    color: 'bg-pink-600',
    svg: NewspaperIcon
  },
  'El Cronista': {
    initials: 'CR',
    color: 'bg-blue-800',
    svg: NewspaperIcon
  }
}

const logoInitials = computed(() => {
  return logoData[props.source]?.initials || props.source.charAt(0).toUpperCase()
})

const logoClasses = computed(() => {
  return logoData[props.source]?.color || 'bg-gray-500'
})

const logoSvg = computed(() => {
  return logoData[props.source]?.svg || null
})
</script>