<template>
  <div class="min-h-screen flex flex-col" :class="isDarkMode ? 'bg-black' : 'bg-gray-50'">
    <!-- Main content -->
    <main class="flex-1">
      <NuxtPage :sidebar-open="isSidebarOpen" @toggle-sidebar="isSidebarOpen = !isSidebarOpen" />
    </main>

    <!-- Sidebar -->
    <Sidebar 
      :isOpen="isSidebarOpen" 
      :news="news"
      @close="isSidebarOpen = false"
      @toggleDarkMode="toggleDarkMode"
    />
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'

// Global dark mode state
const isDarkMode = ref(false)
const isSidebarOpen = ref(false)
const news = ref([])

// Provide dark mode state to all child components
provide('isDarkMode', isDarkMode)

// Toggle dark mode
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value)
  updateDarkModeClass()
}

// Update dark mode class on HTML element
const updateDarkModeClass = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Load news data
const loadNews = async () => {
  try {
    const { data } = await useFetch('/api/news')
    if (data.value) {
      news.value = Array.isArray(data.value) ? data.value : []
    } else {
      // Fallback to local data if API fails
      const { news: localNews } = await import('~/data/news.js')
      news.value = localNews || []
    }
  } catch (error) {
    console.error('Error loading news:', error)
    // Fallback to local data on error
    const { news: localNews } = await import('~/data/news.js')
    news.value = localNews || []
  }
}

// Initialize
onMounted(() => {
  // Load saved dark mode preference
  const savedDarkMode = localStorage.getItem('darkMode')
  if (savedDarkMode !== null) {
    isDarkMode.value = savedDarkMode === 'true'
  } else {
    // Default to system preference
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  updateDarkModeClass()
  
  // Load news
  loadNews()
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans:wght@300;400;500;600;700;800;900&display=swap');

body {
  font-family: 'Noto Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}
</style>
