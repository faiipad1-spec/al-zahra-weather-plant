import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="أسرة الزهراء | مستكشفو الطقس والنبات", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# تصميم عربي واضح مع رسومات SVG أصلية بدل الإيموجي.
CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Tajawal:wght@400;500;700;800&display=swap');
:root { --ink:#183b35; --green:#2d7961; --mint:#dff5e8; --yellow:#ffd66b; --blue:#dff2ff; --coral:#ff9c86; --cream:#fffaf0; }
html, body, [class*="css"] { font-family:'Tajawal','Almarai',sans-serif; }
.stApp { background:linear-gradient(180deg,#eaf7ff 0%,#f5fff6 45%,#fff9ed 100%); color:var(--ink); }
.block-container { max-width:1180px; padding-top:1.2rem; padding-bottom:3rem; }
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
.hero { background:linear-gradient(120deg,#176c65 0%,#2d9276 48%,#a8d86b 100%); border-radius:28px; padding:28px 30px; color:white; position:relative; overflow:hidden; box-shadow:0 12px 30px #235f4b22; }
.hero h1 {font-size:clamp(2rem,4vw,3.4rem); font-weight:800; margin:0; line-height:1.35; color:white;}
.hero p {font-size:1.2rem; margin:.35rem 0 0; color:#f0fff5;}
.hero-art {position:absolute; left:2%; top:3%; width:190px; max-width:30%; opacity:.98;}
.pill {display:inline-block;background:#ffffff26;border:1px solid #ffffff55;border-radius:999px;padding:5px 13px;font-size:.95rem;margin-bottom:12px;}
.section-title {font-size:1.45rem;font-weight:800;color:#1d5547;margin:.25rem 0 .7rem;}
.panel {background:#ffffffd9;border:1px solid #d8e9df;border-radius:22px;padding:20px;box-shadow:0 6px 20px #245a4310;}
.question-card {background:white;border:2px solid #d8eadf;border-radius:24px;padding:24px;box-shadow:0 12px 30px #174b3b12;}
.question-kicker {font-weight:800;color:#2d7961;font-size:1rem;}
.question-text {font-size:clamp(1.35rem,2.5vw,2rem);font-weight:800;line-height:1.7;color:#173d35;margin:.6rem 0 1rem;}
.scene {border-radius:20px;background:linear-gradient(135deg,#dff4ff,#f3ffe8);padding:10px;display:flex;justify-content:center;align-items:center;min-height:155px;margin-bottom:12px;}
.scene svg {width:100%;max-width:510px;height:auto;max-height:210px;}
.stButton>button, .stDownloadButton>button {border-radius:15px!important;border:0!important;background:linear-gradient(100deg,#237d66,#55a878)!important;color:white!important;font-family:'Tajawal',sans-serif!important;font-weight:800!important;font-size:1.05rem!important;padding:.7rem 1rem!important;box-shadow:0 5px 14px #1f76551f!important;}
.stButton>button:hover,.stDownloadButton>button:hover {filter:brightness(1.04);transform:translateY(-1px);}
.stRadio [role="radiogroup"] {gap:9px;}
.stRadio [role="radiogroup"] label {background:#f7fbf8;border:1px solid #d8e8dd;border-radius:14px;padding:10px 13px;}
.stRadio [role="radiogroup"] label:has(input:checked) {background:#e0f5e7;border-color:#4b9b78;}
.stTabs [data-baseweb="tab-list"] {gap:8px;background:#e8f4ec;padding:7px;border-radius:16px;}
.stTabs [data-baseweb="tab"] {border-radius:12px;padding:10px 16px;font-weight:800;}
.stTabs [aria-selected="true"] {background:white!important;color:#1d6b53!important;}
.stProgress > div > div > div > div {background:linear-gradient(90deg,#55a878,#f3c95e);}
.metric-card {background:#fff;border:1px solid #dcebe1;border-radius:18px;padding:16px;text-align:center;}
.metric-number {font-size:2rem;font-weight:800;color:#26785f;}
.metric-label {color:#54736a;font-weight:700;}
.small-note {color:#58766d;font-size:.95rem;}
.stAlert {border-radius:16px;}
@media(max-width:700px){.hero{padding:22px 18px}.hero-art{opacity:.35;width:140px}.question-card{padding:16px}.block-container{padding-left:1rem;padding-right:1rem}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Illustrations are hand-authored vector scenes; no emoji characters are used in the game UI.
SCENES = {
 "clouds": '''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg"><circle cx="420" cy="35" r="23" fill="#FFD56A"/><g stroke="#e8b949" stroke-width="4" stroke-linecap="round"><path d="M420 3v-8M420 68v8M388 35h-8M452 35h8M397 12l-6-6M443 58l6 6M443 12l6-6M397 58l-6 6"/></g><path d="M0 150 Q80 115 160 150 T320 145 T520 140 V190 H0Z" fill="#a8d98c"/><path d="M85 76c0-18 15-32 34-32 14 0 26 8 31 20 5-4 11-6 18-6 18 0 32 14 32 32s-14 32-32 32H118c-19 0-33-14-33-32 0-5 0-9 0-14Z" fill="#fff" stroke="#b9d9e5" stroke-width="3"/><path d="M110 129l-8 18M143 129l-8 18M176 129l-8 18" stroke="#55a8d8" stroke-width="5" stroke-linecap="round"/><path d="M315 151v-46m0 17c-24-3-31-19-31-30 21 0 31 13 31 30m0 8c20-2 29-17 29-28-19 0-29 12-29 28" stroke="#287a58" stroke-width="7" stroke-linecap="round" fill="none"/><path d="M280 153h72" stroke="#9a6947" stroke-width="8" stroke-linecap="round"/></svg>''',
 "plant": '''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="130" width="520" height="60" rx="15" fill="#b9875b"/><path d="M0 130Q80 115 160 130T320 130T520 126V145H0Z" fill="#8c694b"/><path d="M260 133V54" stroke="#32865b" stroke-width="9" stroke-linecap="round"/><path d="M256 94C208 94 187 66 188 43c39 0 68 20 68 51" fill="#60b96f" stroke="#2e8959" stroke-width="3"/><path d="M264 77C303 77 329 53 329 28c-38 0-65 19-65 49" fill="#83ce75" stroke="#2e8959" stroke-width="3"/><path d="M232 135l-17 28m45-28 16 28m-43-28-3 29" stroke="#f1d1a1" stroke-width="5" stroke-linecap="round"/><circle cx="260" cy="40" r="17" fill="#ffd66b"/><circle cx="260" cy="40" r="7" fill="#e98a62"/><path d="M250 17l-4-8m25 8 5-8m8 26 9-2m-66 2-9-2m42 30 1 9" stroke="#e8a844" stroke-width="4" stroke-linecap="round"/></svg>''',
 "sun": '''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg"><circle cx="260" cy="72" r="38" fill="#ffd45e"/><g stroke="#f2b942" stroke-width="5" stroke-linecap="round"><path d="M260 15V4M260 129v-10M203 72h-12M329 72h-12M220 32l-8-8M300 112l8 8M300 32l8-8M220 112l-8 8"/></g><path d="M0 150Q100 120 200 150T400 146T520 145V190H0Z" fill="#9bd68b"/><path d="M95 153v-36m0 14c-19-1-26-14-26-25 17 0 26 10 26 25m0 7c17-2 25-14 25-24-16 0-25 10-25 24" stroke="#34895e" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M80 155h31" stroke="#9a6947" stroke-width="7" stroke-linecap="round"/><path d="M390 153v-36m0 14c-19-1-26-14-26-25 17 0 26 10 26 25m0 7c17-2 25-14 25-24-16 0-25 10-25 24" stroke="#34895e" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M375 155h31" stroke="#9a6947" stroke-width="7" stroke-linecap="round"/></svg>''',
 "garden": '''<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg"><path d="M0 140Q90 100 180 140T360 136T520 135V190H0Z" fill="#9ed98a"/><path d="M0 164Q100 142 210 164T420 160T520 158V190H0Z" fill="#69b979"/><g transform="translate(130 85)"><path d="M0 55V0" stroke="#29845a" stroke-width="7" stroke-linecap="round"/><path d="M-2 26C-40 25-48 3-46-12-18-11-2 5-2 26" fill="#57b86e"/><path d="M2 13C32 12 44-6 42-22 16-21 2-7 2 13" fill="#7acb73"/><circle cx="0" cy="-12" r="12" fill="#ff9d8a"/><circle cx="0" cy="-12" r="4" fill="#ffd66b"/><path d="M-20 56h40" stroke="#9a6947" stroke-width="7" stroke-linecap="round"/></g><g transform="translate(270 100)"><path d="M0 45V0" stroke="#29845a" stroke-width="7" stroke-linecap="round"/><path d="M0 22C-32 22-40 4-38-10-14-9 0 5 0 22" fill="#57b86e"/><path d="M0 10C28 10 38-7 36-20 13-19 0-5 0 10" fill="#7acb73"/><circle cx="0" cy="-14" r="12" fill="#b49bea"/><circle cx="0" cy="-14" r="4" fill="#ffd66b"/><path d="M-18 46h36" stroke="#9a6947" stroke-width="7" stroke-linecap="round"/></g><g transform="translate(390 76)"><path d="M0 70V0" stroke="#29845a" stroke-width="9" stroke-linecap="round"/><path d="M-1 35C-43 34-56 9-52-9-21-8-1 10-1 35" fill="#48a966"/><path d="M2 21C39 20 55-5 50-22 20-21 2-3 2 21" fill="#72c66d"/><circle cx="0" cy="-15" r="15" fill="#ffb4a5"/><circle cx="0" cy="-15" r="5" fill="#ffd66b"/><path d="M-22 71h44" stroke="#9a6947" stroke-width="8" stroke-linecap="round"/></g></svg>'''
}

QUESTIONS = [
 {"level":1,"title":"مراقبو الطبيعة","topic":"ملاحظة الطقس","scene":"clouds","q":"في صورتين للحديقة، لاحظت أن ملابس الغسيل تتحرك والأغصان تميل في الاتجاه نفسه. ما التفسير الأفضل؟","options":["الهواء يتحرك في صورة رياح","النباتات تشرب الماء من الهواء","الشمس اختفت إلى الأبد","التربة أصبحت أخف"],"answer":"الهواء يتحرك في صورة رياح","why":"حركة الأشياء الخفيفة وميل الأغصان في اتجاه واحد دليل على حركة الهواء."},
 {"level":1,"title":"مراقبو الطبيعة","topic":"أجزاء النبات","scene":"plant","q":"عند إخراج نبتة صغيرة من أصيصها برفق، وجدنا خيوطًا دقيقة داخل التربة. ما الوظيفة الأهم لهذه الأجزاء؟","options":["امتصاص الماء والمساعدة على تثبيت النبتة","صنع ضوء الشمس","جذب المطر إلى السماء","تحويل التربة إلى أوراق"],"answer":"امتصاص الماء والمساعدة على تثبيت النبتة","why":"الجذور تمتص الماء والأملاح من التربة وتساعد على تثبيت النبات."},
 {"level":1,"title":"مراقبو الطبيعة","topic":"احتياجات النبات","scene":"sun","q":"نبتة قرب النافذة تنمو جيدًا، وأخرى في خزانة مغلقة لا تنمو مثلها رغم سقيهما. أي فرق يستحق أن نتحقق منه أولًا؟","options":["كمية الضوء التي تصل لكل نبتة","لون الأصيص فقط","اسم النبتة","عدد الألعاب في الغرفة"],"answer":"كمية الضوء التي تصل لكل نبتة","why":"الضوء عامل مهم لنمو كثير من النباتات، ومن المفيد مقارنة ما يصل إلى كل نبتة."},
 {"level":1,"title":"مراقبو الطبيعة","topic":"الماء والتربة","scene":"plant","q":"صببنا قليلًا من الماء على تربة جافة، وبعد لحظات أصبح لونها أغمق وملمسها رطبًا. ماذا تخبرنا الملاحظة؟","options":["الماء دخل بين حبيبات التربة","التربة صنعت بذورًا","الماء تحول إلى ضوء","الجذور نمت فورًا"],"answer":"الماء دخل بين حبيبات التربة","why":"تتغير ملامح التربة عندما تمتص الماء؛ أما نمو الجذور فيحتاج إلى وقت."},
 {"level":1,"title":"مراقبو الطبيعة","topic":"الطقس","scene":"clouds","q":"تريد المعلمة معرفة أي يوم كان أدفأ. ما المعلومة الأكثر فائدة للمقارنة؟","options":["قراءة مقياس الحرارة في اليومين","عدد السيارات في الشارع","لون حقيبة المعلمة","عدد أوراق الشجرة"],"answer":"قراءة مقياس الحرارة في اليومين","why":"مقياس الحرارة يساعدنا على مقارنة درجة الحرارة بدل الاعتماد على التخمين."},
 {"level":2,"title":"باحثو الحديقة","topic":"حل مشكلة نبات","scene":"plant","q":"نبتة أوراقها متدلية، لكن التربة ما زالت مبللة جدًا. ما الخطوة الأذكى قبل إضافة مزيد من الماء؟","options":["أفحص رطوبة التربة وأتأكد أن الماء الزائد يستطيع التصريف","أسقيها فورًا مرة أخرى","أضعها في خزانة مظلمة","أقطع كل الأوراق"],"answer":"أفحص رطوبة التربة وأتأكد أن الماء الزائد يستطيع التصريف","why":"ذبول الأوراق لا يعني دائمًا نقص الماء؛ فزيادة الماء قد تضر الجذور أيضًا."},
 {"level":2,"title":"باحثو الحديقة","topic":"توقع الطقس","scene":"clouds","q":"تجمعت غيوم داكنة وبدأ الهواء يبرد. أي قرار عملي مناسب قبل الخروج إلى الحديقة؟","options":["أراجع حالة الطقس وأجهز ما يلزم إذا نزل المطر","أقرر أن المطر مستحيل","أروي الحديقة بغزارة مهما حدث","أزرع كل البذور فورًا"],"answer":"أراجع حالة الطقس وأجهز ما يلزم إذا نزل المطر","why":"الملاحظات تساعدنا على التوقع، لكن الأفضل جمع معلومات إضافية قبل اتخاذ القرار."},
 {"level":2,"title":"باحثو الحديقة","topic":"النمو والضوء","scene":"sun","q":"وُضعت نبتة قرب نافذة، وبعد أيام مال ساقها نحو النافذة. ما التفسير الأقرب؟","options":["الساق تستجيب لاتجاه الضوء","النبتة تحاول الهرب من الأصيص","الماء يدفع الساق أفقيًا دائمًا","الهواء يحول الساق إلى جذر"],"answer":"الساق تستجيب لاتجاه الضوء","why":"يمكن أن تنمو السيقان باتجاه مصدر الضوء؛ وتُسمى هذه الاستجابة الانتحاء الضوئي."},
 {"level":2,"title":"باحثو الحديقة","topic":"المطر والتربة","scene":"clouds","q":"بعد مطر قوي، لاحظنا بركة ماء بقيت فوق التربة مدة طويلة. ما السؤال الأفضل لفهم السبب؟","options":["هل التربة مضغوطة أو لا تسمح بتصريف الماء جيدًا؟","هل لون الزهرة جميل؟","هل الشمس بعيدة جدًا عن الأرض؟","هل تحتاج النبتة إلى ألعاب؟"],"answer":"هل التربة مضغوطة أو لا تسمح بتصريف الماء جيدًا؟","why":"قد يتجمع الماء عندما يكون تصريف التربة ضعيفًا أو تكون الأرض مشبعة بالماء."},
 {"level":2,"title":"باحثو الحديقة","topic":"ترشيد الماء","scene":"garden","q":"لدينا أصيصان: تربة الأول جافة والثاني لا تزال رطبة. كيف نستخدم الماء بحكمة؟","options":["أفحص كل أصيص وأسقي عند الحاجة فقط","أعطيهما الكمية نفسها دائمًا","أترك الخرطوم مفتوحًا","لا أسقي أي نبات طوال الشهر"],"answer":"أفحص كل أصيص وأسقي عند الحاجة فقط","why":"احتياج النباتات للماء قد يختلف؛ ففحص التربة يساعد على تجنب الإسراف والإفراط في الري."},
 {"level":3,"title":"محقّقو الطبيعة","topic":"تجربة عادلة","scene":"plant","q":"نريد اختبار أثر الضوء في نمو النبات. أي خطة تعطينا مقارنة أوضح؟","options":["نستخدم نبتتين متشابهتين ونغيّر الضوء فقط قدر الإمكان","نغيّر الضوء والماء ونوع التربة معًا","نستخدم نبتة مختلفة لكل يوم","نقرر النتيجة قبل بدء التجربة"],"answer":"نستخدم نبتتين متشابهتين ونغيّر الضوء فقط قدر الإمكان","why":"عندما نغيّر عاملًا واحدًا ونثبت بقية العوامل قدر الإمكان، تصبح المقارنة أوضح."},
 {"level":3,"title":"محقّقو الطبيعة","topic":"الحرارة والتبخر","scene":"sun","q":"وضعت المعلمة كميتين متساويتين من الماء في طبقين، أحدهما في مكان دافئ والآخر في مكان أبرد. ما المتوقع بعد مدة، إذا بقيت الظروف الأخرى متشابهة؟","options":["قد يتبخر ماء الطبق الدافئ أسرع","سيزداد الماء في الطبق الدافئ من دون مصدر","سيتحول الماء إلى تربة","لن يتغير أي طبق أبدًا"],"answer":"قد يتبخر ماء الطبق الدافئ أسرع","why":"ارتفاع الحرارة قد يزيد سرعة التبخر، إذا كانت بقية الظروف متقاربة."},
 {"level":3,"title":"محقّقو الطبيعة","topic":"قراءة الدليل","scene":"garden","q":"وجدنا ورقة صفراء واحدة على نبتة، وبقية الأوراق خضراء. ما الاستنتاج الأكثر حذرًا؟","options":["نحتاج إلى فحص النبتة ومتابعتها قبل الحكم على صحتها","النبتة ماتت بالتأكيد","كل النباتات في الحديقة مريضة","الطقس ممطر حتمًا"],"answer":"نحتاج إلى فحص النبتة ومتابعتها قبل الحكم على صحتها","why":"ملاحظة واحدة لا تكفي دائمًا؛ نجمع أدلة أخرى مثل رطوبة التربة وبقية الأوراق."},
 {"level":3,"title":"محقّقو الطبيعة","topic":"تغير الطقس","scene":"clouds","q":"سجلت المعلمة درجات الحرارة ثلاثة أيام: 29، ثم 25، ثم 22. ما الوصف الذي تدعمه الأرقام؟","options":["درجة الحرارة انخفضت خلال الأيام الثلاثة","درجة الحرارة ارتفعت كل يوم","الأيام الثلاثة متساوية الحرارة","ستُمطر بالتأكيد غدًا"],"answer":"درجة الحرارة انخفضت خلال الأيام الثلاثة","why":"نصف ما تظهره البيانات مباشرة، ولا نستنتج منها أمورًا لا تثبتها مثل حتمية المطر."},
 {"level":3,"title":"محقّقو الطبيعة","topic":"الرياح والنبات","scene":"garden","q":"بعد ليلة عاصفة، مالت إحدى الشتلات بينما بقيت الأخرى مستقيمة خلف حاجز. ما العامل الذي قد يفسر الفرق؟","options":["تعرض الشتلتين لدرجات مختلفة من قوة الرياح","لون أوراقهما وحده","عدد الأيام في الأسبوع","شكل السحب في صورة قديمة"],"answer":"تعرض الشتلتين لدرجات مختلفة من قوة الرياح","why":"الحاجز قد يقلل قوة الرياح التي تصل إلى الشتلة ويحميها من الانحناء."},
 {"level":4,"title":"خبراء أسرة الزهراء","topic":"تخطيط الحديقة","scene":"garden","q":"تنتظر الحديقة أسبوعًا حارًا قليل المطر. أي خطة تجمع أفضل بين حماية النباتات وترشيد الماء؟","options":["فحص التربة، والري عند الحاجة، ووضع غطاء للتربة لتقليل فقد الماء","ري جميع النباتات طوال النهار بلا توقف","منع الماء عن النباتات حتى تذبل","نقل كل النباتات إلى الظلام"],"answer":"فحص التربة، والري عند الحاجة، ووضع غطاء للتربة لتقليل فقد الماء","why":"الري عند الحاجة وتقليل تبخر الماء من التربة يساعدان النباتات ويقللان الهدر."},
 {"level":4,"title":"خبراء أسرة الزهراء","topic":"تصميم تجربة","scene":"plant","q":"اختلف طفلان: أحدهما يقول إن النبتة تنمو بسبب الماء فقط، والآخر يقول إن الضوء مهم أيضًا. كيف نختبر الفكرة؟","options":["نقارن نباتات متشابهة مع توفير الماء للجميع وتغيير الضوء فقط","نحجب الماء والضوء عن كل النباتات","نختار رأي الطفل الأكبر مباشرة","نراقب زهرة بلا تسجيل أي شيء"],"answer":"نقارن نباتات متشابهة مع توفير الماء للجميع وتغيير الضوء فقط","why":"التجربة المنصفة تختبر عاملًا محددًا وتُبقي العوامل الأخرى متشابهة قدر الإمكان."},
 {"level":4,"title":"خبراء أسرة الزهراء","topic":"الاستدلال من البيانات","scene":"sun","q":"سجلنا نمو نبتتين خلال أسبوع: نبتة قرب الضوء زادت 3 سم، وأخرى في الظلام زادت أقل من 1 سم. ما أفضل استنتاج من هذه النتيجة وحدها؟","options":["في هذه التجربة ارتبط الضوء بنمو أكبر، ونحتاج إلى تكرارها للتأكد","ثبت أن كل النباتات تنمو بالطريقة نفسها دائمًا","الظلام أفضل لكل النباتات","الماء لا يؤثر في النمو"],"answer":"في هذه التجربة ارتبط الضوء بنمو أكبر، ونحتاج إلى تكرارها للتأكد","why":"نصف نتيجة التجربة كما ظهرت، ونتجنب التعميم من تجربة واحدة فقط."},
 {"level":4,"title":"خبراء أسرة الزهراء","topic":"حل مشكلة مركبة","scene":"clouds","q":"هطل المطر يومين متتاليين، وأصبحت تربة بعض الأصص مشبعة بالماء. ماذا تفعل المعلمة لحماية النباتات؟","options":["توقف الري مؤقتًا وتتحقق من تصريف الماء وحاجة النباتات","تضيف ماءً أكثر لكل الأصص","تغلق الأصص بإحكام حتى لا يدخلها الهواء","تزيل الأوراق الخضراء كلها"],"answer":"توقف الري مؤقتًا وتتحقق من تصريف الماء وحاجة النباتات","why":"بعد المطر قد لا تحتاج النباتات إلى ري إضافي؛ فحص التربة والتصريف يمنعان تجمع الماء الزائد."},
 {"level":4,"title":"خبراء أسرة الزهراء","topic":"تقييم التوقع","scene":"clouds","q":"توقعنا المطر بسبب الغيوم، لكن اليوم انتهى دون مطر. ماذا يتعلم المستكشف من ذلك؟","options":["التوقع احتمال وليس ضمانًا، ونراجع العلامات والمعلومات المتاحة","كل الغيوم تعني المطر دائمًا","ملاحظات الطقس لا فائدة منها أبدًا","الطقس لا يتغير"],"answer":"التوقع احتمال وليس ضمانًا، ونراجع العلامات والمعلومات المتاحة","why":"التوقع العلمي قابل للمراجعة؛ نستخدم أدلة جديدة لتحسين توقعاتنا القادمة."},
]
LEVELS = {
 1:{"name":"مراقبو الطبيعة","desc":"لاحظوا التفاصيل، وقارنوا المشاهد، واختاروا الدليل المناسب.","need":0,"color":"#d9f3ff"},
 2:{"name":"باحثو الحديقة","desc":"حلوا مشكلات واقعية تخص الطقس والتربة والنبات.","need":3,"color":"#e3f6dc"},
 3:{"name":"محقّقو الطبيعة","desc":"استنتجوا من الأدلة وصمموا مقارنات وتجارب عادلة.","need":6,"color":"#fff0c7"},
 4:{"name":"خبراء أسرة الزهراء","desc":"استخدموا البيانات لاتخاذ قرارات وحل مشكلات مركبة.","need":9,"color":"#fbe0d8"},
}

# أسماء أطفال فصل أسرة الزهراء ثابتة ومضافة مسبقًا.
FIXED_CHILDREN = [
    "نورا خالد", "ميلا", "ملك", "نوال", "أسيل", "منيرة", "ديم",
    "علي محمد", "رشود", "علي الشهراني", "رغد", "مها", "جوزاء", "فهد"
]

for key, default in {"children":FIXED_CHILDREN.copy(),"scores":{},"answered":{},"history":[],"garden_stars":0,"last_result":None}.items():
    if key not in st.session_state: st.session_state[key] = default

# اضمن وجود سجل لكل اسم ثابت حتى لو كانت الجلسة بدأت من نسخة أقدم.
for child in FIXED_CHILDREN:
    if child not in st.session_state.children:
        st.session_state.children.append(child)
    st.session_state.scores.setdefault(child, 0)
    st.session_state.answered.setdefault(child, [])

def get_level(score):
    return 4 if score >= 9 else 3 if score >= 6 else 2 if score >= 3 else 1

def scene_html(name):
    return f'<div class="scene">{SCENES.get(name, SCENES["garden"])}</div>'

def export_data():
    return {"children":st.session_state.children,"scores":st.session_state.scores,"answered":st.session_state.answered,"history":st.session_state.history,"garden_stars":st.session_state.garden_stars,"exported_at":datetime.now().isoformat(timespec="minutes")}

st.markdown(f'''<div class="hero" dir="rtl"><span class="pill">رحلة علمية تفاعلية · عمر 5–6 سنوات</span><h1>مستكشفو الطقس والنبات</h1><p>حديقة أسرة الزهراء تبدأ من سؤال ذكي وملاحظة دقيقة.</p><div class="hero-art">{SCENES['garden']}</div></div>''', unsafe_allow_html=True)
st.write("")

play_tab, garden_tab, teacher_tab = st.tabs(["رحلة المستكشفين", "حديقة أسرة الزهراء", "لوحة المعلمة"])
with play_tab:
    if not st.session_state.children:
        st.markdown('<div class="panel" dir="rtl"><div class="section-title">لنبدأ الرحلة</div><p>أضيفي أسماء الأطفال من لوحة المعلمة، ثم اختاري المستكشف الذي سيحل التحدي.</p></div>', unsafe_allow_html=True)
    else:
        left,right = st.columns([1.7,1], gap="large")
        with left:
            chosen = st.selectbox("اختاري المستكشف", st.session_state.children, key="child_picker")
            score = st.session_state.scores.get(chosen,0)
            level_num = get_level(score); level = LEVELS[level_num]
            st.markdown(f'<div class="panel" dir="rtl"><div class="question-kicker">المحطة {level_num} من 4</div><div class="section-title">{level["name"]}</div><p>{level["desc"]}</p></div>', unsafe_allow_html=True)
            st.progress(min(score/12,1.0), text=f"نقاط {chosen}: {score}")
        with right:
            stars = st.session_state.garden_stars
            stage = 1 if stars < 3 else 2 if stars < 6 else 3 if stars < 10 else 4
            stage_names = ["تجهيز التربة","ظهور البراعم","ازدهار الحديقة","حديقة متكاملة"]
            st.markdown(f'<div class="panel" dir="rtl" style="text-align:center"><div class="question-kicker">تقدم الفصل</div>{SCENES["garden"]}<div class="section-title">{stage_names[stage-1]}</div><p>جمعت أسرة الزهراء <b>{stars}</b> نقطة جماعية.</p></div>', unsafe_allow_html=True)
        eligible = [q for q in QUESTIONS if q["level"] == level_num]
        done = st.session_state.answered.get(chosen,[])
        available = [q for q in eligible if q["q"] not in done]
        if not available:
            st.success(f"أكمل {chosen} تحديات هذه المحطة. يمكن الانتقال لمستوى أعلى مع اكتساب نقاط إضافية أو مراجعة المحطة.")
            if st.button("إعادة تحديات المحطة لهذا الطفل", use_container_width=True):
                st.session_state.answered[chosen] = [q for q in done if q not in [x["q"] for x in eligible]]
                st.session_state.last_result = None; st.rerun()
        else:
            q = available[0]
            st.markdown('<div class="question-card" dir="rtl">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-kicker">تحدي {len(done)+1} · {q["topic"]}</div>{scene_html(q["scene"])}<div class="question-text">{q["q"]}</div>', unsafe_allow_html=True)
            with st.form(key=f"answer_{chosen}_{q['q']}"):
                answer = st.radio("أي تفسير أو قرار تدعمه الملاحظة؟", q["options"], index=None)
                submit = st.form_submit_button("اعتماد الإجابة", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if submit:
                if answer is None: st.warning("اختاري إجابة قبل المتابعة.")
                else:
                    correct = answer == q["answer"]
                    st.session_state.answered.setdefault(chosen,[]).append(q["q"])
                    if correct:
                        st.session_state.scores[chosen] = st.session_state.scores.get(chosen,0)+1
                        st.session_state.garden_stars += 1
                    st.session_state.last_result = {"correct":correct,"child":chosen,"answer":q["answer"],"why":q["why"],"question":q["q"]}
                    st.session_state.history.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M"),"child":chosen,"level":level_num,"question":q["q"],"chosen":answer,"correct":correct})
                    st.rerun()
        if st.session_state.last_result:
            result = st.session_state.last_result
            if result["correct"]: st.success(f"أحسنت يا {result['child']}! اختيارك مبني على دليل جيد.")
            else: st.info(f"محاولة جيدة يا {result['child']}. لنتأمل الدليل معًا.")
            st.markdown(f'<div class="panel" dir="rtl"><div class="section-title">لماذا؟</div><p><b>الإجابة الأنسب:</b> {result["answer"]}</p><p>{result["why"]}</p></div>', unsafe_allow_html=True)
            if st.button("الانتقال إلى التحدي التالي", use_container_width=True): st.session_state.last_result=None; st.rerun()

with garden_tab:
    stars=st.session_state.garden_stars
    stage=1 if stars<3 else 2 if stars<6 else 3 if stars<10 else 4
    stages=[(0,"تجهيز التربة","تبدأ الرحلة بملاحظة التربة وتجهيز مكان الزراعة."),(3,"ظهور البراعم","تظهر البراعم الأولى مع تقدم المستكشفين."),(6,"حديقة خضراء","تزداد النباتات والأوراق في الحديقة."),(10,"حديقة مزهرة","تصل أسرة الزهراء إلى حديقة مزهرة.")]
    st.markdown(f'<div class="panel" dir="rtl" style="text-align:center">{SCENES["garden"]}<div class="section-title">{stages[stage-1][1]}</div><p>كل إجابة صحيحة تقرّب الفصل من المرحلة التالية.</p><div style="font-size:1.5rem;font-weight:800;color:#287b60">{stars} نقطة جماعية</div></div>',unsafe_allow_html=True)
    st.write("")
    cols=st.columns(4)
    for col,(target,title,desc) in zip(cols,stages):
        with col:
            reached=stars>=target
            st.markdown(f'<div class="metric-card"><div class="metric-number">{target}+</div><div class="metric-label">{title}</div><p class="small-note">{desc}</p><b style="color:{"#27805d" if reached else "#9aa9a0"}">{"تم الوصول" if reached else "لم تفتح بعد"}</b></div>',unsafe_allow_html=True)

with teacher_tab:
    st.markdown('<div class="section-title">إدارة الفصل والتقدم</div>',unsafe_allow_html=True)
    st.caption("استخدمي الأسماء الأولى فقط. نزّلي نسخة احتياطية بعد كل جلسة؛ قد لا تستمر البيانات عند إعادة تشغيل التطبيق.")
    st.markdown('<div class="panel" dir="rtl"><div class="section-title">أسماء أطفال الفصل</div><p>تم تثبيت أسماء أطفال أسرة الزهراء مسبقًا. اختاري اسم الطفل من قائمة المستكشفين لبدء التحديات ومتابعة إنجازه.</p></div>', unsafe_allow_html=True)
    st.write("، ".join(FIXED_CHILDREN))
    if st.session_state.children:
        rows=[]
        for child in st.session_state.children:
            rows.append({"الطفل":child,"النقاط":st.session_state.scores.get(child,0),"المحطة":LEVELS[get_level(st.session_state.scores.get(child,0))]["name"],"عدد التحديات":len(st.session_state.answered.get(child,[]))})
        st.dataframe(rows,use_container_width=True,hide_index=True)
        confirm=st.checkbox("أوافق على تصفير جميع النتائج")
        if st.button("تصفير النتائج"):
            if confirm:
                st.session_state.scores={x:0 for x in st.session_state.children}; st.session_state.answered={x:[] for x in st.session_state.children}; st.session_state.history=[]; st.session_state.garden_stars=0; st.session_state.last_result=None; st.rerun()
            else: st.warning("حددي مربع الموافقة أولًا.")
    st.markdown("#### حفظ واستعادة التقدم")
    data=export_data()
    st.download_button("تنزيل نسخة احتياطية",data=json.dumps(data,ensure_ascii=False,indent=2),file_name="zahraa_weather_plant_backup.json",mime="application/json",use_container_width=True)
    uploaded=st.file_uploader("استعادة نسخة احتياطية",type=["json"])
    if uploaded is not None and st.button("استعادة البيانات"):
        try:
            loaded=json.load(uploaded)
            for key in ["children","scores","answered","history","garden_stars"]:
                if key in loaded: st.session_state[key]=loaded[key]
            st.session_state.last_result=None; st.success("تمت استعادة البيانات."); st.rerun()
        except Exception: st.error("تعذر قراءة الملف. اختاري نسخة احتياطية صحيحة.")
    if st.session_state.history:
        st.markdown("#### سجل التحديات")
        st.dataframe(list(reversed(st.session_state.history)),use_container_width=True,hide_index=True)

st.markdown('<div style="text-align:center;color:#658177;padding:20px" dir="rtl">إعداد تعليمي لأسرة الزهراء · نلاحظ، نسأل، نجرب، ثم نستنتج.</div>',unsafe_allow_html=True)
