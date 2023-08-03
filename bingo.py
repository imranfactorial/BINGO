import sys
import argparse
import asyncio
import aiohttp

async def make_request(session, url, headers):
    try:
        async with session.get(url, headers=headers, ssl=False) as response:
            response_text = await response.text()
            response_status = response.status
            return response_text, response_status
    except aiohttp.ClientError as e:
        pass
        return None, None

async def process_subdomain(session, subdomain, path, headers, user_input):
    subdomain = subdomain.strip()
    if not subdomain:
        return

    if not subdomain.startswith("https://") and not subdomain.startswith("http://"):
        url = f"https://{subdomain}"
    else:
        url = subdomain

    if path:
        url += path

    try:
        response, status = await make_request(session, url, headers)
        if response is not None and user_input in response:
            print(f"Input matched in {url}")
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Subdomain Tool")
    parser.add_argument("subdomains_file", help="Path to the file containing subdomains")
    args = parser.parse_args()

    try:
        with open(args.subdomains_file, 'r') as f:
            subdomains = f.read().splitlines()

        if not subdomains:
            print("No subdomains found in the input file.")
            sys.exit(1)

        user_input = input("Provide your input to match from the response: ").strip()
        if not user_input:
            print("Input not provided. Terminating the process.")
            sys.exit(0)

        path = input("Provide any path to add to subdomains (press Enter to skip): ").strip()

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close'
        }

        async with aiohttp.ClientSession() as session:
            tasks = [
                process_subdomain(session, subdomain, path, headers, user_input)
                for subdomain in subdomains
            ]

            await asyncio.gather(*tasks)

    except FileNotFoundError:
        print(f"File '{args.subdomains_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
