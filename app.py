import datetime
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="RooTun | AI Compliance Concierge for SMEs",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
<style>
    .main .block-container { max-width: 1200px; padding-top: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 26px; color: #1e3a8a; }
    hr { margin-top: 1rem; margin-bottom: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

if "sim_days" not in st.session_state:
    st.session_state.sim_days = 0

if "confirmed_items" not in st.session_state:
    st.session_state.confirmed_items = {}

BUSINESS_PROFILE = {
    "name": "BKK Creative Agency Co., Ltd.",
    "type": "นิติบุคคลบริการ (B2B Service / Agency)",
    "start_date": datetime.date(2026, 1, 1),
    "monthly_revenue": 220000,
    "employees": 8,
}

base_date = datetime.date(2026, 10, 6)
current_date = base_date + datetime.timedelta(days=st.session_state.sim_days)

months_active = (
    (current_date.year - BUSINESS_PROFILE["start_date"].year) * 12
    + (current_date.month - BUSINESS_PROFILE["start_date"].month)
    + 1
)

baseline_revenue = BUSINESS_PROFILE["monthly_revenue"] * months_active
extra_revenue = (st.session_state.sim_days // 7) * 45000
total_revenue = baseline_revenue + extra_revenue

VAT_THRESHOLD = 1800000
is_over_vat = total_revenue >= VAT_THRESHOLD

days_passed = (current_date - BUSINESS_PROFILE["start_date"]).days
daily_burn = total_revenue / max(1, days_passed)
if not is_over_vat and daily_burn > 0:
    days_to_threshold = int((VAT_THRESHOLD - total_revenue) / daily_burn)
    est_vat_date = current_date + datetime.timedelta(days=days_to_threshold)
else:
    days_to_threshold = 0
    est_vat_date = current_date

with st.sidebar:
    st.title("🛡️ RooTun (รู้ทัน)")
    st.caption("AI Compliance Concierge for SMEs")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "📊 Executive Dashboard",
            "📋 Corporate Setup Planner",
            "⏱️ Demo Simulation (Time Travel)",
        ],
    )

    st.markdown("---")
    st.caption("COMPANY CONTEXT")
    st.write(f"🏢 **{BUSINESS_PROFILE['name']}**")
    st.write(f"💼 ประเภท: {BUSINESS_PROFILE['type']}")
    st.write(f"👥 จำนวนพนักงาน: {BUSINESS_PROFILE['employees']} คน")
    st.write(f"📅 วันที่ระบบ: **{current_date.strftime('%d %b %Y')}**")

if page == "📊 Executive Dashboard":
    st.title("SME Compliance Dashboard")
    st.markdown(
        "ระบบเฝ้าระวังความเสี่ยงทางภาษีและภาระหน้าที่ตามกฎหมายอัตโนมัติ"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="ยอดขายสะสม YTD (เฉพาะรายรับที่ต้องคิดภาษี)",
            value=f"฿{total_revenue:,.0f}",
            delta=f"+฿{BUSINESS_PROFILE['monthly_revenue']:,.0f} เดือนนี้",
        )
    with col2:
        if is_over_vat:
            st.metric(
                label="สถานะเกณฑ์จด VAT (1.8 ล้านบาท)",
                value="🚨 เกินเกณฑ์แล้ว",
                delta="- ยื่น ภ.พ.01 ภายใน 30 วัน",
                delta_color="inverse",
            )
        else:
            st.metric(
                label="สถานะเกณฑ์จด VAT (1.8 ล้านบาท)",
                value=f"อีก ~{days_to_threshold} วัน",
                delta=f"คาดถึงเกณฑ์: {est_vat_date.strftime('%d %b %Y')}",
                delta_color="normal",
            )
    with col3:
        st.metric(
            label="ภาระภาษีหัก ณ ที่จ่าย รอยืนยัน",
            value="1 รายการ",
            delta="ค่าเช่าสำนักงาน (ภ.ง.ด.53)",
            delta_color="off",
        )

    st.markdown("---")

    dash_col1, dash_col2 = st.columns([1.6, 1])

    with dash_col1:
        st.subheader("📡 VAT Radar & Threshold Forecast")
        vat_progress = min(total_revenue / VAT_THRESHOLD, 1.0)
        st.progress(vat_progress)

        if is_over_vat:
            st.error(
                """
                **🚨 ยอดขายของคุณเกิน 1.8 ล้านบาทแล้ว!**
                * **ภาระผูกพัน:** ต้องยื่นคำขอจดทะเบียนภาษีมูลค่าเพิ่ม (ภ.พ.01) ภายใน 30 วัน
                * **ความเสี่ยงค่าปรับหากละเลย 12 เดือน:** เบี้ยปรับ 2 เท่า + เงินเพิ่ม 1.5%/เดือน $\approx$ **572,000 บาท**
                """
            )
            st.button(
                "⚡ ดึงข้อมูลบริษัทและสร้างร่าง ภ.พ.01 อัตโนมัติ",
                type="primary",
            )
        elif days_to_threshold <= 45:
            st.warning(
                f"""
                **⚠️ สัญญาณเตือน: คาดว่าจะถึงเกณฑ์ 1.8M ในวันที่ {est_vat_date.strftime('%d %b %Y')}**
                * ระบบแนะนำให้จัดเตรียมเอกสารสัญญาเช่าสำนักงาน และแผนที่ตั้งบริษัทไว้ล่วงหน้า
                """
            )
            st.button("📄 เริ่มต้นเตรียมชุดเอกสารล่วงหน้า", type="secondary")
        else:
            st.success(
                f"✅ **สถานะปลอดภัย:** อัตราการเติบโตปัจจุบันคาดว่าจะถึงเกณฑ์ประมาณวันที่ {est_vat_date.strftime('%d %b %Y')}"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("🔔 Regulation Watch (เฝ้าระวังประกาศกฎหมายใหม่)")
        if current_date >= datetime.date(2026, 12, 1):
            st.error(
                """
                **ประกาศใหม่จากราชกิจจานุเบกษา: ปรับเพดานค่าจ้างคำนวณเงินสมทบประกันสังคม (มีผล 1 ม.ค. 2569)**
                * 🗄️ **Rule Database Version:** `SSO-Rule-v2026.1` (อัปเดตเพื่อใช้กับงวดปี 2569)
                * **ผลกระทบต่อนิติบุคคล:** พนักงาน 3 ใน 8 คนมีเงินเดือนเกิน 15,000 บาท
                * **ภาระต้นทุนนายจ้างเพิ่ม:** +375 บาท/เดือน (+4,500 บาท/ปี)
                """
            )
            if st.button("✅ ปรับปรุงสูตรคำนวณ Payroll และแจ้งเตือนฝ่ายบุคคล"):
                st.toast(
                    "บันทึกเวอร์ชันกฎหมายใหม่ลงใน Rule Engine สำเร็จ", icon="✅"
                )
        else:
            st.info(
                "🟢 ไม่พบการเปลี่ยนแปลงกฎหมายหรือระเบียบราชการที่ส่งผลกระทบต่อกิจการในขณะนี้"
            )

    with dash_col2:
        st.subheader("📥 Smart Compliance Inbox")
        st.caption("AI ตรวจจับผ่านการเชื่อมต่อธนาคาร (Bank Sync) และระบบ OCR")
        
        st.file_uploader("📎 อัปโหลดรูปถ่ายใบเสร็จ / สัญญาเช่า เพื่อสกัดข้อมูล", type=["jpg", "png", "pdf"])
        st.markdown("---")
        
        with st.expander("🟢 ค่าน้ำ/ค่าไฟออฟฟิศ (AI Confidence: 98%)", expanded=False):
            st.write("รายการ: จ่ายการไฟฟ้านครหลวง 4,500 บาท")
            st.success("บันทึกเป็นค่าใช้จ่ายบริษัทอัตโนมัติ (ไม่ต้องยืนยัน)")

        with st.expander("🟡 ตรวจพบรายการเงินโอนต้องสงสัย (AI Confidence: 65%)", expanded=True):
            st.markdown("**รายการ:** โอน 50,000 บาท ให้ *บจก. สุขุมวิท พร็อพเพอร์ตี้*")
            st.markdown("**บันทึกช่วยจำ:** `INV-2026-10 Office Rent`")
            st.warning("⚠️ **AI Warning:** ข้อมูลก้ำกึ่งระหว่างค่าใช้จ่ายส่วนตัวหรือค่าเช่าบริษัท กรุณายืนยัน")
            
            choice = st.radio(
                "การจัดหมวดหมู่:",
                ["รอตรวจสอบ", "ใช่: ค่าเช่า (สร้าง ภ.ง.ด.53)", "ไม่ใช่: เงินส่วนตัว (เพิกเฉย)"],
                key="rent_confirm",
            )
            if choice == "ใช่: ค่าเช่า (สร้าง ภ.ง.ด.53)":
                st.success("✅ บันทึก: เตรียมยื่นแบบ ภ.ง.ด.53 ภายใน 15 พ.ย.")

elif page == "📋 Corporate Setup Planner":
    st.title("Corporate Setup & License Planner")
    st.markdown(
        "วางแผนการจัดตั้งและใบอนุญาตสำหรับผู้ประกอบการ SME และธุรกิจบริการ"
    )

    user_input = st.text_area(
        "อธิบายลักษณะธุรกิจของคุณโดยย่อ:",
        "เปิดบริษัทเอเจนซี่รับทำโฆษณาและการตลาด มีพนักงาน 8 คน เช่าสำนักงานในกรุงเทพฯ มีป้ายชื่อบริษัทหน้าอาคาร และรับงานทั้งในและต่างประเทศ",
        height=100,
    )

    if st.button("ประมวลผลข้อกำหนดทางกฎหมาย", type="primary"):
        with st.spinner("AI กำลังวิเคราะห์ข้อกำหนดตาม DBD, กรมสรรพากร และ สปส..."):
            st.success("ประมวลผลสำเร็จ: พบ 4 ภาระหน้าที่สำคัญที่ต้องดำเนินการ")

            st.markdown("### ขั้นตอนการปฏิบัติตามกฎหมาย (Sequential Workflow)")

            col_a, col_b = st.columns(2)
            with col_a:
                st.checkbox(
                    "1. จดทะเบียนจัดตั้งนิติบุคคล (กรมพัฒนาธุรกิจการค้า DBD)",
                    value=True,
                )
                st.caption("เอกสาร: บอจ.1, บอจ.5, หนังสือบริคณห์สนธิ")

                st.checkbox(
                    "2. ขอเลขประจำตัวผู้เสียภาษีอากรและเปิดบัญชีนิติบุคคล",
                    value=True,
                )
                st.caption("หน่วยงาน: กรมสรรพากร / ธนาคารพาณิชย์")

            with col_b:
                st.checkbox(
                    "3. ขึ้นทะเบียนนายจ้างและลูกจ้าง (แบบ สปส. 1-01)",
                    value=False,
                )
                st.caption(
                    "กำหนดเวลา: ภายใน 30 วันนับจากวันที่เริ่มจ้างลูกจ้าง"
                )

                st.checkbox(
                    "4. ยื่นแบบแสดงรายการภาษีป้าย (ภ.ป.1)",
                    value=False,
                )
                st.caption(
                    "หน่วยงาน: ฝ่ายรายได้ สำนักงานเขต (ยื่นภายในเดือน มี.ค.)"
                )

            st.button("📥 ดาวน์โหลดชุดเอกสารและแบบฟอร์มที่กรอกอัตโนมัติ (ZIP)")

elif page == "⏱️ Demo Simulation (Time Travel)":
    st.title("Simulation & Fast-Forward Control")
    st.markdown(
        "หน้าควบคุมการจำลองเวลาสำหรับคณะกรรมการ เพื่อแสดงการทำงานเชิงรุก (Proactive Triggers)"
    )

    st.write(
        f"สถานะเวลาจำลองปัจจุบัน: **เดินหน้าไปแล้ว {st.session_state.sim_days} วัน**"
    )

    sim_slider = st.slider(
        "เร่งเวลาไปข้างหน้า (วัน):", 0, 90, st.session_state.sim_days, step=5
    )

    if st.button("อัปเดตเวลาจำลองเข้าระบบ", type="primary"):
        st.session_state.sim_days = sim_slider
        st.rerun()

    st.markdown("---")
    st.subheader("💡 คำแนะนำสำหรับกรรมการและผู้ทดสอบ:")
    st.markdown(
        """
    1. **ที่ 0 วัน (6 ต.ค.):** ยอดขายสะสมยังต่ำกว่า 1.8M สถานะในหน้า Dashboard จะเป็นสีเขียว (ปลอดภัย)
    2. **เลื่อนไปที่ ~45-50 วัน:** ยอดขายสะสมจะแตะเกณฑ์ VAT Radar จะเปลี่ยนเป็นสีเหลือง/แดง พร้อมคำนวณวันสิ้นสุดการยื่นแบบ ภ.พ.01 อัตโนมัติ
    3. **เลื่อนไปที่ ~60 วันขึ้นไป (เข้าสู่ ธ.ค.):** Regulation Watch จะตรวจพบการประกาศปรับเพดานประกันสังคม และคำนวณผลกระทบของต้นทุนต่อบริษัททันที
    """
    )