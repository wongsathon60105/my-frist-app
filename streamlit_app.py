import streamlit as st

st.set_page_config(page_title="Binary Birthday Game", page_icon="🪄", layout="centered")

st.title("🪄 What is your Brith Day!!")

# สร้างการ์ดทั้ง 5 ใบ โดยแต่ละใบมีเลขที่ bit นั้นๆ ถูกเปิดอยู่
cards = [
    {"base": 1, "nums": [d for d in range(1, 32) if d & 1]},
    {"base": 2, "nums": [d for d in range(1, 32) if d & 2]},
    {"base": 4, "nums": [d for d in range(1, 32) if d & 4]},
    {"base": 8, "nums": [d for d in range(1, 32) if d & 8]},
    {"base": 16, "nums": [d for d in range(1, 32) if d & 16]},
]

# ---- ตัวแปรสถานะ (คงค่าไว้ระหว่างที่ผู้ใช้กดปุ่มต่างๆ) ----
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

# ---- หน้าจอเล่นเกม ----
if idx < len(cards):
    card = cards[idx]

    st.progress(idx / len(cards))
    st.subheader(f"การ์ดใบที่ {idx + 1} / {len(cards)}")
    st.write("**วันเกิดของคุณอยู่ในตัวเลขเหล่านี้หรือไม่?**")

    # แสดงตัวเลขในการ์ดเป็นตาราง 8 คอลัมน์
    nums = card["nums"]
    for row_start in range(0, len(nums), 8):
        row_nums = nums[row_start:row_start + 8]
        st.write(" ".join(f"`{n}`" for n in row_nums))

    st.write("")
    col_yes, col_no = st.columns(2)
    with col_yes:
        st.button(
            "✅ YES",
            use_container_width=True,
            type="primary",
            on_click=go_next,
            args=(card["base"],),
        )
    with col_no:
        st.button(
            "❌ NO",
            use_container_width=True,
            on_click=go_next,
            args=(0,),
        )

# ---- หน้าจอแสดงผลลัพธ์ ----
else:
    st.success("เปิดการ์ดครบทั้ง 5 ใบแล้ว!")
    st.markdown("### วันเกิดของคุณคือวันที่")
    st.markdown(
        f"<h1 style='text-align:center; color:#fbbf24; font-size:80px;'>{st.session_state.total_day}</h1>",
        unsafe_allow_html=True,
    )
    st.balloons()
    st.button("🔄 เล่นอีกรอบ", on_click=reset_game, use_container_width=True)

with st.expander("🧠 หลักการทำงานของเกมนี้"):
    st.write(
        """
        - ตัวเลข 1 ถึง 31 ทุกจำนวนสามารถเขียนเป็นผลรวมของเลขฐานสอง (1, 2, 4, 8, 16) ได้แบบไม่ซ้ำกัน
          เช่น 19 = 16 + 2 + 1
        - การ์ดแต่ละใบเก็บเฉพาะเลขที่ "บิต" ของฐานนั้นเปิดอยู่
        - เมื่อผู้เล่นตอบ "มี" ในการ์ดใบไหน เราจะบวกค่าฐาน (base) ของการ์ดนั้นเข้าไปเรื่อยๆ
          พอครบ 5 ใบ ผลรวมที่ได้ก็คือวันเกิดที่แท้จริง
        """
    )
