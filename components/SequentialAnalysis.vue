<template>
  <div class="bg-gray-50 rounded-lg p-6 mt-4">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900">Proceso de Análisis IA</h3>
      <button
        @click="startAnalysis"
        :disabled="isRunning"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors duration-200 font-medium"
      >
        {{ isRunning ? 'Analizando...' : 'Iniciar Análisis' }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Stepper Progress (Right Side) -->
      <div class="lg:col-span-1 order-2 lg:order-2">
        <div class="bg-white rounded-lg p-4 shadow-sm">
          <h4 class="font-medium text-gray-900 mb-4">Progreso del Análisis</h4>
          
          <div class="space-y-4">
            <div
              v-for="(step, index) in analysisSteps"
              :key="step.type"
              class="flex items-center space-x-3"
            >
              <!-- Step Circle -->
              <div 
                :class="getStepCircleClass(index)"
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-500"
              >
                <span v-if="getStepStatus(index) === 'completed'">✓</span>
                <span v-else-if="getStepStatus(index) === 'active'" class="animate-spin">⟳</span>
                <span v-else>{{ index + 1 }}</span>
              </div>
              
              <!-- Step Info -->
              <div class="flex-1">
                <div class="flex items-center space-x-2">
                  <component 
                    :is="step.icon" 
                    class="w-4 h-4 text-gray-600" 
                  />
                  <span 
                    :class="getStepTextClass(index)"
                    class="font-medium transition-colors duration-500"
                  >
                    {{ step.name }}
                  </span>
                </div>
                <div 
                  v-if="getStepStatus(index) === 'active'"
                  class="text-xs text-blue-600 mt-1"
                >
                  {{ step.description }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis Content (Left Side) -->
      <div class="lg:col-span-2 order-1 lg:order-1">
        <div class="bg-white rounded-lg p-6 shadow-sm min-h-[300px]">
          <!-- Initial State -->
          <div v-if="currentStep === -1" class="flex items-center justify-center h-full text-gray-500">
            <div class="text-center">
              <Bot class="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p class="text-lg font-medium">Listo para analizar</p>
              <p class="text-sm mt-2">Haz clic en "Iniciar Análisis" para comenzar el proceso de verificación IA</p>
            </div>
          </div>

          <!-- Active Analysis Display -->
          <div v-else-if="currentStep < analysisSteps.length" class="space-y-4">
            <div class="flex items-center space-x-3 mb-6">
              <component 
                :is="analysisSteps[currentStep].icon" 
                class="w-6 h-6 text-blue-600" 
              />
              <div>
                <h4 class="text-xl font-semibold text-gray-900">
                  {{ analysisSteps[currentStep].name }}
                </h4>
                <p class="text-gray-600">{{ analysisSteps[currentStep].description }}</p>
              </div>
            </div>

            <!-- Typing Effect for Analysis Text -->
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="text-gray-800 leading-relaxed">
                <span v-if="isTyping" class="typing-text">{{ displayText }}</span>
                <span v-else>{{ analysisSteps[currentStep].fullText }}</span>
                <span v-if="isTyping" class="animate-pulse ml-1">|</span>
              </div>
            </div>
          </div>

          <!-- Final Synthesis Display -->
          <div v-else class="space-y-4">
            <div class="flex items-center space-x-3 mb-6">
              <BarChart3 class="w-6 h-6 text-green-600" />
              <div>
                <h4 class="text-xl font-semibold text-gray-900">Análisis Completado</h4>
                <p class="text-gray-600">Hallazgos clave y síntesis</p>
              </div>
            </div>

            <!-- Synthesis Points -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="(point, index) in synthPoints"
                :key="index"
                :style="{ animationDelay: `${index * 200}ms` }"
                class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 animate-fade-in-up"
              >
                <div class="font-medium text-gray-900">{{ point }}</div>
              </div>
            </div>

            <!-- Reset Button -->
            <div class="mt-6 text-center">
              <button
                @click="resetAnalysis"
                class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200 font-medium"
              >
                Reiniciar Análisis
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Brain, BookOpen, UserCheck, BarChart3, Bot } from 'lucide-vue-next'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

// Analysis state
const currentStep = ref(-1)
const isRunning = ref(false)
const isTyping = ref(false)
const displayText = ref('')

// Analysis steps configuration
const analysisSteps = ref([
  {
    type: 'logic',
    name: 'Agente Lógico',
    icon: Brain,
    description: 'Analizando consistencia factual y coherencia lógica',
    fullText: ''
  },
  {
    type: 'context',
    name: 'Agente de Contexto',
    icon: BookOpen,
    description: 'Recopilando contexto histórico e información de antecedentes',
    fullText: ''
  },
  {
    type: 'expert',
    name: 'Agente Experto',
    icon: UserCheck,
    description: 'Aplicando conocimiento técnico y experiencia del dominio',
    fullText: ''
  }
])

// Synthesis points for final display
const synthPoints = computed(() => {
  if (Array.isArray(props.article.agents.synth)) {
    return props.article.agents.synth
  }
  return []
})

// Initialize analysis texts
onMounted(() => {
  analysisSteps.value[0].fullText = props.article.agents.logic
  analysisSteps.value[1].fullText = props.article.agents.context
  analysisSteps.value[2].fullText = props.article.agents.expert
})

// Step status helpers
const getStepStatus = (index) => {
  if (index < currentStep.value) return 'completed'
  if (index === currentStep.value) return 'active'
  return 'pending'
}

const getStepCircleClass = (index) => {
  const status = getStepStatus(index)
  return {
    'bg-green-500 text-white': status === 'completed',
    'bg-blue-500 text-white': status === 'active',
    'bg-gray-200 text-gray-500': status === 'pending'
  }
}

const getStepTextClass = (index) => {
  const status = getStepStatus(index)
  return {
    'text-green-700': status === 'completed',
    'text-blue-700': status === 'active',
    'text-gray-500': status === 'pending'
  }
}

// Typing effect function
const typeText = (text, callback) => {
  displayText.value = ''
  isTyping.value = true
  
  let i = 0
  const timer = setInterval(() => {
    if (i < text.length) {
      displayText.value += text.charAt(i)
      i++
    } else {
      clearInterval(timer)
      isTyping.value = false
      if (callback) callback()
    }
  }, 30) // Adjust speed here (lower = faster)
}

// Start analysis process
const startAnalysis = async () => {
  if (isRunning.value) return
  
  isRunning.value = true
  currentStep.value = 0

  for (let i = 0; i < analysisSteps.value.length; i++) {
    currentStep.value = i
    
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // Type out the analysis text
    await new Promise(resolve => {
      typeText(analysisSteps.value[i].fullText, resolve)
    })
    
    // Pause before next step
    await new Promise(resolve => setTimeout(resolve, 1200))
  }
  
  // Move to synthesis
  currentStep.value = analysisSteps.value.length
  isRunning.value = false
}

// Reset analysis
const resetAnalysis = () => {
  currentStep.value = -1
  isRunning.value = false
  isTyping.value = false
  displayText.value = ''
}
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
  opacity: 0;
}

.typing-text {
  font-family: 'Courier New', monospace;
}
</style>