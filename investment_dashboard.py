import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io, os, base64
from datetime import datetime
from PIL import Image

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "Investment_Budget_69_Sheet1_.csv")
XLSX_PATH = os.path.join(BASE_DIR, "Investment_Budget_69.xlsx")
IMG_DIR   = os.path.join(BASE_DIR, "images")

# ── SharePoint direct download URL ────────────────────────────────────────
# ใส่ share link จาก SharePoint แล้วเพิ่ม &download=1 ต่อท้าย
SHAREPOINT_DOWNLOAD_URL = (
    "https://mitrphol-my.sharepoint.com/:x:/p/waiyawatc/"
    "IQAjrD_34hOFT5LKvhtSn20ZAS08aHabYXfoyswp7nyuXTE?e=O5kZJG&download=1"
)
# ────────────────────────────────────────────────────────────────────────────
os.makedirs(IMG_DIR, exist_ok=True)

st.set_page_config(page_title="Investment Budget 2569 | MITR PHOL", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&family=IBM+Plex+Sans+Thai:wght@400;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Sarabun', 'IBM Plex Sans Thai', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="collapsedControl"] { display: none !important; }
.stApp { background: #f5f6fa; }
section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
section[data-testid="stSidebar"] * { color: #334155 !important; }
section[data-testid="stSidebar"] label { font-size:12px !important; font-weight:600 !important; color:#64748b !important; text-transform:uppercase; letter-spacing:0.5px; }
.page-header { background: linear-gradient(135deg,#1e3a8a,#2563eb); border-radius:16px; padding:22px 32px; display:flex; align-items:center; justify-content:space-between; margin-bottom:24px; box-shadow:0 4px 20px rgba(29,78,216,0.25); }
.page-header .title { font-size:24px; font-weight:700; color:#fff; letter-spacing:1px; }
.page-header .sub   { font-size:13px; color:rgba(255,255,255,0.75); margin-top:3px; }
.page-header .badge { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); border-radius:10px; padding:10px 20px; text-align:right; }
.page-header .badge .lbl { font-size:10px; color:rgba(255,255,255,0.6); letter-spacing:2px; }
.page-header .badge .val { font-size:18px; font-weight:700; color:#fff; }
.kpi-card { background:#fff; border-radius:14px; padding:20px 22px; border-left:4px solid var(--accent); box-shadow:0 1px 8px rgba(0,0,0,0.06); }
.kpi-card .lbl { font-size:11px; color:#94a3b8; font-weight:600; letter-spacing:1px; text-transform:uppercase; }
.kpi-card .val { font-size:26px; font-weight:700; color:#1e293b; margin:6px 0 2px; }
.kpi-card .sub { font-size:11px; color:#64748b; }
.plant-card { background:#fff; border-radius:12px; padding:16px; text-align:center; border:1px solid #e2e8f0; box-shadow:0 1px 4px rgba(0,0,0,0.04); }
.plant-card .pname { font-size:11px; color:#64748b; font-weight:600; letter-spacing:0.5px; }
.plant-card .pcount { font-size:32px; font-weight:700; margin:4px 0; }
.plant-card .pbudget { font-size:11px; color:#94a3b8; }
.sec-hdr { font-size:13px; font-weight:700; color:#475569; letter-spacing:1.5px; text-transform:uppercase; padding-bottom:8px; border-bottom:2px solid #e2e8f0; margin-bottom:14px; }
.chart-box { background:#fff; border-radius:14px; padding:18px 16px; box-shadow:0 1px 8px rgba(0,0,0,0.06); margin-bottom:16px; }
.pb-wrap { margin-bottom:10px; }
.pb-meta { display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px; }
.pb-name { color:#334155; font-weight:500; }
.pb-pct  { font-weight:700; }
.pb-track { height:9px; background:#f1f5f9; border-radius:5px; overflow:hidden; }
.pb-fill  { height:100%; border-radius:5px; }
.detail-header { background:linear-gradient(135deg,#1e3a8a,#2563eb); border-radius:16px; padding:24px 32px; margin-bottom:24px; color:#fff; box-shadow:0 4px 20px rgba(29,78,216,0.2); }
.detail-header .proj-id { font-size:12px; color:rgba(255,255,255,0.6); letter-spacing:2px; }
.detail-header .proj-name { font-size:22px; font-weight:700; margin:6px 0; }
.info-card { background:#fff; border-radius:14px; padding:20px; box-shadow:0 1px 8px rgba(0,0,0,0.06); height:100%; }
.info-card .card-title { font-size:11px; color:#94a3b8; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px; }
.info-card .card-body  { font-size:14px; color:#334155; line-height:1.7; }
.stat-badge { display:inline-block; padding:5px 14px; border-radius:20px; font-size:12px; font-weight:700; }
.s-completed { background:#dcfce7; color:#16a34a; }
.s-prpo      { background:#dbeafe; color:#1d4ed8; }
.s-onprocess { background:#fef9c3; color:#ca8a04; }
.s-boq       { background:#f3e8ff; color:#7c3aed; }
.s-na        { background:#f1f5f9; color:#94a3b8; }
.stButton > button { background:#1d4ed8 !important; color:#fff !important; border:none !important; border-radius:8px !important; padding:8px 20px !important; font-weight:600 !important; font-size:13px !important; }
.stButton > button:hover { background:#1e40af !important; }
.upload-box { border:2px dashed #cbd5e1; border-radius:12px; padding:24px; text-align:center; color:#94a3b8; font-size:13px; }
div[data-testid="stFileUploader"] > label[data-testid="stWidgetLabel"] { display:none !important; height:0 !important; margin:0 !important; padding:0 !important; }
div[data-testid="stFileUploaderDropzone"] { margin-top:0 !important; }
.proj-table { width:100%; border-collapse:collapse; font-family:'Sarabun',sans-serif; font-size:13px; }
.proj-table thead tr { background:#f8fafc; border-bottom:2px solid #e2e8f0; position:sticky; top:0; z-index:10; }
.proj-table thead th { padding:10px 12px; text-align:left; font-size:11px; font-weight:700; color:#64748b; letter-spacing:0.8px; text-transform:uppercase; white-space:nowrap; }
.proj-table tbody tr { border-bottom:1px solid #f1f5f9; transition:background 0.15s; cursor:pointer; }
.proj-table tbody tr:hover { background:#eff6ff !important; }
.proj-table tbody td { padding:9px 12px; color:#334155; vertical-align:middle; }
.proj-table td.num { text-align:right; font-variant-numeric:tabular-nums; }
.proj-table td.ctr { text-align:center; }
.proj-table .badge { display:inline-block; padding:2px 9px; border-radius:10px; font-size:11px; font-weight:700; white-space:nowrap; }
.proj-table .pct-bar { display:flex; align-items:center; gap:6px; }
.proj-table .pct-track { flex:1; height:6px; background:#f1f5f9; border-radius:3px; overflow:hidden; min-width:48px; }
.proj-table .pct-fill { height:100%; border-radius:3px; }
.proj-table-wrap { background:#fff; border-radius:14px; overflow:hidden; box-shadow:0 1px 8px rgba(0,0,0,0.06); margin-bottom:8px; }
.proj-table-scroll { overflow-x:auto; max-height:460px; overflow-y:auto; }
/* Chart cards — ครอบ Plotly ให้มีกรอบ */
div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border-radius: 14px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    padding: 4px 0 0 0;
    overflow: hidden;
}

/* Lightbox */
.lb-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center; cursor:zoom-out; }
.lb-overlay.active { display:flex; }
</style>
""", unsafe_allow_html=True)

TYPE_MAP = {
    "????????????????????????????": "งบลงทุน (Investment Budget)",
    "?????????????":                "ซ่อมบำรุง (Maintenance)",
    "?????????????????":            "ความปลอดภัย/SHE (Safety)",
}
PROJECT_NAME_MAP = {
    "??????? Auto-titration":"เครื่อง Auto-titration",
    "??????????????????????????????????":"ปรับปรุงระบบท่อ HDPE",
    "????????????????????????????????????????????????????????????":"ปรับปรุงระบบ Compressed Air",
    "???????????????????????? Thermoscan":"กล้อง Thermoscan",
    "??????? Laminar Flow (?????????)":"ตู้ Laminar Flow (ห้องแลป)",
    "?????????????????":"SHE Building",
    "????????????????????????????????????????????":"ระบบบำบัดน้ำเสีย EIA",
    "???????????????????????????? CIP , ????? CIP":"เครื่องล้างถัง CIP, ปั๊ม CIP",
    "????????????????????????":"หม้อแปลงไฟฟ้า",
    "?????????????????? 11 KV ???? 250 KVA ?????????????????????????????????":"หม้อแปลง 11 KV ขนาด 250 KVA (สำรอง)",
    "???????????????????????? (32 ????)":"ลู่วิ่ง (32 เส้น)",
    "Air Dryer (?????????)":"Air Dryer (โรงงาน)",
    "????????????? Thermoscan":"กล้อง Thermoscan (PK)",
    "?????????????????????? Hydraulic":"ปั๊มน้ำมัน Hydraulic",
    "???????????? 1 ???":"เลื่อย 1 ใบ",
    "??????????????????? SHE ????????????":"อาคาร SHE Building",
    "?????????????????? Auto Sprinkler ??????????????????????????":"ติดตั้ง Auto Sprinkler ถังเอทานอล",
    "??????????????????????????????????????????????":"ปรับปรุงระบบดับเพลิงอัตโนมัติ",
    "???????????????????????? Bund Wall ??????????????????":"ก่อสร้าง Bund Wall รอบถังเก็บ",
    "????????????????????????????????????(AI)":"ระบบตรวจจับการรั่วซึม (AI)",
    "???????????????????????????????????????????":"เครื่องวัดอัตราการไหลของน้ำ",
    "??????????????????????????????????????? 2":"ปรับปรุงระบบระบายน้ำ 2",
    "????????????????????????????? 2 (????????HR)":"ปรับปรุงระบบ 2 (แผนก HR)",
    "??????? pH Meter & Electrode for Ethanol samples":"เครื่อง pH Meter & Electrode",
    "??????? Inverter Boiler Feed Pump (BFP) 300 kW":"ติดตั้ง Inverter Boiler Feed Pump 300 kW",
}
OBJECTIVE_MAP = {
    "??????? Auto-titration":"เพิ่มความแม่นยำในการวิเคราะห์ตัวอย่าง ลดเวลาทดสอบ และลดการใช้สารเคมีในห้องปฏิบัติการ",
    "Automatic Sprinkler System":"ติดตั้งระบบดับเพลิงอัตโนมัติครอบคลุมพื้นที่โรงงาน เพื่อความปลอดภัยตามมาตรฐาน NFPA",
    "Vibration Sensor Monitoring":"ติดตั้งเซ็นเซอร์ตรวจจับการสั่นสะเทือนของเครื่องจักร เพื่อวิเคราะห์สภาพด้วย AI",
    "STAAD.Pro Software License":"ซอฟต์แวร์วิเคราะห์โครงสร้างทางวิศวกรรมสำหรับทีมออกแบบ",
    "Biogas Flare":"ติดตั้งระบบเผาก๊าซ Biogas ส่วนเกิน เพื่อความปลอดภัยและลดผลกระทบสิ่งแวดล้อม",
    "Multifunction Calibrator":"สอบเทียบเครื่องมือวัดทุกประเภทภายในโรงงาน ลดการ Outsource",
    "Breather Valve (PSV411 & PSV412)":"วาล์วระบายความดันสำหรับถังเก็บสารเคมี ป้องกันแรงดันเกิน",
}
BENEFIT_MAP = {
    "??????? Auto-titration":"ลดเวลาวิเคราะห์ลง 60% · ลด %Error เหลือ < 0.5% · ประหยัดสารเคมี 200,660 บ./ปี",
    "Automatic Sprinkler System":"เพิ่มความปลอดภัย ป้องกันการสูญเสียจากอัคคีภัย ผ่านมาตรฐาน NFPA",
    "Vibration Sensor Monitoring":"เปลี่ยนจาก Reactive Maintenance เป็น Predictive Maintenance ลด Downtime",
    "STAAD.Pro Software License":"เพิ่มประสิทธิภาพงานวิศวกรรม IRR 64% / NPV 1.28 MB / PB 2 ปี",
    "Biogas Flare":"ลดความเสี่ยงการระเบิด ลด GHG Emission ผ่านมาตรฐานสิ่งแวดล้อม",
    "Multifunction Calibrator":"ลดค่าใช้จ่าย Outsource Calibration · รองรับการสอบเทียบครบทุกประเภท",
}

def to_thai_name(raw):
    if pd.isna(raw): return "-"
    return PROJECT_NAME_MAP.get(str(raw).strip(), str(raw).strip())

def to_thai_type(raw):
    if pd.isna(raw): return "อื่นๆ"
    return TYPE_MAP.get(str(raw).strip(), str(raw).strip())

def get_objective(row):
    en = str(row.get('Project_Name','')).strip()
    raw = str(row.get('Objective','')).strip()
    if en in OBJECTIVE_MAP: return OBJECTIVE_MAP[en]
    if raw and raw != 'nan' and not raw.startswith('?'): return raw
    return "ข้อมูลวัตถุประสงค์ — กรุณาเพิ่มใน OBJECTIVE_MAP"

def get_benefit(row):
    en = str(row.get('Project_Name','')).strip()
    raw = str(row.get('Benefit','')).strip()
    irr = str(row.get('%IRR/NPV/PB','')).strip()
    if en in BENEFIT_MAP: txt = BENEFIT_MAP[en]
    elif raw and raw != 'nan' and not raw.startswith('?'): txt = raw
    else: txt = "ข้อมูลผลประโยชน์ — กรุณาเพิ่มใน BENEFIT_MAP"
    if irr and irr != 'nan' and not irr.startswith('?'): txt += f"\n📊 IRR/NPV/PB: {irr}"
    return txt

@st.cache_data(ttl=300)  # refresh ทุก 5 นาที
def load_data():
    import requests as _req
    df = None

    # ── 1. ดึงจาก SharePoint direct URL ──────────────────────────────────────
    try:
        r = _req.get(SHAREPOINT_DOWNLOAD_URL, timeout=15, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 5000:
            df = pd.read_excel(io.BytesIO(r.content), sheet_name=0)
        else:
            raise Exception(f"status {r.status_code}")
    except Exception:
        pass

    # ── 2. Fallback: local xlsx หรือ csv ─────────────────────────────────────
    if df is None:
        if os.path.exists(XLSX_PATH):
            df = pd.read_excel(XLSX_PATH, sheet_name=0)
        else:
            with open(CSV_PATH, "rb") as f:
                raw = f.read().replace(b'\xa0', b' ')
            df = pd.read_csv(io.BytesIO(raw), encoding='cp874', on_bad_lines='skip')
    df = df[df['Plant'].notna() & df['No.'].notna()].copy()
    df = df[~df['No.'].astype(str).str.contains('Total', na=True)]
    for col in ['Total_Budget','Budget_Used','Available_Budget']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',','').str.strip(), errors='coerce')
    df['Progress_%'] = pd.to_numeric(df['Progress_%'], errors='coerce')
    df['No.'] = pd.to_numeric(df['No.'], errors='coerce')
    df = df.dropna(subset=['No.'])
    df['No.'] = df['No.'].astype(int)
    df['Status'] = df['Status'].fillna('N/A').str.strip()
    # ชื่อโครงการ — ถ้า xlsx มี Thai text ตรงให้ใช้เลย ไม่ต้อง map
    if 'Project_Name' in df.columns:
        df['ชื่อโครงการ'] = df['Project_Name'].apply(
            lambda x: x if (pd.notna(x) and not str(x).startswith('?')) else to_thai_name(x)
        )
    if 'Type_Project' in df.columns:
        df['ประเภทงบ'] = df['Type_Project'].apply(
            lambda x: x if (pd.notna(x) and not str(x).startswith('?')) else to_thai_type(x)
        )
    return df

df_all = load_data()

if 'page' not in st.session_state:        st.session_state.page = 'dashboard'
if 'selected_no' not in st.session_state: st.session_state.selected_no = None

PLANT_COLOR  = {'DC':'#3b82f6','KN':'#10b981','KS':'#f59e0b','PK':'#8b5cf6','MCE':'#ef4444'}
STATUS_COLOR = {'Completed':'#16a34a','PR/PO':'#1d4ed8','On Process':'#ca8a04','BOQ':'#7c3aed','N/A':'#94a3b8'}
STATUS_CSS   = {'Completed':'s-completed','PR/PO':'s-prpo','On Process':'s-onprocess','BOQ':'s-boq','N/A':'s-na'}
TYPE_COLOR   = {
    'งบลงทุน (Investment Budget)': '#ef4444',
    'งบลงทุนทั่วไป':              '#ef4444',
    'ซ่อมบำรุง (Maintenance)':    '#3b82f6',
    'งบสิ่งแวดล้อม':              '#10b981',
    'ความปลอดภัย/SHE (Safety)':  '#f59e0b',
    'งบด้านความปลอดภัย':         '#f59e0b',
    'งบปรับปรุงประสิทธิภาพการผลิต': '#8b5cf6',
    'อื่นๆ':                      '#94a3b8',
}
PLANT_FULL   = {'DC':'MPBF DC','KN':'MPBF KN','KS':'MPBF KS','PK':'MPBF PK','MCE':'MCE'}

def fmt(v, style='M'):
    if pd.isna(v): return "-"
    if style == 'M': return f"฿{v/1e6:.2f}M"
    return f"฿{v:,.2f}"

PLOT_CFG = dict(
    paper_bgcolor='#ffffff', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Sarabun', color='#334155', size=11),
    margin=dict(l=16, r=16, t=56, b=16))

# ══════════════════════════════════════════════════════════════════════════════
def page_detail():
    row = df_all[df_all['No.'] == st.session_state.selected_no].iloc[0]
    if st.button("← กลับหน้าหลัก"):
        st.session_state.page = 'dashboard'; st.rerun()

    sc = STATUS_CSS.get(row['Status'], 's-na')
    pc = PLANT_COLOR.get(row['Plant'], '#3b82f6')
    st.markdown(f"""
    <div class="detail-header">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
        <div>
          <div class="proj-id">PROJECT #{int(row['No.']):02d} · {PLANT_FULL.get(row['Plant'], row['Plant'])}</div>
          <div class="proj-name">{to_thai_name(row['Project_Name'])}</div>
          <span style="background:rgba(255,255,255,0.2);border-radius:6px;padding:3px 12px;font-size:12px;">{row['ประเภทงบ']}</span>
        </div>
        <span class="stat-badge {sc}" style="font-size:14px;padding:8px 24px;align-self:center;">{row['Status']}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    for col, (lbl, v, acc) in zip(st.columns(4),
        [("งบทั้งหมด",row['Total_Budget'],"#1d4ed8"),("ใช้ไปแล้ว",row['Budget_Used'],"#10b981"),
         ("คงเหลือ",row['Available_Budget'],"#f59e0b"),("ความก้าวหน้า",None,pc)]):
        with col:
            base = f'background:#fff;border-radius:14px;padding:20px 22px;border-left:4px solid {acc};box-shadow:0 1px 8px rgba(0,0,0,0.06);'
            lbl_s = f'font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:1px;text-transform:uppercase;'
            if lbl == "ความก้าวหน้า":
                pct = row['Progress_%'] if pd.notna(row['Progress_%']) else 0
                st.markdown(
                    f'<div style="{base}">'
                    f'<div style="{lbl_s}">{lbl}</div>'
                    f'<div style="font-size:26px;font-weight:700;color:#1e293b;margin:6px 0 6px;">{pct:.0f}%</div>'
                    f'<div style="height:10px;background:#f1f5f9;border-radius:5px;overflow:hidden;">'
                    f'<div style="width:{min(pct,100):.1f}%;height:100%;background:{acc};border-radius:5px;"></div></div>'
                    f'</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="{base}">'
                    f'<div style="{lbl_s}">{lbl}</div>'
                    f'<div style="font-size:26px;font-weight:700;color:#1e293b;margin:6px 0 2px;">{fmt(v)}</div>'
                    f'<div style="font-size:11px;color:#64748b;">{fmt(v,"full")}</div>'
                    f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    ic1, ic2 = st.columns(2)
    with ic1:
        st.markdown(f'<div class="info-card"><div class="card-title">🎯 วัตถุประสงค์ (Objective)</div><div class="card-body">{get_objective(row)}</div></div>', unsafe_allow_html=True)
    with ic2:
        st.markdown(f'<div class="info-card"><div class="card-title">💡 ประโยชน์ที่ได้รับ (Benefit)</div><div class="card-body">{get_benefit(row).replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    md1, md2, md3 = st.columns(3)
    remark  = str(row.get('Remark','') or '').strip(); remark  = "-" if remark  in ('nan','') or remark.startswith('?')  else remark
    update  = str(row.get('Update_Date','') or '').strip(); update  = "-" if update  == 'nan' else update
    irr_val = str(row.get('%IRR/NPV/PB','') or '').strip(); irr_val = "-" if irr_val in ('nan','') or irr_val.startswith('?') else irr_val
    with md1: st.markdown(f'<div class="info-card"><div class="card-title">📝 หมายเหตุ</div><div class="card-body">{remark}</div></div>', unsafe_allow_html=True)
    with md2: st.markdown(f'<div class="info-card"><div class="card-title">📅 วันที่อัปเดต</div><div class="card-body" style="font-size:20px;font-weight:700;color:#1d4ed8;">{update}</div></div>', unsafe_allow_html=True)
    with md3: st.markdown(f'<div class="info-card"><div class="card-title">📈 IRR / NPV / Payback</div><div class="card-body" style="font-weight:700;color:#10b981;">{irr_val}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📷 รูปภาพโครงการ</div>', unsafe_allow_html=True)

    proj_no = int(row['No.'])
    saved = [os.path.join(IMG_DIR, f"{proj_no}{sfx}.{ext}")
             for ext in ['jpg','jpeg','png','webp']
             for sfx in ['','_1','_2','_3']
             if os.path.exists(os.path.join(IMG_DIR, f"{proj_no}{sfx}.{ext}"))]

    if saved:
        imgs_html = ""
        modals_html = ""
        for i, path in enumerate(saved[:3]):
            try:
                with open(path, "rb") as fh:
                    b64 = base64.b64encode(fh.read()).decode()
                ext_img = path.rsplit('.',1)[-1].lower()
                mime = "image/jpeg" if ext_img in ('jpg','jpeg') else f"image/{ext_img}"
                fname = os.path.basename(path)
                mid = f"lb_{proj_no}_{i}"
                src = f"data:{mime};base64,{b64}"
                # thumbnail — ขนาด 220px contain
                imgs_html += (
                    f'<div onclick="document.getElementById(\'{mid}\').style.display=\'flex\'"'
                    f' style="flex:1;min-width:0;background:#f8fafc;border-radius:12px;overflow:hidden;'
                    f'border:1px solid #e2e8f0;cursor:zoom-in;transition:box-shadow .15s;"'
                    f' onmouseover="this.style.boxShadow=\'0 4px 16px rgba(0,0,0,0.15)\'"'
                    f' onmouseout="this.style.boxShadow=\'none\'">'
                    f'<img src="{src}" style="width:100%;height:200px;object-fit:contain;'
                    f'background:#f1f5f9;display:block;">'
                    f'<div style="padding:5px 10px;font-size:11px;color:#94a3b8;'
                    f'border-top:1px solid #e2e8f0;">🔍 {fname}</div></div>'
                )
                # lightbox modal
                modals_html += (
                    f'<div id="{mid}" onclick="this.style.display=\'none\'"'
                    f' style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;'
                    f'background:rgba(0,0,0,0.88);z-index:9999;align-items:center;'
                    f'justify-content:center;cursor:zoom-out;">'
                    f'<div onclick="event.stopPropagation()" style="position:relative;'
                    f'max-width:88vw;max-height:88vh;">'
                    f'<img src="{src}" style="max-width:88vw;max-height:82vh;'
                    f'object-fit:contain;border-radius:10px;display:block;">'
                    f'<div style="position:absolute;top:-32px;left:0;color:rgba(255,255,255,0.7);font-size:12px;">{fname}</div>'
                    f'<div onclick="document.getElementById(\'{mid}\').style.display=\'none\'"'
                    f' style="position:absolute;top:-36px;right:0;color:#fff;font-size:26px;'
                    f'cursor:pointer;line-height:1;">✕</div></div></div>'
                )
            except Exception:
                pass
        if imgs_html:
            n = min(len(saved), 3)
            max_w = {1:"400px", 2:"660px", 3:"100%"}.get(n, "100%")
            st.markdown(
                f'<div style="display:flex;gap:12px;max-width:{max_w};margin-bottom:6px;">{imgs_html}</div>'
                f'<div style="font-size:11px;color:#94a3b8;margin-bottom:12px;">💡 คลิกรูปเพื่อดูเต็มจอ</div>'
                f'{modals_html}',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="upload-box">📷 ยังไม่มีรูปภาพสำหรับโครงการนี้</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:12px;padding:10px 14px;background:#f8fafc;border-radius:10px;border:1px solid #e2e8f0;font-size:12px;color:#64748b;">📎 <strong>อัปโหลดรูปภาพ</strong> — สูงสุด 3 รูป (JPG, PNG, JPEG)</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("x", type=["jpg","jpeg","png"], accept_multiple_files=True, key=f"up_{proj_no}", label_visibility="collapsed")
    if uploaded:
        for idx, f in enumerate(uploaded[:3]):
            ext = f.name.rsplit('.',1)[-1].lower(); sfx = '' if idx==0 else f'_{idx}'
            with open(os.path.join(IMG_DIR, f"{proj_no}{sfx}.{ext}"), 'wb') as out: out.write(f.read())
        st.success(f"✅ บันทึก {min(len(uploaded),3)} รูปภาพแล้ว"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    # ── Header + Filters รวมกัน ───────────────────────────────────────────────
    plants   = sorted(df_all['Plant'].dropna().unique().tolist())
    statuses = sorted(df_all['Status'].dropna().unique().tolist())
    types    = sorted(df_all['ประเภทงบ'].dropna().unique().tolist())

    if 'sel_plants' not in st.session_state:  st.session_state['sel_plants'] = plants[:]
    if 'sel_status' not in st.session_state:  st.session_state['sel_status'] = statuses[:]
    if 'sel_types'  not in st.session_state:  st.session_state['sel_types']  = types[:]

    # CSS popover button
    st.markdown("""<style>
    div[data-testid="stPopover"] > div > button {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        border-radius: 8px !important; color: #fff !important;
        font-size: 13px !important; font-weight: 600 !important;
        padding: 6px 16px !important; box-shadow: none !important;
        text-align: center !important; justify-content: center !important;
    }
    div[data-testid="stPopover"] > div > button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    div[data-testid="stPopover"] > div > button svg,
    div[data-testid="stPopover"] > div > button span[data-testid="stIconMaterial"] {
        display: none !important;
    }
    </style>""", unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f'''
    <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);
        border-radius:16px 16px 0 0; padding:20px 28px 16px;
        box-shadow:0 2px 0 rgba(29,78,216,0.4);">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
          <div style="font-size:22px;font-weight:700;color:#fff;letter-spacing:1px;">📊 INVESTMENT BUDGET REPORT</div>
          <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:3px;">MITR PHOL BIO FUEL · ปีงบประมาณ 2569</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:10px;color:rgba(255,255,255,0.6);letter-spacing:2px;">DATE</div>
          <div style="font-size:20px;font-weight:700;color:#fff;">{datetime.today().strftime("%d %b %Y")}</div>
        </div>
      </div>
    </div>''', unsafe_allow_html=True)

    # ── Filter bar ต่อใต้ header — ใช้ CSS ให้ดูเหมือนชิ้นเดียวกัน ───────────
    st.markdown('''<style>
    /* filter bar ต่อจาก header */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPopover"]) {
        background: linear-gradient(135deg,#1e40af,#1d4ed8);
        border-radius: 0 0 16px 16px;
        padding: 10px 28px 14px !important;
        margin-top: -1px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 20px rgba(29,78,216,0.25);
    }
    </style>''', unsafe_allow_html=True)
    fc1, fc2, fc3, fsp = st.columns([1, 1, 1, 2])

    with fc1:
        n_p = len(st.session_state['sel_plants'])
        lbl_p = "🏭 Plant"
        with st.popover(lbl_p, use_container_width=True):
            st.markdown("**เลือก Plant**")
            all_p = st.checkbox("ทั้งหมด", value=(n_p==len(plants)), key="chk_all_p")
            if all_p:
                st.session_state['sel_plants'] = plants[:]
            for p in plants:
                PEMOJI = {"DC":"🔵","KN":"🟢","KS":"🟡","PK":"🟣","MCE":"🔴"}
                val = st.checkbox(f"{PEMOJI.get(p,'•')} {p}", value=(p in st.session_state['sel_plants']), key=f"chk_p_{p}")
                if val and p not in st.session_state['sel_plants']:
                    st.session_state['sel_plants'].append(p)
                elif not val and p in st.session_state['sel_plants']:
                    st.session_state['sel_plants'].remove(p)

    with fc2:
        n_s = len(st.session_state['sel_status'])
        lbl_s = "📊 Status"
        with st.popover(lbl_s, use_container_width=True):
            st.markdown("**เลือก Status**")
            SEMOJI = {"Completed":"✅","PR/PO":"🔷","On Process":"🟡","BOQ":"🔮","N/A":"⬜"}
            all_s = st.checkbox("ทั้งหมด", value=(n_s==len(statuses)), key="chk_all_s")
            if all_s:
                st.session_state['sel_status'] = statuses[:]
            for s in statuses:
                val = st.checkbox(f"{SEMOJI.get(s,'•')} {s}", value=(s in st.session_state['sel_status']), key=f"chk_s_{s}")
                if val and s not in st.session_state['sel_status']:
                    st.session_state['sel_status'].append(s)
                elif not val and s in st.session_state['sel_status']:
                    st.session_state['sel_status'].remove(s)

    with fc3:
        n_t = len(st.session_state['sel_types'])
        lbl_t = "🏷️ ประเภทงบ"
        with st.popover(lbl_t, use_container_width=True):
            st.markdown("**เลือกประเภทงบ**")
            all_t = st.checkbox("ทั้งหมด", value=(n_t==len(types)), key="chk_all_t")
            if all_t:
                st.session_state['sel_types'] = types[:]
            for t in types:
                val = st.checkbox(t, value=(t in st.session_state['sel_types']), key=f"chk_t_{t}")
                if val and t not in st.session_state['sel_types']:
                    st.session_state['sel_types'].append(t)
                elif not val and t in st.session_state['sel_types']:
                    st.session_state['sel_types'].remove(t)

    sel_plants = st.session_state['sel_plants'] or plants
    sel_status = st.session_state['sel_status'] or statuses
    sel_types  = st.session_state['sel_types']  or types

    df = df_all[df_all['Plant'].isin(sel_plants) & df_all['Status'].isin(sel_status) & df_all['ประเภทงบ'].isin(sel_types)].copy()

    total_budget = df['Total_Budget'].sum(); total_used = df['Budget_Used'].sum()
    total_avail  = df['Available_Budget'].sum()
    used_pct = (total_used/total_budget*100) if total_budget > 0 else 0
    for col, (lbl, val, sub, acc) in zip(st.columns(4),
        [("Total Projects",f"{len(df)}","โครงการทั้งหมด","#3b82f6"),
         ("Total Budget",fmt(total_budget),"งบประมาณรวม","#1d4ed8"),
         ("Budget Used",fmt(total_used),f"ใช้ไปแล้ว ({used_pct:.1f}%)","#10b981"),
         ("Available",fmt(total_avail),"คงเหลือ","#f59e0b")]):
        with col:
            st.markdown(
                f'<div style="background:#fff;border-radius:14px;padding:20px 22px;'
                f'border-left:4px solid {acc};box-shadow:0 1px 8px rgba(0,0,0,0.06);">'
                f'<div style="font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:1px;text-transform:uppercase;">{lbl}</div>'
                f'<div style="font-size:26px;font-weight:700;color:#1e293b;margin:6px 0 2px;">{val}</div>'
                f'<div style="font-size:11px;color:#64748b;">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">🏭 สรุปตาม Plant</div>', unsafe_allow_html=True)
    ps = df.groupby('Plant').agg(count=('No.','count'), budget=('Total_Budget','sum')).reset_index()
    cols_p = st.columns(len(ps)+1)
    with cols_p[0]:
        st.markdown(f'<div class="plant-card" style="border-top:3px solid #1d4ed8;"><div class="pname">TOTAL</div><div class="pcount" style="color:#1d4ed8;">{len(df)}</div><div class="pbudget">{fmt(total_budget)}</div></div>', unsafe_allow_html=True)
    for i, (_, r) in enumerate(ps.iterrows()):
        c = PLANT_COLOR.get(r['Plant'],'#94a3b8')
        with cols_p[i+1]:
            st.markdown(f'<div class="plant-card" style="border-top:3px solid {c};"><div class="pname">{PLANT_FULL.get(r["Plant"],r["Plant"])}</div><div class="pcount" style="color:{c};">{int(r["count"])}</div><div class="pbudget">{fmt(r["budget"])}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    ch1, ch2, ch3 = st.columns([1.3, 1, 1])
    with ch1:
        pb = df.groupby('Plant').agg(Total_Budget=('Total_Budget','sum'), Budget_Used=('Budget_Used','sum')).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='งบทั้งหมด', x=pb['Plant'], y=pb['Total_Budget'],
            marker=dict(color=[PLANT_COLOR.get(p,'#94a3b8') for p in pb['Plant']],
                        opacity=0.35),
            text=pb['Total_Budget'].apply(lambda x: f'{x/1e6:.1f}M'),
            textposition='outside', textfont=dict(size=11, color='#000000')))
        fig.add_trace(go.Bar(name='ใช้ไปแล้ว', x=pb['Plant'], y=pb['Budget_Used'],
            marker_color=[PLANT_COLOR.get(p,'#94a3b8') for p in pb['Plant']],
            text=pb['Budget_Used'].apply(lambda x: f'{x/1e6:.1f}M' if pd.notna(x) else ''),
            textposition='outside', textfont=dict(size=11, color='#000000')))
        max_y = max(pb['Total_Budget'].max(), pb['Budget_Used'].fillna(0).max()) * 1.3
        fig.update_layout(**PLOT_CFG,
            title=dict(text='💰 งบประมาณตาม Plant', font=dict(size=13,color='#334155')),
            height=300, barmode='group', showlegend=True,
            legend=dict(orientation='h', y=1.1, x=0),
            xaxis=dict(showgrid=False, color='#64748b'),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', color='#64748b',
                       tickformat=',.0f', range=[0, max_y]))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
    with ch2:
        tc = df.groupby('ประเภทงบ')['No.'].count().reset_index()
        fig2 = go.Figure(go.Pie(labels=tc['ประเภทงบ'], values=tc['No.'], hole=0.55, marker=dict(colors=[
                TYPE_COLOR.get(t, ['#ef4444','#3b82f6','#10b981','#f59e0b','#8b5cf6','#06b6d4','#94a3b8'][i%7])
                for i,t in enumerate(tc['ประเภทงบ'])], line=dict(color='#fff',width=2)), textfont=dict(size=10), hovertemplate='<b>%{label}</b><br>%{value} โครงการ (%{percent})<extra></extra>'))
        fig2.update_layout(**PLOT_CFG, title=dict(text="🏷️ Budget Type", font=dict(size=13,color='#334155')), height=300, legend=dict(font=dict(size=9)))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
    with ch3:
        sc = df.groupby('Status')['No.'].count().reset_index().sort_values('No.',ascending=True)
        fig3 = go.Figure(go.Bar(x=sc['No.'], y=sc['Status'], orientation='h', marker_color=[STATUS_COLOR.get(s,'#94a3b8') for s in sc['Status']], text=sc['No.'], textposition='outside', textfont=dict(size=12,color='#334155')))
        fig3.update_layout(**PLOT_CFG, title=dict(text="📊 Status", font=dict(size=13,color='#334155')), height=300, showlegend=False, xaxis=dict(showgrid=True,gridcolor='#f1f5f9',color='#64748b'), yaxis=dict(showgrid=False,color='#334155'))
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})

    pb_col, pie_col = st.columns([1.6, 1])
    with pb_col:
        prog_df = df[df['Progress_%'].notna()].sort_values('Progress_%', ascending=False)
        bars_html = ""
        for _, r in prog_df.iterrows():
            pct   = float(r['Progress_%'])
            name  = str(r['ชื่อโครงการ'])
            plant = str(r['Plant'])
            color = PLANT_COLOR.get(plant, '#3b82f6')
            if len(name) > 44: name = name[:44] + '…'
            bars_html += (
                f'<div style="margin-bottom:10px;">'
                f'<div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">'
                f'<span style="color:#334155;font-weight:500;">{name}'
                f'<span style="font-size:10px;background:{color}22;color:{color};'
                f'padding:1px 7px;border-radius:10px;margin-left:6px;">{plant}</span></span>'
                f'<span style="font-weight:700;color:{color};">{pct:.1f}%</span></div>'
                f'<div style="height:9px;background:#f1f5f9;border-radius:5px;overflow:hidden;">'
                f'<div style="width:{min(pct,100):.1f}%;height:100%;border-radius:5px;'
                f'background:linear-gradient(90deg,{color}66,{color});"></div></div></div>'
            )
        card = (
            '<div style="background:#fff;border-radius:14px;'
            'box-shadow:0 1px 8px rgba(0,0,0,0.06);'
            f'height:420px;display:flex;flex-direction:column;overflow:hidden;">'
            '<div style="font-size:13px;font-weight:700;color:#475569;'
            'padding:18px 16px 10px;flex-shrink:0;'
            'border-bottom:1px solid #f1f5f9;">📊 Progress</div>'
            f'<div style="overflow-y:auto;padding:14px 16px;flex:1;">{bars_html}</div>'
            '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)
    with pie_col:
        lb = df.groupby('Plant')['Total_Budget'].sum().reset_index()
        fig4 = go.Figure(go.Pie(
            labels=lb['Plant'], values=lb['Total_Budget'], hole=0.45,
            marker=dict(colors=[PLANT_COLOR.get(p,'#94a3b8') for p in lb['Plant']], line=dict(color='#fff',width=2)),
            textinfo='label+percent', textfont=dict(size=11),
            hovertemplate='<b>%{label}</b><br>฿%{value:,.0f}<br>%{percent}<extra></extra>'))
        fig4.update_layout(**PLOT_CFG,
            title=dict(text='🗺️ สัดส่วนงบตาม Plant', font=dict(size=13,color='#334155')),
            height=420, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar':False})


    # ── Table ─────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sec-hdr">📋 รายละเอียดโครงการ — ติ๊ก checkbox เพื่อดูรายละเอียด</div>', unsafe_allow_html=True)

    tbl = df[["No.","Plant","ประเภทงบ","ชื่อโครงการ",
              "Total_Budget","Budget_Used","Available_Budget",
              "Progress_%","Status","Update_Date"]].copy()
    tbl.insert(0, "เลือก", False)
    tbl["No."] = tbl["No."].astype(int)
    tbl["Progress_%"] = pd.to_numeric(tbl["Progress_%"], errors="coerce").fillna(0)
    tbl["Update_Date"] = tbl["Update_Date"].fillna("-")
    PEMOJI = {"DC":"🔵 DC","KN":"🟢 KN","KS":"🟡 KS","PK":"🟣 PK","MCE":"🔴 MCE"}
    SEMOJI = {"Completed":"✅ Completed","PR/PO":"🔷 PR/PO",
              "On Process":"🟡 On Process","BOQ":"🔮 BOQ","N/A":"⬜ N/A"}
    tbl["Plant"]  = tbl["Plant"].map(lambda x: PEMOJI.get(x, x))
    tbl["Status"] = tbl["Status"].map(lambda x: SEMOJI.get(x, x))

    edited = st.data_editor(
        tbl,
        use_container_width=True,
        hide_index=True,
        height=460,
        column_order=["เลือก","Plant","ประเภทงบ","ชื่อโครงการ",
                      "Total_Budget","Budget_Used","Available_Budget",
                      "Progress_%","Status","Update_Date"],
        column_config={
            "เลือก":            st.column_config.CheckboxColumn("☑", width=40, default=False),
            "No.":              None,
            "Plant":            st.column_config.TextColumn("Plant", width=90),
            "ประเภทงบ":         st.column_config.TextColumn("Type", width=190),
            "ชื่อโครงการ":      st.column_config.TextColumn("Project Name", width=290),
            "Total_Budget":     st.column_config.NumberColumn("Budget (฿)", width=115, format="฿%,.2f"),
            "Budget_Used":      st.column_config.NumberColumn("Used (฿)", width=115, format="฿%,.2f"),
            "Available_Budget": st.column_config.NumberColumn("Remain (฿)", width=115, format="฿%,.2f"),
            "Progress_%":       st.column_config.ProgressColumn("Progress", width=130, min_value=0, max_value=100, format="%.0f%%"),
            "Status":           st.column_config.TextColumn("Status", width=125),
            "Update_Date":      st.column_config.TextColumn("Updated", width=90),
        },
        disabled=["No.","Plant","ประเภทงบ","ชื่อโครงการ",
                  "Total_Budget","Budget_Used","Available_Budget",
                  "Progress_%","Status","Update_Date"]
    )

    selected = edited[edited["เลือก"] == True]
    if not selected.empty:
        no = int(selected.iloc[0]["No."])
        st.session_state.selected_no = no
        st.session_state.page = "detail"
        st.rerun()

    st.markdown('<div style="text-align:center;padding:20px 0 4px;font-size:11px;color:#94a3b8;">MITR PHOL BIO FUEL · Investment Budget Dashboard · ปีงบประมาณ 2569</div>', unsafe_allow_html=True)

if st.session_state.page == 'detail' and st.session_state.selected_no is not None:
    page_detail()
else:
    page_dashboard()