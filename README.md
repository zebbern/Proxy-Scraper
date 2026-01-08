# This project is no longer maintained

<div align="center">

## Provides Updated `HTTP/HTTPS/Socks4/Socks5` proxies every hour!
    
<img src="https://github.com/user-attachments/assets/d6ad457b-87de-4b76-8886-402b7c4bfab5" style="width:45%;">

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

**This project is for high performance and reliability, with features like proxy validation, testing, and output customization.**
 
 **[Proxy Tester Settings](#how-to-use)** | **[Proxy Tester Code](#proxy-tester-code)** | **[Important Considerations](#important)** 

---
</div>

## How To Use

Want to test proxies locally? Use the quick tester below! 

### Instructions:
1. Create a file called `proxies.txt` in the same directory.
2. Paste your proxy list (e.g., `IP:Port` format) into the file.
3. At the end you get an option to save working proxies to a file for later use.
4. **Run this Python script:**
###Important
**The more "Workers" u have the less accurate results you get**
- More workers = Faster but less working proxies - 10-100 workers
- Less workers = Slower but more working proxies - 1-10 workers
### Use 1-10 workers max for the optimal result

### Proxy Tester Code
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
    with open('proxies.txt', 'r') as file:
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

5. You can save file as **proxies.txt** to get the new working tested proxies into the same file u put them in

<a name="important"></a>
> [!Important]
> 
> ---
> ### Legal and Ethical Use:
> - **Use the proxies responsibly and ethically.**
> - **Any illegal or unethical use of this tool or its proxies is solely your responsibility.**
> - **This is all public available proxies and has nothing to do with me this list is only for easy access to proxies.**
> ---
> ### Proxy Reliability and Security:
> - **Public proxies may be unreliable and pose security risks.**
> - **Avoid using them for sensitive operations or data.**
> - **Remember that free proxies may log browsing history, so your online privacy may be compromised**
> ---
