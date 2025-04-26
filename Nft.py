import os
import requests
from datetime import datetime

def log_message(folder, message):
    log_path = os.path.join(folder, "log.txt")
    with open(log_path, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")

def download_nft_series(base_url, collection_name, start=1):
    folder_path = os.path.join("nft", collection_name)
    os.makedirs(folder_path, exist_ok=True)

    while True:
        for size in ["large", "small", "medium"]:
            filename = f"{collection_name}-{start}.{size}.jpg"
            url = f"{base_url}{filename}"
            save_path = os.path.join(folder_path, filename)

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    msg = f"Downloaded: {filename}"
                    print(msg)
                    log_message(folder_path, msg)
                    start += 1
                    break  # Move to next index
                elif size == "medium":
                    msg = f"Stopped. No image found for: {collection_name}-{start}"
                    print(msg)
                    log_message(folder_path, msg)
                    return
            except Exception as e:
                msg = f"Error occurred: {e}"
                print(msg)
                log_message(folder_path, msg)
                return

# Run script
if __name__ == "__main__":
    base_url = "https://nft.fragment.com/gift/"
    collection = input("Enter collection name (e.g., plushpepe): ").strip()
    download_nft_series(base_url, collection)
