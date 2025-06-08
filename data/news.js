// Hardcoded news data for prototype
export const news = [
  {
    id: 1,
    title: "El Gobierno anuncia aumento de jubilaciones",
    source: "La Nación",
    date: "2025-06-08",
    summary: "El Estado nacional aplicará un aumento del 8.5% para jubilados en julio.",
    verdict: "true",
    agents: {
      logic: "La afirmación coincide con el comunicado oficial de ANSES.",
      context: "Desde 2021, los aumentos se rigen por la ley 27.609. Similar medida se tomó en 2022.",
      expert: "Basado en la fórmula de movilidad que combina variación salarial y recaudación.",
      synth: [
        "💰 Aumento: 8.5%",
        "📅 Fecha: Julio 2025",
        "📜 Ley: 27.609",
        "👥 Beneficiarios: +6 millones"
      ]
    }
  },
  {
    id: 2,
    title: "Detectan posible caso de gripe aviar en Córdoba",
    source: "Clarín",
    date: "2025-06-07",
    summary: "Se analizan muestras en un criadero del sur provincial.",
    verdict: "uncertain",
    agents: {
      logic: "No hay confirmación aún; es una hipótesis.",
      context: "Hubo brotes previos en 2023, lo cual activó protocolos.",
      expert: "La gripe aviar H5N1 puede afectar aves y humanos; requiere seguimiento.",
      synth: [
        "🧪 Estado: En análisis",
        "📍 Lugar: Córdoba, criadero rural",
        "🦠 Cepa sospechada: H5N1",
        "⚠️ Medida: Activado protocolo sanitario"
      ]
    }
  },
  {
    id: 3,
    title: "Nueva tecnología promete revolucionar la agricultura",
    source: "Página/12",
    date: "2025-06-06",
    summary: "Investigadores desarrollan sistema de riego automatizado con inteligencia artificial que reduce el consumo de agua en un 40%.",
    verdict: "true",
    agents: {
      logic: "Los datos técnicos son consistentes con estudios previos en agricultura de precisión.",
      context: "La tecnología de IA en agricultura ha mostrado resultados similares en otros países.",
      expert: "La reducción del 40% en consumo de agua es factible con sistemas optimizados de riego por goteo y sensores IoT.",
      synth: [
        "💧 Reducción de agua: 40%",
        "🤖 Tecnología: IA + IoT",
        "🌱 Aplicación: Sistema de riego",
        "📍 Desarrollo: Universidad Nacional"
      ]
    }
  },
  {
    id: 4,
    title: "Récord histórico de temperatura en la Antártida",
    source: "Infobae",
    date: "2025-06-05",
    summary: "Científicos registran una temperatura de 25°C en una estación de investigación, superando todos los registros anteriores.",
    verdict: "false",
    agents: {
      logic: "Los 25°C exceden significativamente los registros históricos máximos de la Antártida (18.3°C).",
      context: "Los registros de temperatura en la Antártida están bien documentados desde 1957.",
      expert: "Tal temperatura sería físicamente imposible dadas las condiciones climáticas actuales de la región.",
      synth: [
        "🌡️ Temperatura reportada: 25°C",
        "📊 Récord real: 18.3°C (2020)",
        "❌ Verificación: Datos inconsistentes",
        "🔍 Estado: Información no verificada"
      ]
    }
  },
  {
    id: 5,
    title: "Lanzamiento exitoso del satélite de comunicaciones argentino",
    source: "Télam",
    date: "2025-06-04",
    summary: "ARSAT-3 fue puesto en órbita desde la base de Kourou, expandiendo la cobertura de telecomunicaciones en el país.",
    verdict: "uncertain",
    agents: {
      logic: "No hay confirmación oficial del lanzamiento en las fuentes primarias de ARSAT.",
      context: "ARSAT-1 y ARSAT-2 fueron lanzados exitosamente en 2014 y 2015 respectivamente.",
      expert: "El cronograma de ARSAT-3 estaba planificado para 2025, pero las fechas exactas no estaban confirmadas.",
      synth: [
        "🛰️ Satélite: ARSAT-3",
        "🚀 Base: Kourou, Guayana Francesa",
        "📡 Función: Telecomunicaciones",
        "⏳ Estado: Pendiente de confirmación oficial"
      ]
    }
  }
]
