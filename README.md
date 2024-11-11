# Proxy-Scraper
**Updated HTTP/HTTPS proxies every 5 hours.**

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


