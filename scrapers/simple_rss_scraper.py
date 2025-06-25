#!/usr/bin/env python3
"""
Scraper simple y confiable usando RSS feeds públicos de medios argentinos
"""

import feedparser
import json
from datetime import datetime
import re
import os
import sys

def clean_text(text):
    """Limpia y normaliza texto"""
    if not text:
        return ""
    
    # Remover HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    # Limpiar caracteres especiales
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # Entidades HTML
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'")
    
    return text.strip()

def scrape_rss_feed(source_name, feed_url, max_items=3):
    """Scraper genérico para RSS feeds"""
    try:
        print(f"Obteniendo {source_name}...")
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print(f"No se encontraron entradas en {source_name}")
            return []
        
        news_items = []
        for entry in feed.entries[:max_items]:
            try:
                title = clean_text(entry.title)
                
                # Obtener descripción/resumen
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = clean_text(entry.summary)
                elif hasattr(entry, 'description'):
                    summary = clean_text(entry.description)
                
                # Obtener fecha
                date = datetime.now().strftime('%Y-%m-%d')
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    except:
                        pass
                
                # URL del artículo
                url = entry.link if hasattr(entry, 'link') else ''
                
                if title and len(title) > 5:  # Solo agregar si tiene título válido
                    news_item = {
                        'title': title[:120],
                        'summary': summary[:250] if summary else "Sin resumen disponible",
                        'source': source_name,
                        'date': date,
                        'url': url,
                        'verdict': 'uncertain'
                    }
                    news_items.append(news_item)
                    
            except Exception as e:
                print(f"Error procesando entrada: {e}")
                continue
        
        print(f"✓ {len(news_items)} noticias obtenidas de {source_name}")
        return news_items
        
    except Exception as e:
        print(f"Error obteniendo {source_name}: {e}")
        return []

def main():
    """Función principal"""
    print("=== Scraper RSS de Noticias Argentinas ===")
    
    # Feeds RSS de medios argentinos conocidos
    rss_feeds = {
        'La Nación': 'https://www.lanacion.com.ar/arcio/rss/',
        'Clarín': 'https://www.clarin.com/rss.xml',
        'Infobae': 'https://www.infobae.com/feeds/rss/',
        'Ámbito': 'https://www.ambito.com/rss/home.xml'
    }
    
    all_news = []
    
    # Scrapear cada feed
    for source, feed_url in rss_feeds.items():
        news_items = scrape_rss_feed(source, feed_url, max_items=3)
        all_news.extend(news_items)
    
    if not all_news:
        print("❌ No se pudieron obtener noticias")
        return False
    
    # Ordenar por fecha
    all_news = sorted(all_news, key=lambda x: x['date'], reverse=True)
    
    # Limitar a 12 noticias
    all_news = all_news[:12]
    
    # Agregar estructura de agentes
    for i, news in enumerate(all_news, 1):
        news['id'] = i
        news['agents'] = {
            'logic': f'Noticia de {news["source"]} - Fuente confiable que requiere verificación de hechos específicos',
            'context': f'Publicada el {news["date"]} - Análisis de contexto histórico y social pendiente',
            'expert': 'Evaluación técnica especializada requerida para confirmar datos y cifras mencionadas',
            'synth': [
                f'📰 Fuente: {news["source"]}',
                f'📅 Fecha: {news["date"]}',
                '🔍 Estado: Noticia real obtenida de RSS',
                '⚡ Tipo: Información en tiempo real'
            ]
        }
    
    # Guardar archivo
    try:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'real_news.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {len(all_news)} noticias reales guardadas")
        
        # Mostrar muestra
        print("\n--- NOTICIAS OBTENIDAS ---")
        for news in all_news[:4]:
            print(f"{news['source']}: {news['title'][:60]}...")
        
        return True
        
    except Exception as e:
        print(f"Error guardando archivo: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)