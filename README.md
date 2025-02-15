# Updated HTTP/HTTPS proxies every 3 hours
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

Proxy scraper and tester that provides updated HTTP/HTTPS proxies every 3 hours. This project is optimized for high performance and reliability, with features like proxy validation, testing, and output customization.

---

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Proxies Output Formats](#proxies-output-formats)
- [Proxy Tester Script](#proxy-tester-script)
- [Contribution](#contribution)
- [Important Considerations](#important-considerations)

---

## Features

- **[Proxy Validation](#)**: Tests proxies for connectivity and returns working proxies.
- **[Multi-Endpoint Testing](#)**: Rotates between custom and public endpoints to reduce rate-limiting.
- **[Speed Testing](#)**: Measures latency to rank proxies by performance.
- **[Geolocation Support](#)**: Optionally determines the country and region of each proxy.
- **[Custom Testing Server](#)**: Integrates with your own server (e.g., `http://164.90.187.218:5000/ip`).
- **[Multiple Output Formats](#proxies-output-formats)**: Save results in text, JSON, or CSV formats.
- **[Proxy Tester](#proxy-tester-script)**: Simple script to validate proxies locally.

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

---



## Proxies Output Formats

### Clean Format (`clean_proxies.txt`)
```
192.168.0.1:8080
45.43.82.113:6107
```

### Full Format (`proxies.txt`)
```
http://192.168.0.1:8080
https://45.43.82.113:6107
```

## Proxy Tester Script

Want to test proxies locally? Use the quick tester below! 

### Features:
- **Validates proxies quickly**
- **Outputs valid or invalid status**
- **Option to save working proxies**

### Instructions:
1. Create a file called `proxyhere.txt` in the same directory.
2. Paste your proxy list (e.g., `IP:Port` format) into the file.
3. At the end you get an option to save working proxies to a file for later use.
4. **Run this Python script:**
###Important
**The more "Workers" u have the less accurate results you get**
- More workers = Faster but less working proxies - 10-100 workers
- Less workers = Slower but more working proxies - 1-10 workers
### Use 1-10 workers max for the optimal result
```
What i do:
-----------------------------------------------------------------------------------------
1. First i copy the cleaned_proxies
2. I paste them in proxiehere.txt
3. I run the python script with workers set at 3
4. Done
-----------------------------------------------------------------------------------------
I use 1-5 workers when i do it myself as this gives me most proxies with correct result
-----------------------------------------------------------------------------------------
The Main scraper info:
-----------------------------------------------------------------------------------------
- The Script use 50 workers
- This is done becuase it checks 8000+ Proxies 
- You can run this urself if and set workers to 10 if you want more working proxies
-----------------------------------------------------------------------------------------
What The Checker Under Does:
-----------------------------------------------------------------------------------------
- Uses 5 workers
- Can save results in a new txt at the end
```
### Python Self Checker Script
```python
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
    with ThreadPoolExecutor(max_workers=5) as executor:
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

5. You can save file as **proxieshere.txt** to get the new working tested proxies into the same file u put them in

---

## Contribution

We welcome contributions! If you’d like to add new features or suggest improvements:
- Fork the repository
- Submit a pull request
- Raise issues for discussion

---

## Important Considerations

### Legal and Ethical Use:
- **Use the proxies responsibly and ethically.**
- **Any illegal or unethical use of this tool or its proxies is solely your responsibility.**

### Proxy Reliability and Security:
- **Public proxies may be unreliable and pose security risks.**
- **Avoid using them for sensitive operations or data.**
- **Remember that free proxies may log browsing history, so your online privacy may be compromised**
---

