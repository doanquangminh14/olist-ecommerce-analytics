# Olist Analytics & Machine Learning Reports

Thu muc `report/` duoc cau truc thanh 2 nhanh chuyen biet, moi nhanh di kem tai lieu phan tich chi tiet va thu muc luu tru hinh anh bieu do rieng biet:

---

## Cau Truc Bao Cao

```text
report/
|
+-- README.md                          # Muc luc tong quan bao cao
|
+-- business/                          # BAO CAO PHAN TICH KINH DOANH
|   +-- README.md                      # Tai lieu phan tich chuyen sau (Doanh thu, Khach hang, Pareto, Logistics)
|   +-- images/                        # Thu muc chua 18 hinh anh bieu do EDA & Business Insights
|       +-- monthly_revenue_trend.png
|       +-- monthly_orders_trend.png
|       +-- pareto_analysis.png
|       +-- customer_distribution_by_state.png
|       +-- Late Delivery Percentage.png
|       +-- ... (cac bieu do khac)
|
+-- ml/                                # BAO CAO MO HINH MACHINE LEARNING
    +-- README.md                      # Tai lieu danh gia mo hinh Random Forest, ROC-AUC, Feature Importance
    +-- images/                        # Thu muc chua 4 hinh anh danh gia mo hinh ML
        +-- rf_accuracy_vs_trees.png
        +-- rf_confusion_matrix.png
        +-- rf_roc_curve.png
        +-- rf_top15_feature_importance.png
```

---

## Lien Ket Nhanh Den Cac Bao Cao

- **[Doc Bao Cao Phan Tich Kinh Doanh (Business Insights)](business/README.md)**:
  - Xu huong doanh thu & tang truong don hang qua cac nam.
  - Phan tich phan bo dia ly theo 27 bang cua Brazil va hanh vi chi tieu.
  - Kiem chung nguyen ly Pareto 80/20 tren danh muc san pham.
  - Tac dong cua thoi gian giao hang va su cham tre den danh gia cua khach hang.
  - De xuat chien luoc van hanh va tang truong.

- **[Doc Bao Cao Mo Hinh Machine Learning (ML Insights)](ml/README.md)**:
  - Bai toan du doan su hai long cua khach hang va canh bao som don hang giao tre.
  - Danh gia mo hinh Random Forest Classifier (Do chinh xac 80.37%, Ma tran nham lan, Duong cong ROC).
  - Phan tich Top 15 dac trung quan trong nhat (Feature Importance).
  - Chien luoc ung dung thuc te vao he thong van hanh thuong mai dien tu.
