import streamlit as st

st.set_page_config(page_title="Binary Birthday Game", page_icon="🪄", layout="centered")

st.title("🪄 เกมทายวันเกิดด้วยคณิตศาสตร์")
st.write(
    "เกมนี้ใช้หลักการเลขฐานสอง (Binary) — ทุกวันที่ (1-31) เขียนแทนได้ด้วยผลรวมของเลข "
    "**1, 2, 4, 8, 16** เพียงบอกว่าวันเกิดของคุณ **มีอยู่ในการ์ดใบไหนบ้าง** "
    "แล้วเราจะคำนวณวันเกิดของคุณกลับมาได้ทันที!"
)

# สร้างการ์ดทั้ง 5 ใบ โดยแต่ละใบมีเลขที่ bit นั้นๆ ถูกเปิดอยู่
cards = [
    {"base": 1, "nums": [d for d in range(1, 32) if d & 1]},
    {"base": 2, "nums": [d for d in range(1, 32) if d & 2]},
    {"base": 4, "nums": [d for d in range(1, 32) if d & 4]},
    {"base": 8, "nums": [d for d in range(1, 32) if d & 8]},
    {"base": 16, "nums": [d for d in range(1, 32) if d & 16]},
]

st.divider()
st.subheader("✅ ติ๊กการ์ดที่มีวันเกิดของคุณอยู่")

total_day = 0
cols = st.columns(len(cards))

for i, (col, card) in enumerate(zip(cols, cards)):
    with col:
        st.markdown(f"**การ์ดใบที่ {i + 1}**")
        # แสดงตัวเลขในการ์ดเป็นตาราง 4 คอลัมน์
        nums = card["nums"]
        for row_start in range(0, len(nums), 4):
            row_nums = nums[row_start:row_start + 4]
            st.write(" ".join(f"`{n}`" for n in row_nums))

        checked = st.checkbox("มีวันเกิดฉัน", key=f"card_{i}")
        if checked:
            total_day += card["base"]

st.divider()

if st.button("🔮 ทายวันเกิด", type="primary", use_container_width=True):
    if total_day == 0:
        st.warning("คุณยังไม่ได้ติ๊กการ์ดใบไหนเลย ลองติ๊กการ์ดที่มีวันเกิดของคุณก่อนนะ")
    else:
        st.success(f"### วันเกิดของคุณคือวันที่ **{total_day}** 🎉")
        st.balloons()

with st.expander("🧠 หลักการทำงานของเกมนี้"):
    st.write(
        """
        - ตัวเลข 1 ถึง 31 ทุกจำนวนสามารถเขียนเป็นผลรวมของเลขฐานสอง (1, 2, 4, 8, 16) ได้แบบไม่ซ้ำกัน
          เช่น 19 = 16 + 2 + 1
        - การ์ดแต่ละใบเก็บเฉพาะเลขที่ "บิต" ของฐานนั้นเปิดอยู่ (เช่น การ์ดฐาน 2 จะมีเลขที่บวกด้วย 2 ได้)
        - เมื่อผู้เล่นบอกว่าวันเกิดอยู่ในการ์ดใบไหนบ้าง เราแค่นำค่าฐาน (base) ของการ์ดที่ติ๊กมาบวกกัน
          ก็จะได้วันเกิดที่แท้จริงกลับมา
        """
    )
