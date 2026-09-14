# Bao Cao Phan Tich Chuyen Sau Ve Kinh Doanh (Business Insights)

Thu muc nay tong hop cac bieu do truc quan hoa va bao cao phan tich chuyen sau duoc trich xuat tu qua trinh kham pha du lieu (EDA) trong [`notebook/eda_123.ipynb`](../../notebook/eda_123.ipynb) va [`notebook/eda_456.ipynb`](../../notebook/eda_456.ipynb) tren bo du lieu thuong mai dien tu Olist (Brazil).

---

## Muc Luc
1. [Xu Huong Doanh Thu & Don Hang](#1-xu-huong-doanh-thu--don-hang-revenue--orders-trend)
2. [Phan Phoi & Phat Hien Di Biet Doanh Thu](#2-phan-phoi--phat-hien-di-biet-doanh-thu-revenue-distribution--outliers)
3. [Phan Tich Dia Ly & Khach Hang](#3-phan-tich-dia-ly--hanh-vi-khach-hang-customer--geographic-analysis)
4. [Phan Tich Danh Muc San Pham & Nguyen Ly Pareto 80/20](#4-phan-tich-danh-muc-san-pham--nguyen-ly-pareto-8020)
5. [Van Chuyen, Logistics & Do Hai Long Khach Hang](#5-van-chuyen-logistics--do-hai-long-khach-hang)
6. [Ma Tran Tuong Quan Da Bien](#6-ma-tran-tuong-quan-da-bien-correlation-matrix)
7. [De Xuat & Khuyen Nghi Chien Luoc Kinh Doanh](#7-de-xuat--khuyen-nghi-chien-luoc-kinh-doanh)

---

## 1. Xu Huong Doanh Thu & Don Hang (Revenue & Orders Trend)

### Tang truong doanh thu va so luong don theo thang

| Xu Huong Doanh Thu Hang Thang | Xu Huong Don Hang Hang Thang |
| :---: | :---: |
| ![Monthly Revenue Trend](images/monthly_revenue_trend.png) | ![Monthly Orders Trend](images/monthly_orders_trend.png) |

### Insights Chinh:
- **Tang truong vuot bac**: Giai doan tu cuoi nam 2016 den giua nam 2018 ghi nhan toc do tang truong lien tuc ve ca GMV (Gross Merchandise Value) va so luong don hang.
- **Dinh cao Black Friday**: Thang 11/2017 chung kien su bung no manh me ve doanh thu va luong dat hang nho hieu ung Black Friday.
- **Duy tri on dinh trong nam 2018**: Dau nam 2018 (Quy 1 & Quy 2), doanh thu duy tri o muc cao tren 1 trieu BRL/thang voi trung binh ~6.500 - 7.000 don hang moi thang.

---

## 2. Phan Phoi & Phat Hien Di Biet Doanh Thu (Revenue Distribution & Outliers)

| Phan Phoi Doanh Thu (Histogram & KDE) | Phat Hien Di Biet Doanh Thu (Boxplot) |
| :---: | :---: |
| ![Revenue Distribution](images/revenue_distribution_histogram.png) | ![Revenue Outlier Detection](images/revenue_outlier_detection.png) |

### Insights Chinh:
- **Phan phoi lech phai manh (Right-skewed)**: Phan lon cac giao dich co gia tri don hang tu thap den trung binh (duoi 200 BRL).
- **Diem di biet (Outliers)**: Xuat hien mot so it giao dich co gia tri rat lon (len toi hang nghin BRL), chu yeu thuoc cac danh muc thiet bi cong nghe cao, may tinh hoac dat hang so luong lon (B2B/si).

---

## 3. Phan Tich Dia Ly & Hanh Vi Khach Hang (Customer & Geographic Analysis)

### Phan bo khach hang theo bang & Hanh vi chi tieu

| Phan Bo Khach Hang Theo Bang (Top States) | Nhan Dien Di Biet Chi Tieu Khach Hang |
| :---: | :---: |
| ![Customer Distribution by State](images/customer_distribution_by_state.png) | ![Customer Spending Outliers](images/customer_spending_outlier_detection.png) |

| Top 20 Khach Hang Chi Tieu Cao Nhat | Top 20 Khach Hang Dat Nhieu Don Nhat |
| :---: | :---: |
| ![Top 20 Spending](images/top_20_customers_by_spending.png) | ![Top 20 Orders](images/top_20_customers_by_orders.png) |

### Insights Chinh:
- **Tap trung vung Dong Nam (Southeast Region)**: Bang **São Paulo (SP)** chiem hon 40% tong luong khach hang cua nen tang, tiep theo la Rio de Janeiro (RJ), Minas Gerais (MG) va Rio Grande do Sul (RS).
- **Hanh vi mua sam**: Da so nguoi tieu dung ca nhan chi dat 1 don hang tren san (ty le mua lai thap), cho thay nen tang can cai thien chien luoc Retention va Loyalty Program.
- **Khach hang VIP / Chi tieu khung**: Mot so khach hang chi tieu vuot troi tu 5.000 den hon 13.000 BRL cho cac don hang dac thu.

---

## 4. Phan Tich Danh Muc San Pham & Nguyen Ly Pareto 80/20

### Top Danh Muc San Pham & Phan Tich Ty Trong

| Top 10 Danh Muc Theo Doanh Thu | Top 10 Danh Muc Theo San Luong Ban |
| :---: | :---: |
| ![Top Categories Revenue](images/top_10_categories_by_revenue.png) | ![Top Categories Sales](images/top_10_categories_by_sales_volume.png) |

| Phan Tich Nguyen Ly Pareto 80/20 | Treemap Ty Trong Doanh Thu Danh Muc |
| :---: | :---: |
| ![Pareto Analysis](images/pareto_analysis.png) | ![Treemap Revenue](images/top_categories_revenue_treemap.png) |

| Phat Hien Di Biet Theo Danh Muc San Pham |
| :---: |
| ![Category Revenue Outliers](images/category_revenue_outliers.png) |

### Insights Chinh:
- **Nguyen ly Pareto 80/20 duoc kiem chung ro net**: Khoang **20% so danh muc san pham hang dau dong gop hon 80% tong doanh thu** cho toan san.
- **Top Danh muc dan dau GMV**:
  1. `beleza_saude` (Suc khoe & Sac dep)
  2. `relogios_presentes` (Dong ho & Qua tang)
  3. `cama_mesa_banho` (Noi that phong ngu - Ga trai giuong)
  4. `esporte_lazer` (The thao & Da ngoai)
  5. `informatica_acessorios` (Thiet bi tin hoc & Phu kien may tinh)
- **Top Danh muc theo san luong**: `cama_mesa_banho` va `beleza_saude` la hai nganh hang co khoi luong tieu thu cao nhat.

---

## 5. Van Chuyen, Logistics & Do Hai Long Khach Hang

### Danh gia dich vu giao van va trai nghiem nguoi dung

| Ty Le Giao Hang Tre (Late Delivery Rate) | Phan Nhom Thoi Gian Giao Hang (Delivery Buckets) |
| :---: | :---: |
| ![Late Delivery Percentage](images/Late%20Delivery%20Percentage.png) | ![Delivery Time Categories](images/Delivery%20Time%20Categories.png) |

| Phan Phoi Diem Danh Gia Review (1 - 5 Sao) | Top 10 Danh Muc Duoc Danh Gia Nhieu Nhat |
| :---: | :---: |
| ![Review Score Distribution](images/Review%20Score%20Distribution.png) | ![Top 10 Most Reviewed Categories](images/Top%2010%20Most%20Reviewed%20Categories.png) |

### Insights Chinh:
- **Phan lon don hang giao dung han**: Khoang ~92% don hang duoc giao dung hoac som hon ngay du kien (`estimated_delivery_date`).
- **Giao tre la yeu to lam giam manh diem danh gia**: Khi don hang bi giao tre, ty le danh gia **1 sao va 2 sao tang vot len tren 70%**. Nguoc lai, don giao dung han dat diem trung binh 4.2 - 4.6 sao.
- **Thoi gian giao hang trung binh**: Da so don hang noi vung São Paulo duoc giao trong vong 5-10 ngay, trong khi cac bang vung sau vung xa (Bac/Dong Bac Brazil) co the mat tu 20-30 ngay.

---

## 6. Ma Tran Tuong Quan Da Bien (Correlation Matrix)

| Bieu Do Ma Tran Tuong Quan (Correlation Heatmap) |
| :---: |
| ![Correlation Heatmap](images/Correlation_Heatmap.png) |

### Insights Chinh:
- **Tuong quan manh giua cuoc phi (`freight_value`) va khoang cach dia ly / khoi luong san pham**.
- **Tuong quan am giua thoi gian giao hang (`delivery_days`) va diem danh gia (`review_score`)**: Thoi gian giao hang cang keo dai, diem review cang giam ro ret.
- **Moi quan he giua gia san pham va gia tri thanh toan**: Gia san pham quyet dinh phan lon tong hoa don, phi ship chiem trung binh 15-25% gia tri don hang.

---

## 7. De Xuat & Khuyen Nghi Chien Luoc Kinh Doanh

1. **Toi uu hoa Mang luoi Logistics & Kho van (Fulfillment Centers)**:
   - Thanh lap cac hub kho bai ve tinh tai Dong Nam va Nam Brazil de rut ngan thoi gian giao hang chang cuoi (Last-mile Delivery).
   - Tu dong hoa he thong canh bao don hang co nguy co cham tre de thong bao chu dong cho khach hang truoc khi phat sinh khieu nai.
2. **Chien luoc Quan ly Danh Muc San Pham (Category Management)**:
   - Uu tien nguon luc marketing, tro gia va hop tac voi cac nha ban hang (sellers) thuoc top 20% danh muc cot loi (Suc khoe, Sac dep, Noi that, Dong ho, Phu kien IT).
   - Kiem soat chat luong san pham doi voi cac nganh hang co ty le danh gia 1 sao cao.
3. **Chien Luoc Tang Ty Le Mua Lai (Customer Retention & Re-engagement)**:
   - Thiet lap chuong trinh hoi vien (Loyalty/Cashback) va ca nhan hoa chien dich Email/Voucher dua tren lich su mua sam.
   - Thuc day chinh sach mien phi van chuyen (Free Shipping) theo gia tri don hang toi thieu tai khu vuc trong diem São Paulo.
