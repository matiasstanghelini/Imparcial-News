import { spawn } from 'child_process'
import { readFileSync, existsSync } from 'fs'
import { join } from 'path'

export default defineEventHandler(async (event) => {
  try {
    console.log('Obteniendo noticias reales de medios argentinos...')
    
    // Ejecutar el scraper RSS simplificado
    const scraperPath = join(process.cwd(), 'scrapers', 'simple_rss_scraper.py')
    const dataPath = join(process.cwd(), 'data', 'real_news.json')
    
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python3', [scraperPath], {
        cwd: process.cwd(),
        stdio: ['ignore', 'pipe', 'pipe']
      })
      
      let output = ''
      let errorOutput = ''
      
      pythonProcess.stdout.on('data', (data) => {
        output += data.toString()
      })
      
      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString()
      })
      
      pythonProcess.on('close', (code) => {
        console.log('Scraper terminado con código:', code)
        console.log('Output:', output)
        
        if (errorOutput) {
          console.log('Errores:', errorOutput)
        }
        
        // Intentar leer el archivo generado
        if (existsSync(dataPath)) {
          try {
            const newsData = JSON.parse(readFileSync(dataPath, 'utf-8'))
            
            resolve({
              success: true,
              data: newsData,
              timestamp: new Date().toISOString(),
              count: newsData.length,
              source: "Noticias reales de medios argentinos",
              scraperOutput: output.split('\n').slice(-5) // Últimas 5 líneas del output
            })
          } catch (parseError) {
            console.error('Error parseando JSON:', parseError)
            reject({
              success: false,
              error: 'Error parseando datos de noticias',
              message: parseError.message,
              timestamp: new Date().toISOString()
            })
          }
        } else {
          reject({
            success: false,
            error: 'El scraper no generó archivo de datos',
            message: 'No se pudo crear el archivo de noticias reales',
            timestamp: new Date().toISOString(),
            scraperOutput: output,
            scraperError: errorOutput
          })
        }
      })
      
      pythonProcess.on('error', (error) => {
        console.error('Error ejecutando scraper:', error)
        reject({
          success: false,
          error: 'Error ejecutando scraper de noticias',
          message: error.message,
          timestamp: new Date().toISOString()
        })
      })
      
      // Timeout de 45 segundos
      setTimeout(() => {
        pythonProcess.kill()
        reject({
          success: false,
          error: 'Timeout del scraper',
          message: 'El scraper tardó demasiado tiempo',
          timestamp: new Date().toISOString()
        })
      }, 45000)
    })
    
  } catch (error) {
    console.error('Error obteniendo noticias:', error)
    
    return {
      success: false,
      error: 'Error al obtener noticias en vivo',
      message: error.message,
      timestamp: new Date().toISOString()
    }
  }
})