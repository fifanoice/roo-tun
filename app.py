import streamlit as st
import datetime

# 1. Page Configuration & Custom Styling
st.set_page_config(page_title="RooTun | AI Compliance", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .reportview-container .main .block-container { max-width: 1200px; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    hr { margin-top: 0.5em; margin-bottom: 0.5em; }
</style>
""", unsafe_allow_html=True)

# 2. State Management for Demo (Keeps track of simulated time)
if 'sim_days' not in st.session_state:
    st.session_state.sim_days = 0

BUSINESS_PROFILE = {
    "name": "เชียงใหม่ คอฟฟี่สเปซ",
    "type": "คาเฟ่ / ร้านอาหาร",
    "start_date": datetime.date(2026, 1, 1),
    "monthly_revenue": 220000,
    "employees": 5
}

base_date = datetime.date(2026, 10, 6)
current_date = base_date + datetime.timedelta(days=st.session_state.sim_days)

# 3. Core Logic
months_active = (current_date.year - BUSINESS_PROFILE["start_date"].year) * 12 + (current_date.month - BUSINESS_PROFILE["start_date"].month) + 1
total_revenue = BUSINESS_PROFILE["monthly_revenue"] * months_active
threshold = 1800000
is_over_vat = total_revenue >= threshold
time_left_days = int((threshold / BUSINESS_PROFILE["monthly_revenue"]) * 30.44) - (current_date - BUSINESS_PROFILE["start_date"]).days

# 4. Sidebar Navigation
with st.sidebar:
    st.title("🛡️ RooTun")
    st.caption("AI Compliance Concierge")
    st.markdown("___")
    
    page = st.radio("MAIN MENU", ["📊 Dashboard", "📝 License Planner", "⚙️ Demo Settings"])
    
    st.markdown("___")
    st.caption("BUSINESS PROFILE")
    st.write(f"🏢 **{BUSINESS_PROFILE['name']}**")
    st.write(f"👥 พนักงาน: {BUSINESS_PROFILE['employees']} คน")
    st.write(f"📅 วันที่ระบบ: {current_date.strftime('%d %b %Y')}")

# 5. Dashboard Page
if page == "📊 Dashboard":
    st.title("Overview Dashboard")
    st.markdown("ภาพรวมสถานะภาษีและข้อกําหนดทางกฎหมายของร้านคุณ")
    
    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="ยอดขายสะสมปีนี้ (YTD)", value=f"฿{total_revenue:,.0f}", delta=f"+฿{BUSINESS_PROFILE['monthly_revenue']:,.0f} เดือนนี้")
    with col2:
        if is_over_vat:
            st.metric(label="สถานะ VAT", value="เกินเกณฑ์ 1.8M", delta="- ต้องดำเนินการทันที", delta_color="inverse")
        else:
            st.metric(label="สถานะ VAT", value="ปลอดภัย", delta=f"คาดว่าจะถึงเกณฑ์ใน {max(0, time_left_days)} วัน", delta_color="normal")
    with col3:
        st.metric(label="เอกสารรอดำเนินการ", value="1 รายการ", delta="หัก ณ ที่จ่าย", delta_color="off")

    st.markdown("___")
    
    # Main Dashboard Area
    main_col1, main_col2 = st.columns([1.5, 1])
    
    with main_col1:
        st.subheader("📡 VAT Radar")
        st.progress(min(total_revenue / threshold, 1.0))
        
        if is_over_vat:
            st.error("🚨 **ยอดขายเกิน 1.8 ล้านบาทแล้ว!**\n\nระบบคำนวณว่าคุณอาจโดนค่าปรับสูงสุด 572,000 บาท หากไม่จดทะเบียน ภ.พ.01 ภายใน 30 วัน")
            st.button("📄 สร้างฟอร์ม ภ.พ.01 อัตโนมัติ", type="primary")
        elif time_left_days <= 45:
            st.warning(f"⚠️ **ใกล้ถึงเกณฑ์ VAT (อีกประมาณ {time_left_days} วัน)**\n\nเตรียมเอกสารจดทะเบียน ภ.พ.01 ล่วงหน้าเพื่อหลีกเลี่ยงเบี้ยปรับ")
            st.button("เตรียมเอกสารล่วงหน้า", type="secondary")
        else:
            st.success("✅ **สถานะยอดขายปลอดภัย** ยังไม่ต้องดำเนินการเกี่ยวกับภาษีมูลค่าเพิ่ม")

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("🔔 Regulation Watch")
        if current_date >= datetime.date(2026, 12, 1):
            st.error("**ประกาศใหม่: ปรับเพดานเงินสมทบประกันสังคม (มีผล 1 ม.ค. 2569)**")
            st.markdown("""
            - **ผลกระทบต่อร้านคุณ:** พนักงาน 2 คนได้รับผลกระทบ
            - **ต้นทุนนายจ้างเพิ่ม:** 2,100 บาท/ปี
            """)
            st.button("อัปเดตระบบ Payroll อัตโนมัติ")
        else:
            st.info("ไม่มีประกาศกฎหมายใหม่ที่ส่งผลกระทบต่อร้านของคุณในสัปดาห์นี้")

    with main_col2:
        st.subheader("📥 Action Inbox")
        with st.expander("🚨 พบรายการต้องสงสัย (ธนาคาร)", expanded=True):
            st.write("**โอน 15,000 ให้ นายเอ (ค่าออกแบบโลโก้)**")
            st.caption("AI วิเคราะห์: เข้าข่าย 'ค่าจ้างทำของ' ต้องหักภาษี ณ ที่จ่าย 3% (ภ.ง.ด.3)")
            
            confirm = st.radio("ยืนยันรายการนี้?", ["รอตรวจสอบ", "ใช่ (สร้าง 50 ทวิ)", "ไม่ใช่ (เพิกเฉย)"])
            if confirm == "ใช่ (สร้าง 50 ทวิ)":
                st.success("✅ บันทึกลงปฏิทิน: นำส่ง 450 บาท (15 พ.ย.)")

# 6. License Planner Page
elif page == "📝 License Planner":
    st.title("License Planner")
    st.markdown("ระบบวิเคราะห์และเตรียมใบอนุญาตสำหรับสาขาใหม่")
    
    prompt = st.text_area("อธิบายรูปแบบร้านของคุณ", "เปิดคาเฟ่ 60 ตร.ม. ที่เชียงใหม่ จ้าง 5 คน ขายออนไลน์ มีป้ายหน้าร้าน")
    
    if st.button("ประมวลผลด้วย AI", type="primary"):
        with st.spinner("กำลังเทียบเคียงกฎหมายเทศบาลและข้อบังคับ..."):
            st.success("พบใบอนุญาตที่ต้องใช้ 4 รายการ")
            
            st.markdown("### แผนการดำเนินการ (Roadmap)")
            st.checkbox("1. จดทะเบียนพาณิชย์ (อิเล็กทรอนิกส์) - สำหรับการขายออนไลน์")
            st.checkbox("2. หนังสือรับรองสถานที่จำหน่ายอาหาร - พื้นที่ 60 ตร.ม.")
            st.checkbox("3. ยื่นแบบแสดงรายการภาษีป้าย - สำหรับป้ายหน้าร้าน")
            st.checkbox("4. ขึ้นทะเบียนนายจ้าง สปส. 1-01 - สำหรับพนักงาน 5 คน")
            
            st.button("📥 ดาวน์โหลดชุดแบบฟอร์ม (ZIP)")

# 7. Hidden Demo Settings Page
elif page == "⚙️ Demo Settings":
    st.title("Simulation & Time Travel")
    st.write("ใช้หน้านี้เพื่อจำลองเวลาเดินหน้าสำหรับการพรีเซนต์ (แสดงให้กรรมการเห็นความสามารถเชิงรุก)")
    
    sim_val = st.slider("จำลองเวลาเดินหน้า (วัน)", 0, 90, st.session_state.sim_days)
    if st.button("อัปเดตเวลาจำลอง", type="primary"):
        st.session_state.sim_days = sim_val
        st.rerun()
        
    st.info("""
    **คำแนะนำสำหรับการถ่ายวิดีโอ Demo:**
    1. เริ่มต้นที่ **0 วัน** (ดูหน้า Dashboard ว่าทุกอย่างสีเขียว ปลอดภัย)
    2. กลับมาหน้านี้ เลื่อนไปที่ **40 วัน** (Dashboard จะขึ้นเตือนสีเหลือง/แดง เรื่องยอดขายถึงเกณฑ์ VAT)
    3. เลื่อนไปที่ **60 วัน** (Dashboard จะจับประกาศประกันสังคมใหม่ได้)
    """)