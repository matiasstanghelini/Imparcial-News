import { readFileSync, existsSync, statSync } from 'fs'
import { join } from 'path'
import { execSync } from 'child_process'

export default defineEventHandler(async (event) => {
  try {
    console.log('Obteniendo noticias reales de medios argentinos...')
    
    const scraperPath = join(process.cwd(), 'scrapers', 'fast_combined_scraper.py')
    const dataPath = join(process.cwd(), 'data', 'real_news.json')
    
    // Verificar si el archivo de noticias existe y es reciente (menos de 5 minutos)
    if (existsSync(dataPath)) {
      const stats = statSync(dataPath)
      const ageInMinutes = (Date.now() - stats.mtime.getTime()) / (1000 * 60)
      
      if (ageInMinutes < 5) {
        console.log('Usando noticias cached (menos de 5 minutos)')
        const newsData = JSON.parse(readFileSync(dataPath, 'utf-8'))
        return {
          success: true,
          data: newsData,
          timestamp: new Date().toISOString(),
          count: newsData.length,
          source: "Noticias reales (cached)",
          cached: true
        }
      }
    }
    
    // Ejecutar scraper de forma sincrónica con timeout
    try {
      console.log('Ejecutando scraper...')
      execSync(`python3 ${scraperPath}`, {
        cwd: process.cwd(),
        timeout: 30000,
        stdio: 'pipe'
      })
      
      // Leer el archivo generado
      if (existsSync(dataPath)) {
        const newsData = JSON.parse(readFileSync(dataPath, 'utf-8'))
        
        return {
          success: true,
          data: newsData,
          timestamp: new Date().toISOString(),
          count: newsData.length,
          source: "Noticias reales de medios argentinos"
        }
      } else {
        throw new Error('Archivo no generado por el scraper')
      }
      
    } catch (execError) {
      console.error('Error ejecutando scraper:', execError)
      
      // Fallback: Si hay datos cached antiguos, usarlos
      if (existsSync(dataPath)) {
        const newsData = JSON.parse(readFileSync(dataPath, 'utf-8'))
        return {
          success: true,
          data: newsData,
          timestamp: new Date().toISOString(),
          count: newsData.length,
          source: "Noticias reales (fallback)",
          warning: "Usando datos anteriores debido a error en scraper"
        }
      }
      
      throw execError
    }
    
  } catch (error) {
    console.error('Error general:', error)
    return {
      success: false,
      error: 'Error obteniendo noticias en vivo',
      message: error.message,
      timestamp: new Date().toISOString()
    }
  }
})