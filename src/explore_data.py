
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==================================================
# 1. KHAI BÁO ĐƯỜNG DẪN
# ==================================================

# Thư mục gốc của dự án
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Thư mục chứa dữ liệu
DATA_DIR = PROJECT_DIR / "data"

# Thư mục lưu báo cáo
REPORT_DIR = PROJECT_DIR / "reports"


# ==================================================
# 2. TÌM VÀ ĐỌC DỮ LIỆU
# ==================================================

def find_data_file():
    """Tìm tệp abuse_type.csv trong thư mục data."""

    if not DATA_DIR.exists():
        print(f"LỖI: Không tìm thấy thư mục: {DATA_DIR}")
        return None

    files = list(DATA_DIR.rglob("abuse_type.csv"))

    if not files:
        print("Không tìm thấy tệp abuse_type.csv.")
        print("\nCác tệp CSV hiện có:")

        csv_files = list(DATA_DIR.rglob("*.csv"))

        if csv_files:
            for file in csv_files:
                print("-", file.relative_to(PROJECT_DIR))
        else:
            print("Không có tệp CSV trong thư mục data.")

        return None

    if len(files) > 1:
        print("Có nhiều tệp abuse_type.csv:")
        for file in files:
            print("-", file.relative_to(PROJECT_DIR))

        print("Sử dụng tệp đầu tiên trong danh sách.")

    return files[0]


def load_data(file_path):
    """Đọc dữ liệu CSV và kiểm tra lỗi."""

    try:
        df = pd.read_csv(file_path)

        # Chuẩn hóa tên cột, loại bỏ khoảng trắng ở đầu/cuối
        df.columns = df.columns.str.strip()

        required_columns = {"url", "abuse_type", "rule"}
        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            print("LỖI: Thiếu các cột:", missing_columns)
            print("Các cột hiện có:", df.columns.tolist())
            return None

        print("\nĐọc dữ liệu thành công!")
        print("Tệp:", file_path.name)
        print("Đường dẫn:", file_path)
        return df

    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        print("Không thể đọc tệp dữ liệu:", error)
        return None


# ==================================================
# 3. KHÁM PHÁ DỮ LIỆU
# ==================================================

def explore_data(df):
    """Thống kê thông tin tổng quan về dữ liệu."""

    print("\n" + "=" * 60)
    print("BÁO CÁO KHÁM PHÁ DỮ LIỆU PHISHVN")
    print("=" * 60)

    # Kích thước dữ liệu
    print("\n1. KÍCH THƯỚC DỮ LIỆU")
    print("Số dòng:", df.shape[0])
    print("Số cột:", df.shape[1])

    # Danh sách cột
    print("\n2. DANH SÁCH CỘT")
    print(df.columns.tolist())

    # Kiểu dữ liệu
    print("\n3. KIỂU DỮ LIỆU")
    print(df.dtypes)

    # Năm dòng đầu tiên
    print("\n4. NĂM DÒNG ĐẦU TIÊN")
    print(df.head().to_string(index=False))

    # Giá trị thiếu
    print("\n5. GIÁ TRỊ THIẾU")
    missing_values = df.isnull().sum()
    print(missing_values)

    # Dữ liệu trùng lặp
    print("\n6. DỮ LIỆU TRÙNG LẶP")
    print("Số dòng trùng lặp:", df.duplicated().sum())
    print("Số URL khác nhau:", df["url"].nunique())

    # Phân bố nhãn
    print("\n7. PHÂN BỐ NHÃN ABUSE_TYPE")

    label_counts = df["abuse_type"].value_counts(dropna=False)

    label_percent = (
        df["abuse_type"]
        .value_counts(normalize=True, dropna=False)
        .mul(100)
        .round(2)
    )

    label_summary = pd.DataFrame({
        "so_luong": label_counts,
        "ty_le_phan_tram": label_percent
    })

    print(label_summary)

    # Thống kê rule
    print("\n8. THỐNG KÊ RULE")
    print("Số giá trị rule khác nhau:", df["rule"].nunique())
    print("Số giá trị rule bị thiếu:", df["rule"].isnull().sum())

    print("\nCác rule phổ biến:")
    print(df["rule"].value_counts().head(20))

    return missing_values, label_summary, label_counts


# ==================================================
# 4. LƯU BÁO CÁO
# ==================================================

def save_reports(df, missing_values, label_summary, label_counts):
    """Lưu các bảng thống kê và biểu đồ."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Lưu thống kê giá trị thiếu
    missing_values.to_csv(
        REPORT_DIR / "missing_values.csv",
        header=["missing_count"],
        encoding="utf-8-sig"
    )

    # Lưu phân bố nhãn
    label_summary.to_csv(
        REPORT_DIR / "label_distribution.csv",
        encoding="utf-8-sig"
    )

    # Lưu thống kê các cột
    column_summary = pd.DataFrame({
        "column": df.columns,
        "data_type": [str(dtype) for dtype in df.dtypes],
        "missing_count": df.isnull().sum().values,
        "unique_count": df.nunique().values
    })

    column_summary.to_csv(
        REPORT_DIR / "column_summary.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # Vẽ biểu đồ phân bố nhãn
    plt.figure(figsize=(10, 6))

    label_counts.sort_values().plot(kind="barh")

    plt.title("Phân bố nhãn abuse_type trong PhishVN")
    plt.xlabel("Số lượng URL")
    plt.ylabel("Loại nhãn")
    plt.tight_layout()

    chart_path = REPORT_DIR / "label_distribution.png"

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\n" + "=" * 60)
    print("ĐÃ LƯU BÁO CÁO")
    print("=" * 60)
    print("Thư mục:", REPORT_DIR)
    print("- missing_values.csv")
    print("- label_distribution.csv")
    print("- column_summary.csv")
    print("- label_distribution.png")


# ==================================================
# 5. CHƯƠNG TRÌNH CHÍNH
# ==================================================

def main():
    print("=" * 60)
    print("PHÂN TÍCH BỘ DỮ LIỆU PHISHVN")
    print("=" * 60)

    # Tìm dữ liệu
    data_file = find_data_file()

    if data_file is None:
        return

    # Đọc dữ liệu
    df = load_data(data_file)

    if df is None:
        return

    # Khám phá dữ liệu
    missing_values, label_summary, label_counts = explore_data(df)

    # Lưu báo cáo
    save_reports(
        df,
        missing_values,
        label_summary,
        label_counts
    )

    print("\nHoàn thành quá trình khám phá dữ liệu!")


if __name__ == "__main__":
    main()
