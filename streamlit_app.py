import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Math Function Plotter", page_icon="📈", layout="centered")

st.title("📈 Simple Function Plotter")
st.write("พิมพ์ฟังก์ชันคณิตศาสตร์ $f(x)$ ที่ต้องการ เพื่อคำนวณและวาดกราฟทันที")

# แผงตั้งค่าแกน X และ แกน Y
with st.expander("⚙️ ปรับแต่งช่วงแกน X และ แกน Y", expanded=True):
    col_x1, col_x2 = st.columns(2)
    with col_x1:
        x_min = st.number_input("x ต่ำสุด (Min)", value=-10.0, step=1.0)
    with col_x2:
        x_max = st.number_input("x สูงสุด (Max)", value=10.0, step=1.0)

    # ตัวเลือกควบคุมแกน Y
    custom_y = st.checkbox("กำหนดช่วงแกน Y เอง (ไม่ใช้ Auto-scale)", value=False)
    
    y_min, y_max = None, None
    if custom_y:
        col_y1, col_y2 = st.columns(2)
        with col_y1:
            y_min = st.number_input("y ต่ำสุด (Min)", value=-50.0, step=5.0)
        with col_y2:
            y_max = st.number_input("y สูงสุด (Max)", value=100.0, step=5.0)

# ช่องรับฟังก์ชัน
func_input = st.text_input(
    "พิมพ์ฟังก์ชัน f(x):",
    value="x**2",
    help="เช่น x**2, sin(x), exp(x), x**3 - 5*x"
)
st.caption("💡 ตัวอย่าง: `x**2`, `sin(x) * 10`, `exp(x)`, `x**3 - 4*x`")

# ตรวจสอบความถูกต้องของช่วงแกน
if x_min >= x_max:
    st.error("ค่า 'x ต่ำสุด' ต้องน้อยกว่า 'x สูงสุด'")
elif custom_y and y_min >= y_max:
    st.error("ค่า 'y ต่ำสุด' ต้องน้อยกว่า 'y สูงสุด'")
else:
    try:
        # สุ่มจุดแกน X
        x = np.linspace(x_min, x_max, 500)

        safe_dict = {
            "x": x,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pi": np.pi,
            "e": np.e,
        }

        # คำนวณค่า y
        y = eval(func_input, {"__builtins__": {}}, safe_dict)

        # วาดกราฟด้วย Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.plot(x, y, label=f"$f(x) = {func_input}$", color="#1f77b4", linewidth=2)

        # ลากเส้นแกน 0 กลางกราฟเพื่อให้อ่านง่าย
        ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)

        # ล็อกช่วงแกน Y ถ้าผู้ใช้เลือก
        if custom_y:
            ax.set_ylim(y_min, y_max)

        ax.set_xlim(x_min, x_max)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend()

        # แสดงผลกราฟบน Streamlit
        st.pyplot(fig)

    except ZeroDivisionError:
        st.error("เกิดข้อผิดพลาด: มีการหารด้วยศูนย์")
    except Exception as e:
        st.error(f"รูปแบบฟังก์ชันไม่ถูกต้อง: {e}")
