
print("PHÂN TÍCH BỘ DỮ LIỆU PHISHVN")

ten_de_tai = "Dự đoán URL giả mạo tại Việt Nam"

print("Đề tài: ", ten_de_tai)
print("Môi trường: Python trên VS Code")


from pathlib import Path
import pandas as pd

# Thư mục gốc của dự án
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

print("=" * 50)
print("KIỂM TRA BỘ DỮ LIỆU PHISHVN")
print("=" * 50)

if not DATA_DIR.exists():
    print("Không tìm thấy thư mục data:", DATA_DIR)
else:
    # Liệt kê các tệp bên trong data và thư mục con
    files = [
        p for p in DATA_DIR.rglob("*")
        if p.is_file()
    ]

    if not files:
        print("Thư mục data hiện chưa có tệp dữ liệu.")
    else:
        print("\nCác tệp tìm thấy:")
        for file in files:
            print("-", file.relative_to(PROJECT_DIR))

        # Tìm các tệp CSV
        csv_files = [
            p for p in files
            if p.suffix.lower() == ".csv"
        ]

        if not csv_files:
            print("\nChưa tìm thấy tệp CSV.")
            print("Hãy kiểm tra định dạng dữ liệu trong danh sách trên.")
        else:
            for file in csv_files:
                print("\n" + "=" * 50)
                print("Đang đọc:", file.name)

                try:
                    df = pd.read_csv(file)

                    print("Đọc dữ liệu thành công!")
                    print("Số dòng, số cột:", df.shape)

                    print("\nTên các cột:")
                    print(df.columns.tolist())

                    print("\n5 dòng đầu tiên:")
                    print(df.head().to_string())

                    print("\nThông tin dữ liệu:")
                    df.info()

                    print("\nSố lượng giá trị thiếu:")
                    print(df.isnull().sum())

                except Exception as e:
                    print("Không đọc được tệp:", e)
