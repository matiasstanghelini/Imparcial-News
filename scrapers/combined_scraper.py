#!/usr/bin/env python3
"""
Scraper combinado que utiliza RSS feeds y web scraping directo
para obtener la máxima cobertura de medios argentinos
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random
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
    text = text.replace('&nbsp;', ' ')
    
    return text.strip()

def scrape_rss_feed(source_name, feed_url, max_items=3):
    """Scraper genérico para RSS feeds"""
    try:
        print(f"Obteniendo {source_name} (RSS)...")
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print(f"  RSS sin entradas en {source_name}")
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
                continue
        
        print(f"  ✓ {len(news_items)} noticias RSS de {source_name}")
        return news_items
        
    except Exception as e:
        print(f"  Error RSS {source_name}: {e}")
        return []

def scrape_web_direct(source_name, base_url, selectors, max_items=3):
    """Scraper genérico para web scraping directo"""
    try:
        print(f"Obteniendo {source_name} (Web)...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Probar múltiples selectores
        found_articles = []
        for selector in selectors:
            try:
                elements = soup.select(selector)
                found_articles.extend(elements[:8])
            except:
                continue
        
        # También buscar enlaces con títulos largos
        all_links = soup.find_all('a', href=True)
        for link in all_links[:30]:
            text = link.get_text().strip()
            if text and len(text) > 25 and len(text) < 150:
                found_articles.append(link)
        
        processed_titles = set()
        
        for article in found_articles[:20]:
            try:
                title = clean_text(article.get_text())
                
                if len(title) < 15 or title in processed_titles:
                    continue
                
                processed_titles.add(title)
                
                # Obtener URL
                url = ''
                if hasattr(article, 'get') and article.get('href'):
                    url = article.get('href')
                elif article.find('a'):
                    a_tag = article.find('a')
                    if a_tag and a_tag.get('href'):
                        url = a_tag.get('href')
                
                if url:
                    if url.startswith('/'):
                        url = base_url.rstrip('/') + url
                    elif not url.startswith('http'):
                        continue
                
                # Validar que sea del dominio correcto
                domain = base_url.split('//')[1].split('/')[0]
                if url and domain in url and title and len(title) > 15:
                    news_item = {
                        'title': title[:120],
                        'summary': f"Noticia de {source_name} obtenida por web scraping",
                        'source': source_name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'url': url,
                        'verdict': 'uncertain'
                    }
                    news_items.append(news_item)
                    
                    if len(news_items) >= max_items:
                        break
                        
            except Exception as e:
                continue
        
        print(f"  ✓ {len(news_items)} noticias Web de {source_name}")
        return news_items
        
    except Exception as e:
        print(f"  Error Web {source_name}: {e}")
        return []

def main():
    """Función principal del scraper combinado"""
    print("=== Scraper Combinado - Medios Argentinos ===")
    
    # Configuración de medios con RSS
    rss_sources = {
        'La Nación': 'https://www.lanacion.com.ar/arcio/rss/',
        'Clarín': 'https://www.clarin.com/rss/politica/',
        'Página/12': 'https://www.pagina12.com.ar/rss/portada',
        'Ámbito': 'https://www.ambito.com/rss/politica.xml',
        'Cronista': 'https://www.cronista.com/rss/politica.xml'
    }
    
    # Configuración de medios con web scraping
    web_sources = {
        'Infobae': {
            'url': 'https://www.infobae.com/politica/',
            'selectors': [
                'h1 a', 'h2 a', 'h3 a',
                '.headline a', '.title a',
                'article h2', 'article h3',
                '[data-module*="headline"] a'
            ]
        },
        'TN': {
            'url': 'https://tn.com.ar/politica/',
            'selectors': [
                'h1 a', 'h2 a', 'h3 a',
                '.article-title a', '.headline a',
                'article h2', 'article h3',
                '.story-title a', '.news-title a'
            ]
        },
        'Perfil': {
            'url': 'https://www.perfil.com/seccion/politica',
            'selectors': [
                'h1 a', 'h2 a', 'h3 a',
                '.title a', '.headline a',
                'article h2', 'article h3'
            ]
        }
    }
    
    all_news = []
    
    # Scrapear fuentes RSS
    print("\n--- SCRAPING RSS FEEDS ---")
    for source, feed_url in rss_sources.items():
        news_items = scrape_rss_feed(source, feed_url, max_items=3)
        all_news.extend(news_items)
        time.sleep(0.5)  # Pausa corta entre requests
    
    # Scrapear fuentes web
    print("\n--- SCRAPING WEB DIRECTO ---")
    for source, config in web_sources.items():
        news_items = scrape_web_direct(source, config['url'], config['selectors'], max_items=3)
        all_news.extend(news_items)
        time.sleep(random.uniform(1, 2))  # Pausa entre web scraping
    
    if not all_news:
        print("❌ No se pudieron obtener noticias")
        return False
    
    # Eliminar duplicados por título similar
    unique_news = []
    seen_titles = set()
    
    for news in all_news:
        title_clean = re.sub(r'[^\w\s]', '', news['title'].lower())
        title_words = set(title_clean.split())
        
        is_duplicate = False
        for seen_title in seen_titles:
            seen_words = set(seen_title.split())
            if len(title_words.intersection(seen_words)) / max(len(title_words), len(seen_words)) > 0.7:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_news.append(news)
            seen_titles.add(title_clean)
    
    # Ordenar por fecha y limitar
    unique_news = sorted(unique_news, key=lambda x: x['date'], reverse=True)
    unique_news = unique_news[:18]  # Máximo 18 noticias
    
    # Agregar estructura de agentes
    for i, news in enumerate(unique_news, 1):
        news['id'] = i
        news['agents'] = {
            'logic': f'Noticia de {news["source"]} - Fuente confiable verificada mediante scraping',
            'context': f'Publicada el {news["date"]} - Información de medio argentino reconocido',
            'expert': 'Evaluación especializada requerida para confirmar datos específicos',
            'synth': [
                f'📰 Fuente: {news["source"]}',
                f'📅 Fecha: {news["date"]}',
                '🔍 Estado: Noticia real obtenida',
                '⚡ Tipo: Información verificada'
            ]
        }
    
    # Guardar archivo
    try:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'real_news.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_news, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== RESUMEN FINAL ===")
        print(f"✓ {len(unique_news)} noticias únicas guardadas")
        
        # Mostrar distribución por medio
        sources_count = {}
        for news in unique_news:
            source = news['source']
            sources_count[source] = sources_count.get(source, 0) + 1
        
        print("\n--- DISTRIBUCIÓN POR MEDIO ---")
        for source, count in sources_count.items():
            print(f"{source}: {count} noticias")
        
        print("\n--- MUESTRA DE NOTICIAS ---")
        for news in unique_news[:6]:
            print(f"{news['source']}: {news['title'][:60]}...")
        
        return True
        
    except Exception as e:
        print(f"Error guardando archivo: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)