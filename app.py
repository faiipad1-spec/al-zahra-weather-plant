import streamlit as st
import json
from datetime import datetime
from io import StringIO

st.set_page_config(page_title="مغامرات أسرة الزهراء | الطقس والنبات", page_icon="🌦️", layout="wide")

# لعبة تعليمية عربية للأطفال 5–6 سنوات. البيانات تبقى في جلسة التطبيق؛ نزّلوا نسخة احتياطية من لوحة المعلمة.
QUESTIONS = [
    {"level": 1, "title": "الملاحظ الذكي", "topic": "الطقس", "image": "☀️ 🌧️", "q": "أي رمز يدل على يوم ممطر؟", "options": ["☀️ الشمس", "🌧️ المطر", "🌈 قوس قزح", "🌙 القمر"], "answer": "🌧️ المطر", "why": "السحابة التي تهطل منها قطرات الماء تدل على المطر."},
    {"level": 1, "title": "الملاحظ الذكي", "topic": "النبات", "image": "🌱 💧", "q": "ما الشيء الذي تحتاج إليه النبتة لتعيش؟", "options": ["الماء", "الحلوى", "الألعاب", "الحجارة فقط"], "answer": "الماء", "why": "تحتاج النباتات إلى الماء، والضوء، والهواء، وتربة مناسبة."},
    {"level": 1, "title": "الملاحظ الذكي", "topic": "الطقس", "image": "💨 🌳", "q": "إذا تحركت أغصان الشجرة بقوة، فما الذي قد نشعر به؟", "options": ["الرياح", "الثلج دائمًا", "الليل", "الضباب فقط"], "answer": "الرياح", "why": "تحرّك الرياح أوراق الأشجار وأغصانها."},
    {"level": 1, "title": "الملاحظ الذكي", "topic": "النبات", "image": "🌼 🍃", "q": "أي جزء من النبات يمتص الماء من التربة غالبًا؟", "options": ["الجذور", "الزهرة", "الثمرة", "الورقة فقط"], "answer": "الجذور", "why": "تمتص الجذور الماء من التربة وتساعد على تثبيت النبات."},
    {"level": 1, "title": "الملاحظ الذكي", "topic": "الطقس", "image": "🧥 🌬️", "q": "في يوم بارد، أي اختيار يساعدنا على الدفء؟", "options": ["معطف دافئ", "ملابس صيفية خفيفة", "الجلوس تحت المطر", "خلع الحذاء في الخارج"], "answer": "معطف دافئ", "why": "نختار الملابس المناسبة لحالة الطقس."},

    {"level": 2, "title": "المفكّر الصغير", "topic": "النبات", "image": "🪴 🟤", "q": "أوراق نبتة ذابلة، والتربة جافة. ما أفضل خطوة أولى؟", "options": ["أفحص التربة وأسقيها إذا احتاجت", "أقتلع النبتة", "أضع عليها الرمل فقط", "أمنع عنها الضوء دائمًا"], "answer": "أفحص التربة وأسقيها إذا احتاجت", "why": "نلاحظ حالة التربة أولًا، ثم نروي النبتة عند الحاجة دون إغراقها."},
    {"level": 2, "title": "المفكّر الصغير", "topic": "الطقس", "image": "☁️ 🌬️", "q": "السماء مليئة بالغيوم الداكنة والرياح قوية. ماذا تتوقع؟", "options": ["قد يهطل المطر", "ستظهر الشمس بالتأكيد", "ستزهر كل النباتات فورًا", "لن يتغير الطقس أبدًا"], "answer": "قد يهطل المطر", "why": "الغيوم الداكنة والرياح قد تكونان علامتين على احتمال هطول المطر، لكنهما لا تضمنانه."},
    {"level": 2, "title": "المفكّر الصغير", "topic": "النبات", "image": "🌱 ☀️", "q": "نبتتان تحصلان على الماء؛ واحدة في ضوء مناسب والأخرى في الظلام. أيهما يُتوقع أن تنمو أفضل؟", "options": ["التي تحصل على ضوء مناسب", "التي تبقى في الظلام دائمًا", "كلتاهما لا تحتاجان إلى الضوء", "لا يمكن لأي نبتة أن تنمو"], "answer": "التي تحصل على ضوء مناسب", "why": "تحتاج معظم النباتات إلى الضوء لتصنع غذاءها وتنمو."},
    {"level": 2, "title": "المفكّر الصغير", "topic": "الطقس", "image": "🌧️ 🪴", "q": "هطل المطر وأصبحت التربة رطبة. ماذا قد يحدث للنبتة؟", "options": ["تحصل على الماء", "تتحول إلى حجر", "تتوقف عن الحاجة إلى الضوء", "تطير مع الرياح"], "answer": "تحصل على الماء", "why": "يساعد المطر على تزويد التربة بالماء الذي تمتصه الجذور."},
    {"level": 2, "title": "المفكّر الصغير", "topic": "البيئة", "image": "🚰 🌿", "q": "كيف نحافظ على الماء عند ري الحديقة؟", "options": ["أستخدم كمية مناسبة دون إسراف", "أترك الصنبور مفتوحًا", "أملأ الأرض بالماء دائمًا", "أروي النباتات كل دقيقة"], "answer": "أستخدم كمية مناسبة دون إسراف", "why": "نروي النبات عند الحاجة ونحافظ على الماء من الهدر."},

    {"level": 3, "title": "المحقّق البيئي", "topic": "النبات", "image": "🌱 🕵️", "q": "لاحظت أن نبتة قرب النافذة تميل باتجاه الضوء. ما التفسير الأقرب؟", "options": ["تنمو باتجاه مصدر الضوء", "تبحث عن لعبة", "الرياح تسحبها دائمًا", "الجذور تحولت إلى أوراق"], "answer": "تنمو باتجاه مصدر الضوء", "why": "قد تنمو السيقان باتجاه الضوء الذي تحتاج إليه النبتة."},
    {"level": 3, "title": "المحقّق البيئي", "topic": "الطقس", "image": "🌡️ ☀️", "q": "في يوم شديد الحرارة، جفت التربة أسرع من المعتاد. لماذا قد يحدث ذلك؟", "options": ["قد يتبخر الماء أسرع", "الشمس تصنع ماءً في التربة", "الجذور لا تحتاج إلى الماء", "التربة تحولت إلى نبات"], "answer": "قد يتبخر الماء أسرع", "why": "تساعد الحرارة على تبخر الماء، لذلك قد تجف التربة بسرعة أكبر."},
    {"level": 3, "title": "المحقّق البيئي", "topic": "النبات", "image": "🌿 🔎", "q": "نبتة تحصل على ماء كثير جدًا وبقيت تربتها مشبعة بالماء. ما المشكلة المحتملة؟", "options": ["قد تتضرر الجذور بسبب كثرة الماء", "ستحتاج إلى الغرق أكثر", "لن تحتاج إلى الهواء أبدًا", "ستتحول إلى زهرة فورًا"], "answer": "قد تتضرر الجذور بسبب كثرة الماء", "why": "الإفراط في الري قد يقلل الهواء في التربة ويضر الجذور."},
    {"level": 3, "title": "المحقّق البيئي", "topic": "الطقس", "image": "🌤️ 🌧️", "q": "رأيت الغيوم تتجمع في السماء. ما العبارة العلمية الأدق؟", "options": ["قد يتغير الطقس، لكننا لا نجزم بالمطر", "المطر سيهطل حتمًا", "لن تمطر السماء أبدًا", "الغيوم تعني أن الوقت ليل"], "answer": "قد يتغير الطقس، لكننا لا نجزم بالمطر", "why": "نستخدم الملاحظة للتوقع، لكن العلامات لا تعطينا يقينًا دائمًا."},
    {"level": 3, "title": "المحقّق البيئي", "topic": "البيئة", "image": "🍂 🌱", "q": "وجدت ورقة جافة على الأرض قرب شجرة. ما الاستنتاج الأفضل؟", "options": ["قد تكون ورقة قديمة سقطت طبيعيًا", "الشجرة ماتت بالتأكيد", "كل أوراق الشجرة ستموت الآن", "المطر صنع الورقة"], "answer": "قد تكون ورقة قديمة سقطت طبيعيًا", "why": "ورقة واحدة جافة لا تكفي للحكم على صحة الشجرة كلها."},

    {"level": 4, "title": "خبير أسرة الزهراء", "topic": "الطقس والنبات", "image": "☀️ 💧 🌱", "q": "مرّت أيام حارة ولم تهطل الأمطار. ما أفضل خطة لمساعدة نباتات الحديقة؟", "options": ["أفحص التربة وأسقي عند الحاجة وأوفر ضوءًا مناسبًا", "أغطيها بالماء طوال اليوم", "أضعها في الظلام وأمنع الماء", "أقتلع جميع النباتات"], "answer": "أفحص التربة وأسقي عند الحاجة وأوفر ضوءًا مناسبًا", "why": "الخطة الجيدة تجمع بين الملاحظة والري المناسب والضوء، دون إفراط."},
    {"level": 4, "title": "خبير أسرة الزهراء", "topic": "الطقس والبيئة", "image": "🌧️ 🪣 🌿", "q": "كيف يمكننا الاستفادة من المطر والمحافظة على الماء؟", "options": ["نجمع ماء المطر بطريقة آمنة لري النباتات", "نترك الصنبور مفتوحًا", "نرمي النفايات في مجرى الماء", "نروي الأرض حتى تتجمع البرك دائمًا"], "answer": "نجمع ماء المطر بطريقة آمنة لري النباتات", "why": "يمكن جمع مياه المطر واستخدامها بحكمة، مع مراعاة النظافة والسلامة."},
    {"level": 4, "title": "خبير أسرة الزهراء", "topic": "النبات", "image": "🌱 📋", "q": "نريد معرفة هل يؤثر الضوء في نمو النبات. ما الطريقة الأفضل للمقارنة؟", "options": ["نقارن نبتتين متشابهتين مع تغيير الضوء فقط قدر الإمكان", "نغير الماء والتربة والضوء معًا", "نراقب نبتة واحدة مرة واحدة فقط", "نختار النتيجة قبل التجربة"], "answer": "نقارن نبتتين متشابهتين مع تغيير الضوء فقط قدر الإمكان", "why": "للمقارنة العادلة نغيّر عاملًا واحدًا ونحاول تثبيت العوامل الأخرى."},
    {"level": 4, "title": "خبير أسرة الزهراء", "topic": "الطقس والنبات", "image": "🌬️ 🌼 🪴", "q": "توقّعنا رياحًا قوية. أي إجراء يحمي أصص النباتات الصغيرة بشكل أفضل؟", "options": ["نضعها في مكان آمن ومحمي من الرياح", "نضعها على حافة مرتفعة", "نتركها قرب طريق السيارات", "نزيل جذورها من التربة"], "answer": "نضعها في مكان آمن ومحمي من الرياح", "why": "إبعاد الأصص عن الأماكن المكشوفة يقلل احتمال سقوطها أو تضررها."},
    {"level": 4, "title": "خبير أسرة الزهراء", "topic": "الاستنتاج", "image": "🌱 📈", "q": "بعد أسبوع، نمت نبتة قليلًا رغم حصولها على الماء والضوء. ماذا يفعل المستكشف الجيد؟", "options": ["يفحص عوامل أخرى مثل التربة والحرارة ويواصل الملاحظة", "يقرر فورًا أن الماء غير مهم", "يتوقف عن ملاحظتها", "يضيف أي شيء إلى التربة دون فحص"], "answer": "يفحص عوامل أخرى مثل التربة والحرارة ويواصل الملاحظة", "why": "النمو يتأثر بعدة عوامل، لذا نلاحظ ونتحقق قبل الاستنتاج."},
]

LEVELS = {
    1: {"name": "الملاحظ الذكي", "icon": "👀", "need": 0, "desc": "تمييز وملاحظة الطقس والنبات"},
    2: {"name": "المفكّر الصغير", "icon": "💡", "need": 3, "desc": "اختيار الحل المناسب للمواقف"},
    3: {"name": "المحقّق البيئي", "icon": "🔎", "need": 6, "desc": "توقع النتائج والاستنتاج من الملاحظات"},
    4: {"name": "خبير أسرة الزهراء", "icon": "🏆", "need": 9, "desc": "حل مشكلات تجمع بين الطقس والنبات والبيئة"},
}

if "children" not in st.session_state:
    st.session_state.children = []
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "answered" not in st.session_state:
    st.session_state.answered = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "garden_stars" not in st.session_state:
    st.session_state.garden_stars = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "active_child" not in st.session_state:
    st.session_state.active_child = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = None


def safe_key(text):
    return str(text).strip()


def get_level(score):
    if score >= 9:
        return 4
    if score >= 6:
        return 3
    if score >= 3:
        return 2
    return 1


def garden_art(stars):
    if stars < 3:
        return "🟫 🌱 🪨 🌱 🟫", "بدأت الحديقة تنمو!"
    if stars < 6:
        return "🌱 🌿 🌼 🌱 🌿", "ظهرت أوراق وأزهار جديدة!"
    if stars < 10:
        return "🌳 🌼 🦋 🌷 🌳", "أصبحت الحديقة أكثر خضرة!"
    return "🌳 🌷 🌼 🦋 🌻 🌳", "يا لها من حديقة مزهرة لأسرة الزهراء!"


def export_data():
    return {
        "children": st.session_state.children,
        "scores": st.session_state.scores,
        "answered": st.session_state.answered,
        "history": st.session_state.history,
        "garden_stars": st.session_state.garden_stars,
        "exported_at": datetime.now().isoformat(timespec="minutes"),
    }

st.markdown("<div dir='rtl' style='text-align:center'>", unsafe_allow_html=True)
st.title("🌦️ مغامرات المستكشف الصغير")
st.subheader("وحدة الطقس والنبات · أسرة الزهراء")
st.caption("لعبة جماعية تعليمية للأطفال من 5 إلى 6 سنوات — أسئلة متدرجة من الملاحظة إلى الاستنتاج")
st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🌷 أسرة الزهراء")
    st.markdown("**مستويات المغامرة**")
    for n, info in LEVELS.items():
        st.write(f"{info['icon']} المستوى {n}: {info['name']}")
    st.divider()
    st.caption("ملاحظة للمعلمة: يُفضّل استخدام الأسماء الأولى فقط. نزّلي نسخة احتياطية من لوحة المعلمة بعد كل جلسة؛ قد تُمسح البيانات عند إعادة تشغيل التطبيق.")

play_tab, garden_tab, teacher_tab = st.tabs(["🎮 اللعب والمغامرات", "🌻 حديقة الفصل", "📋 لوحة المعلمة"])

with play_tab:
    if not st.session_state.children:
        st.info("ابدئي بإضافة أسماء الأطفال من لوحة المعلمة، ثم عودي إلى هنا لبدء المغامرة.")
    else:
        left, right = st.columns([2, 1])
        with left:
            chosen = st.selectbox("من المستكشف الذي سيجيب الآن؟", st.session_state.children, key="child_picker")
            st.session_state.active_child = chosen
            child_score = st.session_state.scores.get(chosen, 0)
            level_num = get_level(child_score)
            level = LEVELS[level_num]
            st.markdown(f"### {level['icon']} المستوى {level_num}: {level['name']}")
            st.write(level["desc"])
            st.progress(min(child_score / 12, 1.0), text=f"نجوم {chosen}: {child_score}")
        with right:
            art, caption = garden_art(st.session_state.garden_stars)
            st.markdown(f"<div style='text-align:center; padding:14px; border:1px solid #ddd; border-radius:14px'><div style='font-size:26px'>{art}</div><b>{caption}</b><p>⭐ {st.session_state.garden_stars} نجمة للفصل</p></div>", unsafe_allow_html=True)

        eligible = [q for q in QUESTIONS if q["level"] == level_num]
        # اختر سؤالًا لم يُجب عنه هذا الطفل في المستوى الحالي، ثم أعد المجموعة بعد إكمالها.
        done = st.session_state.answered.get(chosen, [])
        available = [q for q in eligible if q["q"] not in done]
        if not available:
            st.success(f"أحسنت يا {chosen}! أكملت أسئلة هذا المستوى. يمكنك متابعة اللعب ومراجعة الإجابات مع المعلمة.")
            if st.button("🔄 إعادة أسئلة هذا المستوى لهذا الطفل"):
                st.session_state.answered[chosen] = [q for q in done if q not in [item["q"] for item in eligible]]
                st.session_state.last_result = None
                st.rerun()
        else:
            question = available[0]
            st.divider()
            st.markdown(f"#### {question['image']}  {question['topic']}")
            st.markdown(f"### {question['q']}")
            with st.form(key=f"form_{chosen}_{question['q']}"):
                answer = st.radio("اختَر الإجابة الأنسب:", question["options"], index=None)
                submitted = st.form_submit_button("تحقّق من الإجابة ✨", use_container_width=True)
            if submitted:
                if answer is None:
                    st.warning("اختَر إجابة أولًا.")
                else:
                    correct = answer == question["answer"]
                    if chosen not in st.session_state.answered:
                        st.session_state.answered[chosen] = []
                    st.session_state.answered[chosen].append(question["q"])
                    if correct:
                        st.session_state.scores[chosen] = st.session_state.scores.get(chosen, 0) + 1
                        st.session_state.garden_stars += 1
                        st.session_state.last_result = {"correct": True, "child": chosen, "answer": question["answer"], "why": question["why"]}
                        st.session_state.history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "child": chosen, "level": level_num, "question": question["q"], "chosen": answer, "correct": True})
                    else:
                        st.session_state.last_result = {"correct": False, "child": chosen, "answer": question["answer"], "why": question["why"]}
                        st.session_state.history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "child": chosen, "level": level_num, "question": question["q"], "chosen": answer, "correct": False})
                    st.rerun()

        if st.session_state.last_result:
            result = st.session_state.last_result
            if result["correct"]:
                st.success(f"🌟 إجابة رائعة يا {result['child']}! حصل الفصل على نجمة للحديقة.")
            else:
                st.info(f"🌱 محاولة جميلة يا {result['child']}! لنتعلّم معًا.")
            st.write(f"**الإجابة الصحيحة:** {result['answer']}")
            st.write(result["why"])
            if st.button("التالي ➜", use_container_width=True):
                st.session_state.last_result = None
                st.rerun()

with garden_tab:
    art, caption = garden_art(st.session_state.garden_stars)
    st.markdown(f"<div style='text-align:center; padding:22px; border:1px solid #ddd; border-radius:18px'><div style='font-size:48px'>{art}</div><h3>{caption}</h3><p>كل إجابة صحيحة تضيف نجمة إلى حديقة الفصل.</p><h2>⭐ {st.session_state.garden_stars}</h2></div>", unsafe_allow_html=True)
    st.subheader("🌼 محطات نمو الحديقة")
    for target, title, description in [(3, "بداية النمو", "تظهر أوراق صغيرة"), (6, "حديقة خضراء", "تزداد النباتات والأوراق"), (10, "حديقة مزهرة", "تظهر أزهار وفراشات رمزية")]:
        if st.session_state.garden_stars >= target:
            st.success(f"✓ {title} — {description} (تم الإنجاز)")
        else:
            st.write(f"🔒 عند {target} نجوم: {title} — {description}")

with teacher_tab:
    st.subheader("👩‍🏫 لوحة المعلمة")
    st.write("أضيفي أسماء الأطفال، تابعي النقاط، واحفظي نسخة احتياطية من التقدم.")
    with st.form("add_child_form", clear_on_submit=True):
        new_name = st.text_input("اسم الطفل الأول فقط", placeholder="مثال: سارة")
        add = st.form_submit_button("إضافة الطفل")
        if add:
            name = safe_key(new_name)
            if not name:
                st.warning("اكتبي اسمًا أولًا.")
            elif name in st.session_state.children:
                st.warning("هذا الاسم موجود بالفعل.")
            else:
                st.session_state.children.append(name)
                st.session_state.scores[name] = 0
                st.session_state.answered[name] = []
                st.success(f"تمت إضافة {name}.")
                st.rerun()

    if st.session_state.children:
        st.markdown("#### تقدم الأطفال")
        rows = []
        for child in st.session_state.children:
            score = st.session_state.scores.get(child, 0)
            rows.append({"الطفل": child, "النجوم الشخصية": score, "المستوى الحالي": LEVELS[get_level(score)]["name"], "عدد الأسئلة المجاب عنها": len(st.session_state.answered.get(child, []))})
        st.dataframe(rows, use_container_width=True, hide_index=True)
        c1, c2 = st.columns(2)
        with c1:
            remove_name = st.selectbox("إزالة اسم طفل", ["— اختاري —"] + st.session_state.children, key="remove_child")
            if st.button("إزالة الطفل المحدد"):
                if remove_name != "— اختاري —":
                    st.session_state.children.remove(remove_name)
                    st.session_state.scores.pop(remove_name, None)
                    st.session_state.answered.pop(remove_name, None)
                    st.session_state.history = [x for x in st.session_state.history if x["child"] != remove_name]
                    st.rerun()
        with c2:
            reset_confirm = st.checkbox("أوافق على تصفير نقاط الفصل وسجل الإجابات")
            if st.button("تصفير التقدم"):
                if reset_confirm:
                    st.session_state.scores = {child: 0 for child in st.session_state.children}
                    st.session_state.answered = {child: [] for child in st.session_state.children}
                    st.session_state.history = []
                    st.session_state.garden_stars = 0
                    st.session_state.last_result = None
                    st.success("تم تصفير التقدم.")
                    st.rerun()
                else:
                    st.warning("حددي مربع الموافقة أولًا.")

    st.markdown("#### 💾 حفظ واستعادة التقدم")
    data = export_data()
    st.download_button("تنزيل نسخة احتياطية (JSON)", data=json.dumps(data, ensure_ascii=False, indent=2), file_name="zahraa_weather_plant_backup.json", mime="application/json", use_container_width=True)
    uploaded = st.file_uploader("استعادة نسخة احتياطية سابقة", type=["json"])
    if uploaded is not None:
        if st.button("استعادة البيانات من الملف"):
            try:
                loaded = json.load(uploaded)
                st.session_state.children = loaded.get("children", [])
                st.session_state.scores = loaded.get("scores", {})
                st.session_state.answered = loaded.get("answered", {})
                st.session_state.history = loaded.get("history", [])
                st.session_state.garden_stars = loaded.get("garden_stars", 0)
                st.session_state.last_result = None
                st.success("تمت استعادة البيانات.")
                st.rerun()
            except Exception:
                st.error("تعذر قراءة الملف. اختاري نسخة احتياطية صحيحة من اللعبة.")

    if st.session_state.history:
        st.markdown("#### سجل الإجابات")
        st.dataframe(list(reversed(st.session_state.history)), use_container_width=True, hide_index=True)

st.divider()
st.caption("🌦️ إعداد تعليمي لأسرة الزهراء. الإجابات الخاطئة تُستخدم للتعلّم، وليست عقوبة. البيانات في هذه النسخة تجريبية وتحتاج إلى تنزيل نسخة احتياطية للحفاظ عليها.")
