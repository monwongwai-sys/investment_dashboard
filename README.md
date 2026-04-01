# 📊 Investment Budget Dashboard - MITR PHOL

## วิธีติดตั้งและรัน

### 1. ติดตั้ง dependencies
```bash
pip install streamlit plotly pandas
```

### 2. วางไฟล์ทั้งหมดไว้ใน folder เดียวกัน
```
📁 dashboard/
├── investment_dashboard.py
└── Investment_Budget_69_Sheet1_.csv
```

### 3. รัน Dashboard
```bash
streamlit run investment_dashboard.py
```

### 4. เปิดใน Browser
Browser จะเปิดอัตโนมัติที่ `http://localhost:8501`

---

## Features
- 🎛️ **Sidebar Filter**: กรองตาม Plant / Status / Budget Type
- 📊 **KPI Cards**: Total Projects, Total Budget, Budget Used, Available
- 🏭 **Plant Summary**: จำนวนโครงการและงบแต่ละโรงงาน  
- 📈 **Bar Chart**: เปรียบเทียบงบและใช้จ่ายตาม Plant
- 🍩 **Donut Chart**: สัดส่วน Budget Type และ Location
- 📉 **Status Bar**: จำนวนโครงการตามสถานะ
- ⚡ **Progress Bars**: ความก้าวหน้าแต่ละโครงการ
- 📋 **Detail Table**: ตารางรายละเอียดโครงการทั้งหมด

## Tech Stack
- Python + Streamlit
- Plotly (Interactive Charts)
- Pandas (Data Processing)
