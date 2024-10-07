import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Define your bot token
BOT_TOKEN = '7885663302:AAEIGj5b1peU6676VrCmjDCR3RZJeoQwFuQ'

# Dictionary of readers and their corresponding URLs
readers = {
    1: ("ماهر المعيقلي", "Maher_Al-Muaiqly"),
    2: ("زكي داغستاني", "Zaki_Daghistani"),
    3: ("أحمد الحذيفي", "Ahmad_Al-Hudhaify"),
    4: ("عبدالباسط عبدالصمد", "3bdulbasit_Abdulsamad"),
    5: ("فهد العتيبي", "Fahd-Al3tiby"),
    6: ("ياسر الدوسري", "Yasser_Aldosari"),

}

# Surah list (1-114 in the Quran)
surahs = {
    1: "الفاتحة",
    2: "البقرة",
    3: "آل عمران",
    4: "النساء",
    5: "المائدة",
    6: "الأنعام",
    7: "الأعراف",
    8: "الأنفال",
    9: "التوبة",
    10: "يونس",
    11: "هود",
    12: "يوسف",
    13: "الرعد",
    14: "إبراهيم",
    15: "الحجر",
    16: "النحل",
    17: "الإسراء",
    18: "الكهف",
    19: "مريم",
    20: "طه",
    21: "الأنبياء",
    22: "الحج",
    23: "المؤمنون",
    24: "النور",
    25: "الفرقان",
    26: "الشعراء",
    27: "النمل",
    28: "القصص",
    29: "العنكبوت",
    30: "الروم",
    31: "لقمان",
    32: "السجدة",
    33: "الأحزاب",
    34: "سبأ",
    35: "فاطر",
    36: "يس",
    37: "الصافات",
    38: "ص",
    39: "الزمر",
    40: "غافر",
    41: "فصلت",
    42: "الشورى",
    43: "الزخرف",
    44: "الدخان",
    45: "الجاثية",
    46: "الأحقاف",
    47: "محمد",
    48: "الفتح",
    49: "الحجرات",
    50: "ق",
    51: "الذاريات",
    52: "الطور",
    53: "النجم",
    54: "القمر",
    55: "الرحمن",
    56: "الواقعة",
    57: "الحديد",
    58: "المجادلة",
    59: "الحشر",
    60: "الممتحنة",
    61: "الصف",
    62: "الجمعة",
    63: "المنافقون",
    64: "التغابن",
    65: "الطلاق",
    66: "التحريم",
    67: "الملك",
    68: "القلم",
    69: "الحاقة",
    70: "المعارج",
    71: "نوح",
    72: "الجن",
    73: "المزمل",
    74: "المدثر",
    75: "القيامة",
    76: "الإنسان",
    77: "المرسلات",
    78: "النبأ",
    79: "النازعات",
    80: "عبس",
    81: "التكوير",
    82: "الإنفطار",
    83: "المطففين",
    84: "الإنشقاق",
    85: "البروج",
    86: "الطارق",
    87: "الأعلى",
    88: "الغاشية",
    89: "الفجر",
    90: "البلد",
    91: "الشمس",
    92: "الليل",
    93: "الضحى",
    94: "الشرح",
    95: "التين",
    96: "العلق",
    97: "القدر",
    98: "البينة",
    99: "الزلزلة",
    100: "العاديات",
    101: "القارعة",
    102: "التكاثر",
    103: "العصر",
    104: "الهمزة",
    105: "الفيل",
    106: "قريش",
    107: "الماعون",
    108: "الكوثر",
    109: "الكافرون",
    110: "النصر",
    111: "المسد",
    112: "الإخلاص",
    113: "الفلق",
    114: "الناس"
    # Continue until 114...
}

# Start command handler
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton(f"{name}", callback_data=f"reader_{i}")]
        for i, (name, _) in readers.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        'السلام عليكم و رحمة الله و براكاته  \n'
        'تفضل باختيار القارئ المفضل لديك للاستماع و تحميل القرآن الكريم. \n'
        'الَّذِينَ آمَنُوا وَتَطْمَئِنُّ قُلُوبُهُم بِذِكْرِ اللَّهِ ۗ أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ {سورة الرعد}', 
        reply_markup=reply_markup
    )


# Reader selection handler
async def handle_reader_selection(update: Update, context):
    query = update.callback_query
    reader_id = int(query.data.split("_")[1])
    context.user_data['reader'] = reader_id  # Save reader selection
    
    # List of buttons for all surahs (assuming 'surahs' is a dict or list of names)
    keyboard = [
        [InlineKeyboardButton(f"{name}", callback_data=f"surah_{i}")]
        for i, name in surahs.items()
    ]
    
    # Send the first batch of up to 100 buttons
    first_keyboard = keyboard[:100]
    reply_markup_first = InlineKeyboardMarkup(first_keyboard)
    await query.edit_message_text('اختر السورة:', reply_markup=reply_markup_first)
    
    # If there are more than 100 buttons, send the rest in a new message
    if len(keyboard) > 100:
        second_keyboard = keyboard[100:]
        reply_markup_second = InlineKeyboardMarkup(second_keyboard)
        await query.message.reply_text('ㅤ', reply_markup=reply_markup_second)


# Surah selection handler
async def handle_surah_selection(update: Update, context):
    query = update.callback_query
    surah_id = int(query.data.split("_")[1])
    reader_id = context.user_data.get('reader')
    
    if reader_id and surah_id:
        reader_name_en = readers[reader_id][1]  # Get the English name of the reader
        mp3_url = f"https://download.ourquraan.com/{reader_name_en}/{str(surah_id).zfill(3)}.mp3"
        
        # Download the MP3 file
        response = requests.get(mp3_url)
        file_name = f"surah_{surah_id}.mp3"
        
        with open(file_name, "wb") as f:
            f.write(response.content)
        
        # Create a new keyboard with only the chosen Surah
        selected_surah_button = [[InlineKeyboardButton(f"{surahs[surah_id]}", callback_data=f"surah_{surah_id}")]]
        reply_markup = InlineKeyboardMarkup(selected_surah_button)
        
        # Edit the message to show only the chosen Surah button
        await query.edit_message_text(
            f"تم إرسال السورة {surahs[surah_id]}",
            reply_markup=reply_markup
        )
        
        # Send the MP3 file to the user
        await context.bot.send_audio(chat_id=query.message.chat.id, audio=open(file_name, "rb"))



# Main function to set up the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_reader_selection, pattern="^reader_"))
    application.add_handler(CallbackQueryHandler(handle_surah_selection, pattern="^surah_"))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
