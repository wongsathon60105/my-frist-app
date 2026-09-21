import streamlit as st

st.set_page_config(page_title="Binary Birthday Game", page_icon="🪄", layout="centered")

st.title("🪄 เกมทายวันเกิดด้วยคณิตศาสตร์")

# 1. ข้อมูลการ์ด 5 ใบ (แต่ละใบมี 16 จำนวน)
cards = [
    {"base": 1, "nums": [d for d in range(1, 32) if d & 1]},
    {"base": 2, "nums": [d for d in range(1, 32) if d & 2]},
    {"base": 4, "nums": [d for d in range(1, 32) if d & 4]},
    {"base": 8, "nums": [d for d in range(1, 32) if d & 8]},
    {"base": 16, "nums": [d for d in range(1, 32) if d & 16]},
]

# 2. ตัวแปรบันทึกสถานะ (Session State)
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "total_day" not in st.session_state:
    st.session_state.total_day = 0

def go_next(add_base: int = 0):
    st.session_state.total_day += add_base
    st.session_state.current_idx += 1

def reset_game():
    st.session_state.current_idx = 0
    st.session_state.total_day = 0

idx = st.session_state.current_idx

# 3. หน้าจอเล่นเกม
if idx < len(cards):
    card = cards[idx]

    st.progress(idx / len(cards))
    st.subheader(f"การ์ดใบที่ {idx + 1} จาก {len(cards)}")
    st.write("👉 **วันเกิดของคุณอยู่ในตาราง 4x4 ด้านล่างนี้หรือไม่?**")

    # สไตล์ CSS สร้าง Grid ตาราง 4x4
    card_items = "".join([
        f"<div style='background:rgba(128,128,128,0.15); border:1px solid rgba(128,128,128,0.3); border-radius:10px; font-size:24px; font-weight:bold; height:60px; display:flex; align-items:center; justify-content:center;'>{n}</div>"
        for n in card["nums"]
    ])

    grid_html = f"""
    <div style='display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0;'>
        {card_items}
    </div>
    """
    st.markdown(grid_html, unsafe_allow_html=True)

    # ปุ่มคำตอบ
    col_yes, col_no = st.columns(2)
    with col_yes:
        st.button(
            "✅ มี (Yes)",
            use_container_width=True,
            type="primary",
            on_click=go_next,
            args=(card["base"],),
        )
    with col_no:
        st.button(
            "❌ ไม่มี (No)",
            use_container_width=True,
            on_click=go_next,
            args=(0,),
        )

# 4. หน้าจอแสดงผลเฉลย
else:
    st.balloons()
    st.success("🎉 คำนวณเสร็จสิ้นแล้ว!")
    st.markdown("### วันเกิดของคุณคือวันที่")
    st.markdown(
        f"<div style='text-align:center; color:#ff4b4b; font-size:84px; font-weight:bold; margin:20px 0;'>{st.session_state.total_day}</div>",
        unsafe_allow_html=True,
    )
    st.button("🔄 เล่นใหม่อีกครั้ง", on_click=reset_game, use_container_width=True)

with st.expander("🧠 เฉลยกลคณิตศาสตร์"):
    st.markdown("""
    - ทุกจำนวนระหว่าง **1 ถึง 31** เขียนแทนด้วยเลขฐานสอง 5 บิตได้ ($2^0, 2^1, 2^2, 2^3, 2^4$ หรือ $1, 2, 4, 8, 16$)
    - แต่ละการ์ดมีตัวเลข 16 ตัว (จัดเรียงแบบตาราง 4×4)
    - ตัวเลขวันเกิดของคุณคือผลบวกของเลขมุมซ้ายบนตัวแรกของการ์ดทุกใบที่คุณตอบว่า **"มี"**
    """)
