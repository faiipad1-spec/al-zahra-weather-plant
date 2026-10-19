import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="مملكتي أجمل | أسرة الزهراء", layout="wide", initial_sidebar_state="collapsed")

CHILDREN = ["نورا خالد", "ميلا", "ملك", "نوال", "أسيل", "منيرة", "ديم", "علي محمد", "رشود", "علي الشهراني", "رغد", "مها", "جوزاء", "فهد"]

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
html, body, [class*="css"] {font-family:'Tajawal',sans-serif;}
.stApp {background:linear-gradient(180deg,#e9f7ff 0%,#f4fff5 48%,#fff8e9 100%);color:#173b35;}
.block-container {max-width:1180px;padding-top:1.1rem;padding-bottom:3rem;}
#MainMenu,footer {visibility:hidden;} header[data-testid="stHeader"]{background:transparent;}
.hero {position:relative;overflow:hidden;border-radius:30px;padding:30px 32px;background:linear-gradient(115deg,#075e58,#159a79 56%,#a5d96b);color:#fff;box-shadow:0 15px 32px #155f4b22;}
.hero h1{font-size:clamp(2.1rem,4vw,3.5rem);font-weight:900;line-height:1.25;margin:0;color:white;}
.hero p{font-size:1.18rem;color:#effff4;margin:.5rem 0 0;max-width:700px;}
.hero .eyebrow{display:inline-block;padding:6px 14px;border-radius:99px;background:#ffffff26;border:1px solid #ffffff55;font-weight:700;margin-bottom:12px;}
.hero-art{position:absolute;left:12px;bottom:-12px;width:33%;max-width:340px;opacity:.97;}
.panel{background:#ffffffdf;border:1px solid #d7e9de;border-radius:23px;padding:20px;box-shadow:0 7px 22px #205d4410;}
.section-title{font-size:1.5rem;font-weight:900;color:#176c56;margin:0 0 8px;}
.subtle{color:#57776c;font-size:1rem;}
.child-card{border:2px solid #b8e5cc;background:linear-gradient(135deg,#fff,#effcf3);border-radius:20px;padding:16px;text-align:center;}
.child-name{font-size:1.6rem;font-weight:900;color:#125d4a;line-height:1.4;}
.score-pill{display:inline-block;border-radius:99px;background:#fff0b7;color:#79510a;padding:5px 13px;font-weight:800;margin-top:8px;}
.mission{border:2px solid #d7e9de;border-radius:22px;background:white;padding:22px;box-shadow:0 10px 25px #205d4410;}
.question{font-size:1.55rem;font-weight:900;line-height:1.7;color:#173b35;margin:.7rem 0 1rem;}
.artbox{border-radius:20px;background:linear-gradient(135deg,#dff5ff,#f3ffe6);padding:8px;margin:12px 0;}
.artbox svg{width:100%;height:auto;max-height:260px;}
.stButton>button,.stDownloadButton>button{border:0!important;border-radius:15px!important;background:linear-gradient(100deg,#137b62,#43a86e)!important;color:white!important;font-family:'Tajawal',sans-serif!important;font-size:1.04rem!important;font-weight:800!important;padding:.7rem 1rem!important;box-shadow:0 5px 14px #1f76551f!important;}
.stButton>button:hover,.stDownloadButton>button:hover{filter:brightness(1.06);transform:translateY(-1px);}
.stRadio [role=radiogroup]{gap:8px;}
.stRadio [role=radiogroup] label{border:1px solid #d7e8dd;background:#f8fcf9;border-radius:15px;padding:10px 13px;}
.stRadio [role=radiogroup] label:has(input:checked){background:#e2f7e9;border-color:#47a577;}
.stTabs [data-baseweb=tab-list]{gap:8px;background:#e4f2e9;padding:7px;border-radius:17px;}
.stTabs [data-baseweb=tab]{border-radius:12px;padding:10px 16px;font-weight:800;}
.stTabs [aria-selected=true]{background:#fff!important;color:#176c56!important;}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#43a86e,#f4c94d);}
div[data-testid="stMetric"]{background:#fff;border:1px solid #dcebe1;padding:14px;border-radius:17px;}
@media(max-width:700px){.hero{padding:23px 18px}.hero-art{opacity:.25;width:45%}.question{font-size:1.3rem}.block-container{padding-left:1rem;padding-right:1rem}.child-name{font-size:1.35rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

CITY = '''<svg viewBox="0 0 620 245" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="مدينة خضراء سعودية نظيفة"><circle cx="520" cy="42" r="25" fill="#FFD46A"/><g stroke="#F2B844" stroke-width="4" stroke-linecap="round"><path d="M520 5v-8M520 80v8M483 42h-8M557 42h8M494 16l-6-6M546 68l6 6M546 16l6-6M494 68l-6 6"/></g><path d="M0 158Q100 124 205 160T410 151T620 150V245H0Z" fill="#9DDB8D"/><path d="M0 191Q130 165 270 194T620 185V245H0Z" fill="#6DBB76"/><g><rect x="80" y="78" width="84" height="89" rx="5" fill="#F7D7A7"/><path d="M70 80l52-39 52 39Z" fill="#E58B65"/><rect x="98" y="100" width="18" height="25" rx="3" fill="#85C9E9"/><rect x="130" y="100" width="18" height="25" rx="3" fill="#85C9E9"/><rect x="112" y="139" width="22" height="28" fill="#B7784E"/><rect x="188" y="104" width="61" height="65" rx="4" fill="#E6F0F6"/><path d="M181 106l37-29 38 29Z" fill="#E5A078"/><rect x="202" y="119" width="14" height="17" fill="#7BC3E5"/><rect x="225" y="119" width="14" height="17" fill="#7BC3E5"/></g><g transform="translate(322 99)"><rect x="-8" y="38" width="16" height="55" rx="5" fill="#9B6948"/><circle cx="0" cy="12" r="38" fill="#3D9C65"/><circle cx="-25" cy="26" r="23" fill="#55B878"/><circle cx="25" cy="27" r="24" fill="#2F8C59"/></g><g transform="translate(435 118)"><rect x="-6" y="34" width="12" height="43" rx="4" fill="#9B6948"/><circle cx="0" cy="12" r="28" fill="#3A9A61"/><circle cx="-19" cy="20" r="18" fill="#63C67D"/><circle cx="19" cy="20" r="18" fill="#2D8754"/></g><g transform="translate(550 157)"><rect x="-5" y="12" width="10" height="30" rx="4" fill="#9B6948"/><path d="M0 15C-32 14-37-7-34-20-11-18 0-3 0 15M0 6C27 5 36-13 33-26 12-24 0-8 0 6" fill="#238C5C"/></g><g transform="translate(265 182)"><rect x="-22" y="-9" width="44" height="34" rx="5" fill="#3F8DC8"/><rect x="-16" y="-17" width="32" height="12" rx="3" fill="#2870A8"/><rect x="-12" y="0" width="24" height="7" rx="2" fill="#D9F4FF"/><path d="M-22 8h44" stroke="#D9F4FF" stroke-width="3"/></g><g transform="translate(185 195)"><path d="M-15-6h30l-4 28h-22Z" fill="#D89A69"/><path d="M0-7v-23m0 12c-19 0-21-11-20-19 13 1 20 8 20 19m0-4c18 0 21-11 20-18-13 1-20 8-20 18" stroke="#278D59" stroke-width="5" fill="#63BF70" stroke-linecap="round"/></g><g transform="translate(390 205)"><path d="M-13-4h26l-3 24h-20Z" fill="#D89A69"/><path d="M0-5v-24m0 12c-17 0-20-11-18-18 12 1 18 8 18 18m0-4c16 0 19-10 18-17-12 1-18 8-18 17" stroke="#278D59" stroke-width="5" fill="#63BF70" stroke-linecap="round"/></g></svg>'''
SORTING = '''<svg viewBox="0 0 620 245" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="620" height="245" rx="18" fill="#EAF8FF"/><path d="M0 196Q150 170 310 197T620 190V245H0Z" fill="#A7DDA0"/><g transform="translate(110 105)"><rect x="-45" y="-30" width="90" height="100" rx="10" fill="#418CC7"/><rect x="-52" y="-39" width="104" height="15" rx="5" fill="#286DA8"/><path d="M-22-5h44M-22 9h44M-22 23h44" stroke="#DFF4FF" stroke-width="7" stroke-linecap="round"/><path d="M-26-60h52l-5 27h-42Z" fill="#FFFFFF" stroke="#BCD6E4" stroke-width="3"/><path d="M-12-48h24" stroke="#79B8D9" stroke-width="4"/></g><g transform="translate(310 105)"><rect x="-45" y="-30" width="90" height="100" rx="10" fill="#48A96F"/><rect x="-52" y="-39" width="104" height="15" rx="5" fill="#287D50"/><path d="M-20-3h40M-20 12h40" stroke="#E7FFF0" stroke-width="7" stroke-linecap="round"/><path d="M-28-60h56l-5 27h-46Z" fill="#FFFFFF" stroke="#BCD6E4" stroke-width="3"/><path d="M-12-48h24" stroke="#79B8D9" stroke-width="4"/></g><g transform="translate(510 105)"><rect x="-45" y="-30" width="90" height="100" rx="10" fill="#E4A64A"/><rect x="-52" y="-39" width="104" height="15" rx="5" fill="#B77A28"/><path d="M-20-4h40M-20 11h40" stroke="#FFF4D8" stroke-width="7" stroke-linecap="round"/><path d="M-28-60h56l-5 27h-46Z" fill="#FFFFFF" stroke="#BCD6E4" stroke-width="3"/><path d="M-12-48h24" stroke="#79B8D9" stroke-width="4"/></g><g transform="translate(200 180) rotate(-12)"><path d="M-22-15h44v30h-44Z" fill="#FFFDF5" stroke="#D2C6A8" stroke-width="2"/><path d="M-12-5h24M-12 2h24M-12 9h16" stroke="#8DA7A0" stroke-width="2"/></g><g transform="translate(420 177) rotate(15)"><rect x="-14" y="-27" width="28" height="54" rx="8" fill="#F6A17D" stroke="#D47C5B" stroke-width="3"/><rect x="-8" y="-35" width="16" height="9" rx="2" fill="#D47C5B"/><path d="M-8-3h16" stroke="#FFE2D6" stroke-width="3"/></g></svg>'''
REUSE = '''<svg viewBox="0 0 620 245" xmlns="http://www.w3.org/2000/svg"><rect width="620" height="245" rx="18" fill="#F0FBEA"/><circle cx="310" cy="111" r="80" fill="#D7F1CB"/><g transform="translate(220 98)"><path d="M-34-28h68l-6 85h-56Z" fill="#F1A36D" stroke="#C97C4A" stroke-width="4"/><path d="M-39-35h78v13h-78Z" fill="#D97D4D"/><path d="M0-28v-45m0 18c-30 0-38-18-35-31 24 1 35 13 35 31m0-6c27 0 36-18 33-30-22 1-33 13-33 30" fill="#68BE70" stroke="#2B8B58" stroke-width="5" stroke-linecap="round"/></g><path d="M300 105h65" stroke="#F0B84D" stroke-width="8" stroke-linecap="round"/><path d="M349 88l18 17-18 17" fill="none" stroke="#F0B84D" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><g transform="translate(420 100)"><path d="M-32-20h64l-6 76h-52Z" fill="#D5E8F0" stroke="#6FA7BA" stroke-width="4"/><path d="M-36-28h72v13h-72Z" fill="#6FA7BA"/><path d="M-21 5h42M-21 18h42" stroke="#A1D3E1" stroke-width="5" stroke-linecap="round"/><path d="M0-20v-35m0 13c-24 0-30-14-28-24 19 1 28 10 28 24m0-4c22 0 29-14 27-23-18 1-27 10-27 23" fill="#4EA76B" stroke="#2A8756" stroke-width="4"/></g><path d="M0 198Q160 174 310 199T620 195V245H0Z" fill="#9DD68C"/></svg>'''

MISSIONS = [
 {"id":"sort-paper","stage":1,"title":"مهمة فرز المخلفات","scene":SORTING,"q":"وجدتِ ورقة رسم قديمة لم تعودي تحتاجينها، لكنها نظيفة وجافة. ما التصرف الأفضل إذا كانت مدرستك تجمع الورق لإعادة تدويره؟","options":["أضعها في حاوية الورق المخصصة","أرميها في الحديقة بين النباتات","أضعها مع بقايا الطعام"],"answer":"أضعها في حاوية الورق المخصصة","why":"الورق النظيف والجاف يمكن جمعه وإرساله لإعادة التدوير، بدل تلويث المكان أو خلطه ببقايا الطعام."},
 {"id":"bottle","stage":1,"title":"مهمة العبوة البلاستيكية","scene":SORTING,"q":"انتهى الماء في عبوة بلاستيكية. قبل وضعها في حاوية التدوير، ما التصرف الأنسب؟","options":["أترك بداخلها الماء وأغلقها بإحكام","أتأكد من تعليمات الفرز المحلية وأفرغها من السوائل","أدفنها في تربة الحديقة"],"answer":"أتأكد من تعليمات الفرز المحلية وأفرغها من السوائل","why":"اتباع تعليمات الفرز وإفراغ السوائل يساعد على تجهيز العبوة للتدوير. لا تُدفن المخلفات في التربة."},
 {"id":"reuse-pot","stage":2,"title":"مهمة العبوة ذات الفائدة الجديدة","scene":REUSE,"q":"لديك عبوة بلاستيكية متينة ونظيفة، وتريدين صنع شيء يفيد حديقة الصف. أي فكرة تعطيها استخدامًا جديدًا؟","options":["أستخدمها أصيصًا بعد تجهيزها بأمان وبمساعدة المعلمة","أحرقها لتصبح أصغر","أرميها في مجرى الماء"],"answer":"أستخدمها أصيصًا بعد تجهيزها بأمان وبمساعدة المعلمة","why":"إعادة الاستخدام تعني الاستفادة من الغرض مرة أخرى. ويجب أن يجهز الكبار العبوة بطريقة آمنة."},
 {"id":"litter","stage":2,"title":"مهمة الحديقة النظيفة","scene":CITY,"q":"في نزهة، لاحظتِ غلافًا على العشب قرب مكان جلوس العائلة. ما القرار الذي يحافظ على المكان ويشجع الآخرين؟","options":["أتركه لأن شخصًا آخر سيراه","ألتقطه إن كان آمنًا وأضعه في الحاوية المناسبة، أو أطلب مساعدة شخص بالغ","أدفعه تحت الشجيرة حتى لا يظهر"],"answer":"ألتقطه إن كان آمنًا وأضعه في الحاوية المناسبة، أو أطلب مساعدة شخص بالغ","why":"المحافظة على الأماكن العامة مسؤولية مشتركة. لا نلمس المخلفات الحادة أو المجهولة، بل نطلب مساعدة شخص بالغ."},
 {"id":"water","stage":3,"title":"مهمة حماية الماء","scene":CITY,"q":"لاحظتِ أن صنبور الماء في الحديقة يقطر بعد انتهاء الري. ما الخطوة الأفضل للمحافظة على مورد مهم في وطننا؟","options":["أخبر المعلمة أو شخصًا بالغًا ليغلقه أو يصلحه","أتركه لأن الماء يتجدد دائمًا","أفتح صنبورًا آخر"],"answer":"أخبر المعلمة أو شخصًا بالغًا ليغلقه أو يصلحه","why":"ترشيد الماء يحافظ على مورد مهم، وإخبار شخص بالغ يساعد على معالجة التسرب بأمان."},
 {"id":"fair-sort","stage":3,"title":"مهمة المحقق البيئي","scene":SORTING,"q":"وجد الفريق ورقًا نظيفًا وعلبة طعام عليها بقايا كثيرة. لماذا لا نضع كل الأشياء في حاوية الورق؟","options":["لأن بقايا الطعام قد تلوث الورق وتؤثر في إعادة تدويره","لأن الورق لا يمكن تدويره أبدًا","لأن الحاويات للزينة فقط"],"answer":"لأن بقايا الطعام قد تلوث الورق وتؤثر في إعادة تدويره","why":"الفرز الصحيح مهم؛ فالمواد الملوثة قد لا تصلح لعملية التدوير. نتبع دائمًا تعليمات الحاويات المحلية."},
 {"id":"community","stage":4,"title":"مهمة مملكة أجمل","scene":CITY,"q":"أراد الصف تنظيم مبادرة تجعل الحي أجمل وتستمر فائدتها. أي خطة تجمع أكثر من طريقة للمحافظة على الوطن؟","options":["حملة فرز آمنة، وتقليل الهدر، وتوعية الأسر، والمحافظة على الحدائق","تنظيف مكان واحد ثم رمي المخلفات في مكان آخر","استخدام أشياء جديدة دائمًا ورمي كل ما يُستعمل مرة واحدة"],"answer":"حملة فرز آمنة، وتقليل الهدر، وتوعية الأسر، والمحافظة على الحدائق","why":"المبادرة الأفضل تجمع بين تقليل النفايات والفرز الصحيح وإعادة الاستخدام والتعاون للحفاظ على الممتلكات العامة."},
]

if "scores" not in st.session_state: st.session_state.scores = {n:0 for n in CHILDREN}
if "completed" not in st.session_state: st.session_state.completed = {n:[] for n in CHILDREN}
if "history" not in st.session_state: st.session_state.history = []
if "city_points" not in st.session_state: st.session_state.city_points = 0
if "last_result" not in st.session_state: st.session_state.last_result = None
# Ensure fixed names remain present after updates/restarts in the session.
for n in CHILDREN:
    st.session_state.scores.setdefault(n, 0)
    st.session_state.completed.setdefault(n, [])

st.markdown(f'''<div class="hero" dir="rtl"><span class="eyebrow">مغامرة تفاعلية · أسرة الزهراء</span><h1>مملكتي أجمل</h1><p>مهمتك أن تساعد مدينتك على أن تصبح أنظف وأكثر خضرة. اتخذ قرارات ذكية، وتعلّم كيف نحافظ على وطننا بإعادة التدوير وتقليل الهدر.</p><div class="hero-art">{CITY}</div></div>''', unsafe_allow_html=True)
st.write("")

play_tab, city_tab, teacher_tab = st.tabs(["مغامرة أبطال البيئة", "مدينتي تتغير", "متابعة المعلمة"])

with play_tab:
    st.markdown('<div class="section-title" dir="rtl">اختيار المستكشف أو المستكشفة</div>', unsafe_allow_html=True)
    st.caption("أسماء أطفال أسرة الزهراء ثابتة ومضافة مسبقًا. اختاري اسم الطفل قبل بدء التحدي حتى تُسجّل النقاط باسمه الصحيح.")
    # Use a large, readable dropdown and repeat the selected name in a dedicated name card.
    chosen = st.selectbox("اسم الطفل / الطفلة", CHILDREN, key="fixed_child", format_func=lambda x: x)
    score = st.session_state.scores[chosen]
    st.markdown(f'<div class="child-card" dir="rtl"><div class="subtle">المستكشف الحالي</div><div class="child-name">{chosen}</div><div class="score-pill">{score} نقطة شخصية</div></div>', unsafe_allow_html=True)
    st.write("")
    completed = st.session_state.completed[chosen]
    available = [m for m in MISSIONS if m["id"] not in completed]
    city_points = st.session_state.city_points
    city_stage = 1 if city_points < 2 else 2 if city_points < 4 else 3 if city_points < 6 else 4
    stage_titles = ["بداية التغيير", "الحديقة تستعيد جمالها", "المدينة تزداد خضرة", "مملكة أجمل للجميع"]
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("نقاط هذا الطفل", score)
    with c2: st.metric("تحديات مكتملة", len(completed))
    with c3: st.metric("إنجازات الفصل", city_points)
    st.progress(min(len(completed)/len(MISSIONS),1.0), text=f"تقدم {chosen}: {len(completed)} من {len(MISSIONS)} مهام")
    if not available:
        st.success(f"أحسنت يا {chosen}! أكملت جميع مغامرات مملكتي أجمل.")
        st.markdown('<div class="panel" dir="rtl"><div class="section-title">بطل / بطلة البيئة</div><p>اذكر للمعلمة ثلاث طرق تحافظ بها على وطنك: مثل فرز المواد القابلة للتدوير، وإعادة استخدام الأشياء بأمان، والمحافظة على نظافة الأماكن العامة وترشيد الماء.</p></div>', unsafe_allow_html=True)
        if st.button("إعادة مهام هذا الطفل", use_container_width=True):
            st.session_state.completed[chosen] = []
            st.session_state.last_result = None
            st.rerun()
    else:
        # Missions unlock gradually using classroom-wide progress; keep the first two available at start.
        unlocked = [m for m in available if m["stage"] <= city_stage]
        if not unlocked: unlocked = available
        mission = unlocked[0]
        st.markdown('<div class="mission" dir="rtl">', unsafe_allow_html=True)
        st.markdown(f'<div class="subtle">المرحلة {mission["stage"]} · تحدي أبطال البيئة</div><div class="section-title">{mission["title"]}</div><div class="artbox">{mission["scene"]}</div><div class="question">{mission["q"]}</div>', unsafe_allow_html=True)
        with st.form(key=f"mission_{chosen}_{mission['id']}"):
            answer = st.radio("اختاري القرار الأفضل:", mission["options"], index=None)
            submit = st.form_submit_button("اعتماد القرار", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if submit:
            if answer is None:
                st.warning("اختاري إجابة قبل اعتماد القرار.")
            else:
                correct = answer == mission["answer"]
                st.session_state.completed[chosen].append(mission["id"])
                if correct:
                    st.session_state.scores[chosen] += 1
                    st.session_state.city_points += 1
                st.session_state.last_result = {"child":chosen,"correct":correct,"answer":mission["answer"],"why":mission["why"],"title":mission["title"]}
                st.session_state.history.append({"الوقت":datetime.now().strftime("%Y-%m-%d %H:%M"),"اسم الطفل":chosen,"المهمة":mission["title"],"إجابة الطفل":answer,"النتيجة":"صحيح" if correct else "يحتاج إلى مراجعة"})
                st.rerun()
    if st.session_state.last_result:
        r = st.session_state.last_result
        if r["correct"]:
            st.success(f"قرار رائع يا {r['child']}! لقد ساعدتَ مملكتك على أن تصبح أجمل.")
        else:
            st.info(f"محاولة جيدة يا {r['child']}! نراجع الفكرة معًا ثم نحاول في تحدٍ جديد.")
        st.markdown(f'<div class="panel" dir="rtl"><div class="section-title">لنتعلم من القرار</div><p><b>القرار الأفضل:</b> {r["answer"]}</p><p>{r["why"]}</p></div>', unsafe_allow_html=True)
        if st.button("متابعة المغامرة", use_container_width=True):
            st.session_state.last_result = None
            st.rerun()

with city_tab:
    points = st.session_state.city_points
    stage = 1 if points < 2 else 2 if points < 4 else 3 if points < 6 else 4
    st.markdown(f'<div class="panel" dir="rtl" style="text-align:center"><div class="section-title">{stage_titles[stage-1]}</div><div class="artbox">{CITY}</div><p>كل قرار صحيح يضيف إنجازًا إلى مغامرة الفصل. تعاونوا لتصلوا إلى مملكة أنظف وأكثر خضرة.</p><div class="child-name">{points} إنجازات للفصل</div></div>', unsafe_allow_html=True)
    st.write("")
    stages = [(0,"بداية التغيير","نتعلم كيف نفرز المخلفات ونحافظ على المكان."),(2,"حديقة أنظف","نقلل المخلفات ونضعها في المكان المناسب."),(4,"مدينة أكثر خضرة","نعيد استخدام الأشياء ونحافظ على الماء."),(6,"مملكة أجمل","نشارك أفكارنا ونشجع الآخرين على حماية وطننا.")]
    cols = st.columns(4)
    for col,(target,title,desc) in zip(cols,stages):
        with col:
            reached = points >= target
            st.markdown(f'<div class="panel" style="text-align:center;min-height:180px"><div class="section-title">{title}</div><div style="font-size:1.8rem;font-weight:900;color:{"#16845d" if reached else "#9aaea5"}">{"مفتوحة" if reached else "قريبًا"}</div><p class="subtle">{desc}</p></div>', unsafe_allow_html=True)

with teacher_tab:
    st.markdown('<div class="section-title" dir="rtl">قائمة أطفال أسرة الزهراء</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel" dir="rtl"><p>الأسماء ثابتة ولا تحتاج المعلمة إلى إضافتها. تظهر في قائمة اختيار المستكشف، ويُعرض الاسم المختار بخط كبير قبل بدء كل تحدٍ.</p></div>', unsafe_allow_html=True)
    # Show each fixed name as a visible tile, so no child is hidden in a list.
    cols = st.columns(2)
    for i, child in enumerate(CHILDREN):
        with cols[i % 2]:
            st.markdown(f'<div class="child-card" dir="rtl" style="margin:5px 0"><div class="child-name">{child}</div><div class="score-pill">{st.session_state.scores[child]} نقطة</div></div>', unsafe_allow_html=True)
    st.write("")
    rows = []
    for child in CHILDREN:
        rows.append({"اسم الطفل":child,"النقاط":st.session_state.scores[child],"المهام المكتملة":len(st.session_state.completed[child])})
    st.dataframe(rows, use_container_width=True, hide_index=True)
    export = {"scores":st.session_state.scores,"completed":st.session_state.completed,"history":st.session_state.history,"city_points":st.session_state.city_points,"exported_at":datetime.now().isoformat(timespec="minutes")}
    st.download_button("تنزيل نسخة احتياطية للنتائج", data=json.dumps(export,ensure_ascii=False,indent=2), file_name="mamlakati-ajmal-backup.json", mime="application/json", use_container_width=True)
    uploaded = st.file_uploader("استعادة نتائج محفوظة", type=["json"])
    if uploaded is not None and st.button("استعادة النسخة الاحتياطية", use_container_width=True):
        try:
            data = json.load(uploaded)
            for child in CHILDREN:
                st.session_state.scores[child] = int(data.get("scores",{}).get(child,0))
                st.session_state.completed[child] = data.get("completed",{}).get(child,[])
            st.session_state.history = data.get("history",[])
            st.session_state.city_points = int(data.get("city_points",0))
            st.session_state.last_result = None
            st.success("تمت استعادة النتائج.")
            st.rerun()
        except Exception:
            st.error("تعذر قراءة الملف. تأكدي أنه نسخة احتياطية من لعبة مملكتي أجمل.")
    confirm = st.checkbox("أؤكد أنني أريد تصفير جميع النتائج")
    if st.button("تصفير النتائج", use_container_width=True):
        if confirm:
            st.session_state.scores = {n:0 for n in CHILDREN}
            st.session_state.completed = {n:[] for n in CHILDREN}
            st.session_state.history = []
            st.session_state.city_points = 0
            st.session_state.last_result = None
            st.rerun()
        else:
            st.warning("حددي مربع التأكيد أولًا.")
    if st.session_state.history:
        st.markdown("#### سجل الإجابات")
        st.dataframe(list(reversed(st.session_state.history)), use_container_width=True, hide_index=True)

st.markdown('<div style="text-align:center;color:#658177;padding:22px" dir="rtl">مملكتي أجمل · نعيد الاستخدام، نفرز المخلفات، ونحافظ على وطننا.</div>', unsafe_allow_html=True)
