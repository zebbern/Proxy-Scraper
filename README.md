# Updated HTTP/HTTPS Proxies Every 3 Hours
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

This repository offers a high-performance solution for scraping, validating, and testing HTTP/HTTPS proxies. Proxies are updated every 3 hours, ensuring users have access to the latest and most reliable options. Additionally, a Python-based proxy checker script is included to allow for efficient testing and validation of proxies.

---

## Table of Contents
- [Features](#features)
- [Proxy Output Formats](#proxy-output-formats)
- [Python Self-Checker Script](#python-self-checker-script)
- [Important Considerations](#important-considerations)
- [License](#license)

---

## Features

- **Regular Proxy Updates:** Fetches updated proxies every 3 hours.
- **Proxy Validation:** Ensures proxies are functional before use.
- **Flexible Output Formats:** Supports formats such as `proxies.txt`, `proxyScrapeDump.txt`, and `cleaned_proxies.txt`.
- **Python Proxy Checker Script:** Allows users to test proxy functionality locally with a range of customization options.

---

## Proxy Output Formats

1. **Cleaned Format (`cleaned_proxies.txt`):**
   ```
   IP:PORT
   IP:PORT
   ```
2. **Full Format (`proxies.txt`):**
   ```
   http://IP:PORT
   https://IP:PORT
   ```
3. **Unchecked Proxies Format (`proxyScrapeDump.txt`):**
   ```
   http://IP:PORT
   https://IP:PORT
   ```
---

## Python Self-Checker Script

This repository includes a Python script designed to validate proxies locally. 

### Features:
- Tests proxies for connectivity and outputs working results.
- Allows users to save valid proxies for later use.
- Supports adjustable worker threads to balance speed and accuracy.

### How It Works:
1. Paste proxies into `proxyhere.txt` in the `IP:Port` format.
2. Run the script with a recommended worker setting of 3-5 for optimal accuracy.
3. Optionally save working proxies to a file for future use.

**Key Notes:**
- Increasing the number of workers enhances speed but may reduce accuracy.
- Detailed usage instructions are included in the script itself.

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

---

## Important Considerations

### Legal and Ethical Use
```
- Ensure the proxies are used ethically and responsibly.
- The repository owner is not liable for any misuse of this tool or the proxies.
```
### Proxy Reliability and Security
```
- Be cautious of public proxies, as they may log browsing history and compromise security.
- Avoid using free proxies for sensitive operations.
```
---

