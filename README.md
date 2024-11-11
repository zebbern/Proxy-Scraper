# Proxy-Scraper
**Updated HTTP/HTTPS proxies every 5 hours**

## clean_proxies.txt for list with:
```
IP:Port
```

## proxies.txt for list with:
```
http://:IP:Port
https://:IP:Port
```

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

A comprehensive proxy checker tool to validate, test, and categorize HTTP, HTTPS, and SOCKS proxies. This script is designed to handle large proxy lists, identify working proxies, and save results in various formats. It is optimized for high performance and supports custom testing servers, geolocation checks, speed testing, and proxy rotation.

---

## Features

- **Proxy Validation**: Tests proxies for connectivity and returns working proxies.
- **Multi-Endpoint Testing**: Rotates between custom and public endpoints to reduce rate-limiting.
- **Speed Testing**: Measures the latency of each proxy to rank performance.
- **Anonymity Detection**: Identifies proxy anonymity levels (Transparent, Anonymous, or Elite).
- **Geolocation Support**: Optionally determines the country and region of each proxy.
- **Custom Testing Server**: Integrates with your own server for IP detection (e.g., `http://164.90.187.218:5000/ip`).
- **Multiple Output Formats**: Saves results in text, JSON, or CSV formats.
- **Multithreading**: Efficiently handles large proxy lists with multithreading.
- **Failover Support**: Automatically retries proxies using backup endpoints.
- **Easy Integration**: Export working proxies for use in web scraping or automation tasks.

---

## Getting Started

### Prerequisites
- **Python 3.x**
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`
  - `concurrent.futures`
  - `urllib3`

Install dependencies using:
```
pip install -r requirements.txt
```
# Want to test out the proxies yourself? Use this script! "PS": Most testers on the internett are really bad do not trust them.
```
import requests
import sys
import os

def test_proxy(proxy, timeout=5):
    """
    Tests a single proxy by making a request to http://httpbin.org/ip.
    Returns True if the proxy is working, else False.
    """
    try:
        response = requests.get(
            'http://164.90.187.218:5000/ip',
            proxies={'http': proxy, 'https': proxy},
            timeout=timeout,
            verify=False  # Disable SSL verification
        )
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False

def test_single_proxy():
    """
    Allows the user to input a single proxy and tests it.
    """
    proxy = input("Enter the proxy to test (e.g., http://ip:port or https://ip:port): ").strip()
    if not proxy:
        print("No proxy entered. Exiting.")
        return
    print(f"Testing proxy: {proxy}...")
    if test_proxy(proxy):
        print(f"✅ Proxy {proxy} is working.")
    else:
        print(f"❌ Proxy {proxy} is not working.")

def test_proxies_from_file(input_file, output_file='working_proxies.txt'):
    """
    Tests multiple proxies from an input file and saves working proxies to an output file.
    Each proxy should be on a separate line in the input file.
    """
    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist.")
        return

    with open(input_file, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    if not proxies:
        print(f"No proxies found in '{input_file}'.")
        return

    print(f"Testing {len(proxies)} proxies from '{input_file}'...")
    working_proxies = []

    for idx, proxy in enumerate(proxies, 1):
        status = "✅" if test_proxy(proxy) else "❌"
        print(f"[{idx}/{len(proxies)}] {status} {proxy}")
        if status == "✅":
            working_proxies.append(proxy)

    if working_proxies:
        with open(output_file, 'w') as f:
            for proxy in working_proxies:
                f.write(proxy + '\n')
        print(f"\nSaved {len(working_proxies)} working proxies to '{output_file}'.")
    else:
        print("\nNo working proxies found.")

def main():
    """
    Main function to provide a menu for the user to choose between testing a single proxy or multiple proxies from a file.
    """
    print("=== Proxy Tester ===")
    print("1. Test a single proxy")
    print("2. Test multiple proxies from a file")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == '1':
        test_single_proxy()
    elif choice == '2':
        input_file = input("Enter the path to the input file containing proxies: ").strip()
        output_choice = input("Do you want to save working proxies to a file? (y/n): ").strip().lower()
        if output_choice == 'y':
            output_file = input("Enter the name for the output file (default: working_proxies.txt): ").strip()
            output_file = output_file if output_file else 'working_proxies.txt'
        else:
            output_file = None
        if output_file:
            test_proxies_from_file(input_file, output_file)
        else:
            test_proxies_from_file(input_file)
    elif choice == '3':
        print("Exiting.")
        sys.exit(0)
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    # Disable SSL warnings
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    main()

```
