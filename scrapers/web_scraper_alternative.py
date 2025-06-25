#!/usr/bin/env python3
"""
Scraper alternativo para sitios argentinos que no tienen RSS funcional
Usa web scraping directo para Infobae, TN y otros medios
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random

def clean_text(text):
    """Limpia y normaliza texto"""
    if not text:
        return ""
    
    # Remover HTML tags y normalizar espacios
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # Entidades HTML básicas
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'")
    text = text.replace('&nbsp;', ' ')
    
    return text.strip()

def scrape_infobae():
    """Scraper específico para Infobae"""
    try:
        print("Obteniendo Infobae...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Página de política argentina en Infobae
        response = requests.get('https://www.infobae.com/politica/', headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Buscar múltiples selectores para títulos
        selectors = [
            'h1 a', 'h2 a', 'h3 a',
            '.headline a', '.title a', '.story-title a',
            'article h1', 'article h2', 'article h3',
            '[data-testid*="headline"]', '[data-testid*="title"]'
        ]
        
        found_articles = []
        for selector in selectors:
            elements = soup.select(selector)
            found_articles.extend(elements[:5])
        
        # También buscar enlaces que contengan palabras clave
        all_links = soup.find_all('a', href=True)
        for link in all_links[:20]:
            if link.get_text() and len(link.get_text().strip()) > 20:
                found_articles.append(link)
        
        for article in found_articles[:15]:
            try:
                title = clean_text(article.get_text() if hasattr(article, 'get_text') else str(article))
                
                if len(title) < 10:
                    continue
                
                # Obtener URL
                url = ''
                if hasattr(article, 'get') and article.get('href'):
                    url = article.get('href')
                elif article.find('a'):
                    url = article.find('a').get('href', '')
                
                if url:
                    if url.startswith('/'):
                        url = 'https://www.infobae.com' + url
                    elif not url.startswith('http'):
                        continue
                
                # Filtrar URLs de Infobae válidas
                if url and 'infobae.com' in url and title and len(title) > 15:
                    news_item = {
                        'title': title[:120],
                        'summary': "Noticia de política argentina - Infobae",
                        'source': 'Infobae',
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'url': url,
                        'verdict': 'uncertain'
                    }
                    
                    # Evitar duplicados
                    if not any(existing['title'] == news_item['title'] for existing in news_items):
                        news_items.append(news_item)
                        
                        if len(news_items) >= 3:
                            break
                        
            except Exception as e:
                continue
        
        print(f"✓ {len(news_items)} noticias obtenidas de Infobae")
        return news_items
        
    except Exception as e:
        print(f"Error obteniendo Infobae: {e}")
        return []

def scrape_tn():
    """Scraper específico para TN"""
    try:
        print("Obteniendo TN...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Página principal de TN
        response = requests.get('https://tn.com.ar/', headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Buscar artículos principales
        articles = soup.find_all(['article', 'div', 'section'], class_=re.compile(r'.*(?:article|story|news|headline).*'), limit=10)
        
        for article in articles:
            try:
                # Buscar título
                title_elem = article.find(['h1', 'h2', 'h3', 'a'], class_=re.compile(r'.*(?:title|headline).*'))
                if not title_elem:
                    title_elem = article.find(['h1', 'h2', 'h3'])
                
                if title_elem:
                    title = clean_text(title_elem.get_text())
                    
                    # Buscar enlace
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                    if not link_elem:
                        link_elem = article.find('a')
                    
                    url = ''
                    if link_elem and link_elem.get('href'):
                        url = link_elem.get('href')
                        if url.startswith('/'):
                            url = 'https://tn.com.ar' + url
                    
                    # Buscar resumen/descripción
                    summary_elem = article.find(['p', 'div'], class_=re.compile(r'.*(?:summary|description|lead).*'))
                    if not summary_elem:
                        summary_elem = article.find('p')
                    
                    summary = ''
                    if summary_elem:
                        summary = clean_text(summary_elem.get_text())
                    
                    if title and len(title) > 10 and url:
                        news_item = {
                            'title': title[:120],
                            'summary': summary[:250] if summary else "Noticia de TN",
                            'source': 'TN',
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'url': url,
                            'verdict': 'uncertain'
                        }
                        news_items.append(news_item)
                        
                        if len(news_items) >= 3:
                            break
                        
            except Exception as e:
                continue
        
        print(f"✓ {len(news_items)} noticias obtenidas de TN")
        return news_items
        
    except Exception as e:
        print(f"Error obteniendo TN: {e}")
        return []

def scrape_cnn_espanol():
    """Scraper para CNN en Español (Argentina)"""
    try:
        print("Obteniendo CNN en Español...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get('https://cnnespanol.cnn.com/category/america-latina/argentina/', headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = []
        
        # Buscar artículos
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'.*(?:article|post|story).*'), limit=8)
        
        for article in articles:
            try:
                title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                if title_elem:
                    title = clean_text(title_elem.get_text())
                    
                    link_elem = title_elem if title_elem.name == 'a' else title_elem.find('a')
                    if not link_elem:
                        link_elem = article.find('a')
                    
                    url = ''
                    if link_elem and link_elem.get('href'):
                        url = link_elem.get('href')
                        if not url.startswith('http'):
                            url = 'https://cnnespanol.cnn.com' + url
                    
                    if title and len(title) > 10 and url and 'argentina' in url.lower():
                        news_item = {
                            'title': title[:120],
                            'summary': "Noticia internacional sobre Argentina",
                            'source': 'CNN Español',
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'url': url,
                            'verdict': 'uncertain'
                        }
                        news_items.append(news_item)
                        
                        if len(news_items) >= 2:
                            break
                        
            except Exception as e:
                continue
        
        print(f"✓ {len(news_items)} noticias obtenidas de CNN Español")
        return news_items
        
    except Exception as e:
        print(f"Error obteniendo CNN Español: {e}")
        return []

def main():
    """Función principal del scraper alternativo"""
    print("=== Scraper Alternativo - Medios Argentinos ===")
    
    all_news = []
    
    # Delay entre requests para ser respetuosos
    scrapers = [
        scrape_infobae,
        scrape_tn,
        scrape_cnn_espanol
    ]
    
    for scraper in scrapers:
        try:
            news_items = scraper()
            all_news.extend(news_items)
            
            # Pausa entre scrapers
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"Error en scraper: {e}")
            continue
    
    if not all_news:
        print("❌ No se pudieron obtener noticias del scraper alternativo")
        return False
    
    # Agregar estructura de agentes
    for i, news in enumerate(all_news, 1):
        news['id'] = 1000 + i  # IDs altos para evitar conflictos
        news['agents'] = {
            'logic': f'Noticia de {news["source"]} - Fuente verificada mediante scraping directo',
            'context': f'Obtenida el {news["date"]} - Información extraída de sitio web oficial',
            'expert': 'Contenido obtenido directamente del medio, requiere análisis detallado',
            'synth': [
                f'📰 Fuente: {news["source"]}',
                f'📅 Fecha: {news["date"]}',
                '🔍 Estado: Scraping directo exitoso',
                '⚡ Tipo: Contenido web extraído'
            ]
        }
    
    print(f"\n=== RESUMEN SCRAPER ALTERNATIVO ===")
    print(f"✓ {len(all_news)} noticias adicionales obtenidas")
    
    for news in all_news:
        print(f"{news['source']}: {news['title'][:60]}...")
    
    return all_news

if __name__ == "__main__":
    news = main()
    if news:
        print(f"\n✓ Scraper alternativo completado: {len(news)} noticias")
    else:
        print("❌ Scraper alternativo falló")