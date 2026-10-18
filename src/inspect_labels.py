
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = (
    PROJECT_DIR
    / "data"
    / "PhishVN_v3.1.0_open"
    / "data"
)

FILES = [
    DATA_DIR / "dataset_url.csv",
    DATA_DIR / "splits" / "url_train.csv",
    DATA_DIR / "splits" / "url_val.csv",
    DATA_DIR / "splits" / "url_test.csv",
]


def inspect_file(file_path):
    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    if not file_path.exists():
        print("Không tìm thấy file:", file_path)
        return

    df = pd.read_csv(file_path)

    print("Kích thước:", df.shape)
    print("\nTên cột:")
    print(df.columns.tolist())

    print("\nKiểu dữ liệu:")
    print(df.dtypes)

    print("\n5 dòng dữ liệu mẫu:")
    print(df.head().to_string(index=False))

    print("\nGiá trị thiếu:")
    print(df.isna().sum().to_string())

    print("\nSố dòng trùng lặp toàn bộ:")
    print(df.duplicated().sum())

    # Thống kê các cột có ít giá trị khác nhau,
    # thường có thể là cột nhãn.
    print("\nCác cột có tối đa 20 giá trị khác nhau:")
    for column in df.columns:
        if df[column].nunique(dropna=False) <= 20:
            print(f"\nCột: {column}")
            print(df[column].value_counts(dropna=False).to_string())


def main():
    for file_path in FILES:
        inspect_file(file_path)

    print("\nĐã hoàn thành kiểm tra cấu trúc dữ liệu.")


if __name__ == "__main__":
    main()
