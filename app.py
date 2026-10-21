import os
import streamlit as st
from openai import OpenAI

# تنظیمات صفحه
st.set_page_config(
    page_title="ANESTKAM | هوش مصنوعی بیهوشی",
    page_icon="🩺",
    layout="wide",
)

# استایل راست‌چین فارسی
st.markdown(
    """
    <style>
    body, .stApp { direction: rtl; text-align: right; }
    </style>
""",
    unsafe_allow_html=True,
)

# هدر آنست‌کام
st.markdown(
    """
    <div style='background-color: #1e3d59; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;'>
        <h3>سلام عزیزای دلم، خیلی خوش اومدید! من آنست‌کام هستم، دستیار هوشمند بیهوشی شما. 🩺✨</h3>
    </div>
""",
    unsafe_allow_html=True,
)

# بانک اطلاعاتی پشتیبان میلر
MILLER_COMPREHENSIVE_KB = {
    "مالمپاتی": "امتیازدهی مالمپاتی (Mallampati): ارزیابی راه هوایی از کلاس I تا IV.",
    "روکورونیوم": "دوز انتوباسیون روکورونیوم: 0.6 الی 1.2 میلی‌گرم بر کیلوگرم.",
    "هایپرترمی بدخیم": "درمان MH: قطع داروهای محرک، دانترولن 2.5 mg/kg، اکسیژن 100%.",
    "کاپنوگرافی": "موج شارک فین (Shark-fin): نشانه اسپاسم برنش و انسداد بازدمی (COPD/Asthma).",
    "npo": "دستورالعمل ناشتایی: آب و مایعات شفاف ۲ ساعت، غذای سنگین ۸ ساعت.",
}


# تابع مغز آنست‌کام با خطایاب هوشمند
def ask_anestkam(prompt):
  # ۱. بررسی وجود کلید
  GAPGPTMASKTOKEN9o77pdvukuX0X = None
  source = "یافت نشد"

  if "OPENROUTER_API_KEY" in st.secrets:
    GAPGPTMASKTOKEN9o77pdvukuX1X = GAPGPTMASKTOKEN9o77pdvukuX2X"OPENROUTER_API_KEY"]
    source = "Streamlit Secrets"
  elif os.getenv("OPENROUTER_API_KEY"):
    GAPGPTMASKTOKEN9o77pdvukuX3X = os.getenv("OPENROUTER_API_KEY")
    source = "Environment Variable"

  # اگر اصلاً کلید پیدا نشد
  if not GAPGPTMASKTOKEN9o77pdvukuX4X:
    return (
        "❌ **کلید پیدا نشد!**\nسیستم نتونست `OPENROUTER_API_KEY` رو بخونه. لطفاً"
        " مطمئن شو توی بخش Secrets کلمه رو درست نوشتی.",
        "🔴 عدم دسترسی به کلید",
    )

  # ۲. تلاش برای ارتباط با هوش مصنوعی
  try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        GAPGPTMASKTOKEN9o77pdvukuX5X=GAPGPTMASKTOKEN9o77pdvukuX6X,
        default_headers={
            "HTTP-Referer": "https://streamlit.app",
            "X-Title": "ANESTKAM",
        },
    )

    # تست مدل فوق‌العاده پایدار و رایگان Llama 3
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": (
                    "تو آنست‌کام هستی؛ دستیار حرفه‌ای، صمیمی و علمی هوشبری."
                    " فارسی جواب بده."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        timeout=15,
    )
    return completion.choices[0].message.content, "🟢 آنلاین (Llama 3.3)"

  except Exception as err:
    # چاپ دقیق علت خطا برای عیب‌یابی آنی
    error_msg = str(err)

    # فال‌بک به میلر
    prompt_lower = prompt.lower()
    for k, v in MILLER_COMPREHENSIVE_KB.items():
      if k in prompt_lower:
        return (
            f"🟠 **پاسخ میلر:**\n{v}\n\n*(علت عدم اتصال آنلاین: `{error_msg}`)*",
            "🟠 آفلاین میلر",
        )

    return (
        f"⚠️ **مغز آنلاین پاسخ نداد!**\n\n**پیام دقیق سرور:**\n`{error_msg}`\n\nمنبع"
        f" کلید: {source}",
        "🔴 خطای ارتباط",
    )


# رابط کاربری چت
if "messages" not in st.session_state:
  st.session_state.messages = []

for m in st.session_state.messages:
  with st.chat_message(m["role"]):
    st.markdown(m["content"])

if user_input := st.chat_input("سوال هوشبری خود را بپرسید..."):
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  with st.chat_message("assistant"):
    with st.spinner("در حال تفکر بالینی..."):
      res, badge = ask_anestkam(user_input)
      st.markdown(res)
      st.caption(badge)

  st.session_state.messages.append({"role": "assistant", "content": res})

