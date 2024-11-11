import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import logging
import random
import urllib3
from tqdm import tqdm  # For progress bars

# -------------------- Configuration -------------------- #

# Suppress only the single warning from urllib3 needed.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Set to ERROR to minimize console output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("proxy_scraper.log"),
        logging.StreamHandler()
    ]
)

# List of proxy sources
PROXY_SOURCES = {
    'free_proxy_list': 'https://free-proxy-list.net/',
    'ssl_proxies': 'https://www.sslproxies.org/',
    'us_proxies': 'https://www.us-proxy.org/',
    'proxyscrape_http': 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'proxyscrape_https': 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all',
    
    # Added new proxy sources
    'aliila_proxy': 'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt',
    'andigwandi_proxy': 'https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt',
    'hendrikbgr_proxy': 'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',
    'aslisk_proxy_https': 'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt',
    'mmpx12_proxy_https': 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt',
    'ercindedeoglu_proxy_https': 'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt',
    'mmpx12_proxy_http': 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
    'sunny9577_proxy_http': 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt',
    'monosans_proxy_http': 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'speedx_proxy_http': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
}

# Headers to mimic a browser visit
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.8',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59', 
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 SamsungBrowser/14.0',

    # Add more user agents as needed
]

HEADERS = {
    'User-Agent': random.choice(USER_AGENTS)
}

# Timeout settings
REQUEST_TIMEOUT = 10  # seconds
TEST_TIMEOUT = 5      # seconds

# Maximum number of concurrent threads
MAX_WORKERS = 50

# -------------------------------------------------------- #

def fetch_proxies_from_api(url):
    """
    Fetches proxies from API endpoints that return plain text lists.
    Returns a list of proxies in 'http://IP:Port' or 'https://IP:Port' format.
    """
    proxies = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, verify=False)
        response.raise_for_status()
        proxy_list = response.text.strip().split('\n')
        for proxy in proxy_list:
            proxy = proxy.strip()
            if proxy:
                if 'https' in url:
                    proxy_str = f"https://{proxy}"
                else:
                    proxy_str = f"http://{proxy}"
                proxies.append(proxy_str)
    except requests.RequestException as e:
        logging.error(f"Error fetching proxies from API {url}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error fetching proxies from API {url}: {e}")
    return proxies

def fetch_proxies_from_static_site(url):
    """
    Fetches proxies from static HTML sites like free-proxy-list.net, sslproxies.org, us-proxy.org.
    Returns a list of proxies in 'http://IP:Port' or 'https://IP:Port' format.
    """
    proxies = []
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all tables and identify the one with proxy headers
        tables = soup.find_all('table')
        target_table = None
        for table in tables:
            headers = [th.text.strip().lower() for th in table.find_all('th')]
            if 'ip address' in headers and 'port' in headers and 'https' in headers:
                target_table = table
                break

        if not target_table:
            return proxies

        # Identify header indices dynamically
        headers = [th.text.strip().lower() for th in target_table.find_all('th')]
        try:
            ip_idx = headers.index('ip address')
            port_idx = headers.index('port')
            https_idx = headers.index('https')
        except ValueError:
            return proxies

        # Extract proxy details from table rows
        for row in target_table.tbody.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) < max(ip_idx, port_idx, https_idx) + 1:
                continue  # Skip incomplete rows
            ip = cols[ip_idx].text.strip()
            port = cols[port_idx].text.strip()
            https = cols[https_idx].text.strip().lower()
            if https == 'yes':
                proxy = f"https://{ip}:{port}"
            else:
                proxy = f"http://{ip}:{port}"
            proxies.append(proxy)

    except requests.RequestException as e:
        logging.error(f"Error fetching proxies from {url}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error fetching proxies from {url}: {e}")
    return proxies

def fetch_proxies():
    """
    Aggregates proxies from all defined sources.
    Yields each proxy source's proxies.
    """
    # Define the order of sources: APIs, static sites, and additional raw text sources
    api_keys = ['proxyscrape_http', 'proxyscrape_https']
    static_keys = ['free_proxy_list', 'ssl_proxies', 'us_proxies']
    additional_api_keys = [
        'aliila_proxy',
        'andigwandi_proxy',
        'hendrikbgr_proxy',
        'aslisk_proxy_https',
        'mmpx12_proxy_https',
        'ercindedeoglu_proxy_https',
        'mmpx12_proxy_http',
        'sunny9577_proxy_http',
        'monosans_proxy_http',
        'speedx_proxy_http'
    ]

    total_sources = len(PROXY_SOURCES)
    current_source = 0

    # Scraping Phase
    for key in api_keys:
        current_source += 1
        proxies = fetch_proxies_from_api(PROXY_SOURCES[key])
        yield proxies
    for key in static_keys:
        current_source += 1
        proxies = fetch_proxies_from_static_site(PROXY_SOURCES[key])
        yield proxies
    for key in additional_api_keys:
        current_source += 1
        proxies = fetch_proxies_from_api(PROXY_SOURCES[key])
        yield proxies

test_urls = [
    "http://164.90.187.218:5000/ip",
    "http://httpbin.org/ip",
    "https://api.ipify.org"
]

def test_proxy(proxy):
    url = random.choice(test_urls)
    try:
        response = requests.get(
            url,
            proxies={"http": proxy, "https": proxy},
            headers=HEADERS,
            timeout=TEST_TIMEOUT,
            verify=False
        )
        if response.status_code == 200:
            print(f"Working proxy: {proxy} via {url}")
            return proxy
    except Exception as e:
        print(f"Failed proxy: {proxy} via {url} - {e}")
    return None



def save_proxies(proxies, filename='proxies.txt'):
    """
    Saves the list of working proxies to a file.
    """
    try:
        with open(filename, 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')
        print(f"\nSaved {len(proxies)} working proxies to '{filename}'")
    except Exception as e:
        logging.error(f"Error saving proxies to {filename}: {e}")

def main():
    """
    Main function to orchestrate proxy scraping and testing.
    Designed for automation without user interaction.
    """
    working_proxies = set()
    all_scraped_proxies = set()
    tested_proxies = set()

    try:
        print("Starting proxy scraping and testing...")

        # Scraping Phase
        print("\nScraping proxies...")
        total_sources = len(PROXY_SOURCES)
        with tqdm(total=total_sources, desc="Processing links", unit="link") as pbar:
            for proxies in fetch_proxies():
                all_scraped_proxies.update(proxies)
                pbar.update(1)
        print("\nScraping complete.")

        # Testing Phase
        print("\nStarting proxy testing...")
        proxies_to_test = list(all_scraped_proxies)
        total_to_test = len(proxies_to_test)

        if total_to_test == 0:
            print("No proxies found to test.")
            return

        with tqdm(total=total_to_test, desc="Testing proxies", unit="proxy") as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxies_to_test}
                for future in concurrent.futures.as_completed(futures):
                    proxy = futures[future]
                    tested_proxies.add(proxy)
                    result = future.result()
                    if result:
                        working_proxies.add(result)
                    pbar.update(1)

        print("\nTesting complete.")
        save_proxies(working_proxies, 'proxies.txt')

    except KeyboardInterrupt:
        print("\nProcess aborted by user.")
        if working_proxies:
            save_proxies(working_proxies, 'proxies.txt')
        else:
            print("No working proxies to save.")
        print("Exiting gracefully.")
        exit()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred. Check 'proxy_scraper.log' for details.")
        exit()

    # Summary
    print(f"\nFinished! {len(working_proxies)} working proxies have been collected and saved to 'proxies.txt'.")

if __name__ == "__main__":
    main()
