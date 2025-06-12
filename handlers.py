from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية")],
            [KeyboardButton("📤 آلية تقديم اعتراض")],
            [KeyboardButton("👨‍💻 المطور والدعم")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى")],
            [KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة")],
            [KeyboardButton("السنة الرابعة")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("الفصل الأول")],
            [KeyboardButton("الفصل الثاني")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def subjects_keyboard(subjects_list):
    buttons = [[KeyboardButton(sub)] for sub in subjects_list]
    buttons.append([KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 القسم النظري")],
            [KeyboardButton("🧪 القسم العملي")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 محاضرات Gate")],
            [KeyboardButton("📚 محاضرات الكميت")],
            [KeyboardButton("✍ محاضرات كتابة زميل")],
            [KeyboardButton("📄 ملخصات")],
            [KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في بوت فريق زيرو x التعليمي 👋\n"
        "اختر أحد الأقسام التالية:",
        reply_markup=main_menu_keyboard()
    )
    context.user_data.clear()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ["🏠 القائمة الرئيسية", "🔙 رجوع"]:
        await start(update, context)
        return

    if text == "📘 المواد الدراسية":
        await update.message.reply_text("اختر السنة الدراسية:", reply_markup=year_keyboard())
        return

    if text == "📤 آلية تقديم اعتراض":
        await update.message.reply_text(
            "إعلان بخصوص الاعتراض على النتائج:\n\n"
            "بعد صدور النتائج، يُفتح باب تقديم طلبات الاعتراض لفترة محددة. ونُلفت عنايتكم إلى أن آلية الاعتراض الجديدة أصبحت كما يلي:\n\n"
            "1. التوجه إلى النافذة الواحدة للحصول على نموذج طلب الاعتراض.\n"
            "2. تعبئة الطلب وإرفاق الطوابع المطلوبة.\n"
            "3. تقديم الطلب إلى شعبة الشؤون ليتم توليد الرسوم اللازمة.\n"
            "4. دفع الرسوم عبر مصرف أو سيريتل كاش.\n"
            "5. التوجه إلى المحاسب لتوقيع الطلب بعد الدفع.\n"
            "6. إعادة الطلب إلى النافذة الواحدة لاستكمال الإجراءات.\n\n"
            "وبهذا تكون عملية الاعتراض قد اكتملت.\n"
            "مع تمنياتنا بالتوفيق للجميع!",
            reply_markup=main_menu_keyboard()
        )
        return

    if text == "👨‍💻 المطور والدعم":
        await update.message.reply_text(
            """👨‍💻 المطور: عمار سطوف | Developer: Ammar Satouf
مطوّر تطبيقات وبوتات مهتم بالذكاء الاصطناعي وبناء الأنظمة التفاعلية.
من أعماله: ITGenix Academy Bot، المصمم لخدمة المستخدمين بفعالية.

🤝 بالمساعدة مع: غدير ونوس | Ghadeer Wanous
ساهم في إعداد محتوى البوت وتنسيقه لخدمة الطلاب بشكل أفضل.

📬 للتواصل | Contact: @Ammarsa51
🔗 غدير ونوس: @ghadeer_wanous
""",
            reply_markup=main_menu_keyboard()
        )
        return

    if text in ["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة"]:
        year_map = {
            "السنة الأولى": "1",
            "السنة الثانية": "2",
            "السنة الثالثة": "3",
            "السنة الرابعة": "4"
        }
        context.user_data['year'] = year_map[text]
        await update.message.reply_text("اختر الفصل:", reply_markup=term_keyboard())
        return

    if text in ["الفصل الأول", "الفصل الثاني"]:
        term_map = {
            "الفصل الأول": "1",
            "الفصل الثاني": "2"
        }
        context.user_data['term'] = term_map[text]
        if context.user_data.get('year') == "1" and context.user_data.get('term') == "2":
            subjects = [
                "تحليل 2",
                "برمجة 2",
                "فيزياء انصاف نواقل",
                "جبر خطي",
                "لغة انجليزية 2"
            ]
            await update.message.reply_text("اختر المادة:", reply_markup=subjects_keyboard(subjects))
        else:
            await update.message.reply_text(
                "لا يوجد محتوى حاليا، نحاول توفيره بأقرب وقت.",
                reply_markup=main_menu_keyboard()
            )
        return

    subjects_list = [
        "تحليل 2",
        "برمجة 2",
        "فيزياء انصاف نواقل",
        "جبر خطي",
        "لغة انجليزية 2"
    ]
    if text in subjects_list:
        context.user_data['subject'] = text
        if text == "لغة انجليزية 2":
            context.user_data['section'] = "theoretical"
            await update.message.reply_text("اختر نوع المحتوى:", reply_markup=content_type_keyboard())
        else:
            await update.message.reply_text("اختر القسم:", reply_markup=section_keyboard())
        return

    if text in ["📘 القسم النظري", "🧪 القسم العملي"]:
        context.user_data['section'] = "theoretical" if text == "📘 القسم النظري" else "practical"
        await update.message.reply_text("اختر نوع المحتوى:", reply_markup=content_type_keyboard())
        return

    content_map = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميل": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes"
    }
    if text in content_map:
        content_key = content_map[text]
        year = context.user_data.get('year')
        term = context.user_data.get('term')
        section = context.user_data.get('section')
        subject = context.user_data.get('subject')

        try:
            msgs = resources[year][term][section][subject][content_key]
        except KeyError:
            msgs = []

        if not msgs:
            await update.message.reply_text(
                "لا يوجد محتوى حاليا، نحاول توفيره بأقرب وقت.",
                reply_markup=main_menu_keyboard()
            )
            return

        cid = channel_ids.get(content_key)
        if not cid:
            await update.message.reply_text(
                "تعذر الوصول لقناة المحتوى.",
                reply_markup=main_menu_keyboard()
            )
            return

        for mid in msgs:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=cid,
                message_id=mid
            )

        await update.message.reply_text(
            "يمكنك اختيار محتوى آخر أو العودة.",
            reply_markup=content_type_keyboard()
        )
        return

    # في حالة النص غير معروف
    await update.message.reply_text(
        "الرجاء اختيار خيار صحيح من القائمة.",
        reply_markup=main_menu_keyboard()
    )
