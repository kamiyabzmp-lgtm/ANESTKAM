import os
import streamlit as st
from openai import OpenAI

# تنظیمات صفحه استریم‌لیت
st.set_page_config(
    page_title="ANESTKAM | هوش مصنوعی بیهوشی",
    page_icon="🩺",
    layout="wide",
)

# استایل CSS برای راست‌چین کردن (RTL) و ظاهر جذاب چت
st.markdown(
    """
    <style>
    body, .stApp {
        direction: rtl;
        text-align: right;
    }
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; flex-direction: column;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# هدر و خوش‌آمدگویی اختصاصی
st.markdown(
    """
    <div style='background-color: #1e3d59; padding: 20px; border-radius: 10px; color: white; text-align: center;'>
        <h2>سلام عزیزای دلم، خیلی خوش اومدید! من آنست‌کام هستم، دستیار هوشمند بیهوشی شما. 🩺✨</h2>
        <p>طراحی شده برای دانشجویان هوشبری، پزشکان و کادر درمان - بر اساس کتاب مرجع میلر (Miller's Anesthesia)</p>
    </div>
""",
    unsafe_allow_html=True,
)

# ۱۰ محور کلیدی پایگاه دانش آفلاین میلر (برای پشتیبان قطعی اینترنت)
MILLER_COMPREHENSIVE_KB = {
    "مالمپاتی": "امتیازدهی مالمپاتی (Mallampati Score):\n- کلاس I: کام نرم، زبان کوچک، قوس‌های حلقی و ستون‌های لوزه کاملاً دیده می‌شوند (راه هوایی آسان).\n- کلاس II: کام نرم و پایه زبان کوچک دیده می‌شوند.\n- کلاس III: کام نرم و پایه زبان کوچک قابل مشاهده است اما کام سخت تنها دیده می‌شود.\n- کلاس IV: فقط کام سخت قابل مشاهده است (انتوباسیون سخت احتمالی).",
    "روکورونیوم": (
        "دوز داروی روکورونیوم (Rocuronium):\n- دوز انتوباسیون استاندارد: 0.6 تا 1.2 میلی‌گرم بر کیلوگرم وزن بدن (mg/kg).\n- شروع اثر:"
        " حدود 60 تا 90 ثانیه.\n- مدت اثر: حدود 30 تا 60 دقیقه.\n- در بیماران با اختلال کبدی یا چاقی، تنظیم دوز بر اساس وزن ایده‌آل"
        " (IBW) انجام شود."
    ),
    "هایپرترمی بدخیم": (
        "درمان اورژانسی هایپرترمی بدخیم (Malignant Hyperthermia - MH):\n1. قطع فوری داروهای محرک (مانند شل‌کننده‌های دپولاریزان مثل ساکسنیل‌کولین"
        " و هوشبرهای استنشاقی).\n2. هایپرونتیلاسیون بیمار با 100% اکسیژن با جریان بالا (High Flow).\n3. تزریق فوری دارو اختصاصی"
        " **دانترولن (Dantrolene)** با دوز اولیه 2.5 میلی‌گرم بر کیلوگرم و تکرار آن.\n4. خنک‌سازی فعال بیمار (سرم سرد، لاواژ"
        " و...).\n5. کنترل دقیق اسیدوز و الکترولیت‌ها (به‌ویژه پتاسیم)."
    ),
    "کاپنوگرافی": (
        "کاپنوگرافی (Capnography) و موج شارک فین (Shark Fin):\n- شکل موج شارک فین نشان‌دهنده انسداد راه هوایی کوچک است؛ مانند بیماران مبتلا"
        " به **آسم (Asthma)** یا **COPD** (اسپاسم برنش).\n- افزایش ناگهانی EtCO2: نشان‌دهنده افزایش متابولیسم، تب شدید، آمبولی ریوی اولیه"
        " یا رهاسازی تورنیکه.\n- افت ناگهانی EtCO2: نشان‌دهنده قطع لوله تراشه (Intubation failure)، ایست قلبی یا آمبولی ریوی"
        " وسیع."
    ),
    "npo": (
        "دستورالعمل NPO (ناشتا بودن پیش از بیهوشی):\n- مایعات شفاف: حداقل 2 ساعت.\n- شیر مادر: حداقل 4 ساعت.\n- شیر خشک / غذای سبک / شیر غیرمادر:"
        " حداقل 6 ساعت.\n- غذای چرب یا گوشت: حداقل 8 ساعت."
    ),
}


# تابع دریافت پاسخ (ترکیب آنلاین OpenRouter + پشتیبان آفلاین میلر)
def ask_anestkam(prompt):
  # گرفتن کلید از استریم‌لیت سیکرتز یا متغیرهای محیطی سیستم
  api_key = None
  try:
    if "OPENROUTER_API_KEY" in st.secrets:
      api_key = st.secrets["OPENROUTER_API_KEY"]
  except Exception:
    pass

  if not api_key:
    api_key = os.getenv("OPENROUTER_API_KEY")

  # اگر کلید موجود بود، تلاش برای اتصال آنلاین به OpenRouter
  if api_key:
    try:
      client = OpenAI(
          base_url="https://openrouter.ai/api/v1",
          api_key=api_key,
      )
      completion = client.chat.completions.create(
          model="meta-llama/llama-3.3-70b-instruct:free",
          messages=[
              {
                  "role": "system",
                  "content": (
                      "تو آنست‌کام (ANESTKAM) هستی؛ دستیار هوشمند و فوق‌پزشکی"
                      " بیهوشی. با لحنی صمیمی، علمی و دقیق بر اساس کتاب میلر"
                      " به سوالات پاسخ بده."
                  ),
              },
              {"role": "user", "content": prompt},
          ],
      )
      return completion.choices[0].message.content, "🟢 پاسخ آنلاین (Llama" \
          " 3.3)"
    except Exception as e:
      # اگر خطای شبکه یا تحریم پیش آمد، فال‌بک به سیستم آفلاین
      pass

  # بخش آفلاین هوشمند (جستجوی کلمات کلیدی در پایگاه دانش میلر)
  prompt_lower = prompt.lower()
  for key, value in MILLER_COMPREHENSIVE_KB.items():
    if key in prompt_lower:
      return (
          f"🟠 **سوییچ آفلاین میلر (پاسخ اضطراری تخصصی):**\n\n{value}",
          "🟠 سیستم آفلاین میلر",
      )

  # پاسخ پیش‌فرض آفلاین اگر کلمه کلیدی پیدا نشد
  return (
      (
          "🟠 **موتور آفلاین آنست‌کام فعال است:**\n ارتباط آنلاین موقتاً"
          " در دسترس نیست، اما سیستم روی ۱۰ محور میلر فعاله!\n\nمی‌تونی کلماتی"
          " مثل: *مالمپاتی*، *روکورونیوم*، *هایپرترمی بدخیم*، *کاپنوگرافی* یا"
          " *NPO* رو سرچ کنی تا پروتکل خط‌به‌خط میلر برات نمایش داده بشه."
      ),
      "🟠 سیستم آفلاین میلر",
  )


# مدیریت تاریخچه چت در سشن استیت
if "messages" not in st.session_state:
  st.session_state.messages = []

# نمایش پیام‌های قبلی
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# دریافت ورودی از کاربر
if user_prompt := st.chat_input(
    "سوال خود را درباره بیهوشی، داروها یا تجهیزات بپرسید..."
):
  st.session_state.messages.append({"role": "user", "content": user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)

  # تولید پاسخ
  with st.chat_message("assistant"):
    with st.spinner("در حال تحلیل بالینی..."):
      response_text, status_badge = ask_anestkam(user_prompt)
      st.markdown(response_text)
      st.caption(status_badge)

  st.session_state.messages.append(
      {"role": "assistant", "content": response_text}
  )
