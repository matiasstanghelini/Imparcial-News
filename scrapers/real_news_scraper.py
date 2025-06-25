#!/usr/bin/env python3
"""
Scraper real de noticias argentinas - Obtiene noticias actuales de sitios web
"""

import requests
from bs4 import BeautifulSoup
import feedparser
import json
from datetime import datetime
import time
import re
import sys
import os

class RealArgentinianNewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_lanacion(self):
        """Scraper para La Nación"""
        try:
            print("Scrapeando La Nación...")
            
            # Usar RSS feed de La Nación
            feed_url = "https://www.lanacion.com.ar/arcio/rss/"
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:3]:
                try:
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250], 
                        'source': 'La Nación',
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de La Nación: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando La Nación: {e}")
            return []

    def scrape_clarin(self):
        """Scraper para Clarín"""
        try:
            print("Scrapeando Clarín...")
            
            # Usar RSS feed de Clarín
            feed_url = "https://www.clarin.com/rss.xml"
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:3]:
                try:
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250],
                        'source': 'Clarín',
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de Clarín: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando Clarín: {e}")
            return []

    def scrape_infobae(self):
        """Scraper para Infobae"""
        try:
            print("Scrapeando Infobae...")
            
            # Usar RSS feed de Infobae
            feed_url = "https://www.infobae.com/feeds/rss/"
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:3]:
                try:
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250],
                        'source': 'Infobae',
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de Infobae: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando Infobae: {e}")
            return []

    def scrape_pagina12(self):
        """Scraper para Página/12"""
        try:
            print("Scrapeando Página/12...")
            
            # Usar RSS feed de Página/12
            feed_url = "https://www.pagina12.com.ar/rss/portada"
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:2]:
                try:
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250],
                        'source': 'Página/12',
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de Página/12: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando Página/12: {e}")
            return []

    def scrape_ambito(self):
        """Scraper para Ámbito"""
        try:
            print("Scrapeando Ámbito...")
            
            # Usar RSS feed de Ámbito
            feed_url = "https://www.ambito.com/rss/home.xml"
            feed = feedparser.parse(feed_url)
            
            news_items = []
            for entry in feed.entries[:2]:
                try:
                    title = self.clean_text(entry.title)
                    summary = self.clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Obtener fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250],
                        'source': 'Ámbito',
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    news_items.append(news_item)
                    
                except Exception as e:
                    print(f"Error procesando entrada de Ámbito: {e}")
                    continue
                    
            return news_items
            
        except Exception as e:
            print(f"Error scrapeando Ámbito: {e}")
            return []

    def clean_text(self, text):
        """Limpia y normaliza el texto"""
        if not text:
            return ""
        
        # Remover HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        # Limpiar caracteres especiales
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # Remover entidades HTML comunes
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&quot;', '"').replace('&#39;', "'")
        
        return text.strip()

    def scrape_all_sources(self):
        """Scrape todas las fuentes reales"""
        all_news = []
        
        # Lista de funciones de scraping
        scrapers = [
            self.scrape_lanacion,
            self.scrape_clarin,
            self.scrape_infobae,
            self.scrape_pagina12,
            self.scrape_ambito
        ]
        
        for scraper_func in scrapers:
            try:
                news_items = scraper_func()
                all_news.extend(news_items)
                time.sleep(2)  # Pausa entre scrapers para ser respetuosos
            except Exception as e:
                print(f"Error en scraper {scraper_func.__name__}: {e}")
                continue
        
        # Filtrar noticias válidas
        valid_news = []
        for news in all_news:
            if news['title'] and len(news['title']) > 10 and news['summary']:
                valid_news.append(news)
        
        # Ordenar por fecha (más recientes primero)
        valid_news = sorted(valid_news, key=lambda x: x['date'], reverse=True)
        
        return valid_news[:12]  # Limitar a 12 noticias

    def save_to_json(self, news_data, filename):
        """Guarda las noticias en formato JSON"""
        try:
            # Agregar IDs únicos y estructura de agentes
            for i, news in enumerate(news_data, 1):
                news['id'] = i
                news['agents'] = {
                    'logic': f'Noticia obtenida de {news["source"]} - Requiere verificación de fuentes primarias',
                    'context': f'Información publicada el {news["date"]} - Análisis contextual pendiente',
                    'expert': 'Análisis técnico especializado pendiente - Evaluación de credibilidad requerida',
                    'synth': [
                        f'📰 Fuente: {news["source"]}',
                        f'📅 Fecha: {news["date"]}',
                        f'🔗 URL: Disponible',
                        '🔍 Estado: Noticia real obtenida'
                    ]
                }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(news_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Noticias reales guardadas en {filename}")
            return True
            
        except Exception as e:
            print(f"Error guardando archivo: {e}")
            return False

def main():
    """Función principal para ejecutar el scraper real"""
    scraper = RealArgentinianNewsScraper()
    
    print("=== Iniciando scraping REAL de noticias argentinas ===")
    
    try:
        news_data = scraper.scrape_all_sources()
        
        if news_data:
            print(f"\n✓ Se obtuvieron {len(news_data)} noticias reales")
            
            # Guardar en archivo para la aplicación
            output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'real_news.json')
            scraper.save_to_json(news_data, output_file)
            
            # Mostrar muestra de noticias obtenidas
            print("\n--- MUESTRA DE NOTICIAS REALES ---")
            for i, news in enumerate(news_data[:3], 1):
                print(f"\n{i}. {news['source']}")
                print(f"   Título: {news['title']}")
                print(f"   Fecha: {news['date']}")
                print(f"   Resumen: {news['summary'][:80]}...")
            
            return True
            
        else:
            print("❌ No se pudieron obtener noticias reales")
            return False
            
    except Exception as e:
        print(f"❌ Error general en el scraper: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)