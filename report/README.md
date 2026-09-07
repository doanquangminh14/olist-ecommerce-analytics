# 📈 Olist Analytics & Machine Learning Reports

Thư mục `report/` được cấu trúc thành 2 nhánh chuyên biệt, mỗi nhánh đi kèm tài liệu phân tích chi tiết và thư mục lưu trữ hình ảnh biểu đồ riêng biệt:

---

## 📁 Cấu Trúc Báo Cáo

```text
report/
│
├── README.md                          # Mục lục tổng quan báo cáo
│
├── business/                          # 📊 BÁO CÁO PHÂN TÍCH KINH DOANH
│   ├── README.md                      # Tài liệu phân tích chuyên sâu (Doanh thu, Khách hàng, Pareto, Logistics)
│   └── images/                        # Thư mục chứa 18 hình ảnh biểu đồ EDA & Business Insights
│       ├── monthly_revenue_trend.png
│       ├── monthly_orders_trend.png
│       ├── pareto_analysis.png
│       ├── customer_distribution_by_state.png
│       ├── Late Delivery Percentage.png
│       └── ... (các biểu đồ khác)
│
└── ml/                                # 🤖 BÁO CÁO MÔ HÌNH MACHINE LEARNING
    ├── README.md                      # Tài liệu đánh giá mô hình Random Forest, ROC-AUC, Feature Importance
    └── images/                        # Thư mục chứa 4 hình ảnh đánh giá mô hình ML
        ├── rf_accuracy_vs_trees.png
        ├── rf_confusion_matrix.png
        ├── rf_roc_curve.png
        └── rf_top15_feature_importance.png
```

---

## 🔗 Liên Kết Nhanh Đến Các Báo Cáo

- 📊 **[Đọc Báo Cáo Phân Tích Kinh Doanh (Business Insights)](business/README.md)**:
  - Xu hướng doanh thu & tăng trưởng đơn hàng qua các năm.
  - Phân tích phân bố địa lý theo 27 bang của Brazil và hành vi chi tiêu.
  - Kiểm chứng nguyên lý Pareto 80/20 trên danh mục sản phẩm.
  - Tác động của thời gian giao hàng và sự chậm trễ đến đánh giá của khách hàng.
  - Đề xuất chiến lược vận hành và tăng trưởng.

- 🤖 **[Đọc Báo Cáo Mô Hình Machine Learning (ML Insights)](ml/README.md)**:
  - Bài toán dự đoán sự hài lòng của khách hàng và cảnh báo sớm đơn hàng giao trễ.
  - Đánh giá mô hình Random Forest Classifier (Độ chính xác 80.37%, Ma trận nhầm lẫn, Đường cong ROC).
  - Phân tích Top 15 đặc trưng quan trọng nhất (Feature Importance).
  - Chiến lược ứng dụng thực tế vào hệ thống vận hành thương mại điện tử.
