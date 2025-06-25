import { execSync } from 'child_process'
import { writeFileSync, readFileSync, unlinkSync } from 'fs'
import { join } from 'path'

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody(event)
    const { url } = body

    if (!url) {
      return {
        success: false,
        error: 'URL requerida'
      }
    }

    console.log('Extrayendo contenido de:', url)

    // Crear un script temporal para extraer contenido
    const tempScript = join(process.cwd(), 'temp_extract.py')
    const scriptContent = `
import trafilatura
import sys
import json

def extract_content(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            if text:
                return {
                    'success': True,
                    'content': text,
                    'length': len(text)
                }
        return {
            'success': False,
            'error': 'No se pudo extraer contenido'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    url = sys.argv[1]
    result = extract_content(url)
    print(json.dumps(result, ensure_ascii=False))
`

    // Escribir script temporal
    writeFileSync(tempScript, scriptContent)

    try {
      // Ejecutar el script
      const output = execSync(`python3 ${tempScript} "${url}"`, {
        timeout: 15000,
        encoding: 'utf-8',
        maxBuffer: 1024 * 1024 * 5 // 5MB buffer
      })

      // Limpiar archivo temporal
      unlinkSync(tempScript)

      const result = JSON.parse(output.trim())
      
      if (result.success) {
        return {
          success: true,
          content: result.content,
          length: result.length,
          timestamp: new Date().toISOString()
        }
      } else {
        return {
          success: false,
          error: result.error || 'Error extrayendo contenido'
        }
      }

    } catch (execError) {
      // Limpiar archivo temporal en caso de error
      try {
        unlinkSync(tempScript)
      } catch {}

      console.error('Error ejecutando extractor:', execError)
      return {
        success: false,
        error: 'Error procesando el contenido del artículo',
        details: execError.message
      }
    }

  } catch (error) {
    console.error('Error general:', error)
    return {
      success: false,
      error: 'Error interno del servidor',
      message: error.message
    }
  }
})