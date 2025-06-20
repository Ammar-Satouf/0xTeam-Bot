import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids, temporary_culture_doc, practical_exam_schedule
from datetime import datetime
from db import load_notified_users, add_notified_user


# إضافة زر تفعيل الإشعارات للقائمة الرئيسية
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🏛️ الأفرع الجامعية"), 
             KeyboardButton("📗 مقرر الثقافة المؤقت")],
            [KeyboardButton("👥 عن البوت والفريق"), 
             KeyboardButton("🔔 تفعيل إشعارات التحديثات")],
            [KeyboardButton("📤 آلية تقديم اعتراض")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def university_branches_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💻 الهندسة المعلوماتية"), 
             KeyboardButton("🏗️ الهندسة المعمارية")],
            [KeyboardButton("🚧 الهندسة المدنية"), 
             KeyboardButton("🏥 الهندسة الطبية")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def informatics_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية"), 
             KeyboardButton("📅 برنامج الامتحان العملي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى"),
             KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة"),
             KeyboardButton("السنة الرابعة")],
            [KeyboardButton("السنة الخامسة")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def specialization_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("هندسة البرمجيات"),
                KeyboardButton("الشبكات والنظم")
            ],
            [KeyboardButton("الذكاء الاصطناعي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("الفصل الأول ⚡"),
                KeyboardButton("الفصل الثاني 🔥")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📘 القسم النظري"),
                KeyboardButton("🧪 القسم العملي")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📚 محاضرات Gate"),
                KeyboardButton("📚 محاضرات الكميت")
            ],
            [KeyboardButton("✍ محاضرات كتابة زميلنا / دكتور المادة")],
            [KeyboardButton("📄 ملخصات"),
             KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def subjects_keyboard(subjects):
    keyboard = []
    for i in range(0, len(subjects), 2):
        row = [KeyboardButton(subjects[i])]
        if i + 1 < len(subjects):
            row.append(KeyboardButton(subjects[i + 1]))
        keyboard.append(row)

    keyboard.append(
        [KeyboardButton("🔙 رجوع"),
         KeyboardButton("🏠 القائمة الرئيسية")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# التحية حسب الوقت
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "صباح الخير ☀"
    elif hour < 18:
        return "مساء النور 🌇"
    else:
        return "سهرة سعيدة 🌙"


# إرسال إشعارات التحديثات للمستخدمين المفعّلين
async def notify_update_to_users(bot):
    try:
        users = await load_notified_users()
        for user_id in users:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=
                    "🔔 تم تحديث محتوى البوت بنجاح! يمكنك الآن استعراض المواد الجديدة."
                )
            except Exception as e:
                print(f"Error notifying user {user_id}: {e}")
    except Exception as e:
        print(f"Database error in notify_update_to_users: {e}")


# 🚀 البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name or "طالبنا"
    greeting = get_greeting()

    await update.message.reply_text(
        f"🌟 {greeting} يا {user_first_name}! أهلاً وسهلاً بك في منصتك التعليمية 🌟\n\n"
        "🏛️ مرحباً بك في البوت التعليمي الخاص بجامعة اللاذقية\n"
        "✨ مكانك الأمثل للحصول على كل ما تحتاجه في رحلتك الأكاديمية\n\n"
        "🎓 نوفر لك محتوى شامل لجميع الأفرع الهندسية:\n"
        "💻 الهندسة المعلوماتية • 🏗️ الهندسة المعمارية\n"
        "🚧 الهندسة المدنية • 🏥 الهندسة الطبية\n\n"
        "🚀 فريق 0x Team معك خطوة بخطوة نحو التفوق\n"
        "💡 مواد منظمة • ملخصات شاملة • امتحانات سابقة • نصائح دراسية\n\n"
        "📚 فريق SP_ITE ساعد في تقديم محتوى مواد كلية الهندسة المعلوماتية\n\n"
        "🎯 اختر فرعك من القائمة أدناه وابدأ رحلة التميز! 📚✨",
        reply_markup=main_menu_keyboard(),
    )
    context.user_data.clear()


# 📩 المعالجة الرئيسية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # تفعيل إشعارات التحديثات
    if text == "🔔 تفعيل إشعارات التحديثات":
        try:
            from db import is_user_notified
            is_already_notified = await is_user_notified(user_id)

            if not is_already_notified:
                # جلب معلومات المستخدم
                first_name = update.effective_user.first_name or ""
                last_name = update.effective_user.last_name or ""

                success = await add_notified_user(user_id, first_name,
                                                  last_name)
                if success:
                    await update.message.reply_text(
                        "✅ تم تفعيل إشعارات التحديثات بنجاح. ستتلقى تنبيهات عند تحديث محتوى البوت.",
                        reply_markup=main_menu_keyboard(),
                    )
                else:
                    await update.message.reply_text(
                        "⚠ حدث خطأ في تفعيل الإشعارات. يرجى المحاولة لاحقاً.",
                        reply_markup=main_menu_keyboard(),
                    )
            else:
                await update.message.reply_text(
                    "ℹ أنت مفعل الإشعارات سابقاً.",
                    reply_markup=main_menu_keyboard(),
                )
        except Exception as e:
            print(f"Database error: {e}")
            await update.message.reply_text(
                "⚠ حدث خطأ في تفعيل الإشعارات. يرجى المحاولة لاحقاً.",
                reply_markup=main_menu_keyboard(),
            )
        return

    # رجوع أو القائمة الرئيسية
    if text == "🔙 رجوع":
        # نحدد المرحلة الحالية بناء على البيانات المحفوظة
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = context.user_data.get("term")
        subject = context.user_data.get("subject")
        section = context.user_data.get("section")
        current_step = context.user_data.get("current_step")

        print(
            f"Debug - Back button pressed. Data: year={year}, specialization={specialization}, term={term}, subject={subject}, section={section}, current_step={current_step}"
        )

        # إذا كان في مرحلة اختيار نوع المحتوى، يرجع للمرحلة السابقة
        if current_step == "content_type":
            # إذا كان القسم محدد، يرجع لاختيار القسم
            if section:
                context.user_data["current_step"] = "section"
                await update.message.reply_text(
                    "اختر القسم (نظري أو عملي):",
                    reply_markup=section_keyboard())
                return
            # إذا لم يكن محتاج قسم، يرجع للمواد
            else:
                context.user_data["current_step"] = "subject"

                # جلب المواد حسب السنة والتخصص
                if year in ["السنة الرابعة", "السنة الخامسة"]:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year, {}).get(term, {}).get(
                                specialization, {}).get(section_key,
                                                        {}).keys())
                else:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year,
                                          {}).get(term,
                                                  {}).get(section_key,
                                                          {}).keys())

                subjects_all_set = set(subjects_all)
                prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
                subjects_with_emoji = [
                    prefix + subj for subj in sorted(subjects_all_set)
                ]

                await update.message.reply_text(
                    "اختر المادة:",
                    reply_markup=subjects_keyboard(subjects_with_emoji))
                return

        # إذا كان في مرحلة اختيار القسم، يرجع لاختيار المادة
        if current_step == "section":
            context.user_data["current_step"] = "subject"
            context.user_data.pop("section", None)

            # جلب المواد حسب السنة والتخصص
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year,
                                      {}).get(term,
                                              {}).get(specialization,
                                                      {}).get(section_key,
                                                              {}).keys())
            else:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year, {}).get(term,
                                                    {}).get(section_key,
                                                            {}).keys())

            subjects_all_set = set(subjects_all)
            prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
            subjects_with_emoji = [
                prefix + subj for subj in sorted(subjects_all_set)
            ]

            await update.message.reply_text(
                "اختر المادة:",
                reply_markup=subjects_keyboard(subjects_with_emoji))
            return

        # إذا كان في مرحلة اختيار المادة، يرجع لاختيار الفصل
        if current_step == "subject":
            context.user_data["current_step"] = "term"
            context.user_data.pop("subject", None)
            context.user_data.pop("section", None)

            await update.message.reply_text("اختر الفصل الدراسي:",
                                            reply_markup=term_keyboard())
            return

        # إذا كان في مرحلة اختيار الفصل، يرجع لاختيار التخصص أو السنة
        if current_step == "term":
            context.user_data.pop("term", None)

            # إذا كانت السنة الرابعة أو الخامسة، يرجع لاختيار التخصص
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                context.user_data["current_step"] = "specialization"
                await update.message.reply_text(
                    "اختر التخصص:", reply_markup=specialization_keyboard())
                return
            else:
                context.user_data["current_step"] = "year"
                await update.message.reply_text("اختر السنة الدراسية:",
                                                reply_markup=year_keyboard())
                return

        # إذا كان في مرحلة اختيار التخصص، يرجع لاختيار السنة
        if current_step == "specialization":
            context.user_data["current_step"] = "year"
            context.user_data.pop("specialization", None)

            await update.message.reply_text("اختر السنة الدراسية:",
                                            reply_markup=year_keyboard())
            return

        # إذا كان في مرحلة اختيار السنة أو أي حالة أخرى، يرجع للقائمة الرئيسية
        context.user_data.clear()
        await start(update, context)
        return

    # تحديث معالج الرجوع للأفرع الجامعية
    if context.user_data.get("from_informatics"):
        context.user_data.pop("from_informatics", None)
        await update.message.reply_text(
            "اختر الفرع الجامعي:",
            reply_markup=university_branches_keyboard()
        )
        return

    if text == "🏠 القائمة الرئيسية":
        await start(update, context)
        return

    # الأفرع الجامعية
    if text == "🏛️ الأفرع الجامعية":
        context.user_data.clear()
        await update.message.reply_text(
            "اختر الفرع الجامعي:",
            reply_markup=university_branches_keyboard()
        )
        return

    # الهندسة المعلوماتية
    if text == "💻 الهندسة المعلوماتية":
        await update.message.reply_text(
            "🎓 الهندسة المعلوماتية\n\nاختر ما تريد:",
            reply_markup=informatics_menu_keyboard()
        )
        return

    # الأفرع الأخرى
    if text in ["🏗️ الهندسة المعمارية", "🚧 الهندسة المدنية", "🏥 الهندسة الطبية"]:
        branch_name = text.split(" ", 1)[1]  # إزالة الإيموجي
        await update.message.reply_text(
            f"🔧 {branch_name}\n\nسنضيف محتوى لهذا الفرع في الأيام القادمة بإذن الله.\nتابعونا للحصول على التحديثات! 📚",
            reply_markup=university_branches_keyboard()
        )
        return

    # المواد الدراسية - بداية اختيار السنة
    if text == "📘 المواد الدراسية":
        context.user_data.clear()
        context.user_data["current_step"] = "year"
        await update.message.reply_text("اختر السنة الدراسية:",
                                        reply_markup=year_keyboard())
        return

    # آلية تقديم اعتراض
    if text == "📤 آلية تقديم اعتراض":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "📣 إعلان بخصوص الاعتراض على النتائج:\n\n"
            "بعد صدور النتائج، يُفتح باب تقديم طلبات الاعتراض لفترة محددة. آلية الاعتراض كالتالي:\n"
            "1. التوجه إلى النافذة الواحدة للحصول على نموذج الاعتراض.\n"
            "2. تعبئة الطلب وإرفاق الطوابع.\n"
            "3. تقديمه لشعبة الشؤون لتوليد الرسوم.\n"
            "4. دفع الرسوم عبر مصرف أو سيريتل كاش.\n"
            "5. توقيع الطلب لدى المحاسب.\n"
            "6. إعادة الطلب للنافذة لاستكمال الإجراء.\n\n"
            "مع تمنياتنا بالتوفيق 🍀",
            reply_markup=main_menu_keyboard(),
        )
        return

    # عن البوت والفريق
    if text == "👥 عن البوت والفريق":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "👥 <b>عن البوت والفريق</b>\n\n"
            "🏛️ منصة تعليمية شاملة مصممة خصيصاً لطلاب جامعة اللاذقية\n\n"
            "🎯 نهدف إلى تقديم محتوى منظم وسهل الوصول لجميع الأفرع الهندسية، بما يسرّع عملية الدراسة والمراجعة ويوفر الوقت والجهد على الطلاب في رحلتهم الأكاديمية.\n\n"
            "🚀 <b>رؤيتنا:</b> تمكين المجتمع الطلابي من خلال أدوات تقنية متطورة تدعم التعلم والتفوق الأكاديمي\n\n"
            "💻 هذا العمل هو نتاج رؤية برمجية متقدمة وخبرة أكاديمية عميقة، أعدّه <a href=\"https://t.me/ammarsa51\">عمار سطوف</a> – مطوّر ومهندس برمجيات مختص في بناء الأنظمة التعليمية والتقنية المتقدمة.\n\n"
            "🤝 <b>فريق العمل:</b>\n"
            "• فريق <a href=\"https://t.me/zeroxxteam\">0x Team</a> - التطوير التقني والبرمجة\n"
            "• فريق SP_ITE - ساعد في تقديم محتوى مواد كلية الهندسة المعلوماتية\n\n"
            "🌟 نعمل معاً لخدمة الطلاب وتوفير بيئة تعليمية رقمية متميزة\n\n"
            "🔹 <i>Developed with passion and precision to support all Engineering students on their academic journey</i>\n\n"
            "© 2025 <a href=\"https://t.me/zeroxxteam\">0x Team</a> – جميع الحقوق محفوظة\n"
            "🔧 Designed & Developed by <a href=\"https://t.me/ammarsa51\">Ammar Satouf</a>",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML"
        )
        return
    # مقرر الثقافة المؤقت
    if text == "📗 مقرر الثقافة المؤقت":
        context.user_data["previous_step"] = start
        cid = channel_ids.get("komit1")  # تحديث للسنة الأولى
        msg_id = temporary_culture_doc

        if not cid or not msg_id:
            await update.message.reply_text(
                "📗 لا يتوفر محتويات مقرر الثقافة حالياً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        await context.bot.copy_message(chat_id=update.effective_chat.id,
                                       from_chat_id=cid,
                                       message_id=msg_id,
                                       protect_content=True)
        await update.message.reply_text(
            "🎯 تم إرسال مقرر الثقافة المؤقت بنجاح.\nلا تنسَ تشارك البوت مع زملائك ❤",
            reply_markup=main_menu_keyboard(),
        )
        return

    # برنامج الامتحان العملي
    if text == "📅 برنامج الامتحان العملي":
        cid = channel_ids.get("exams1")  # قناة الامتحانات للسنة الأولى
        msg_id = practical_exam_schedule

        if not cid or not msg_id:
            await update.message.reply_text(
                "📅 لا يتوفر برنامج الامتحان العملي حالياً.",
                reply_markup=informatics_menu_keyboard(),
            )
            return

        await context.bot.copy_message(chat_id=update.effective_chat.id,
                                       from_chat_id=cid,
                                       message_id=msg_id,
                                       protect_content=True)
        await update.message.reply_text(
            "📅 تم إرسال برنامج الامتحان العملي بنجاح.\nبالتوفيق في امتحاناتك! 💪",
            reply_markup=informatics_menu_keyboard(),
        )
        return

    # اختيار السنة الدراسية
    years_map = {
        "السنة الأولى": "السنة الأولى",
        "السنة الثانية": "السنة الثانية",
        "السنة الثالثة": "السنة الثالثة",
        "السنة الرابعة": "السنة الرابعة",
        "السنة الخامسة": "السنة الخامسة",
    }

    if text in years_map:
        year = text
        context.user_data["year"] = year

        # إذا كانت السنة الرابعة أو الخامسة، نطلب اختيار التخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            context.user_data["current_step"] = "specialization"
            await update.message.reply_text(
                "اختر التخصص:", reply_markup=specialization_keyboard())
        else:
            context.user_data["current_step"] = "term"
            await update.message.reply_text("اختر الفصل الدراسي:",
                                            reply_markup=term_keyboard())
        return

    # اختيار التخصص (للسنة الرابعة والخامسة)
    specializations_map = {
        "هندسة البرمجيات": "هندسة البرمجيات",
        "الشبكات والنظم": "الشبكات والنظم",
        "الذكاء الاصطناعي": "الذكاء الاصطناعي",
    }

    if text in specializations_map:
        context.user_data["specialization"] = text
        context.user_data["current_step"] = "term"
        await update.message.reply_text("اختر الفصل الدراسي:",
                                        reply_markup=term_keyboard())
        return

    # اختيار الفصل الدراسي
    term_map = {
        "الفصل الأول ⚡": "الفصل الأول",
        "الفصل الثاني 🔥": "الفصل الثاني"
    }
    if text in term_map:
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = term_map[text]
        context.user_data["term"] = term
        context.user_data["current_step"] = "subject"

        # التحقق من وجود المواد حسب السنة والتخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            if (year not in resources or term not in resources[year]
                    or specialization not in resources[year][term]):
                await update.message.reply_text(
                    "لا توجد مواد لهذا التخصص والفصل.",
                    reply_markup=term_keyboard())
                return

            # جلب المواد من النظري والعملي للتخصص المحدد
            theoretical_subjects = list(
                resources[year][term][specialization].get("theoretical",
                                                          {}).keys())
            practical_subjects = list(
                resources[year][term][specialization].get("practical",
                                                          {}).keys())
        else:
            if year not in resources or term not in resources[year]:
                await update.message.reply_text("لا توجد مواد لهذا الفصل.",
                                                reply_markup=term_keyboard())
                return

            # جلب المواد من النظري والعملي للسنوات العادية
            theoretical_subjects = list(resources[year][term].get(
                "theoretical", {}).keys())
            practical_subjects = list(resources[year][term].get(
                "practical", {}).keys())

        all_subjects_set = set(theoretical_subjects + practical_subjects)
        all_subjects = sorted(all_subjects_set)

        prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
        subjects = [prefix + subj for subj in all_subjects]

        if not subjects:
            await update.message.reply_text("لا توجد مواد لهذا الفصل.",
                                            reply_markup=term_keyboard())
            return

        await update.message.reply_text(
            "اختر المادة:", reply_markup=subjects_keyboard(subjects))
        return

    # دالة لإزالة الإيموجي من بداية اسم المادة
    def strip_emoji(text):
        return text[2:] if len(text) > 2 else text

    # جميع المواد في resources تحت السنة والفصل والقسمين
    year = context.user_data.get("year")
    specialization = context.user_data.get("specialization")
    term = context.user_data.get("term")

    if year and term:
        subjects_all = []
        if year in ["السنة الرابعة", "السنة الخامسة"] and specialization:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year,
                                  {}).get(term,
                                          {}).get(specialization,
                                                  {}).get(section_key,
                                                          {}).keys())
        else:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year, {}).get(term, {}).get(section_key,
                                                              {}).keys())
        subjects_all_set = set(subjects_all)
    else:
        subjects_all_set = set()

    if strip_emoji(text) in subjects_all_set:
        subj_clean = strip_emoji(text)
        context.user_data["subject"] = subj_clean

        # نتحقق الأقسام المتوفرة للمادة
        available_sections = []

        if year in ["السنة الرابعة", "السنة الخامسة"]:
            subject_data = resources.get(year,
                                         {}).get(term,
                                                 {}).get(specialization, {})
        else:
            subject_data = resources.get(year, {}).get(term, {})

        if subj_clean in subject_data.get("theoretical", {}):
            available_sections.append("theoretical")
        if subj_clean in subject_data.get("practical", {}):
            available_sections.append("practical")

        if len(available_sections) == 1:
            context.user_data["section"] = available_sections[0]
            context.user_data["current_step"] = "content_type"
            await update.message.reply_text(
                "اختر نوع المحتوى المطلوب:",
                reply_markup=content_type_keyboard(),
            )
        else:
            context.user_data["current_step"] = "section"
            await update.message.reply_text(
                "اختر القسم (نظري أو عملي):",
                reply_markup=section_keyboard(),
            )
        return

    # اختيار القسم
    if text == "📘 القسم النظري":
        context.user_data["section"] = "theoretical"
        context.user_data["current_step"] = "content_type"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    if text == "🧪 القسم العملي":
        context.user_data["section"] = "practical"
        context.user_data["current_step"] = "content_type"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    # اختيار نوع المحتوى
    content_type_map = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميلنا / دكتور المادة": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes",
    }

    if text in content_type_map:
        content_key_base = content_type_map[text]
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = context.user_data.get("term")
        section = context.user_data.get("section")
        subject = context.user_data.get("subject")

        if not all([year, term, section, subject]):
            await update.message.reply_text(
                "يبدو أن هناك خطأ في اختيارك. الرجاء البدء من جديد.",
                reply_markup=main_menu_keyboard(),
            )
            context.user_data.clear()
            return

        # تحديد مفتاح المحتوى حسب السنة والتخصص
        if year == "السنة الأولى":
            content_key = content_key_base + "1"
        elif year == "السنة الثانية":
            content_key = content_key_base + "2"
        elif year == "السنة الثالثة":
            content_key = content_key_base + "3"
        elif year in ["السنة الرابعة", "السنة الخامسة"]:
            year_num = "4" if year == "السنة الرابعة" else "5"
            spec_code = resources[year]["specializations"][specialization]
            content_key = content_key_base + year_num + spec_code

        # جلب البيانات حسب السنة والتخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            messages_list = resources.get(year, {}).get(term, {}).get(
                specialization,
                {}).get(section, {}).get(subject, {}).get(content_key, [])
        else:
            messages_list = resources.get(year, {}).get(term, {}).get(
                section, {}).get(subject, {}).get(content_key, [])

        if not messages_list or messages_list == [0]:
            await update.message.reply_text(
                "عذرًا، لا توجد ملفات متاحة لهذا المحتوى حالياً.",
                reply_markup=content_type_keyboard(),
            )
            return

        channel_id = channel_ids.get(content_key)
        if not channel_id:
            await update.message.reply_text(
                "حدث خطأ في جلب القناة. الرجاء المحاولة لاحقاً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        for msg_id in messages_list:
            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True,
                )
            except Exception as e:
                print(f"Error sending message {msg_id} from {channel_id}: {e}")

        # البقاء في نفس مرحلة اختيار نوع المحتوى
        context.user_data["current_step"] = "content_type"

        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    # إذا لم يتعرف على النص
    await update.message.reply_text(
        "عذراً، لم أفهم طلبك. الرجاء استخدام الأزرار المتاحة.",
        reply_markup=main_menu_keyboard(),
    )
