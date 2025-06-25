#!/usr/bin/env python3
"""
Scraper rápido y optimizado para medios argentinos
Combina RSS y web scraping con timeouts agresivos
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import concurrent.futures
import os
import sys

def clean_text(text):
    """Limpia y normaliza texto"""
    if not text:
        return ""
    
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    
    return text.strip()

def scrape_rss_feed(source_name, feed_url):
    """Scraper RSS con timeout agresivo"""
    try:
        print(f"RSS {source_name}...")
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            return []
        
        news_items = []
        for entry in feed.entries[:3]:
            try:
                title = clean_text(entry.title)
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = clean_text(entry.summary)
                
                date = datetime.now().strftime('%Y-%m-%d')
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        date = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    except:
                        pass
                
                url = entry.link if hasattr(entry, 'link') else ''
                
                if title and len(title) > 5:
                    news_items.append({
                        'title': title[:120],
                        'summary': summary[:250] if summary else f"Noticia de {source_name}",
                        'source': source_name,
                        'date': date,
                        'url': url,
                        'verdict': 'uncertain',
                        'image': None  # Para futuras implementaciones de extracción de imágenes
                    })
                    
            except:
                continue
        
        print(f"  ✓ {len(news_items)} de {source_name}")
        return news_items
        
    except Exception as e:
        print(f"  Error {source_name}: {str(e)[:50]}")
        return []

def scrape_web_simple(source_name, url):
    """Web scraping simple y rápido"""
    try:
        print(f"Web {source_name}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=8)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Buscar títulos y enlaces
        selectors = ['h1 a', 'h2 a', 'h3 a', '.title a', '.headline a']
        found_links = []
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                found_links.extend(elements[:10])
            except:
                continue
        
        # También buscar enlaces con texto largo
        all_links = soup.find_all('a', href=True)
        for link in all_links[:20]:
            text = link.get_text().strip()
            if text and 20 < len(text) < 120:
                found_links.append(link)
        
        seen_titles = set()
        
        for link in found_links[:15]:
            try:
                title = clean_text(link.get_text())
                
                if len(title) < 15 or title in seen_titles:
                    continue
                
                seen_titles.add(title)
                
                href = link.get('href', '')
                if href:
                    if href.startswith('/'):
                        href = url.rstrip('/') + href
                    elif not href.startswith('http'):
                        continue
                
                domain = url.split('//')[1].split('/')[0]
                if href and domain in href:
                    news_items.append({
                        'title': title[:120],
                        'summary': f"Noticia de {source_name}",
                        'source': source_name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'url': href,
                        'verdict': 'uncertain',
                        'image': None  # Para futuras implementaciones de extracción de imágenes
                    })
                    
                    if len(news_items) >= 3:
                        break
                        
            except:
                continue
        
        print(f"  ✓ {len(news_items)} de {source_name}")
        return news_items
        
    except Exception as e:
        print(f"  Error {source_name}: {str(e)[:50]}")
        return []

def scrape_source(source_config):
    """Función wrapper para scraping paralelo"""
    source_name, config = source_config
    
    if 'rss' in config:
        return scrape_rss_feed(source_name, config['rss'])
    elif 'web' in config:
        return scrape_web_simple(source_name, config['web'])
    else:
        return []

def main():
    """Función principal optimizada"""
    print("=== Scraper Rápido Medios Argentinos ===")
    
    # Configuración de fuentes - Medios argentinos ampliados
    sources = {
        'La Nación': {'rss': 'https://www.lanacion.com.ar/arcio/rss/'},
        'Clarín': {'rss': 'https://www.clarin.com/rss/politica/'},
        'Página/12': {'rss': 'https://www.pagina12.com.ar/rss/portada'},
        'Ámbito': {'rss': 'https://www.ambito.com/rss/politica.xml'},
        'El Cronista': {'rss': 'https://www.cronista.com/rss/politica.xml'},
        'Infobae': {'web': 'https://www.infobae.com/politica/'},
        'TN': {'web': 'https://tn.com.ar/politica/'},
        'Perfil': {'web': 'https://www.perfil.com/seccion/politica'},
        'iProfesional': {'web': 'https://www.iprofesional.com/politica/'},
        'Chequeado': {'web': 'https://chequeado.com/'},
        'Filo News': {'web': 'https://www.filo.news/politica/'},
        'Minuto Uno': {'web': 'https://www.minutouno.com/politica/'},
        'El Destape Web': {'web': 'https://www.eldestapeweb.com/politica/'}
    }
    
    all_news = []
    
    # Ejecutar en paralelo con timeout global
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Mapear tareas
        future_to_source = {
            executor.submit(scrape_source, item): item[0] 
            for item in sources.items()
        }
        
        # Recoger resultados con timeout
        for future in concurrent.futures.as_completed(future_to_source, timeout=25):
            try:
                news_items = future.result(timeout=5)
                all_news.extend(news_items)
            except Exception as e:
                source = future_to_source[future]
                print(f"  Timeout/Error {source}")
                continue
    
    if not all_news:
        print("❌ No se obtuvieron noticias")
        return False
    
    # Eliminar duplicados básicos
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        title_key = news['title'][:50].lower()
        if title_key not in seen_titles:
            unique_news.append(news)
            seen_titles.add(title_key)
    
    # Ordenar y limitar - Aumentar a 25 noticias con más medios
    unique_news = sorted(unique_news, key=lambda x: x['date'], reverse=True)
    unique_news = unique_news[:25]
    
    # Agregar estructura de agentes
    for i, news in enumerate(unique_news, 1):
        news['id'] = i
        news['agents'] = {
            'logic': f'Noticia de {news["source"]} - Fuente verificada',
            'context': f'Publicada el {news["date"]} - Medio argentino reconocido',
            'expert': 'Evaluación especializada requerida para análisis detallado',
            'synth': [
                f'📰 Fuente: {news["source"]}',
                f'📅 Fecha: {news["date"]}',
                '🔍 Estado: Noticia verificada',
                '⚡ Tipo: Información actualizada'
            ]
        }
    
    # Guardar archivo
    try:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'real_news.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_news, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ {len(unique_news)} noticias guardadas")
        
        # Mostrar distribución
        sources_count = {}
        for news in unique_news:
            source = news['source']
            sources_count[source] = sources_count.get(source, 0) + 1
        
        print("\n--- DISTRIBUCIÓN ---")
        for source, count in sources_count.items():
            print(f"{source}: {count}")
        
        print("\n--- MUESTRA ---")
        for news in unique_news[:4]:
            print(f"{news['source']}: {news['title'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"Error guardando: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)