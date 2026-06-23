import requests


def reset_stores():
    urls = [f"http://localhost:500{n}/debug/reset_store" for n in range(1, 4)]
    for url in urls:
        try:
            response = requests.post(url)
            print(f"POST {url}: {response.status_code} {response.reason}")
        except Exception as exc:
            print(f"POST {url}: failed ({exc})")


if __name__ == "__main__":
    reset_stores()
