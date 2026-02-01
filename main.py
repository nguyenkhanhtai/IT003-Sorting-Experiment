import numpy as np
import time
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import random

# Thêm đường dẫn để có thể import từ folder sorting
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from sorting import MergeSort, GeminiMergeSort
from sorting import HeapSort, GeminiHeapSort
from sorting import QuickSort
from sorting import NumpySort

def generate_datasets():
    datasets = []
    n = 1_000_000  # 1 triệu phần tử
    
    print(f"Đang khởi tạo dữ liệu (N={n})...")
    
    # 1. Dãy số thực tăng dần
    datasets.append(("Float Ascending", np.sort(np.random.uniform(-n, n, n))))
    
    # 2. Dãy số thực giảm dần
    datasets.append(("Float Descending", np.sort(np.random.uniform(-n, n, n))[::-1]))
    
    # 3-5. Dãy số thực ngẫu nhiên
    for i in range(3):
        datasets.append((f"Float Random {i+1}", np.random.uniform(-n, n, n)))

    # 6-10. Dãy số nguyên ngẫu nhiên
    for i in range(5):
        datasets.append((f"Int Random {i+1}", np.random.randint(-n, n, n, dtype=np.int64)))
        
    return datasets

def run_experiment():
    # Set seed để đảm bảo tính lặp lại (reproducibility)
    np.random.seed(42)
    random.seed(42)

    datasets = generate_datasets()
    
    # Tăng giới hạn đệ quy cho QuickSort với dữ liệu lớn
    sys.setrecursionlimit(2000000)
    
    sorters = [
        ("NumpySort", NumpySort()),
        ("QuickSort", QuickSort()),
        ("HeapSort", HeapSort()),
        ("GeminiHeapSort", GeminiHeapSort()),
        ("MergeSort", MergeSort()),
        ("GeminiMergeSort", GeminiMergeSort())
    ]
    
    results = []

    print("\n" + "="*65)
    print(f"{'Dataset':<20} | {'Algorithm':<15} | {'Time (s)':<10}")
    print("="*65)
    
    for data_name, data_array in datasets:
        for algo_name, sorter in sorters:
            # Copy dữ liệu để thuật toán không làm thay đổi mảng gốc cho các thuật toán sau
            arr_copy = np.copy(data_array)
            
            start_time = time.time()
            try:
                sorter.sort(arr_copy)
                end_time = time.time()
                elapsed = end_time - start_time
                
                results.append({"Dataset": data_name, "Algorithm": algo_name, "Time (s)": elapsed})
                print(f"{data_name:<20} | {algo_name:<15} | {elapsed:.5f}")
            except Exception as e:
                results.append({"Dataset": data_name, "Algorithm": algo_name, "Time (s)": None})
                print(f"{data_name:<20} | {algo_name:<15} | Error: {e}")
        print("-" * 65)

    # --- Xuất ra Excel ---
    df = pd.DataFrame(results)

    # --- Xử lý bảng kết quả (Pivot Table) ---
    # Tạo cột ID cho dataset (1 -> 10) dựa trên thứ tự xuất hiện
    dataset_ids = {name: i+1 for i, name in enumerate(df['Dataset'].unique())}
    df['ID'] = df['Dataset'].map(dataset_ids)
    pivot_df = df.pivot_table(index=['ID', 'Dataset'], columns='Algorithm', values='Time (s)')

    print("\n" + "="*80)
    print("BẢNG TỔNG HỢP THỜI GIAN CHẠY (s)")
    print("="*80)
    print(pivot_df.to_string())
    print("="*80)

    # Tạo folder statistics nếu chưa tồn tại
    output_folder = "statistics"
    os.makedirs(output_folder, exist_ok=True)

    try:
        excel_path = os.path.join(output_folder, "sorting_results.xlsx")
        pivot_df.to_excel(excel_path)
        print(f"\n[INFO] Kết quả đã được lưu vào file '{excel_path}'")
    except Exception as e:
        print(f"\n[ERROR] Không thể lưu file Excel: {e}")

    # --- Vẽ biểu đồ ---
    try:
        plt.figure(figsize=(14, 8))
        
        # Sắp xếp dữ liệu theo ID để đảm bảo thứ tự dataset trên trục X đúng trình tự chạy
        df_sorted = df.sort_values('ID')
        
        # Vẽ đường cho từng thuật toán
        for algo in df_sorted['Algorithm'].unique():
            subset = df_sorted[df_sorted['Algorithm'] == algo]
            plt.plot(subset['Dataset'], subset['Time (s)'], marker='o', label=algo)

        plt.title("So sánh thời gian chạy các thuật toán sắp xếp")
        plt.xlabel("Dataset")
        plt.ylabel("Time (s)")
        plt.xticks(rotation=45, ha='right') # Xoay tên dataset để dễ đọc
        plt.legend() # Hiển thị chú thích
        plt.grid(True) # Thêm lưới để dễ dóng số liệu
        plt.tight_layout()
        
        filename = os.path.join(output_folder, "sorting_comparison_line_graph.png")
        plt.savefig(filename)
        print(f"[INFO] Đã lưu biểu đồ đường: {filename}")
        plt.close()
            
    except Exception as e:
        print(f"\n[ERROR] Không thể vẽ biểu đồ: {e}")

if __name__ == "__main__":
    run_experiment()
