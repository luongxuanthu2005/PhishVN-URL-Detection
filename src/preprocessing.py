
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "PhishVN_v3.1.0_open" / "data"
SPLIT_DIR = DATA_DIR / "splits"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

# Các cột cần cho việc phân loại URL
KEEP_COLUMNS = [
    "url",
    "url_norm",
    "domain",
    "tld",
    "url_len",
    "num_dots",
    "num_subdomains",
    "has_ip",
    "has_at",
    "suspicious_tld",
    "label",
]

VALID_LABELS = {"phishing", "benign"}


def preprocess_file(filename):
    input_path = SPLIT_DIR / filename
    df = pd.read_csv(input_path, low_memory=False)

    print(f"\nĐang xử lý: {filename}")
    print("Kích thước ban đầu:", df.shape)

    # Kiểm tra các cột bắt buộc
    required = {"url", "label"}
    missing_columns = required - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{filename} thiếu các cột: {missing_columns}"
        )

    # Chuẩn hóa khoảng trắng ở URL và nhãn
    df["url"] = df["url"].astype("string").str.strip()
    df["label"] = df["label"].astype("string").str.strip().str.lower()

    # Loại bỏ dòng thiếu URL hoặc nhãn
    before = len(df)
    df = df.dropna(subset=["url", "label"])
    df = df[df["url"] != ""]
    print("Số dòng bị loại do thiếu URL/nhãn:", before - len(df))

    # Chỉ giữ nhãn hợp lệ
    invalid = ~df["label"].isin(VALID_LABELS)
    print("Số dòng có nhãn không hợp lệ:", int(invalid.sum()))
    df = df[~invalid].copy()

    # Kiểm tra URL trùng lặp
    duplicates = df["url_norm"].duplicated().sum() if "url_norm" in df.columns else 0
    print("Số URL chuẩn hóa trùng lặp:", int(duplicates))

    # Không tự động xóa URL trùng ở bước này để tránh
    # vô tình thay đổi cấu trúc của các tập train/val/test.
    # Giữ các cột thực sự có trong file.
    selected_columns = [
        column for column in KEEP_COLUMNS
        if column in df.columns
    ]
    df = df[selected_columns].copy()

    # Kiểm tra thiếu dữ liệu trong các cột giữ lại
    print("Giá trị thiếu trong các cột được giữ:")
    print(df.isna().sum().to_string())

    print("Kích thước sau xử lý:", df.shape)
    print("Phân bố nhãn:")
    print(df["label"].value_counts().to_string())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("Đã lưu:", output_path)


def main():
    for filename in [
        "url_train.csv",
        "url_val.csv",
        "url_test.csv",
    ]:
        preprocess_file(filename)

    print("\nHoàn thành tiền xử lý train/validation/test.")


if __name__ == "__main__":
    main()
