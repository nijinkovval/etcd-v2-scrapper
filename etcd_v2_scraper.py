import requests
import sys
from urllib.parse import urljoin
from tabulate import tabulate

def scrape_v2(ip, port):
    endpoint = f"http://{ip}:{port}"
    url = urljoin(endpoint + "/", "v2/keys/?recursive=true")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[v2] Request failed: {e}")
        return []

    data = response.json()
    result_map = {}

    def flatten(node):
        if node.get("dir", False):
            for child in node.get("nodes", []):
                flatten(child)
        else:
            key = node.get("key", "")
            val = node.get("value", "")
            result_map[key] = val 

    flatten(data.get("node", {}))

    return sorted([[k, v] for k, v in result_map.items()])


def print_results(data):
    if data:
        print(tabulate(data, headers=["Key", "Value"], tablefmt="fancy_grid", maxcolwidths=[50, 60]))
    else:
        print("No data found or connection failed.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python etcd_v2_scraper.py <ip> <port>")
        sys.exit(1)

    ip, port = sys.argv[1], sys.argv[2]
    print(f"\n Scraping etcd v2 at {ip}:{port} ...\n")
    data = scrape_v2(ip, port)

    print_results(data)

if __name__ == "__main__":
    main()
