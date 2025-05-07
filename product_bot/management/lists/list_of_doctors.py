from telebot import types

general_practitioner_button = types.InlineKeyboardButton(
    "General Practitioner",
    callback_data="select_doctor_gp",
)
reproductive_specialist_button = types.InlineKeyboardButton(
    "Reproductive Specialist",
    callback_data="select_doctor_reproductive",
)
men_health_specialist_button = types.InlineKeyboardButton(
    "Men’s Health Specialist",
    callback_data="select_doctor_mens_health",
)
genetics_specialist_button = types.InlineKeyboardButton(
    "Genetics Specialist",
    callback_data="select_doctor_genetics",
)
endocrine_specialist_button = types.InlineKeyboardButton(
    "Endocrine Specialist",
    callback_data="select_doctor_endocrine",
)
breast_health_specialist_button = types.InlineKeyboardButton(
    "Breast Health Specialist",
    callback_data="select_doctor_breast",
)
oncology_specialist_button = types.InlineKeyboardButton(
    "Oncology Specialist",
    callback_data="select_doctor_oncology",
)
internal_medicine_button = types.InlineKeyboardButton(
    "Internal Medicine",
    callback_data="select_doctor_internal",
)
urinary_specialist_button = types.InlineKeyboardButton(
    "Urology Specialist",
    callback_data="select_doctor_urology",
)
blood_disorders_specialist_button = types.InlineKeyboardButton(
    "Blood Disorders Specialist",
    callback_data="select_doctor_hematology",
)
prenatal_expert_button = types.InlineKeyboardButton(
    "Prenatal Diagnosis Expert",
    callback_data="select_doctor_prenatal",
)
legal_consultant_button = types.InlineKeyboardButton(
    "Legal Consultant",
    callback_data="select_doctor_legal",
)
anesthesia_specialist_button = types.InlineKeyboardButton(
    "Anesthesia Specialist",
    callback_data="select_doctor_anesthesia",
)
mental_health_specialist_button = types.InlineKeyboardButton(
    "Mental Health Specialist",
    callback_data="select_doctor_mental_health",
)
