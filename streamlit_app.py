import streamlit as st
import numpy as np
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Math Function Plotter", page_icon="📈", layout="centered")

st.title("📈 Simple Function Plotter")
st.write("พิมพ์ฟังก์ชันคณิตศาสตร์ $f(x)$ ที่ต้องการ เพื่อคำนวณและวาดกราฟทันที")

# แถบควบคุมด้านข้าง (Sidebar) หรือในหน้าหลัก
with st.expander("⚙️ ปรับแต่งช่วงแกน X", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        x_min = st.number_input("x ต่ำสุด (Min)", value=-10.0, step=1.0)
    with col2:
        x_max = st.number_input("x สูงสุด (Max)", value=10.0, step=1.0)
    with col3:
        num_points = st.slider("จำนวนจุดคำนวณ", min_value=50, max_value=1000, value=300, step=50)

# ช่องรับฟังก์ชันจากผู้ใช้
func_input = st.text_input(
    "พิมพ์ฟังก์ชัน f(x):",
    value="sin(x)",
    help="สามารถใช้คำนวณทั่วไป เช่น x**2, sin(x), cos(x), exp(x), sqrt(x), abs(x)"
)

# คำอธิบายตัวอย่างฟังก์ชัน
st.caption("💡 ตัวอย่างที่พิมพ์ได้: `x**2 - 4`, `sin(x) * cos(x)`, `exp(-x**2)`, `x**3 - 3*x`")

# คำนวณและวาดกราฟ
if x_min >= x_max:
    st.error("ค่า 'x ต่ำสุด' ต้องน้อยกว่า 'x สูงสุด' ครับ")
else:
    try:
        # สร้าง array ของค่า x
        x = np.linspace(x_min, x_max, num_points)

        # เตรียมสภาพแวดล้อมที่ปลอดภัยสำหรับคำนวณฟังก์ชันทางคณิตศาสตร์
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

        # คำนวณค่า y จากข้อความที่พิมพ์
        y = eval(func_input, {"__builtins__": {}}, safe_dict)

        # แปลงเป็น DataFrame เพื่อพล็อตด้วย st.line_chart
        df = pd.DataFrame({"x": x, "f(x)": y})
        
        st.subheader(f"📊 กราฟของ $f(x) = {func_input}$")
        st.line_chart(df, x="x", y="f(x)")

    except ZeroDivisionError:
        st.error("เกิดข้อผิดพลาด: มีการหารด้วยศูนย์ในช่วงค่า x ดังกล่าว")
    except Exception as e:
        st.error(f"รูปแบบฟังก์ชันไม่ถูกต้อง: {e}")
