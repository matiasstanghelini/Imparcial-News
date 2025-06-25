#!/usr/bin/env python3
"""
Scraper rápido de noticias argentinas usando RSS feeds
"""

import feedparser
import json
from datetime import datetime
import re

def clean_text(text):
    """Limpia y normaliza el texto"""
    if not text:
        return ""
    
    # Remover HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    # Limpiar caracteres especiales
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    return text.strip()

def scrape_rss_feeds():
    """Scrapa noticias de feeds RSS argentinos"""
    
    feeds = {
        'La Nación': 'https://www.lanacion.com.ar/arcio/rss/',
        'Clarín': 'https://www.clarin.com/rss.xml',
        'Infobae': 'https://www.infobae.com/feeds/rss/',
        'Ámbito': 'https://www.ambito.com/rss/home.xml'
    }
    
    all_news = []
    
    for source, feed_url in feeds.items():
        try:
            print(f"Obteniendo noticias de {source}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:4]:  # Solo 4 por fuente
                try:
                    title = clean_text(entry.title)
                    summary = clean_text(entry.summary if hasattr(entry, 'summary') else entry.description)
                    
                    # Fecha
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    else:
                        date = datetime.now().strftime('%Y-%m-%d')
                    
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250],
                        'source': source,
                        'date': date,
                        'url': entry.link if hasattr(entry, 'link') else '',
                        'verdict': 'uncertain'
                    }
                    
                    all_news.append(news_item)
                    
                except Exception as e:
                    print(f"Error con entrada de {source}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error con feed de {source}: {e}")
            continue
    
    return all_news

def main():
    print("Iniciando scraping rápido de noticias...")
    
    news_data = scrape_rss_feeds()
    
    if news_data:
        # Agregar IDs y estructura de agentes
        for i, news in enumerate(news_data, 1):
            news['id'] = i
            news['agents'] = {
                'logic': 'Noticia obtenida de fuente oficial - Pendiente análisis detallado',
                'context': 'Información reciente - Requiere contextualización histórica',
                'expert': 'Análisis técnico pendiente - Evaluación de veracidad requerida',
                'synth': [
                    f'📰 Fuente: {news["source"]}',
                    f'📅 Fecha: {news["date"]}',
                    '🔍 Estado: Recién obtenida',
                    '⏳ Verificación: Pendiente'
                ]
            }
        
        # Guardar datos
        with open('../data/live_news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Se obtuvieron {len(news_data)} noticias en vivo")
        
        # Mostrar muestra
        for news in news_data[:3]:
            print(f"\n{news['source']}: {news['title']}")
    
    else:
        print("No se pudieron obtener noticias")

if __name__ == "__main__":
    main()