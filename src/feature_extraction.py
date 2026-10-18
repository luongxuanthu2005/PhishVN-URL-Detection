
from pathlib import Path
from urllib.parse import urlparse
import ipaddress
import re

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR = PROJECT_DIR / "data" / "features"

FILES = ["url_train.csv", "url_val.csv", "url_test.csv"]


def extract_features(url):
    """Trích xuất các đặc trưng từ một URL."""
    url = str(url).strip()
    parsed = urlparse(url if "://" in url else "//" + url)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    # Kiểm tra hostname có phải địa chỉ IP hay không
    has_ip = 0
    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except ValueError:
        pass

    return {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(char.isdigit() for char in url),
        "num_special_chars": sum(
            not char.isalnum() for char in url
        ),
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_at": int("@" in url),
        "has_ip": has_ip,
        "num_subdirectories": len(
            [part for part in path.split("/") if part]
        ),
        "num_query_params": (
            len(query.split("&")) if query else 0
        ),
        "hostname_length": len(hostname),
        "has_suspicious_keyword": int(
            bool(
                re.search(
                    r"login|verify|account|secure|update|"
                    r"password|bank|signin",
                    url,
                    re.IGNORECASE,
                )
            )
        ),
    }


def process_file(filename):
    input_path = INPUT_DIR / filename
    df = pd.read_csv(input_path)

    if not {"url", "label"}.issubset(df.columns):
        raise ValueError(
            f"{filename} phải có hai cột url và label."
        )

    # Chỉ sử dụng URL để tạo đặc trưng.
    # Không đưa nhãn vào tập đặc trưng X.
    features = pd.DataFrame(
        df["url"].apply(extract_features).tolist()
    )

    # Giữ nhãn làm biến mục tiêu y.
    features["label"] = df["label"].values

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    features.to_csv(
        output_path, index=False, encoding="utf-8-sig"
    )

    print(f"\nĐã xử lý: {filename}")
    print("Số dòng:", len(features))
    print("Số đặc trưng:", len(features.columns) - 1)
    print("Phân bố nhãn:")
    print(features["label"].value_counts().to_string())
    print("Đã lưu:", output_path)


def main():
    for filename in FILES:
        process_file(filename)

    print("\nHoàn thành trích xuất đặc trưng.")


if __name__ == "__main__":
    main()
