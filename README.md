# Proxy-Scraper
- **Updated HTTP/HTTPS proxies every 5 hours**
<br><br/>

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
# Want to test out the proxies yourself? Use this script!
- **Most testers on the internett are really bad do not trust them**
- **Here is a nice quick tester**
- **Gives u Valid or Not**
- **Gives an option to save working proxies at the end**
### Create a file called **proxyhere.txt** place it in the same directory then run ur .py that has this code!
```
import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def check_proxy(args):
    index, total, proxy = args
    proxy = proxy.strip()
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}',
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code == 200:
            result = f'{Fore.GREEN}[{index}/{total}] ✅ {proxy}{Style.RESET_ALL}'
            is_valid = True
        else:
            result = f'{Fore.RED}[{index}/{total}] ❌ {proxy}{Style.RESET_ALL}'
            is_valid = False
    except requests.exceptions.RequestException:
        result = f'{Fore.RED}[{index}/{total}] ❌ {proxy}{Style.RESET_ALL}'
        is_valid = False
    sleep(0.5)  # Delay to prevent overloading the service
    return (result, proxy if is_valid else None)

if __name__ == '__main__':
    with open('proxyhere.txt', 'r') as file:
        proxies_list = [line.strip() for line in file if line.strip()]
    total_proxies = len(proxies_list)
    valid_proxies = []

    # Prepare arguments for map
    args_list = [(idx, total_proxies, proxy) for idx, proxy in enumerate(proxies_list, start=1)]

    # Use ThreadPoolExecutor with fewer workers to control request rate
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Use executor.map to process proxies in order
        for result, valid_proxy in executor.map(check_proxy, args_list):
            print(result)
            if valid_proxy:
                valid_proxies.append(valid_proxy)

    # After all proxies have been checked, prompt to save valid ones
    if valid_proxies:
        save_choice = input("Do you want to save the valid proxies to a file? (y/n): ")
        if save_choice.lower() == 'y':
            output_file = input("Enter the filename to save valid proxies (default: valid_proxies.txt): ").strip()
            if not output_file:
                output_file = 'valid_proxies.txt'
            with open(output_file, 'w') as f:
                for proxy in valid_proxies:
                    f.write(f'{proxy}\n')
            print(f"Valid proxies saved to {output_file}")
    else:
        print("No valid proxies found.")

```
# Contribution
We welcome contributions! Please submit pull requests or raise issues for feature requests.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

## Important Considerations
Legal and Ethical Use:
```
Legal and Ethical Use:
Keep in mind that any illegal or unethical use of this information/proxy is solely your responsibility
Use the proxies responsibly and ethically
```
## Proxy Reliability and Security:
```
Public proxies can be unreliable and may pose security risks
Avoid using them for sensitive data or operations
```
