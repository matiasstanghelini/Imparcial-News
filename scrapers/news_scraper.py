#!/usr/bin/env python3
"""
Scraper de noticias para diarios argentinos
Extrae noticias principales del día de múltiples fuentes
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import json
from datetime import datetime
import time
import re

class ArgentinianNewsScraper:
    def __init__(self):
        self.sources = {
            'La Nación': {
                'url': 'https://www.lanacion.com.ar',
                'rss': 'https://www.lanacion.com.ar/arcio/rss/',
                'selectors': {
                    'title': '.com-title a, h1 a, h2 a',
                    'summary': '.com-summary, .bajada, p',
                    'link': 'a'
                }
            },
            'Clarín': {
                'url': 'https://www.clarin.com',
                'rss': 'https://www.clarin.com/rss.xml',
                'selectors': {
                    'title': '.title a, h1 a, h2 a',
                    'summary': '.summary, .volanta, p',
                    'link': 'a'
                }
            },
            'Infobae': {
                'url': 'https://www.infobae.com',
                'rss': 'https://www.infobae.com/feeds/rss/',
                'selectors': {
                    'title': '.headline a, h1 a, h2 a',
                    'summary': '.summary, .subheadline, p',
                    'link': 'a'
                }
            },
            'Página/12': {
                'url': 'https://www.pagina12.com.ar',
                'rss': 'https://www.pagina12.com.ar/rss/portada',
                'selectors': {
                    'title': '.title-art a, h1 a, h2 a',
                    'summary': '.summary-art, .copete, p',
                    'link': 'a'
                }
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_rss_news(self, source_name, rss_url, limit=5):
        """Extrae noticias de RSS feeds"""
        try:
            feed = feedparser.parse(rss_url)
            news_items = []
            
            for entry in feed.entries[:limit]:
                try:
                    # Limpiar título y resumen
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    published = entry.published_parsed if hasattr(entry, 'published_parsed') else None
                    date = datetime(*published[:6]).strftime('%Y-%m-%d') if published else datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:150],  # Limitar longitud
                        'summary': summary[:300],  # Limitar longitud
                        'source': source_name,
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'  # Por defecto, requiere análisis IA
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de {source_name}: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error obteniendo RSS de {source_name}: {e}")
            return []

    def scrape_website(self, source_name, url, limit=3):
        """Scrapa noticias directamente del sitio web"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # Buscar títulos principales
            title_elements = soup.select('h1 a, h2 a, .title a, .headline a')[:limit]
            
            for element in title_elements:
                try:
                    title = self.clean_text(element.get_text())
                    link = element.get('href', '')
                    
                    # Hacer absoluta la URL si es relativa
                    if link.startswith('/'):
                        link = url + link
                    
                    # Intentar obtener resumen
                    summary = self.get_article_summary(link) if link else "Sin resumen disponible"
                    
                    news_item = {
                        'title': title[:150],
                        'summary': summary[:300],
                        'source': source_name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'url': link,
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    time.sleep(1)  # Respetar el sitio web
                    
                except Exception as e:
                    print(f"Error procesando artículo de {source_name}: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando {source_name}: {e}")
            return []

    def get_article_summary(self, url):
        """Obtiene un resumen del artículo desde su URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar párrafos con contenido
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = self.clean_text(p.get_text())
                if len(text) > 50:  # Párrafo con contenido sustancial
                    return text[:300]
                    
            return "Sin resumen disponible"
            
        except:
            return "Sin resumen disponible"

    def clean_text(self, text):
        """Limpia y normaliza el texto"""
        if not text:
            return ""
        
        # Remover HTML tags remanentes
        text = re.sub(r'<[^>]+>', '', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Remover caracteres especiales problemáticos
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        return text.strip()

    def scrape_all_sources(self):
        """Scrape todas las fuentes configuradas"""
        all_news = []
        
        for source_name, config in self.sources.items():
            print(f"Scrapeando {source_name}...")
            
            # Intentar primero con RSS
            if 'rss' in config:
                rss_news = self.get_rss_news(source_name, config['rss'])
                if rss_news:
                    all_news.extend(rss_news)
                    continue
            
            # Si RSS falla, usar scraping directo
            web_news = self.scrape_website(source_name, config['url'])
            all_news.extend(web_news)
            
            time.sleep(2)  # Pausa entre fuentes
        
        # Filtrar y ordenar noticias
        all_news = [news for news in all_news if news['title'] and len(news['title']) > 10]
        all_news = sorted(all_news, key=lambda x: x['date'], reverse=True)
        
        return all_news[:15]  # Limitar a 15 noticias principales

    def save_to_json(self, news_data, filename):
        """Guarda las noticias en formato JSON"""
        try:
            # Agregar IDs únicos
            for i, news in enumerate(news_data, 1):
                news['id'] = i
                # Agregar estructura de agentes vacía para análisis posterior
                news['agents'] = {
                    'logic': 'Análisis pendiente - Requiere verificación con IA',
                    'context': 'Contexto pendiente - Requiere análisis histórico',
                    'expert': 'Análisis experto pendiente - Requiere evaluación técnica',
                    'synth': [
                        'Estado: Noticia recién obtenida',
                        'Fuente: ' + news['source'],
                        'Fecha: ' + news['date'],
                        'Verificación: Pendiente'
                    ]
                }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            print(f"Noticias guardadas en {filename}")
            return True
            
        except Exception as e:
            print(f"Error guardando archivo: {e}")
            return False

def main():
    """Función principal para ejecutar el scraper"""
    scraper = ArgentinianNewsScraper()
    
    print("Iniciando scraping de noticias argentinas...")
    news_data = scraper.scrape_all_sources()
    
    if news_data:
        print(f"Se obtuvieron {len(news_data)} noticias")
        
        # Guardar en JSON para la aplicación
        scraper.save_to_json(news_data, 'data/scraped_news.json')
        
        # Mostrar resumen
        for news in news_data[:5]:  # Mostrar las primeras 5
            print(f"\n--- {news['source']} ---")
            print(f"Título: {news['title']}")
            print(f"Resumen: {news['summary'][:100]}...")
            
    else:
        print("No se pudieron obtener noticias")

if __name__ == "__main__":
    main()