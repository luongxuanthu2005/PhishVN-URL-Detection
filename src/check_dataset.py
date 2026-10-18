
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

print("=" * 60)
print("KIỂM TRA CÁC FILE TRONG BỘ DỮ LIỆU PHISHVN")
print("=" * 60)

# Các file cần kiểm tra
target_names = {
    "dataset_url.csv",
    "url_train.csv",
    "url_val.csv",
    "url_test.csv",
}

found_targets = []

# Liệt kê tất cả file CSV trong thư mục data
csv_files = list(DATA_DIR.rglob("*.csv"))

if not csv_files:
    print("\nKhông tìm thấy file CSV nào trong:", DATA_DIR)
else:
    print(f"\nTìm thấy {len(csv_files)} file CSV:\n")

    for file in sorted(csv_files):
        relative_path = file.relative_to(PROJECT_DIR)
        print(f"- {relative_path}")

        if file.name.lower() in target_names:
            found_targets.append(file)

print("\n" + "=" * 60)
print("KẾT QUẢ KIỂM TRA CÁC FILE QUAN TRỌNG")
print("=" * 60)

for name in sorted(target_names):
    matches = [
        file for file in found_targets
        if file.name.lower() == name
    ]

    if matches:
        for file in matches:
            print(f"[CÓ] {name}: {file}")
    else:
        print(f"[KHÔNG THẤY] {name}")

print("\nHoàn thành kiểm tra.")
