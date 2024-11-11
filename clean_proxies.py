def clean_proxies(input_file='proxies.txt', output_file='cleaned_proxies.txt'):
    """
    Reads proxies from input_file, removes http/https prefixes,
    and saves the cleaned list to output_file.
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Remove 'http://' or 'https://' prefixes
                cleaned_line = line.strip().replace('http://', '').replace('https://', '')
                if cleaned_line:  # Ensure it's not an empty line
                    outfile.write(cleaned_line + '\n')
        print(f"Cleaned proxies saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clean_proxies()
