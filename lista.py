import requests
import os
import re
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def merger_playlist():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  # File locale
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"  # Remoto
    url5 = "eventisps.m3u8"
    url6 = "eventisz.m3u8"
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist5 = download_playlist(url5)
    playlist6 = download_playlist(url6)
    
    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist5 + "\n" + playlist6
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
    
# Funzione per il primo script (merger_playlist.py)
def merger_playlistworld():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u" 
    url4 = "world.m3u8"           
    url5 = "eventisps.m3u8"      
    url6 = "eventisz.m3u8"
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist4 = download_playlist(url4, exclude_group_title="Italy")
    playlist5 = download_playlist(url5)
    playlist6 = download_playlist(url6)

    
    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist4 + "\n" + playlist5 + "\n" + playlist6
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
def eventi_sz():
    import requests
    from bs4 import BeautifulSoup
    import re
    import time
    import json
    from urllib.parse import urljoin, urlparse
    from urllib.parse import parse_qs, quote
    import os
    from dotenv import load_dotenv
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError:
        print("Pillow library not found. Please install it: pip install Pillow")
        # You might want to exit or handle this more gracefully if Pillow is essential
        Image = None 
        UnidentifiedImageError = None
    import hashlib
    import io

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()
    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

    class SportZoneScraper:
        STATIC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        STATIC_USER_AGENT_ENCODED = 'Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/120.0.0.0%20Safari/537.36'

        def __init__(self):
            self.base_url = os.getenv("LINK_SPORTZONE", "https://sportzone.yoga").strip()
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': self.STATIC_USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': f'{self.base_url}/'
            })
            self.logos_dir = "logos"
            os.makedirs(self.logos_dir, exist_ok=True)
        
        def get_page_content(self, url):
            """Ottiene il contenuto HTML di una pagina"""
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Errore nel recuperare {url}: {e}")
                return None
        
        def extract_match_links(self, html_content):
            """Estrae i link delle partite dalla pagina calcio con selettori più specifici"""
            soup = BeautifulSoup(html_content, 'html.parser')
            match_links = []
            
            # Cerca diversi pattern comuni per i link delle partite
            selectors = [
                'a[href*="match"]',
                'a[href*="partita"]', 
                'a[href*="live"]',
                'a[href*="stream"]',
                '.match-link a',
                '.game-link a',
                '.event-link a',
                'article a',
                '.post-title a',
                '.entry-title a',
                '.post a',
                '.item a',
                '.content a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        title = link.get_text(strip=True)
                        if title and len(title) > 2:  # Evita link con titoli troppo corti o vuoti
                            full_url = urljoin(self.base_url, href)
                            
                            # Escludi link che sono pagine di categoria o serie
                            if '/category/' in full_url.lower() or '/series/' in full_url.lower():
                                continue # Salta questo link
                                
                            match_links.append({'title': title, 'url': full_url})
            
            # Se non trova nulla con i selettori, cerca tutti i link
            if not match_links:
                print("🔍 Nessun link trovato con selettori specifici, cerco tutti i link...")
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    title = link.get_text(strip=True)
                    if href and title and len(title) > 2:
                        # Filtra solo link che sembrano essere partite o contenuti sportivi
                        keywords = ['match', 'partita', 'live', 'vs', 'serie', 'champions', 'europa', 
                                   'calcio', 'football', 'streaming', 'diretta', 'oggi', 'domani']
                        if any(keyword in href.lower() or keyword in title.lower() for keyword in keywords):
                            full_url = urljoin(self.base_url, href)

                            # Escludi link che sono pagine di categoria o serie anche qui
                            if '/category/' in full_url.lower() or '/series/' in full_url.lower():
                                continue # Salta questo link

                            match_links.append({'title': title, 'url': full_url})

            
            # Rimuovi duplicati
            seen_urls = set()
            unique_matches = []
            for match in match_links:
                if match['url'] not in seen_urls:
                    seen_urls.add(match['url'])
                    unique_matches.append(match)
            
            return unique_matches
        
        def extract_stream_urls(self, match_url, original_match_title=""):
            """Estrae gli URL di streaming con tecniche avanzate"""
            html_content = self.get_page_content(match_url)
            if not html_content:
                print(f"    ⚠️  Impossibile ottenere contenuto da {match_url} per estrarre stream.")
                return []
            
            soup = BeautifulSoup(html_content, 'html.parser')
            stream_urls = []
            
            # 1. Cerca iframe (molto comune per gli embed)
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src') or iframe.get('data-src')
                if src:
                    full_url = urljoin(self.base_url, src)
                    stream_urls.append(full_url)
            
            # 2. Cerca video tags
            for video in soup.find_all('video'):
                src = video.get('src') or video.get('data-src')
                if src:
                    stream_urls.append(urljoin(self.base_url, src))
                
                # Cerca anche nei source tags dentro video
                for source in video.find_all('source'):
                    src = source.get('src')
                    if src:
                        stream_urls.append(urljoin(self.base_url, src))
            
            # 3. Cerca negli script JavaScript con pattern più avanzati
            for script in soup.find_all('script'):
                if script.string:
                    script_content = script.string
                    
                    # Pattern per URL di streaming
                    patterns = [
                        r'["\']([^"\']*.m3u8[^"\']*)["\']',
                        r'["\']([^"\']*.mp4[^"\']*)["\']',
                        r'["\']([^"\']*.ts[^"\']*)["\']',
                        r'src[\s]*:[\s]*["\']([^"\']*)["\']',
                        r'url[\s]*:[\s]*["\']([^"\']*)["\']',
                        r'stream[\s]*:[\s]*["\']([^"\']*)["\']',
                        r'player[\s]*:[\s]*["\']([^"\']*)["\']',
                        r'https?://[^\s"\'>]+\.m3u8[^\s"\'>]*',
                        r'https?://[^\s"\'>]+\.mp4[^\s"\'>]*',
                        r'file[\s]*:[\s]*["\']([^"\']*)["\']',
                        r'source[\s]*:[\s]*["\']([^"\']*)["\']'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, script_content, re.IGNORECASE)
                        for match in matches:
                            if match.startswith('http') or match.startswith('//'):
                                stream_urls.append(match)
                            elif match.startswith('/'):
                                stream_urls.append(urljoin(self.base_url, match))
            
            # 4. Cerca link diretti a file multimediali
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and any(ext in href.lower() for ext in ['.m3u8', '.mp4', '.ts', '.flv', '.avi', '.mkv']):
                    stream_urls.append(urljoin(self.base_url, href))
            
            # 5. Cerca attributi data-* che potrebbero contenere URL
            data_attributes = ['data-src', 'data-url', 'data-stream', 'data-file', 'data-video']
            for attr in data_attributes:
                for element in soup.find_all(attrs={attr: True}):
                    data_value = element.get(attr)
                    if data_value:
                        stream_urls.append(urljoin(self.base_url, data_value))
            
            # 6. Cerca nei meta tags
            for meta in soup.find_all('meta'):
                content = meta.get('content', '')
                if content and any(ext in content.lower() for ext in ['.m3u8', '.mp4']):
                    if content.startswith('http'):
                        stream_urls.append(content)
            
            # Filtra e pulisci gli URL
            cleaned_urls = []
            for url in stream_urls:
                if url and url.startswith('http'):
                    # Rimuovi parametri di tracking comuni
                    clean_url = re.sub(r'[?&](utm_|ref|track)', '', url)
                    
                    parsed_url = urlparse(clean_url)
                    domain = parsed_url.netloc.lower()
                    path = parsed_url.path.lower()

                    # Gestione speciale per newembedplay.xyz/calcio.php
                    if domain == 'newembedplay.xyz' and path == '/calcio.php':
                        query_parameters = parse_qs(parsed_url.query)
                        stream_id_list = query_parameters.get('id')
                        if stream_id_list:
                            stream_id = stream_id_list[0] # Prendi il primo valore dell'id
                            new_kso_url = f"https://new.newkso.ru/calcio/calcio{stream_id}/mono.m3u8"
                            if len(new_kso_url) > 10 and new_kso_url not in cleaned_urls:
                                print(f"    🔄 Trasformato URL: {clean_url[:60]}... -> {new_kso_url}")
                                cleaned_urls.append(new_kso_url)
                            continue # URL processato (trasformato o scartato se id non valido), passa al prossimo


                    # Lista di domini da escludere a priori (pagine di embed generiche, pubblicità)
                    generic_embed_domains = [
                        'newembedplay.xyz', 'embedsito.net', 'playeronline.xyz', 'streamgo.to',
                        'playhd.xyz', 'streaminghd.live', # Aggiungere altri domini problematici osservati
                    ]

                    if any(ex_domain in domain for ex_domain in generic_embed_domains):
                        print(f"    ⚠️  URL scartato (dominio di embed generico): {clean_url[:80]}...")
                        continue
                    
                    # Filtro specifico per "calcio.php" se il titolo non è calcistico
                    is_calcio_event = "calcio" in original_match_title.lower()
                    if "calcio.php" in path and not is_calcio_event:
                        print(f"    ⚠️  URL scartato ('calcio.php' in evento non calcistico '{original_match_title[:30]}...'): {clean_url[:80]}...")
                        continue

                    # Aggiungi solo se non già presente e di lunghezza ragionevole
                    if len(clean_url) > 10 and clean_url not in cleaned_urls:
                        cleaned_urls.append(clean_url)
            
            
            return cleaned_urls
        
        def _clean_m3u_title(self, title_str):
            """Cleans and formats a title string for M3U8 playlist."""
            processed_title = title_str
            time_component = ""

            # 1. Extract and format time (HH:MM), then remove it from the main title string.
            #    Handles HH:MM, H:M, HH.MM, H.M, with optional AM/PM.
            #    The time will be put in parentheses, e.g., (HH:MM).
            time_pattern = r'\b(\d{1,2})[:.](\d{1,2})\b(?:\s*(?:AM|PM|A\.M\.|P\.M\.))?'
            
            def time_replacer(match):
                nonlocal time_component
                hours = match.group(1).zfill(2) # Format hours to HH
                minutes = match.group(2).zfill(2) # Format minutes to MM
                time_component = f"({hours}:{minutes})"
                return "" # Remove the time from its original position

            # Apply substitution to extract time and remove it from processed_title
            # count=1 ensures only the first occurrence of time is processed.
            processed_title, num_subs = re.subn(time_pattern, time_replacer, processed_title, count=1, flags=re.IGNORECASE)
            if num_subs > 0:
                processed_title = processed_title.strip() # Clean spaces left by removal

            # 2. Handle |: Ensure it's surrounded by spaces.
            processed_title = processed_title.replace('|', ' | ')

            # 3. Insert space before date if concatenated (e.g., "TeamNameYYYY-MM-DD").
            # Example: "EventName2025-01-01" -> "EventName 2025-01-01"
            processed_title = re.sub(r'(\w)(\d{4}-\d{2}-\d{2})', r'\1 \2', processed_title)

            # 4. Remove Date (YYYY-MM-DD), replacing it and any surrounding spaces with a single space.
            processed_title = re.sub(r'\s*\d{4}-\d{2}-\d{2}\s*', ' ', processed_title)

            # 5. Clean unwanted characters:
            # Keep letters, numbers, spaces, hyphens (e.g., for team names), and pipes.
            # Colons are removed from the allowed set as time is now handled separately.
            processed_title = re.sub(r'[^\w\s\-\|]', '', processed_title)

            # 6. Normalize multiple spaces to single spaces and strip leading/trailing whitespace.
            processed_title = re.sub(r'\s+', ' ', processed_title).strip()
            
            # 7. Append the extracted and formatted time component if it exists.
            if time_component:
                if processed_title: # If title is not empty after cleaning
                    processed_title = f"{processed_title} {time_component}"
                else: # If title became empty (e.g., was just a date and time)
                    processed_title = time_component
            
            return processed_title

        def _make_logo_filename(self, text_identifier):
            """Creates a unique, filesystem-safe filename for a logo using a hash."""
            hasher = hashlib.md5()
            hasher.update(text_identifier.encode('utf-8'))
            filename_hash = hasher.hexdigest()
            return f"{filename_hash}.png"

        def extract_and_combine_team_logos(self, event_page_url, event_title):
            """
            Extracts two team logos from an event page, combines them side-by-side,
            and saves the result.
            Returns the path to the combined logo, or None if unsuccessful.
            Requires Pillow library.
            """
            if not Image or not UnidentifiedImageError:
                print("      ⚠️  Pillow library is not available. Cannot process logos.")
                return None

            print(f"      🖼️  Fetching event page for logos: {event_page_url}")
            html_content = self.get_page_content(event_page_url)
            if not html_content:
                print(f"      ⚠️  Could not get content from {event_page_url} for logos.")
                return None

            soup = BeautifulSoup(html_content, 'html.parser')
            logo_img_tags = []

            # --- !!! CRITICAL SECTION - ADJUST SELECTORS !!! ---
            # The following selectors are GENERIC GUESSES. You MUST inspect the HTML
            # of your target event pages (those with '/event/' in the URL or similar)
            # and update these selectors to accurately find the two team logo images.
            # Examples:
            # - If logos are <div class="home-team-logo"><img src="..."></div> and <div class="away-team-logo"><img src="..."></div>
            #   Use: soup.select('.home-team-logo img') and soup.select('.away-team-logo img')
            # - Or look for specific IDs, or images within certain article structures.

            # Updated selector based on the provided HTML structure: <img class="tist" src="...">
            potential_logo_containers = soup.select('img.tist')
            if len(potential_logo_containers) >= 2:
                logo_img_tags = potential_logo_containers[:2] # Take the first two plausible ones
            
            if len(logo_img_tags) < 2:
                print(f"      ⚠️  Found {len(logo_img_tags)} potential logo image tag(s) using generic selectors for '{event_title}'. Need 2. Please refine selectors.")
                return None

            logo_urls = [urljoin(event_page_url, img.get('src')) for img in logo_img_tags if img.get('src')]
            if len(logo_urls) < 2:
                print(f"      ⚠️  Could not extract 2 valid logo URLs for '{event_title}'.")
                return None
                
            print(f"      Found logo URLs: {logo_urls[0]}, {logo_urls[1]}")

            images = []
            for i, logo_url in enumerate(logo_urls[:2]):
                try:
                    print(f"        Downloading logo {i+1}: {logo_url}")
                    img_response = self.session.get(logo_url, timeout=10, stream=True)
                    img_response.raise_for_status()
                    img_data = io.BytesIO(img_response.content)
                    img = Image.open(img_data)
                    images.append(img)
                except requests.RequestException as e:
                    print(f"      ❌ Error downloading logo {logo_url}: {e}")
                    return None
                except UnidentifiedImageError:
                    print(f"      ❌ Error: Cannot identify image file {logo_url}.")
                    return None
                except Exception as e:
                    print(f"      ❌ Unexpected error processing logo {logo_url}: {e}")
                    return None

            if len(images) != 2: return None
            img1, img2 = images

            target_height = 64 # Desired height for logos
            img1 = img1.resize((int(img1.width * target_height / img1.height), target_height), Image.Resampling.LANCZOS)
            img2 = img2.resize((int(img2.width * target_height / img2.height), target_height), Image.Resampling.LANCZOS)

            combined_width = img1.width + img2.width
            combined_height = target_height
            combined_image = Image.new('RGBA', (combined_width, combined_height), (255, 255, 255, 0))
            combined_image.paste(img1, (0, 0), img1.convert('RGBA'))
            combined_image.paste(img2, (img1.width, 0), img2.convert('RGBA'))

            combined_logo_filename = self._make_logo_filename(event_page_url)
            combined_logo_path = os.path.join(self.logos_dir, combined_logo_filename)
            combined_image.save(combined_logo_path, "PNG")
            print(f"      ✅ Combined logo saved: {combined_logo_path}")
            return combined_logo_path

        def create_m3u8_playlist(self, matches_data, filename="eventisz.m3u8"):
            """Crea una playlist M3U8 con tutti i match trovati"""
            playlist_content = "#EXTM3U\n\n" # Inizia con #EXTM3U

            # Aggiungi il canale statico SPORTZONE
            sportzone_url = f"{self.base_url}" 
            playlist_content += f'#EXTINF:-1 tvg-name="SPORTZONE" group-title="Eventi Live",SPORTZONE\n'
            playlist_content += f'{sportzone_url}\n'
            MOTOGP_LOGO_URL = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/30fe8b41-1200-49f2-9d7e-8c604d04d601/d3bsjwp-3d0220a9-6673-4a17-b398-08c3d7208997.png/v1/fill/w_1024,h_676,strp/motogp_logo_by_grishnak_mcmlxxix_d3bsjwp-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9Njc2IiwicGF0aCI6IlwvZlwvMzBmZThiNDEtMTIwMC00OWYyLTlkN2UtOGM2MDRkMDRkNjAxXC9kM2JzandwLTNkMDIyMGE5LTY2NzMtNGExNy1iMzk4LTA4YzNkNzIwODk5Ny5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.d9DcxJeZ_XzlyLYfrxe4qnnhuDkGItSXgvgnSTjkhEY"
            FORMULA1_LOGO_URL = "https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-2-2.png"
            
            for match in matches_data:
                title = match.get('title', 'Unknown Match')
                streams = match.get('streams', [])
                event_page_url = match.get('url', '') # Corrected: 'url' is the key for the event page
                tvg_logo_path = match.get('tvg_logo_path')
                match_category = match.get('category', 'Sport') # Categoria specifica del match

                # Se non ci sono stream, salta questo evento e non aggiungerlo alla playlist
                if not streams:
                    print(f"      ℹ️  Skipping '{title}' from playlist: No streams found.")
                    continue

                tvg_logo_attr = ""
                if match_category == "Motogp": # "Motogp" è come viene generato da .title()
                    tvg_logo_attr = f' tvg-logo="{MOTOGP_LOGO_URL}"'
                elif match_category == "Formula 1": # "Formula 1" è come viene generato da .title()
                    tvg_logo_attr = f' tvg-logo="{FORMULA1_LOGO_URL}"'
                elif tvg_logo_path:
                    # tvg_logo_path is the OS-specific local path, e.g., "logos\hash.png" or "logos/hash.png"
                    logo_filename = os.path.basename(tvg_logo_path)
                    if NOMEGITHUB and NOMEREPO:
                        # Construct GitHub raw URL. Assuming 'main' as the default branch.
                        # self.logos_dir is "logos".
                        github_logo_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{self.logos_dir}/{logo_filename}"
                        tvg_logo_attr = f' tvg-logo="{github_logo_url}"'
                    else:
                        # Fallback to relative path, ensuring forward slashes for M3U8
                        standardized_local_path = tvg_logo_path.replace('\\', '/')
                        print(f"      ⚠️  NOMEGITHUB o NOMEREPO non impostati nel .env. Uso percorso relativo per il logo: {standardized_local_path}")
                        tvg_logo_attr = f' tvg-logo="{standardized_local_path}"'
                
                # Dato che abbiamo già verificato la presenza di 'streams', procediamo ad aggiungerli
                for stream_url in streams:
                    # Codifica self.base_url per l'uso nei parametri URL, mantenendo ':/'
                    encoded_base_url_for_param = quote(self.base_url, safe=':/')

                    # Costruisci la stringa dei parametri da aggiungere
                    params_to_add = f"h_user-agent={self.STATIC_USER_AGENT_ENCODED}&h_referer={encoded_base_url_for_param}%2F&h_origin={encoded_base_url_for_param}"

                    # Aggiungi i parametri all'URL dello stream
                    if '?' in stream_url: # Se ci sono già parametri, aggiungi con '&'
                        modified_stream_url = f"{stream_url}&{params_to_add}"
                    else: # Altrimenti, inizia i parametri con '?'
                        modified_stream_url = f"{stream_url}?{params_to_add}"
                    
                    clean_title = self._clean_m3u_title(title)
                    playlist_content += f'#EXTINF:-1 group-title="Eventi Live" tvg-name="{clean_title}"{tvg_logo_attr},{clean_title}\n'
                    playlist_content += f'{PROXY}{modified_stream_url}\n'

            # Salva la playlist
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(playlist_content)
            
            print(f"Playlist M3U8 salvata come {filename}")
            return filename
        
        def scrape_calcio_matches(self, max_matches=20):
            """Funzione principale migliorata"""
            print("🚀 Inizio scraping di SportZone Calcio (solo requests)...")
            
            # Lista di URL da provare
            urls_to_try = [
                f"{self.base_url}/category/Calcio/1",
                f"{self.base_url}/category/FORMULA%201/1",
                f"{self.base_url}/category/MotoGP/1",
                f"{self.base_url}/category/Tennis/1",
                f"{self.base_url}/category/Basket/1"
            ]
            
            all_matches = []
            
            for url in urls_to_try:
                print(f"🔍 Tentativo con: {url}")
                
                # Estrai la categoria dall'URL per usarla nel group-title
                category_match = re.search(r'/category/([^/]+)', url, re.IGNORECASE)
                category_name = "Sport" # Default
                if category_match:
                    cat_raw = category_match.group(1)
                    cat_decoded = requests.utils.unquote(cat_raw) # Gestisce %20 etc.
                    category_name = cat_decoded.replace('-', ' ').replace('_', ' ').title() # Pulisce e formatta

                html_content = self.get_page_content(url)
                if html_content:
                    matches_from_url = self.extract_match_links(html_content)
                    if matches_from_url:
                        print(f"✅ Trovate {len(matches_from_url)} partite in {url} (Categoria: {category_name})")
                        for match_item in matches_from_url:
                            match_item['category'] = category_name # Associa la categoria al match
                        all_matches.extend(matches_from_url)
                    else:
                        print(f"❌ Nessuna partita trovata in {url}")
                else:
                    print(f"❌ Impossibile accedere a {url}")
            
            if not all_matches:
                print("❌ Nessuna partita trovata in nessun URL")
                return []
            
            # Rimuovi duplicati
            seen_urls = set()
            unique_matches = []
            for match in all_matches:
                if match['url'] not in seen_urls:
                    seen_urls.add(match['url'])
                    unique_matches.append(match)
            
            print(f"📊 Totale partite uniche trovate: {len(unique_matches)}")
            
            # Limita il numero di partite da processare
            matches_to_process = unique_matches[:max_matches]
            matches_data = []
            
            for i, match in enumerate(matches_to_process, 1):
                print(f"⚽ Elaborando {i}/{len(matches_to_process)}: {match['title'][:50]}...")
                
                combined_logo_path = None
                # Attempt to get logos if it seems like an event page that might have them
                # The condition "/event/" is a heuristic based on your description.
                # Adjust if your event pages have a different URL pattern.
                if "/event/" in match['url'].lower() or " vs " in match['title'].lower() : # Added " vs " as another heuristic
                    print(f"    Trying to extract logos for: {match['title'][:50]} from {match['url']}")
                    combined_logo_path = self.extract_and_combine_team_logos(match['url'], match['title'])

                streams = self.extract_stream_urls(match['url'], match['title']) # Passa anche il titolo originale
                
                matches_data.append({
                    'title': match['title'],
                    'url': match['url'],
                    'streams': streams,
                    'stream_count': len(streams),
                    'category': match.get('category', 'Sport'), # Propaga la categoria
                    'tvg_logo_path': combined_logo_path
                })
                
                if streams:
                    print(f"  ✅ Trovati {len(streams)} stream")
                    for stream in streams[:2]:  # Mostra solo i primi 2
                        print(f"    🔗 {stream[:80]}...")
                else:
                    print(f"  ❌ Nessuno stream trovato")
                if combined_logo_path:
                    print(f"  🖼️  Logo generato: {combined_logo_path}")
                
                # Pausa per evitare sovraccarico
                time.sleep(1.5)
            
            return matches_data

    def main():
        """Funzione principale per eseguire lo scraping"""
        print("🚀 Avvio SportZone Scraper...")
        scraper = SportZoneScraper()
        
        try:
            matches = scraper.scrape_calcio_matches(max_matches=50)
            
            if matches:
                playlist = scraper.create_m3u8_playlist(matches)
                
                print("\n" + "=" * 50)
                print("📋 RIEPILOGO RISULTATI")
                print("=" * 50)
                
                total_streams = sum(match['stream_count'] for match in matches)
                matches_with_streams = sum(1 for match in matches if match['stream_count'] > 0)
                
                print(f"📊 Partite totali: {len(matches)}")
                print(f"🎥 Partite con stream: {matches_with_streams}")
                print(f"🔗 Stream totali trovati: {total_streams}")
                
                print("\n📝 DETTAGLIO PARTITE:")
                for i, match in enumerate(matches, 1):
                    status = "✅" if match['stream_count'] > 0 else "❌"
                    logo_status = "🖼️" if match.get('tvg_logo_path') else "▫️"
                    print(f"{i:2d}. {status} {logo_status} {match['title'][:60]}... ({match['stream_count']} stream)")
                
                print("\nNote:")
                print("- 🖼️ indica che un logo combinato è stato generato.")
                print("- ▫️ indica che non è stato generato un logo combinato per l'evento.")
                if total_streams > 0:
                    print(f"\n🎉 Playlist generata con successo!")
                    print(f"📁 File: {playlist}")
                elif matches_with_streams == 0 and len(matches) > 0:
                    print(f"📄 Playlist creata con le pagine delle partite.")
            else:
                print("❌ Nessuna partita trovata")
        
        except KeyboardInterrupt:
            print("\n⏹️  Scraping interrotto dall'utente")
        except Exception as e:
            print(f"❌ Errore durante lo scraping: {e}")
            import traceback
            traceback.print_exc()

    if __name__ == "__main__":
        main()
    
    # Aggiungi questo codice per creare sempre la lista anche se vuota
    try:
        # Ottieni la directory dove si trova lo script
        script_directory = os.path.dirname(os.path.abspath(__file__))
        playlist_file = os.path.join(script_directory, "eventisz.m3u8")
        
        # Se il file non esiste o è vuoto, crea una playlist vuota
        if not os.path.exists(playlist_file) or os.path.getsize(playlist_file) == 0:
            with open(playlist_file, 'w', encoding='utf-8') as f:
                f.write('#EXTM3U\n')
            print(f"📄 Creata playlist vuota: {playlist_file}")
        else:
            print(f"📁 Playlist esistente: {playlist_file}")
    except Exception as e:
        print(f"❌ Errore nella creazione della playlist vuota: {e}")
        # Crea comunque il file vuoto
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))
            playlist_file = os.path.join(script_directory, "eventisz.m3u8")
            with open(playlist_file, 'w', encoding='utf-8') as f:
                f.write('#EXTM3U\n')
        except:
            pass
    
# Funzione per il secondo script (epg_merger.py)
def epg_merger():
    # Codice del secondo script qui
    # Aggiungi il codice del tuo script "epg_merger.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo l'epg_merger.py...")
    # Il codice che avevi nello script "epg_merger.py" va qui, senza modifiche.
    import requests
    import gzip
    import os
    import xml.etree.ElementTree as ET
    import io

    # URL dei file GZIP o XML da elaborare
    urls_gzip = [
        'https://www.open-epg.com/files/italy1.xml',
        'https://www.open-epg.com/files/italy2.xml',
        'https://www.open-epg.com/files/italy3.xml',
        'https://www.open-epg.com/files/italy4.xml',
        'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'
    ]

    # File di output
    output_xml = 'epg.xml'    # Nome del file XML finale

    # URL remoto di it.xml
    url_it = 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/it.xml'

    # File eventi locale
    path_eventi = 'eventi.xml'

    def download_and_parse_xml(url):
        """Scarica un file .xml o .gzip e restituisce l'ElementTree."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Prova a decomprimere come GZIP
            try:
                with gzip.open(io.BytesIO(response.content), 'rb') as f_in:
                    xml_content = f_in.read()
            except (gzip.BadGzipFile, OSError):
                # Non è un file gzip, usa direttamente il contenuto
                xml_content = response.content

            return ET.ElementTree(ET.fromstring(xml_content))
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download da {url}: {e}")
        except ET.ParseError as e:
            print(f"Errore nel parsing del file XML da {url}: {e}")
        return None

    # Creare un unico XML vuoto
    root_finale = ET.Element('tv')
    tree_finale = ET.ElementTree(root_finale)

    # Processare ogni URL
    for url in urls_gzip:
        tree = download_and_parse_xml(url)
        if tree is not None:
            root = tree.getroot()
            for element in root:
                root_finale.append(element)

    # Aggiungere eventi.xml da file locale
    if os.path.exists(path_eventi):
        try:
            tree_eventi = ET.parse(path_eventi)
            root_eventi = tree_eventi.getroot()
            for programme in root_eventi.findall(".//programme"):
                root_finale.append(programme)
        except ET.ParseError as e:
            print(f"Errore nel parsing del file eventi.xml: {e}")
    else:
        print(f"File non trovato: {path_eventi}")

    # Aggiungere it.xml da URL remoto
    tree_it = download_and_parse_xml(url_it)
    if tree_it is not None:
        root_it = tree_it.getroot()
        for programme in root_it.findall(".//programme"):
            root_finale.append(programme)
    else:
        print(f"Impossibile scaricare o analizzare il file it.xml da {url_it}")

    # Funzione per pulire attributi
    def clean_attribute(element, attr_name):
        if attr_name in element.attrib:
            old_value = element.attrib[attr_name]
            new_value = old_value.replace(" ", "").lower()
            element.attrib[attr_name] = new_value

    # Pulire gli ID dei canali
    for channel in root_finale.findall(".//channel"):
        clean_attribute(channel, 'id')

    # Pulire gli attributi 'channel' nei programmi
    for programme in root_finale.findall(".//programme"):
        clean_attribute(programme, 'channel')

    # Salvare il file XML finale
    with open(output_xml, 'wb') as f_out:
        tree_finale.write(f_out, encoding='utf-8', xml_declaration=True)
    print(f"File XML salvato: {output_xml}")
    
def eventi_m3u8_generator_world():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
    import json 
    import re 
    import requests 
    from urllib.parse import quote 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()  # Proxy HLS 
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    # Base URLs for the standard stream checking mechanism
    NEW_KSO_BASE_URLS = [
        "https://new.newkso.ru/wind/",
        "https://new.newkso.ru/ddy6/",
        "https://new.newkso.ru/zeko/",
        "https://new.newkso.ru/nfs/",
        "https://new.newkso.ru/dokko1/",
    ]
    # Specific base URL for tennis channels
    WIKIHZ_TENNIS_BASE_URL = "https://new.newkso.ru/wikihz/"

    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(text_input):
        """
        Pulisce il testo per tvg-id: minuscolo, senza spazi, senza caratteri speciali (solo a-z0-9).
        """
        import re
        # Convert to lowercase
        cleaned = str(text_input).lower()
        # Remove spaces
        cleaned = re.sub(r'\s+', '', cleaned)
        # Remove special characters (keep only a-z, 0-9)
        cleaned = re.sub(r'[^a-z0-9]', '', cleaned)
        return cleaned
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerà l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id_str, is_tennis_channel=False): 
        # channel_id_str is the numeric ID like "121"
        # is_tennis_channel is a boolean flag
        raw_m3u8_url_found = None
        daddy_headers_str = "&h_User-Agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_Referer=https%3A%2F%2Falldownplay.xyz%2F&h_Origin=https%3A%2F%2Falldownplay.xyz"


        # Determine if we should use the special tennis URL logic
        # True if flagged by name OR if channel ID is like "15xx" (4 digits starting with 15)
        should_try_tennis_url = is_tennis_channel or \
                                (channel_id_str.startswith("15") and len(channel_id_str) == 4)

        if should_try_tennis_url:
            if not is_tennis_channel and channel_id_str.startswith("15") and len(channel_id_str) == 4:
                # Log if we're trying tennis logic based on ID pattern only
                print(f"[INFO] Channel ID {channel_id_str} matches 15xx pattern. Attempting tennis-specific URL.")
            # Try the specific tennis URL first
            last_two_digits = channel_id_str[-2:].zfill(2)
            tennis_stream_path = f"wikiten{last_two_digits}/mono.m3u8"
            candidate_url = f"{WIKIHZ_TENNIS_BASE_URL.rstrip('/')}/{tennis_stream_path.lstrip('/')}"
            try:
                response = session.get(candidate_url, stream=True, timeout=HTTP_TIMEOUT / 2)
                if response.status_code == 200:
                    print(f"[✓] Stream TENNIS (or 15xx ID) trovato per channel ID {channel_id_str} at: {candidate_url}")
                    raw_m3u8_url_found = candidate_url
                response.close()
            except requests.exceptions.Timeout:
                # print(f"[!] Timeout checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}")
                pass
            except requests.exceptions.ConnectionError:
                # print(f"[!] Connection error checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}")
                pass
            except requests.exceptions.RequestException:
                # print(f"[!] Error checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}: {e}")
                pass
        
        if raw_m3u8_url_found: # If found with tennis/15xx logic, apply proxy and return
            url_with_headers = raw_m3u8_url_found + daddy_headers_str
            if PROXY:
                return f"{PROXY.rstrip('/')}{url_with_headers}"
            return url_with_headers

        # If not found with tennis/15xx logic OR if it wasn't a tennis/15xx channel, try standard URLs
        for base_url in NEW_KSO_BASE_URLS: # These are the standard base URLs
            stream_path = f"premium{channel_id_str}/mono.m3u8"
            candidate_url = f"{base_url.rstrip('/')}/{stream_path.lstrip('/')}"
            try:
                response = session.get(candidate_url, stream=True, timeout=HTTP_TIMEOUT / 2) # HTTP_TIMEOUT is 10, so 5s timeout
                if response.status_code == 200:
                    print(f"[✓] Stream found for channel ID {channel_id_str} at: {candidate_url}")
                    raw_m3u8_url_found = candidate_url
                    response.close() # Close the stream connection
                    break 
                else:
                    pass
                response.close() # Ensure connection is closed
            except requests.exceptions.Timeout:
                pass 
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.RequestException: 
                pass 
        
        if raw_m3u8_url_found: # This will be from the standard loop if reached here
            url_with_headers = raw_m3u8_url_found + daddy_headers_str
            if PROXY: # PROXY is a global variable from .env
                return f"{PROXY.rstrip('/')}{url_with_headers}"
            return url_with_headers
        else:
            # This print might be too verbose if many channels fail, consider removing or reducing frequency
            # print(f"[✗] No stream found for channel ID {channel_id_str} after checking all base URLs.")
            return None 
     
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it", "uk", "tnt", "usa", "tennis", "la"} 
        now = datetime.now()  # Ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
     
            # filtro solo per eventi del giorno corrente 
            if date_obj != now.date(): 
                continue 
     
            date_str = date_obj.strftime("%Y-%m-%d") 
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") 
                    try: 
                        # Parse orario evento 
                        time_obj = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2)  # correzione timezone? 
     
                        # crea datetime completo con data evento e orario evento 
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 
     
                        # Controllo: includi solo se l'evento è iniziato da meno di 2 ore 
                        if now - event_datetime > timedelta(hours=2): 
                            # Evento iniziato da più di 2 ore -> salto 
                            continue 
     
                        time_formatted = time_obj.strftime("%H:%M") 
                    except Exception: 
                        time_formatted = time_str 
     
                    event_title = item.get("event", "Evento") 
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 

                        # Determine if it's a tennis channel based on its name
                        is_tennis = False
                        if "tennis channel" in channel_name.lower() or "tennis stream" in channel_name.lower():
                            is_tennis = True
                            
                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title,  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                                "is_tennis": is_tennis # Add the flag
                            }) 
     
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 
     
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Aggiungi il canale iniziale/informativo
            f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live",DADDYLIVE\n')
            f.write("https://example.com.m3u8\n\n")
     
            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
          
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    # channel_id_original = ch["channel_id"] # ID numerico originale, usato per get_stream
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    is_tennis_event_channel = ch.get("is_tennis", False) # Get the flag
                    
                    # Genera tvg-id basato sul nome dell'evento pulito
                    event_based_tvg_id = clean_tvg_id(event_title)
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title) 
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        stream = get_stream_from_channel_id(ch["channel_id"], is_tennis_channel=is_tennis_event_channel) # Pass the flag
                        if stream: 
                            f.write(f'#EXTINF:-1 tvg-id="{event_based_tvg_id}" tvg-name="{category} | {tvg_name}"{logo_attribute} group-title="Eventi Live",{category} | {tvg_name}\n{stream}\n\n') 
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    if __name__ == "__main__": 
        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)

# Funzione per il terzo script (eventi_m3u8_generator.py)
def eventi_m3u8_generator():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
    import json 
    import re 
    import requests 
    from urllib.parse import quote 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()
    
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()  # Proxy HLS 
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    # Base URLs for the standard stream checking mechanism
    NEW_KSO_BASE_URLS_ITA = [ # Renamed to avoid conflict if this script was one giant file
        "https://new.newkso.ru/wind/",
        "https://new.newkso.ru/ddy6/",
        "https://new.newkso.ru/zeko/",
        "https://new.newkso.ru/nfs/",
        "https://new.newkso.ru/dokko1/",
    ]
    # Specific base URL for tennis channels (duplicate for this function's scope)
    WIKIHZ_TENNIS_BASE_URL_ITA = "https://new.newkso.ru/wikihz/"

    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(text_input):
        """
        Pulisce il testo per tvg-id: minuscolo, senza spazi, senza caratteri speciali (solo a-z0-9).
        """
        import re
        # Convert to lowercase
        cleaned = str(text_input).lower()
        # Remove spaces
        cleaned = re.sub(r'\s+', '', cleaned)
        # Remove special characters (keep only a-z, 0-9)
        cleaned = re.sub(r'[^a-z0-9]', '', cleaned)
        return cleaned
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerà l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id_str, is_tennis_channel=False): 
        # channel_id_str is the numeric ID like "121"
        # is_tennis_channel is a boolean flag
        raw_m3u8_url_found = None
        daddy_headers_str = "&h_User-Agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_Referer=https%3A%2F%2Falldownplay.xyz%2F&h_Origin=https%3A%2F%2Falldownplay.xyz"


        # Determine if we should use the special tennis URL logic
        # True if flagged by name OR if channel ID is like "15xx" (4 digits starting with 15)
        should_try_tennis_url = is_tennis_channel or \
                                (channel_id_str.startswith("15") and len(channel_id_str) == 4)

        if should_try_tennis_url:
            if not is_tennis_channel and channel_id_str.startswith("15") and len(channel_id_str) == 4:
                # Log if we're trying tennis logic based on ID pattern only
                print(f"[INFO] Channel ID {channel_id_str} matches 15xx pattern. Attempting tennis-specific URL.")
            # Try the specific tennis URL first
            last_two_digits = channel_id_str[-2:].zfill(2)
            tennis_stream_path = f"wikiten{last_two_digits}/mono.m3u8"
            candidate_url = f"{WIKIHZ_TENNIS_BASE_URL_ITA.rstrip('/')}/{tennis_stream_path.lstrip('/')}"
            try:
                response = session.get(candidate_url, stream=True, timeout=HTTP_TIMEOUT / 2)
                if response.status_code == 200:
                    print(f"[✓] Stream TENNIS (or 15xx ID) trovato per channel ID {channel_id_str} at: {candidate_url}")
                    raw_m3u8_url_found = candidate_url
                response.close()
            except requests.exceptions.Timeout:
                # print(f"[!] Timeout checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}")
                pass
            except requests.exceptions.ConnectionError:
                # print(f"[!] Connection error checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}")
                pass
            except requests.exceptions.RequestException:
                # print(f"[!] Error checking TENNIS stream for channel ID {channel_id_str} at {candidate_url}: {e}")
                pass

        if raw_m3u8_url_found: # If found with tennis/15xx logic, apply proxy and return
            url_with_headers = raw_m3u8_url_found + daddy_headers_str
            if PROXY:
                return f"{PROXY.rstrip('/')}{url_with_headers}"
            return url_with_headers

        # If not found with tennis/15xx logic OR if it wasn't a tennis/15xx channel, try standard URLs
        for base_url in NEW_KSO_BASE_URLS_ITA: # These are the standard base URLs
            stream_path = f"premium{channel_id_str}/mono.m3u8"
            candidate_url = f"{base_url.rstrip('/')}/{stream_path.lstrip('/')}"
            try:
                response = session.get(candidate_url, stream=True, timeout=HTTP_TIMEOUT / 2)
                if response.status_code == 200:
                    print(f"[✓] Stream found for channel ID {channel_id_str} at: {candidate_url}")
                    raw_m3u8_url_found = candidate_url
                    response.close()
                    break
                else:
                    pass
                response.close()
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.RequestException:
                pass
        
        if raw_m3u8_url_found: # This will be from the standard loop if reached here
            url_with_headers = raw_m3u8_url_found + daddy_headers_str
            if PROXY: # PROXY is a global variable from .env
                return f"{PROXY.rstrip('/')}{url_with_headers}"
            return url_with_headers
        else:
            return None 
     
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it"} 
        now = datetime.now()  # ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
     
            is_today = (date_obj == now.date())
            is_yesterday_target_event = (date_obj == yesterday_date)

            if not (is_today or is_yesterday_target_event):
                continue # Salta se non è né oggi né un evento target di ieri
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") # Orario dal JSON
                    event_title = item.get("event", "Evento") 
                    
                    try: 
                        event_time_from_json = datetime.strptime(time_str, "%H:%M").time()

                        # Logica di filtraggio basata sulla data
                        if is_today:
                            # Per gli eventi di oggi, applica la correzione timezone e il filtro "non più vecchio di 2 ore"
                            time_obj_corrected = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2) # correzione timezone
                            event_datetime_corrected = datetime.combine(date_obj, time_obj_corrected.time())
                            
                            if now - event_datetime_corrected > timedelta(hours=2):
                                # Evento di oggi iniziato da più di 2 ore -> salto
                                continue
                            time_formatted = time_obj_corrected.strftime("%H:%M")

                        elif is_yesterday_target_event:
                            # Per gli eventi di ieri, controlla se l'orario JSON è tra 00:00 e 04:00
                            start_filter_time = datetime.strptime("00:00", "%H:%M").time()
                            end_filter_time = datetime.strptime("04:00", "%H:%M").time()
                            
                            if not (start_filter_time <= event_time_from_json <= end_filter_time):
                                # Evento di ieri fuori dall'intervallo 00:00-04:00 (ora JSON) -> salto
                                continue
                            
                            # Per gli eventi di ieri in questo range, usiamo l'orario corretto per la visualizzazione
                            time_obj_corrected = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2)
                            time_formatted = time_obj_corrected.strftime("%H:%M")
                        
                        else: # Non dovrebbe accadere a causa del controllo sulla data esterna, ma per sicurezza
                            continue 

                    except ValueError: # Errore nel parsing di time_str
                        print(f"[!] Orario evento non valido '{time_str}' per l'evento '{event_title}'. Evento saltato.")
                        continue
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 

                        # Determine if it's a tennis channel based on its name
                        is_tennis = False
                        if "tennis channel" in channel_name.lower() or "tennis stream" in channel_name.lower():
                            is_tennis = True

                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})"
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title,  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                                "is_tennis": is_tennis # Add the flag
                            }) 
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 
     
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Aggiungi il canale iniziale/informativo
            f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live",DADDYLIVE\n')
            f.write("https://example.com.m3u8\n\n")
     
            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
          
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    # channel_id_original = ch["channel_id"] # ID numerico originale, usato per get_stream
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    is_tennis_event_channel = ch.get("is_tennis", False) # Get the flag
                    
                    # Genera tvg-id basato sul nome dell'evento pulito
                    event_based_tvg_id = clean_tvg_id(event_title)
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title) 
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        stream = get_stream_from_channel_id(ch["channel_id"], is_tennis_channel=is_tennis_event_channel) # Pass the flag
                        if stream: 
                            f.write(f'#EXTINF:-1 tvg-id="{event_based_tvg_id}" tvg-name="{category} | {tvg_name}"{logo_attribute} group-title="Eventi Live",{category} | {tvg_name}\n{stream}\n\n') 
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    if __name__ == "__main__": 
        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)
        
def eventi_sps():
    import requests
    import re
    import os
    from bs4 import BeautifulSoup
    from urllib.parse import quote_plus
    from datetime import datetime # Aggiunto import per la data corrente
    from dotenv import load_dotenv

    load_dotenv()

    # Prefisso per il proxy dello stream
    PROXY = os.getenv("PROXYIP", "").strip()

    # URL di partenza (homepage o pagina con elenco eventi)
    base_url = "https://www.sportstreaming.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Origin": "https://www.sportstreaming.net",
        "Referer": "https://www.sportstreaming.net/"
    }

    # Funzione helper per formattare la data dell'evento
    def format_event_date(date_text):
        """
        Formatta la data dell'evento e restituisce la stringa formattata completa e una stringa DD/MM per il confronto.
        Restituisce: (full_formatted_date, simple_date_dd_mm)
        Esempio: ("20:45 23/07", "23/07") o ("", "") se non parsabile.
        """
        if not date_text:
            return "", ""
        match = re.search(
            r'(?:[a-zA-Zì]+\s+)?(\d{1,2})\s+([a-zA-Z]+)\s+(?:ore\s+)?(\d{1,2}:\d{2})',
            date_text,
            re.IGNORECASE
        )
        if match:
            day_str = match.group(1).zfill(2)
            month_name = match.group(2).lower()
            time = match.group(3)
            month_number = ITALIAN_MONTHS_MAP.get(month_name)
            if month_number:
                return f"{time} {day_str}/{month_number}", f"{day_str}/{month_number}"
        return "", ""

    # Mappa dei mesi italiani per la formattazione della data
    ITALIAN_MONTHS_MAP = {
        "gennaio": "01", "febbraio": "02", "marzo": "03", "aprile": "04",
        "maggio": "05", "giugno": "06", "luglio": "07", "agosto": "08",
        "settembre": "09", "ottobre": "10", "novembre": "11", "dicembre": "12"
    }

    # Funzione per trovare i link alle pagine evento
    def find_event_pages():
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            event_links = []
            seen_links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if re.match(r'/live-(perma-)?\d+', href):
                    full_url = base_url + href.lstrip('/')
                    if full_url not in seen_links:
                        event_links.append(full_url)
                        seen_links.add(full_url)
                elif re.match(r'https://www\.sportstreaming\.net/live-(perma-)?\d+', href):
                    if href not in seen_links:
                        event_links.append(href)
                        seen_links.add(href)

            return event_links

        except requests.RequestException as e:
            print(f"Errore durante la ricerca delle pagine evento: {e}")
            return []

    # Funzione per estrarre il flusso video e i dettagli dell'evento dalla pagina evento
    def get_event_details(event_url):
        try:
            response = requests.get(event_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            stream_url = None
            element = None
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src')
                if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts|html|php)', src, re.IGNORECASE)):
                    stream_url = src
                    element = iframe
                    break

            if not stream_url:
                for embed in soup.find_all('embed'):
                    src = embed.get('src')
                    if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts|html|php)', src, re.IGNORECASE)):
                        stream_url = src
                        element = embed
                        break

            if not stream_url:
                for video in soup.find_all('video'):
                    src = video.get('src')
                    if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts)', src, re.IGNORECASE)):
                        stream_url = src
                        element = video
                        break
                    for source in video.find_all('source'):
                        src = source.get('src')
                        if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts)', src, re.IGNORECASE)):
                            stream_url = src
                            element = source
                            break

            # Estrai data e ora formattate
            full_event_datetime_str = ""
            event_date_comparable = "" # Conterrà "DD/MM" per il confronto
            event_time_str = ""        # Conterrà "HH:MM"
            date_span = soup.find('span', class_='uk-text-meta uk-text-small')
            if date_span:
                date_text = date_span.get_text(strip=True)
                full_event_datetime_str, event_date_comparable = format_event_date(date_text)
                if full_event_datetime_str:
                    # Estrai solo l'orario (es. "20:45" da "20:45 23/07")
                    time_match = re.match(r'(\d{1,2}:\d{2})', full_event_datetime_str)
                    if time_match:
                        event_time_str = time_match.group(1)
     
            # Estrai il titolo dell'evento dal tag <title>
            event_title_from_html = "Unknown Event"
            title_tag = soup.find('title')
            if title_tag:
                event_title_from_html = title_tag.get_text(strip=True)
                event_title_from_html = re.sub(r'\s*\|\s*Sport Streaming\s*$', '', event_title_from_html, flags=re.IGNORECASE).strip()

            # Estrai informazioni sulla lega/competizione
            league_info = "Event" # Default
            is_perma_channel = "perma" in event_url.lower()

            if is_perma_channel:
                if event_title_from_html and event_title_from_html != "Unknown Event":
                    league_info = event_title_from_html
                # Se il titolo del canale perma non è stato trovato, league_info resta "Event"
            else:
                # Per canali non-perma (eventi specifici), cerca lo span della lega/competizione
                league_spans = soup.find_all(
                    lambda tag: tag.name == 'span' and \
                                'uk-text-small' in tag.get('class', []) and \
                                'uk-text-meta' not in tag.get('class', []) # Escludi lo span della data
                )
                if league_spans:
                    # Prendi il testo del primo span corrispondente, pulito
                    league_info = ' '.join(league_spans[0].get_text(strip=True).split())
                # Se lo span non viene trovato per un evento non-perma, league_info resta "Event"

            return stream_url, event_date_comparable, event_time_str, event_title_from_html, league_info

        except requests.RequestException as e:
            print(f"Errore durante l'accesso a {event_url}: {e}")
            return None, "", "", "Unknown Event", "Event"

    # Funzione per aggiornare il file M3U8
    def update_m3u_file(video_streams, m3u_file="eventisps.m3u8"):
        REPO_PATH = os.getenv('GITHUB_WORKSPACE', '.')
        file_path = os.path.join(REPO_PATH, m3u_file)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            perma_count = 1

            for event_url, stream_url, event_time, event_title, league_info in video_streams:
                if not stream_url:
                    continue

                # Determina se è un canale permanente o standard
                is_perma = "perma" in event_url.lower()
                if is_perma:
                    image_url = f"https://sportstreaming.net/assets/img/live/perma/live{perma_count}.png"
                    perma_count += 1
                else:
                    # Estrai il numero dall'URL per i canali standard (es. live-3 -> 3)
                    match = re.search(r'live-(\d+)', event_url)
                    if match:
                        live_number = match.group(1)
                        image_url = f"https://sportstreaming.net/assets/img/live/standard/live{live_number}.png"
                    else:
                        image_url = "https://sportstreaming.net/assets/img/live/standard/live1.png"  # Fallback

                tvg_name_prefix = f"{event_time} " if event_time else ""
                tvg_name_final = f"{event_title} | {league_info} | {tvg_name_prefix}".strip()
                if not tvg_name_final: # Fallback se il titolo è vuoto
                    tvg_name_final = "Eventi Live"

                # Codifica gli header per l'URL
                encoded_ua = quote_plus(headers["User-Agent"])
                encoded_referer = quote_plus(headers["Referer"])
                encoded_origin = quote_plus(headers["Origin"])

                # Costruisci l'URL finale con il proxy e gli header
                # stream_url qui è l'URL originale dello stream (es. https://xuione.sportstreaming.net/...)
                final_stream_url = f"{PROXY}{stream_url}&h_user-agent={encoded_ua}&h_referer={encoded_referer}&h_origin={encoded_origin}"

                group_title_text = "Sport" if is_perma else "Eventi Live"

                # Aggiungi il canale iniziale/informativo solo se ci sono eventi da scrivere
                if f.tell() == len("#EXTM3U\n"): # Controlla se è stata scritta solo l'intestazione iniziale
                    f.write(f'#EXTINF:-1 tvg-name="SPORTSTREAMING" group-title="Eventi Live",SPORTSTREAMING\n')
                    f.write("https://example.com.m3u8\n\n")

                f.write(f"#EXTINF:-1 tvg-name=\"{tvg_name_final} (SPS)\"group-title=\"{group_title_text}\" tvg-logo=\"{image_url}\",{tvg_name_final} (SPS)\n")
                f.write(f"{final_stream_url}\n")
                f.write("\n") # Aggiungi una riga vuota dopo ogni canale


        print(f"File M3U8 aggiornato con successo: {file_path}")

    # Esegui lo script
    if __name__ == "__main__":
        current_date_dd_mm = datetime.now().strftime("%d/%m")
        print(f"Recupero eventi per il giorno: {current_date_dd_mm}")

        event_pages = find_event_pages()
        if not event_pages:
            print("Nessuna pagina evento trovata.")
        else:
            video_streams = []
            for event_url in event_pages:
                # print(f"Analizzo: {event_url}") # Rimosso per output più pulito, riattivare se necessario
                stream_url, event_date_str, event_time, event_title, league_info = get_event_details(event_url)
                
                if stream_url:
                    is_perma = "perma" in event_url.lower()
                    # Modifica: Includi solo se NON è perma E la data corrisponde
                    if not is_perma and (event_date_str == current_date_dd_mm):
                        print(f"Includo: {event_title} (URL: {event_url}, Data evento: {event_date_str})")
                        video_streams.append((event_url, stream_url, event_time, event_title, league_info))
                    elif is_perma:
                        print(f"Scarto canale perma: {event_title} (URL: {event_url})")
                    # else: # Evento non perma ma di un altro giorno
                        # print(f"Scarto evento (data non corrispondente): {event_title} (Data evento: {event_date_str}, Richiesta: {current_date_dd_mm})")
                else:
                    print(f"Nessun flusso trovato per {event_url}")

            update_m3u_file(video_streams)

            # Add a note if no actual video streams were processed and added to the file.
            if not video_streams:
                if not event_pages:
                    # "Nessuna pagina evento trovata." was already printed.
                    # update_m3u_file confirms file creation.
                    pass # Avoid redundant messages.
                else: # event_pages were found, but no streams matched criteria
                    print("Nota: Nessun flusso video specifico per gli eventi odierni è stato aggiunto a eventisps.m3u8 (potrebbe contenere solo l'intestazione).")
    
# Funzione per il quarto script (schedule_extractor.py)
def schedule_extractor():
    # Codice del quarto script qui
    # Aggiungi il codice del tuo script "schedule_extractor.py" in questa funzione.
    print("Eseguendo lo schedule_extractor.py...")
    # Il codice che avevi nello script "schedule_extractor.py" va qui, senza modifiche.
    from playwright.sync_api import sync_playwright
    import os
    import json
    from datetime import datetime
    import re
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()
    
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    
    def html_to_json(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}
        
        date_rows = soup.find_all('tr', class_='date-row')
        if not date_rows:
            print("AVVISO: Nessuna riga di data trovata nel contenuto HTML!")
            return {}
    
        current_date = None
        current_category = None
    
        for row in soup.find_all('tr'):
            if 'date-row' in row.get('class', []):
                current_date = row.find('strong').text.strip()
                result[current_date] = {}
                current_category = None
    
            elif 'category-row' in row.get('class', []) and current_date:
                current_category = row.find('strong').text.strip() + "</span>"
                result[current_date][current_category] = []
    
            elif 'event-row' in row.get('class', []) and current_date and current_category:
                time_div = row.find('div', class_='event-time')
                info_div = row.find('div', class_='event-info')
    
                if not time_div or not info_div:
                    continue
    
                time_strong = time_div.find('strong')
                event_time = time_strong.text.strip() if time_strong else ""
                event_info = info_div.text.strip()
    
                event_data = {
                    "time": event_time,
                    "event": event_info,
                    "channels": []
                }
    
                # Cerca la riga dei canali successiva
                next_row = row.find_next_sibling('tr')
                if next_row and 'channel-row' in next_row.get('class', []):
                    channel_links = next_row.find_all('a', class_='channel-button-small')
                    for link in channel_links:
                        href = link.get('href', '')
                        channel_id_match = re.search(r'stream-(\d+)\.php', href)
                        if channel_id_match:
                            channel_id = channel_id_match.group(1)
                            channel_name = link.text.strip()
                            channel_name = re.sub(r'\s*\(CH-\d+\)$', '', channel_name)
    
                            event_data["channels"].append({
                                "channel_name": channel_name,
                                "channel_id": channel_id
                            })
    
                result[current_date][current_category].append(event_data)
    
        return result
    
    def modify_json_file(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        current_month = datetime.now().strftime("%B")
    
        for date in list(data.keys()):
            match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\d{4})", date)
            if match:
                day_part = match.group(1)
                suffix = match.group(2)
                year_part = match.group(3)
                new_date = f"{day_part}{suffix} {current_month} {year_part}"
                data[new_date] = data.pop(date)
    
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"File JSON modificato e salvato in {json_file_path}")
    
    def extract_schedule_container():
        url = f"{LINK_DADDY}/"
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_output = os.path.join(script_dir, "daddyliveSchedule.json")
    
        print(f"Accesso alla pagina {url} per estrarre il main-schedule-container...")
    
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
    
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Tentativo {attempt} di {max_attempts}...")
                    page.goto(url)
                    print("Attesa per il caricamento completo...")
                    page.wait_for_timeout(10000)  # 10 secondi
    
                    schedule_content = page.evaluate("""() => {
                        const container = document.getElementById('main-schedule-container');
                        return container ? container.outerHTML : '';
                    }""")
    
                    if not schedule_content:
                        print("AVVISO: main-schedule-container non trovato o vuoto!")
                        if attempt == max_attempts:
                            browser.close()
                            return False
                        else:
                            continue
    
                    print("Conversione HTML in formato JSON...")
                    json_data = html_to_json(schedule_content)
    
                    with open(json_output, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4)
    
                    print(f"Dati JSON salvati in {json_output}")
    
                    modify_json_file(json_output)
                    browser.close()
                    return True
    
                except Exception as e:
                    print(f"ERRORE nel tentativo {attempt}: {str(e)}")
                    if attempt == max_attempts:
                        print("Tutti i tentativi falliti!")
                        browser.close()
                        return False
                    else:
                        print(f"Riprovando... (tentativo {attempt + 1} di {max_attempts})")
    
            browser.close()
            return False
    
    if __name__ == "__main__":
        success = extract_schedule_container()
        if not success:
            exit(1)

def epg_eventi_generator_world():
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator_world.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it', 'uk', 'tnt', 'usa', 'tennis channel', 'tennis stream', 'la']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events: # Original loop for events
                    # Filtra gli eventi in base all'orario specificato (00:00 - 04:00)
                    event_time_str = event_info.get("time", "00:00") # Prende l'orario dell'evento, default a "00:00" se mancante
                    try:
                        event_actual_time = datetime.strptime(event_time_str, "%H:%M").time()
                        
                        # Definisci gli orari limite per il filtro
                        filter_start_time = datetime.strptime("00:00", "%H:%M").time()
                        filter_end_time = datetime.strptime("04:00", "%H:%M").time()

                        # Escludi eventi se l'orario Ã¨ compreso tra 00:00 e 04:00 inclusi
                        if filter_start_time <= event_actual_time <= filter_end_time:
                            continue # Salta questo evento e passa al successivo
                    except ValueError:
                        print(f"[!] Orario evento non valido '{event_time_str}' per l'evento '{event_info.get('event', 'Sconosciuto')}' durante il caricamento JSON. Evento saltato.")
                        continue

                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name_original = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_name = event_name_original.replace('&', 'and')
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)
    
                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False
    
    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso
        
        # Percorso del file XML di output
        output_xml_path = "eventi.xml"
        
        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)

# Funzione per il quinto script (epg_eventi_generator.py)
def epg_eventi_generator():
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events:
                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)
    
                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False
    
    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso
        
        # Percorso del file XML di output
        output_xml_path = "eventi.xml"
        
        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)
        
# Funzione per il sesto script (italy_channels.py)
def italy_channels():
    print("Eseguendo il italy_channels.py...")

    import requests
    import re
    import os
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv
    import urllib.parse # Aggiunto per urlencode e quote
    import json         # Aggiunto per json.JSONDecodeError
    from bs4 import BeautifulSoup # Aggiunto per il parsing HTML

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_SZ = os.getenv("LINK_SPORTZONE", "https://sportzone.yoga").strip()
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()
    EPG_FILE = "epg.xml"
    LOGOS_FILE = "logos.txt"
    OUTPUT_FILE = "channels_italy.m3u8"
    DEFAULT_TVG_ICON = ""
    HTTP_TIMEOUT = 20  # Timeout per le richieste HTTP in secondi

    # Crea una sessione requests per riutilizzare connessioni e gestire cookies
    session = requests.Session()

    # Base URLs for the new stream checking mechanism for Daddylive channels
    NEW_KSO_BASE_URLS_FOR_ITALY_CHANNELS = [
        "https://new.newkso.ru/wind/",
        "https://new.newkso.ru/ddy6/",
        "https://new.newkso.ru/zeko/",
        "https://new.newkso.ru/nfs/",
        "https://new.newkso.ru/dokko1/",
    ]

    BASE_URLS = [
        "https://vavoo.to"
    ]

    CATEGORY_KEYWORDS = {
        "Rai": ["rai"],
        "Mediaset": ["twenty seven", "twentyseven", "mediaset", "italia 1", "italia 2", "canale 5"],
        "Sport": ["inter", "milan", "lazio", "calcio", "tennis", "sport", "super tennis", "supertennis", "dazn", "eurosport", "sky sport", "rai sport"],
        "Film & Serie TV": ["crime", "primafila", "cinema", "movie", "film", "serie", "hbo", "fox", "rakuten", "atlantic"],
        "News": ["news", "tg", "rai news", "sky tg", "tgcom"],
        "Bambini": ["frisbee", "super!", "fresbee", "k2", "cartoon", "boing", "nick", "disney", "baby", "rai yoyo"],
        "Documentari": ["documentaries", "discovery", "geo", "history", "nat geo", "nature", "arte", "documentary"],
        "Musica": ["deejay", "rds", "hits", "rtl", "mtv", "vh1", "radio", "music", "kiss", "kisskiss", "m2o", "fm"],
        "Altro": ["focus", "real time"]
    }

    def fetch_epg(epg_file):
        try:
            tree = ET.parse(epg_file)
            return tree.getroot()
        except Exception as e:
            print(f"Errore durante la lettura del file EPG: {e}")
            return None

    def fetch_logos(logos_file):
        logos_dict = {}
        try:
            with open(logos_file, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r'\s*"(.+?)":\s*"(.+?)",?', line)
                    if match:
                        channel_name, logo_url = match.groups()
                        logos_dict[channel_name.lower()] = logo_url
        except Exception as e:
            print(f"Errore durante la lettura del file dei loghi: {e}")
        return logos_dict

    def normalize_channel_name(name):
        name = re.sub(r"\s+", "", name.strip().lower())
        name = re.sub(r"\.it\b", "", name)
        name = re.sub(r"hd|fullhd", "", name)
        return name

    def create_channel_id_map(epg_root):
        channel_id_map = {}
        for channel in epg_root.findall('channel'):
            tvg_id = channel.get('id')
            display_name = channel.find('display-name').text
            if tvg_id and display_name:
                normalized_name = normalize_channel_name(display_name)
                channel_id_map[normalized_name] = tvg_id
        return channel_id_map

    def fetch_channels(base_url):
        try:
            response = session.get(f"{base_url}/channels", timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []

    def clean_channel_name(name):
        name = re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name)
        name = re.sub(r"\s*\(.*?\)", "", name)
        if "zona dazn" in name.lower() or "dazn 1" in name.lower():
            return "DAZN2"
        if "mediaset 20" in name.lower():
            return "20 MEDIASET"
        if "mediaset italia 2" in name.lower():
            return "ITALIA 2"
        if "mediaset 1" in name.lower():
            return "ITALIA 1"
        return name.strip()

    def filter_italian_channels(channels, base_url):
        seen = {}
        results = []
        for ch in channels:
            if ch.get("country") == "Italy":
                clean_name = clean_channel_name(ch["name"])
                if clean_name.lower() in ["dazn", "dazn 2"]:
                    continue
                count = seen.get(clean_name, 0) + 1
                seen[clean_name] = count
                if count > 1:
                    clean_name = f"{clean_name} ({count})"
                results.append((clean_name, f"{base_url}/play/{ch['id']}/index.m3u8"))
        return results

    def classify_channel(name):
        for category, words in CATEGORY_KEYWORDS.items():
            if any(word in name.lower() for word in words):
                return category
        return "Altro"

    def get_manual_channels():
        encoded_link_sz = urllib.parse.quote(LINK_SZ, safe=':/') # Encode LINK_SZ
        return [
            {"name": "SKY SPORT 251 (SS)", "url": f"https://hls.kangal.icu/hls/sky251/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..251.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 252 (SS)", "url": f"https://hls.kangal.icu/hls/sky252/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..252.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 253 (SS)", "url": f"https://hls.kangal.icu/hls/sky253/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..253.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 254 (SS)", "url": f"https://hls.kangal.icu/hls/sky254/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..254.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 255 (SS)", "url": f"https://hls.kangal.icu/hls/sky255/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..255.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 256 (SS)", "url": f"https://hls.kangal.icu/hls/sky256/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..256.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 257 (SS)", "url": f"https://hls.kangal.icu/hls/sky257/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..257.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 258 (SS)", "url": f"https://hls.kangal.icu/hls/sky258/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..258.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 259 (SS)", "url": f"https://hls.kangal.icu/hls/sky259/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..259.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 260 (SS)", "url": f"https://hls.kangal.icu/hls/sky260/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..260.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 261 (SS)", "url": f"https://hls.kangal.icu/hls/sky261/index.m3u8&h_user-agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_referer={encoded_link_sz}%2F&h_origin={encoded_link_sz}", "tvg_id": "sky.sport..261.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
        ]

    # --- Funzioni per risolvere gli stream Daddylive ---
    def get_stream_from_channel_id(channel_id_str): # channel_id_str is the numeric ID like "121"
        raw_m3u8_url_found = None
        # Use the NEW_KSO_BASE_URLS_FOR_ITALY_CHANNELS defined in this function's scope
        for base_url in NEW_KSO_BASE_URLS_FOR_ITALY_CHANNELS:
            stream_path = f"premium{channel_id_str}/mono.m3u8"
            candidate_url = f"{base_url.rstrip('/')}/{stream_path.lstrip('/')}"
            
            try:
                # Using GET with stream=True and a timeout.
                # HTTP_TIMEOUT is a global in this function's scope (italy_channels)
                response = session.get(candidate_url, stream=True, timeout=HTTP_TIMEOUT / 2) 
                if response.status_code == 200:
                    print(f"[✓] Stream Daddylive (italy_channels) trovato per ID {channel_id_str} a: {candidate_url}")
                    raw_m3u8_url_found = candidate_url
                    response.close() # Close the stream connection
                    break 
                else:
                    # Optional: log if status is not 200 but not an exception
                    # print(f"[INFO] ID Canale {channel_id_str} non trovato a {candidate_url} (Status: {response.status_code})")
                    pass
                response.close() # Ensure connection is closed
            except requests.exceptions.Timeout:
                # print(f"[!] Timeout controllo stream per ID canale {channel_id_str} a {candidate_url}")
                pass 
            except requests.exceptions.ConnectionError:
                # print(f"[!] Errore connessione controllo stream per ID canale {channel_id_str} a {candidate_url}")
                pass
            except requests.exceptions.RequestException: 
                # print(f"[!] Errore controllo stream per ID canale {channel_id_str} a {candidate_url}: {e}")
                pass 
        
        if raw_m3u8_url_found:
            # PROXY is a global in this function's scope (italy_channels)
            # Non applichiamo il proxy qui, verrà fatto in save_m3u8 se PROXY è definito
            return raw_m3u8_url_found
        else:
            # print(f"[✗] Nessuno stream trovato per ID canale {channel_id_str} dopo aver controllato tutte le URL base.")
            return None
    # --- Fine funzioni Daddylive ---

    def fetch_channels_from_daddylive_page(page_url, base_daddy_url):
        print(f"Tentativo di fetch dei canali da: {page_url}")
        channels = []
        seen_daddy_channel_ids = set() # Set per tracciare i channel_id già visti da Daddylive
        try:
            response = session.get(page_url, timeout=HTTP_TIMEOUT, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # --- INIZIO LOGICA DI PARSING E FILTRAGGIO SPECIFICA PER DADDYLIVE 24-7 CHANNELS ---

            # Marcatori che suggeriscono un canale NON italiano (per evitare falsi positivi)
            non_italian_markers = [
                " (de)", " (fr)", " (es)", " (uk)", " (us)", " (pt)", " (gr)", " (nl)", " (tr)", " (ru)",
                " deutsch", " france", " español", " arabic", " greek", " turkish", " russian", " albania",
                " portugal" # Aggiunto basandomi sull'esempio fornito
            ]

            grid_items = soup.find_all('div', class_='grid-item')
            print(f"Trovati {len(grid_items)} elementi 'grid-item' nella pagina Daddylive.")

            for item in grid_items:
                link_tag = item.find('a', href=re.compile(r'/stream/stream-\d+\.php'))
                if not link_tag:
                    continue

                strong_tag = link_tag.find('strong')
                if not strong_tag:
                    continue

                channel_name_raw = strong_tag.text.strip()
                href = link_tag.get('href')
                
                # Estrai l'ID del canale dall'href, es. /stream/stream-717.php -> 717
                channel_id_match = re.search(r'/stream/stream-(\d+)\.php', href)

                if channel_id_match and channel_name_raw:
                    channel_id = channel_id_match.group(1)
                    lower_channel_name = channel_name_raw.lower()

                    if channel_id in seen_daddy_channel_ids:
                        print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché l'ID è già stato processato.")
                        continue # Passa al prossimo item

                    # Filtro primario: deve contenere "italy"
                    if "italy" in lower_channel_name:
                        is_confirmed_non_italian_by_marker = False
                        for marker in non_italian_markers:
                            if marker in lower_channel_name:
                                is_confirmed_non_italian_by_marker = True
                                print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché, pur contenendo 'italy', ha anche un marcatore non italiano: '{marker}'")
                                break
                        
                        if not is_confirmed_non_italian_by_marker:
                            seen_daddy_channel_ids.add(channel_id) # Aggiungi l'ID al set prima di tentare la risoluzione
                            print(f"Trovato canale potenzialmente ITALIANO (Daddylive HTML): {channel_name_raw}, ID: {channel_id}. Tentativo di risoluzione stream...")
                            stream_url = get_stream_from_channel_id(channel_id)
                            if stream_url:
                                channels.append((channel_name_raw, stream_url))
                                print(f"Risolto e aggiunto stream per {channel_name_raw}: {stream_url}")
                            else:
                                print(f"Impossibile risolvere lo stream per {channel_name_raw} (ID: {channel_id})")
                    # else:
                        # Questo blocco è commentato per non intasare i log con canali non italiani
                        # Non stampiamo nulla per i canali che non contengono "italy" per non intasare il log
                        # print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché non contiene 'italy' nel nome.")
            # --- FINE LOGICA DI PARSING E FILTRAGGIO ---

            if not channels:
                print(f"Nessun canale estratto/risolto da {page_url}. Controlla la logica di parsing o la struttura della pagina.")

        except requests.RequestException as e:
            print(f"Errore durante il download da {page_url}: {e}")
        except Exception as e:
            print(f"Errore imprevisto durante il parsing di {page_url}: {e}")
        return channels

    def save_m3u8(organized_channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')

            vavoo_headers_str = "&h_User-Agent=VAVOO2%2F6&h_Referer=https%3A%2F%2Fvavoo.to%2F&h_Origin=https%3A%2F%2Fvavoo.to"
            daddy_headers_str = "&h_User-Agent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F133.0.0.0%20Safari%2F537.36&h_Referer=https%3A%2F%2Falldownplay.xyz%2F&h_Origin=https%3A%2F%2Falldownplay.xyz"

            for category, channels_list in organized_channels.items():
                channels_list.sort(key=lambda x: x["name"].lower())
                for ch in channels_list:
                    tvg_name_cleaned = re.sub(r"\s*\(.*?\)", "", ch["name"])
                    
                    base_stream_url = ch['url']
                    channel_display_name = ch['name']
                    url_with_specific_headers = base_stream_url

                    if channel_display_name.upper().endswith(" (D)"):
                        url_with_specific_headers += daddy_headers_str
                    elif not channel_display_name.upper().endswith(" (SS)"): # Assumed Vavoo
                        url_with_specific_headers += vavoo_headers_str
                    # Manual (SS) channels already have headers in base_stream_url

                    final_url = url_with_specific_headers
                    if PROXY:
                        final_url = f"{PROXY.rstrip('/')}{url_with_specific_headers}"
                    
                    f.write(f'#EXTINF:-1 tvg-id="{ch.get("tvg_id", "")}" tvg-name="{tvg_name_cleaned}" tvg-logo="{ch.get("logo", DEFAULT_TVG_ICON)}" group-title="{category}",{ch["name"]}\n')
                    f.write(f"{final_url}\n\n")

    def main():
        epg_root = fetch_epg(EPG_FILE)
        if epg_root is None:
            print("Impossibile recuperare il file EPG, procedura interrotta.")
            return
        logos_dict = fetch_logos(LOGOS_FILE)
        channel_id_map = create_channel_id_map(epg_root)
        
        all_fetched_channels = [] # Conterrà tuple (nome_canale, url_stream)

        # 1. Canali da sorgenti JSON (Vavoo)
        print("\n--- Fetching canali da sorgenti Vavoo (JSON) ---")
        for base_vavoo_url in BASE_URLS:
            json_channels_data = fetch_channels(base_vavoo_url)
            all_fetched_channels.extend(filter_italian_channels(json_channels_data, base_vavoo_url))

        # 2. Canali dalla pagina HTML di Daddylive
        print("\n--- Fetching canali da Daddylive (HTML) ---")
        daddylive_247_page_url = f"{LINK_DADDY.rstrip('/')}/24-7-channels.php"
        scraped_daddylive_channels = fetch_channels_from_daddylive_page(daddylive_247_page_url, LINK_DADDY)

        processed_scraped_channels = []
        seen_scraped_names = {}
        # Rinominato seen_scraped_names a seen_daddy_transformed_base_names per chiarezza
        seen_daddy_transformed_base_names = {}
        for raw_name, stream_url in scraped_daddylive_channels:
            # 1. Pulizia iniziale generica del nome grezzo
            name_after_initial_clean = clean_channel_name(raw_name)

            # 2. Trasformazioni specifiche per Daddylive:
            #    - Rimuovi "italy" (case insensitive)
            #    - Converti in maiuscolo
            # Questo sarà il nome base per la gestione dei duplicati Daddylive
            base_daddy_name = re.sub(r'italy', '', name_after_initial_clean, flags=re.IGNORECASE).strip()
            base_daddy_name = re.sub(r'\s+', ' ', base_daddy_name).strip() # Rimuovi spazi doppi
            base_daddy_name = base_daddy_name.upper()
            
            # Rinominare i canali Sky Calcio e Sky Calcio 7 specifici di Daddylive
            # Questo avviene DOPO la pulizia iniziale e l'uppercase,
            # e PRIMA della gestione dei duplicati e dell'aggiunta di "(D)"
            sky_calcio_rename_map = {
                "SKY CALCIO 1": "SKY SPORT 251",
                "SKY CALCIO 2": "SKY SPORT 252",
                "SKY CALCIO 3": "SKY SPORT 253",
                "SKY CALCIO 4": "SKY SPORT 254",
                "SKY CALCIO 5": "SKY SPORT 255",
                "SKY CALCIO 6": "SKY SPORT 256",
                "SKY CALCIO 7": "DAZN 1"
            }

            if base_daddy_name in sky_calcio_rename_map:
                original_bdn_for_log = base_daddy_name
                base_daddy_name = sky_calcio_rename_map[base_daddy_name]
                print(f"Rinominato canale Daddylive (HTML) da '{original_bdn_for_log}' a '{base_daddy_name}'")


            # Gestione skip DAZN (usa il nome base trasformato per il check)
            # clean_channel_name potrebbe già aver trasformato "dazn 1" in "DAZN2"
            if base_daddy_name == "DAZN" or base_daddy_name == "DAZN2":
                print(f"Skipping canale Daddylive (HTML) a causa della regola DAZN: {raw_name} (base trasformato: {base_daddy_name})")
                continue
            
            # 3. Gestione duplicati basata sul nome base trasformato di Daddylive
            count = seen_daddy_transformed_base_names.get(base_daddy_name, 0) + 1
            seen_daddy_transformed_base_names[base_daddy_name] = count
            
            # 4. Costruzione del nome finale per Daddylive
            final_name = base_daddy_name
            if count > 1:
                final_name = f"{base_daddy_name} ({count})" # Es. NOME CANALE (2)
            final_name = f"{final_name} (D)" # Es. NOME CANALE (D) o NOME CANALE (2) (D)
            
            processed_scraped_channels.append((final_name, stream_url))

        all_fetched_channels.extend(processed_scraped_channels)

        # 3. Canali manuali
        manual_channels_data = get_manual_channels()

        # Organizzazione di tutti i canali raccolti
        print("\n--- Organizzazione canali ---")
        organized_channels = {category: [] for category in CATEGORY_KEYWORDS.keys()}

        # Processa canali da Vavoo e Daddylive HTML (formato: (nome, url))
        for name, url in all_fetched_channels:
            # 'name' è il nome finale che verrà visualizzato, 
            # es. "CANALE SPORT (D) (2)" o "CANALE NEWS (3)" (da Vavoo)
            category = classify_channel(name)

            # Crea un nome base per il lookup di EPG e Logo:
            name_for_lookup = name
            # Rimuovi il suffisso (D) specifico di Daddylive, se presente
            if name_for_lookup.upper().endswith(" (D)"): # Controllo case-insensitive per robustezza
                # Rimuove l'ultima occorrenza di " (D)" (case insensitive)
                match_d_suffix = re.search(r'\s*\([Dd]\)$', name_for_lookup)
                if match_d_suffix:
                    name_for_lookup = name_for_lookup[:match_d_suffix.start()]
            
            # Rimuovi suffissi numerici per duplicati, es. (2), (3)...
            name_for_lookup = re.sub(r'\s*\(\d+\)$', '', name_for_lookup).strip()
            # A questo punto, name_for_lookup dovrebbe essere il nome del canale "pulito" 
            # es. "CANALE SPORT" o "CANALE NEWS" (già in maiuscolo se da Daddylive)

            # Logica per assegnazione logo
            final_logo_url = DEFAULT_TVG_ICON # Inizializza con il logo di default
            sky_sport_daddy_logo = "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png"

            # Controlla se il canale è uno dei canali Daddylive SKY SPORT 251-256
            # name_for_lookup è il nome base pulito (es. "SKY SPORT 251")
            # name è il nome completo con suffisso (es. "SKY SPORT 251 (D)")
            if name.upper().endswith(" (D)"): # Verifica se è un canale Daddylive
                if re.match(r"SKY SPORT (25[1-6])$", name_for_lookup.upper()):
                    # È un canale Daddylive SKY SPORT 251-256
                    final_logo_url = sky_sport_daddy_logo
                    print(f"Logo specifico '{final_logo_url}' assegnato a Daddylive channel '{name}' (lookup name: '{name_for_lookup}')")
                else:
                    # È un canale Daddylive, ma non uno dei SKY SPORT 251-256 target, usa il lookup normale
                    final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)
            else:
                # Non è un canale Daddylive (es. Vavoo), usa il lookup normale
                final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)

            organized_channels.setdefault(category, []).append({
                "name": name, # Nome completo da visualizzare
                "url": url,
                "tvg_id": channel_id_map.get(normalize_channel_name(name_for_lookup), ""), # Usa il nome pulito per tvg-id
                "logo": final_logo_url # Usa il logo determinato dalla logica sopra
            })

        # Processa canali manuali (formato: dict)
        for ch_data in manual_channels_data:
            cat = ch_data.get("category") or classify_channel(ch_data["name"])
            organized_channels.setdefault(cat, []).append({
                "name": ch_data["name"],
                "url": ch_data["url"],
                "tvg_id": ch_data.get("tvg_id", ""),
                "logo": ch_data.get("logo", DEFAULT_TVG_ICON)
            })

        save_m3u8(organized_channels)
        print(f"\nFile {OUTPUT_FILE} creato con successo!")

    if __name__ == "__main__":
        main()

# Funzione per il settimo script (world_channels_generator.py)
def world_channels_generator():
    # Codice del settimo script qui
    # Aggiungi il codice del tuo script "world_channels_generator.py" in questa funzione.
    print("Eseguendo il world_channels_generator.py...")
    # Il codice che avevi nello script "world_channels_generator.py" va qui, senza modifiche.
    import requests
    import re
    import os
    from collections import defaultdict
    from dotenv import load_dotenv
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()
    OUTPUT_FILE = "world.m3u8"
    BASE_URLS = [
        "https://vavoo.to"
    ]
    
    # Scarica la lista dei canali
    def fetch_channels(base_url):
        try:
            response = requests.get(f"{base_url}/channels", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []
    
    # Pulisce il nome del canale
    def clean_channel_name(name):
        return re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name).strip()
    
    # Salva il file M3U8 con i canali ordinati alfabeticamente per categoria
    def save_m3u8(channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    
        # Raggruppa i canali per nazione (group-title)
        grouped_channels = defaultdict(list)
        for name, url, country in channels:
            grouped_channels[country].append((name, url))
    
        # Ordina le categorie alfabeticamente e i canali dentro ogni categoria
        sorted_categories = sorted(grouped_channels.keys())
    
        vavoo_headers_str = "&h_User-Agent=VAVOO2%2F6&h_Referer=https%3A%2F%2Fvavoo.to%2F&h_Origin=https%3A%2F%2Fvavoo.to"
            
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')
    
            for country in sorted_categories:
                # Ordina i canali in ordine alfabetico dentro la categoria
                grouped_channels[country].sort(key=lambda x: x[0].lower())
    
                for name, base_vavoo_url in grouped_channels[country]:
                    url_with_specific_headers = base_vavoo_url + vavoo_headers_str
                    
                    final_url_to_write = url_with_specific_headers
                    if PROXY: 
                        final_url_to_write = f"{PROXY.rstrip('/')}{url_with_specific_headers}"

                    f.write(f'#EXTINF:-1 tvg-name="{name}" group-title="{country}", {name}\n')
                    f.write(f"{final_url_to_write}\n\n")
    
    # Funzione principale
    def main():
        all_channels = []
        for url in BASE_URLS:
            channels = fetch_channels(url)
            for ch in channels:
                clean_name = clean_channel_name(ch["name"])
                country = ch.get("country", "Unknown")  # Estrai la nazione del canale, default Ã¨ "Unknown"
                all_channels.append((clean_name, f"{url}/play/{ch['id']}/index.m3u8", country))
    
        save_m3u8(all_channels)
        print(f"File {OUTPUT_FILE} creato con successo!")
    
    if __name__ == "__main__":
        main()

def removerworld():
    import os
    
    # Lista dei file da eliminare
    files_to_delete = ["eventisz.m3u8", "eventisps.m3u8", "world.m3u8", "channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")
            
def remover():
    import os
    
    # Lista dei file da eliminare
    files_to_delete = ["eventisz.m3u8", "eventisps.m3u8", "channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

# Funzione principale che esegue tutti gli script
def main():
    try:
        schedule_success = schedule_extractor()
    except Exception as e:
        print(f"Errore durante l'esecuzione di schedule_extractor: {e}")
        
    try:
        eventi_sps()
    except Exception as e:
        print(f"Errore durante l'esecuzione di eventi_sps: {e}")
        return

    try:
        eventi_sz()
    except Exception as e:
        print(f"Errore durante l'esecuzione di eventi_sps: {e}")
        return

    eventi_en = os.getenv("EVENTI_EN", "no").strip().lower()
    world_flag = os.getenv("WORLD", "si").strip().lower()

    # EPG Eventi
    try:
        if eventi_en == "si":
            epg_eventi_generator_world()
        else:
            epg_eventi_generator()
    except Exception as e:
        print(f"Errore durante la generazione EPG eventi: {e}")
        return

    # Eventi M3U8
    try:
        if eventi_en == "si":
            eventi_m3u8_generator_world()
        else:
            eventi_m3u8_generator()
    except Exception as e:
        print(f"Errore durante la generazione eventi.m3u8: {e}")
        return

    # EPG Merger
    try:
        epg_merger()
    except Exception as e:
        print(f"Errore durante l'esecuzione di epg_merger: {e}")
        return

    # Canali Italia
    try:
        italy_channels()
    except Exception as e:
        print(f"Errore durante l'esecuzione di italy_channels: {e}")
        return

    # Canali World e Merge finale
    try:
        if world_flag == "si":
            world_channels_generator()
            merger_playlistworld()
            removerworld()
        elif world_flag == "no":
            merger_playlist()
            remover()
        else:
            print(f"Valore WORLD non valido: '{world_flag}'. Usa 'si' o 'no'.")
            return
    except Exception as e:
        print(f"Errore nella fase finale: {e}")
        return

    print("Tutti gli script sono stati eseguiti correttamente!")

if __name__ == "__main__":
    main()
