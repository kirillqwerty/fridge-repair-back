"""Initial data for refrigerator repair website."""
import uuid


def _id() -> str:
    return str(uuid.uuid4())


INITIAL_CONTACTS = {
    "phones": [
        "+375 (29) 609-54-31",
        "+375 (29) 77-000-83",
    ],
    "hours": "Работаем 8:00 - 22:00",
    "days": "Без выходных",
    "address": "Минск, ул. Бельского, 14",
    "company_name": "Сервис ремонта холодильников",
    "email": "",
    "footer_note": "Информация на сайте не является публичной офертой",
    "telegram_link": "",
    "viber_link": "",
    "whatsapp_link": "",
}


INITIAL_SERVICES = [
    {"id": _id(), "name": "Диагностика на дому", "price_from": 0, "price_to": 0, "unit": "BYN", "warranty": "—", "order": 1},
    {"id": _id(), "name": "Заправка фреоном", "price_from": 80, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 2},
    {"id": _id(), "name": "Замена компрессора", "price_from": 180, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 3},
    {"id": _id(), "name": "Замена пускового реле", "price_from": 50, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 4},
    {"id": _id(), "name": "Замена термостата", "price_from": 60, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 5},
    {"id": _id(), "name": "Ремонт системы No Frost", "price_from": 90, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 6},
    {"id": _id(), "name": "Замена уплотнительной резины", "price_from": 70, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 7},
    {"id": _id(), "name": "Замена ТЭНа оттайки", "price_from": 70, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 8},
    {"id": _id(), "name": "Устранение засора дренажа", "price_from": 40, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 9},
    {"id": _id(), "name": "Замена вентилятора", "price_from": 80, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 10},
    {"id": _id(), "name": "Замена платы управления", "price_from": 120, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 11},
    {"id": _id(), "name": "Перевеска дверей", "price_from": 60, "price_to": 0, "unit": "BYN", "warranty": "до 24 мес.", "order": 12},
]


INITIAL_BENEFITS = [
    {"id": _id(), "icon": "Clock", "title": "Экономишь время", "description": "Приезжаем в день звонка, весь процесс 1–2 часа", "order": 1},
    {"id": _id(), "icon": "Wallet", "title": "Экономишь деньги", "description": "Ремонт в 3–5 раз дешевле покупки нового холодильника", "order": 2},
    {"id": _id(), "icon": "Snowflake", "title": "Спасаешь продукты", "description": "Холодильник готов к работе уже сегодня", "order": 3},
    {"id": _id(), "icon": "ShieldCheck", "title": "Получишь гарантию", "description": "1 год гарантии на все работы и запчасти", "order": 4},
    {"id": _id(), "icon": "BadgeCheck", "title": "Никакого риска", "description": "Фиксированная цена, без скрытых платежей", "order": 5},
    {"id": _id(), "icon": "Wrench", "title": "Профессионалы", "description": "Сертифицированные мастера, опыт 10+ лет", "order": 6},
]


INITIAL_REVIEWS = [
    {
        "id": _id(),
        "author": "Иван К.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-09-12",
        "text": "Холодильник не холодил. Вызвал на дом, мастер приехал в день звонка. За 30 минут все исправил. Спасибо, рекомендую!",
        "brand": "Atlant",
        "problem": "Не холодит",
        "image_url": "",
        "featured": True,
        "order": 1,
    },
    {
        "id": _id(),
        "author": "Мария П.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-09-21",
        "text": "Честная цена, мастер профессионал. Не жалею! Холодильник работает как новый.",
        "brand": "Bosch",
        "problem": "Утечка фреона",
        "image_url": "",
        "featured": True,
        "order": 2,
    },
    {
        "id": _id(),
        "author": "Пётр В.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-10-02",
        "text": "Сломался холодильник Samsung. Не знал, что делать. Позвонил, приехали сразу. Теперь все работает! Спасибо!",
        "brand": "Samsung",
        "problem": "No Frost не работает",
        "image_url": "",
        "featured": True,
        "order": 3,
    },
    {
        "id": _id(),
        "author": "Анна С.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-10-15",
        "text": "Долго искала проверенный сервис. Мастер очень вежливый, объяснил всё подробно. Заменили компрессор, дали гарантию 1 год.",
        "brand": "LG",
        "problem": "Замена компрессора",
        "image_url": "",
        "featured": False,
        "order": 4,
    },
    {
        "id": _id(),
        "author": "Дмитрий Л.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-11-04",
        "text": "Очень оперативно! Приехали через час после звонка. Цены прозрачные, без сюрпризов.",
        "brand": "Indesit",
        "problem": "Шум при работе",
        "image_url": "",
        "featured": False,
        "order": 5,
    },
    {
        "id": _id(),
        "author": "Светлана М.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-11-22",
        "text": "Электролюкс перестал морозить. Мастер диагностировал быстро, заменил термостат. Уже месяц работает отлично.",
        "brand": "Electrolux",
        "problem": "Не морозит",
        "image_url": "",
        "featured": False,
        "order": 6,
    },
    {
        "id": _id(),
        "author": "Алексей Т.",
        "city": "Минск",
        "rating": 5,
        "date": "2024-12-08",
        "text": "Beko был старенький, думал — менять. Мастер реанимировал! Уже 2 месяца работает. Спасибо большое.",
        "brand": "BEKO",
        "problem": "Капитальный ремонт",
        "image_url": "",
        "featured": False,
        "order": 7,
    },
    {
        "id": _id(),
        "author": "Ольга Р.",
        "city": "Минск",
        "rating": 5,
        "date": "2025-01-14",
        "text": "Очень довольна! Liebherr — техника недешёвая, поэтому искала именно специалистов. Не разочаровалась.",
        "brand": "Liebherr",
        "problem": "Замена платы управления",
        "image_url": "",
        "featured": False,
        "order": 8,
    },
]


INITIAL_FAQ = [
    {"id": _id(), "question": "Сколько стоит ремонт холодильника?", "answer": "Стоимость зависит от типа поломки. Простые ремонты — от 60 BYN, замена компрессора с запчастью — от 180 BYN. Точную цену называем по телефону или после диагностики на месте. Никаких скрытых платежей.", "order": 1},
    {"id": _id(), "question": "Плачу ли я за диагностику?", "answer": "Если вы заказываете ремонт у нас — диагностика бесплатна. Если решили не ремонтировать — оплата только 30 BYN за выезд и работу мастера.", "order": 2},
    {"id": _id(), "question": "Сколько времени занимает ремонт?", "answer": "Большинство ремонтов выполняем за 30–120 минут на дому. Сложные случаи (замена компрессора, платы) могут занять до 2–3 часов. Везём все запчасти с собой.", "order": 3},
    {"id": _id(), "question": "Даёте ли гарантию?", "answer": "Да, 1 год гарантии на все виды работ и установленные запчасти. Если поломка повторилась — приедем и устраним бесплатно.", "order": 4},
    {"id": _id(), "question": "Когда вы можете приехать?", "answer": "Работаем 8:00–22:00 без выходных. Стандартное время приезда — 30–90 минут после звонка. В будние дни возможен срочный выезд в течение 30 минут.", "order": 5},
    {"id": _id(), "question": "С какими брендами работаете?", "answer": "Ремонтируем все популярные бренды: Атлант, Samsung, LG, Bosch, Ariston, Liebherr, Electrolux, Indesit, BEKO, SHARP, DAEWOO, AEG. Опыт 10+ лет с каждым.", "order": 6},
    {"id": _id(), "question": "Используете оригинальные запчасти?", "answer": "Да, только оригинальные запчасти или сертифицированные аналоги, согласованные с заказчиком. Никакого «китайского ноунейма».", "order": 7},
]


INITIAL_MASTERS = [
    {"id": _id(), "name": "Сергей", "role": "Старший мастер", "experience": "19 лет опыта", "specialization": "Все бренды, сложные случаи", "image_url": "", "order": 1},
    {"id": _id(), "name": "Андрей", "role": "Мастер по холодильникам", "experience": "12 лет опыта", "specialization": "Atlant, Indesit, BEKO, Samsung", "image_url": "", "order": 2},
    {"id": _id(), "name": "Алексей", "role": "Мастер по холодильникам", "experience": "10 лет опыта", "specialization": "LG, Bosch, Liebherr, Electrolux", "image_url": "", "order": 3},
    {"id": _id(), "name": "Виктор", "role": "Мастер по холодильникам", "experience": "15 лет опыта", "specialization": "Ariston, SHARP, DAEWOO, AEG", "image_url": "", "order": 4},
]


INITIAL_PORTFOLIO = [
    {"id": _id(), "title": "Замена вентилятора", "description": "Установлен новый вентилятор, проверена система обдува.", "before_url": "/assets/portfolio/zamena-ventilyatora-do.jpg", "after_url": "/assets/portfolio/zamena-ventilyatora-posle.jpg", "brand": "", "order": 1},
    {"id": _id(), "title": "Замена компрессора", "description": "Заменён компрессор, восстановлена работа холодильника.", "before_url": "/assets/portfolio/zamena-kompressora-do.jpg", "after_url": "/assets/portfolio/zamena-kompressora-posle.jpg", "brand": "", "order": 2},
    {"id": _id(), "title": "Замена термостата", "description": "Заменён термостат, отрегулирован холод.", "before_url": "/assets/portfolio/zamena-termostata-do.jpg", "after_url": "/assets/portfolio/zamena-termostata-posle.jpg", "brand": "", "order": 3},
    {"id": _id(), "title": "Заправка фреоном", "description": "Найдена утечка, система заправлена фреоном.", "before_url": "/assets/portfolio/zapravka-freonom-do.jpg", "after_url": "/assets/portfolio/zapravka-freonom-posle.jpg", "brand": "", "order": 4},
    {"id": _id(), "title": "Восстановление No Frost", "description": "Прочистка дренажа и восстановление системы оттайки.", "before_url": "/assets/portfolio/no-frost-do.jpg", "after_url": "/assets/portfolio/no-frost-posle.jpg", "brand": "", "order": 5},
    {"id": _id(), "title": "Ремонт платы управления", "description": "Проведён ремонт платы управления и проверка работы.", "before_url": "/assets/portfolio/remont-platy-do.jpg", "after_url": "/assets/portfolio/remont-platy-posle.jpg", "brand": "", "order": 6},
]


INITIAL_STATS = {
    "rating": 5.0,
    "reviews_count": 234,
    "years_experience": 19,
    "repairs_done": 2300,
    "guarantee_months": 12,
    "arrival_minutes": 30,
}


INITIAL_PROCESS_STEPS = [
    {"id": _id(), "step": 1, "title": "Звонок клиента", "description": "Принимаем заявку 8:00–22:00 без выходных"},
    {"id": _id(), "step": 2, "title": "Консультация (2–3 мин)", "description": "Уточняем модель и проблему"},
    {"id": _id(), "step": 3, "title": "Приезд мастера (30–60 мин)", "description": "Бесплатный выезд по Минску"},
    {"id": _id(), "step": 4, "title": "Диагностика (10–15 мин)", "description": "Профессиональное оборудование"},
    {"id": _id(), "step": 5, "title": "Названия цены", "description": "Честная фиксированная стоимость"},
    {"id": _id(), "step": 6, "title": "Согласие клиента", "description": "Начинаем ремонт только после вашего «да»"},
    {"id": _id(), "step": 7, "title": "Ремонт (30–120 мин)", "description": "Запчасти с собой"},
    {"id": _id(), "step": 8, "title": "Проверка работы", "description": "Тестируем перед уходом"},
    {"id": _id(), "step": 9, "title": "Оплата", "description": "Наличными или картой после работы"},
    {"id": _id(), "step": 10, "title": "Гарантия 1 год", "description": "Чек и гарантийный талон"},
]


INITIAL_GUARANTEES = {
    "result": {
        "title": "Гарантия результата",
        "icon": "ShieldCheck",
        "items": [
            "1 год гарантии на все работы",
            "Если не помогли — вернём деньги за 3 дня",
            "Используем только оригинальные запчасти",
        ],
    },
    "work": {
        "title": "Условия работы",
        "icon": "Clock",
        "items": [
            "Работаем без выходных (8:00–22:00)",
            "Приезжаем в день обращения",
            "Выезд на дом без дополнительной платы",
        ],
    },
    "payment": {
        "title": "Условия оплаты",
        "icon": "Wallet",
        "items": [
            "Фиксированная цена, без скрытых платежей",
            "Называем цену ДО работы (за 2 мин по телефону)",
            "Оплата наличными или картой после работы",
        ],
    },
}


BRAND_LIST = [
    {"slug": "atlant", "name": "Атлант", "name_en": "Atlant", "country": "Беларусь"},
    {"slug": "sharp", "name": "SHARP", "name_en": "Sharp", "country": "Япония"},
    {"slug": "lg", "name": "LG", "name_en": "LG", "country": "Южная Корея"},
    {"slug": "daewoo", "name": "DAEWOO", "name_en": "Daewoo", "country": "Южная Корея"},
    {"slug": "samsung", "name": "Samsung", "name_en": "Samsung", "country": "Южная Корея"},
    {"slug": "electrolux", "name": "Electrolux", "name_en": "Electrolux", "country": "Швеция"},
    {"slug": "indesit", "name": "Indesit", "name_en": "Indesit", "country": "Италия"},
    {"slug": "beko", "name": "BEKO", "name_en": "Beko", "country": "Турция"},
    {"slug": "bosch", "name": "BOSCH", "name_en": "Bosch", "country": "Германия"},
    {"slug": "ariston", "name": "ARISTON", "name_en": "Ariston", "country": "Италия"},
    {"slug": "liebherr", "name": "LIEBHERR", "name_en": "Liebherr", "country": "Германия"},
    {"slug": "aeg", "name": "AEG", "name_en": "AEG", "country": "Германия"},
]


BRAND_DETAILS = {
    "atlant": {
        "intro": "Холодильники Атлант — самая популярная марка в Беларуси. Мы знаем их буквально «наизусть»: от советских моделей до новых двухкамерных. Большинство запчастей всегда есть на складе.",
        "features": [
            "Доступная цена ремонта и быстрая доставка запчастей",
            "Опыт с моделями серий ХМ, МХМ и Side-by-Side",
            "Решаем типичные проблемы: реле, мотор-компрессор, термостат",
        ],
        "common_issues": [
            "Не запускается компрессор — замена пускового реле",
            "Не морозит верхняя камера — замена термостата",
            "Намерзает лёд в морозильной — ремонт системы оттайки",
        ],
        "meta_description": "Ремонт холодильников Атлант в Минске на дому. Выезд за 30 минут, гарантия 1 год. Звоните: +375 (29) 609-54-31. Работаем без выходных 8:00-22:00.",
    },
    "sharp": {
        "intro": "Японские холодильники SHARP — премиальная техника со сложной электроникой. Наши мастера прошли обучение по работе с инверторными компрессорами и платами управления SHARP.",
        "features": [
            "Опыт с инверторными системами и Plasmacluster",
            "Диагностика плат управления и сенсоров",
            "Оригинальные запчасти под заказ за 1–3 дня",
        ],
        "common_issues": [
            "Ошибки на дисплее — диагностика и сброс/перепрошивка платы",
            "Не работает инвертор — замена силовой части",
            "Не охлаждает — заправка хладагентом, поиск утечек",
        ],
        "meta_description": "Ремонт холодильников SHARP в Минске на дому. Опытные мастера, инверторные системы, оригинальные запчасти. Звоните: +375 (29) 609-54-31.",
    },
    "lg": {
        "intro": "LG — лидер по инверторным компрессорам и системе Door-in-Door. Ремонтируем все серии: GR, GA, GW, Multi Air Flow. Многолетний опыт с электроникой LG.",
        "features": [
            "Сертифицированный сервис по линейным инверторным компрессорам",
            "Замена плат, датчиков и сенсоров холодильников LG",
            "Опыт с моделями InstaView и Side-by-Side",
        ],
        "common_issues": [
            "Холодильник не включается — диагностика платы",
            "Не работает No Frost — ремонт вентиляторов и ТЭНа",
            "Ошибка ER на дисплее — расшифровка и устранение",
        ],
        "meta_description": "Ремонт холодильников LG в Минске на дому. Инверторные компрессоры, плата управления, No Frost. Гарантия 1 год. +375 (29) 609-54-31.",
    },
    "daewoo": {
        "intro": "DAEWOO — корейская техника с собственной электроникой. Мы знаем все слабые места моделей FN, FRS, RTN: от компрессоров до клапанов.",
        "features": [
            "Опыт с системой охлаждения DAEWOO",
            "Запчасти под заказ за 2–4 дня",
            "Решаем большинство неисправностей за один визит",
        ],
        "common_issues": [
            "Слабое охлаждение — заправка хладагентом",
            "Намерзает иней — ремонт системы оттайки",
            "Шум при работе — замена вентилятора или компрессора",
        ],
        "meta_description": "Ремонт холодильников DAEWOO в Минске на дому. Быстро, с гарантией 1 год. Звоните: +375 (29) 609-54-31.",
    },
    "samsung": {
        "intro": "Samsung — это сложная электроника и инверторные технологии. Чиним все серии: RB, RS, RF, RT. Опыт с системой Twin Cooling и Smart Inverter.",
        "features": [
            "Опыт с Twin Cooling Plus и Digital Inverter",
            "Диагностика и ремонт плат управления Samsung",
            "Сертифицированные запчасти",
        ],
        "common_issues": [
            "Ошибки 22E, 8E, OF OF — диагностика и сброс",
            "Не охлаждает основная камера — замена датчика или вентилятора",
            "Намерзает на задней стенке — ремонт оттайки и дренажа",
        ],
        "meta_description": "Ремонт холодильников Samsung в Минске на дому. Twin Cooling, Digital Inverter, No Frost. Гарантия 1 год. +375 (29) 609-54-31.",
    },
    "electrolux": {
        "intro": "Electrolux — шведское качество, требующее точной диагностики. Работаем со всеми сериями: ERB, ENB, EN, ERT. Запчасти Electrolux всегда в наличии.",
        "features": [
            "Опыт с системой A++/A+++ и TwinTech",
            "Замена компрессоров, термостатов, ТЭНов",
            "Бережная работа с фасадами Inox",
        ],
        "common_issues": [
            "Слабо охлаждает — диагностика и заправка фреоном",
            "Не работает оттайка — замена ТЭНа или таймера",
            "Стук компрессора — замена амортизаторов или мотора",
        ],
        "meta_description": "Ремонт холодильников Electrolux в Минске на дому. Опыт работы с TwinTech, A+++, гарантия 1 год. Звоните: +375 (29) 609-54-31.",
    },
    "indesit": {
        "intro": "Indesit — массовая марка с типичными «болячками». Мы знаем все слабые места: от пусковых реле до системы No Frost.",
        "features": [
            "Большой склад запчастей Indesit",
            "Ремонт за 1 визит в 80% случаев",
            "Опыт с моделями SAA, TIA, BIA, BCB",
        ],
        "common_issues": [
            "Не включается — замена пускового реле",
            "Намерзает на задней стенке — ремонт оттайки",
            "Сильный шум — замена компрессора или вентилятора",
        ],
        "meta_description": "Ремонт холодильников Indesit в Минске на дому. Большой склад запчастей, гарантия 1 год. +375 (29) 609-54-31.",
    },
    "beko": {
        "intro": "BEKO — турецкая техника, популярная в Беларуси. Знаем особенности их компрессоров и электроники, чиним даже сложные случаи.",
        "features": [
            "Опыт с системой NeoFrost Dual Cooling",
            "Запчасти BEKO под заказ за 1–3 дня",
            "Ремонт всех серий: CN, RCNA, RCSA, MN",
        ],
        "common_issues": [
            "Не охлаждает камера — диагностика контура",
            "Намерзает лёд — ремонт системы No Frost",
            "Ошибка на табло — диагностика платы",
        ],
        "meta_description": "Ремонт холодильников BEKO в Минске на дому. NeoFrost, плата управления, компрессор. Гарантия 1 год. +375 (29) 609-54-31.",
    },
    "bosch": {
        "intro": "BOSCH — немецкая надёжность, но и сложная электроника. Мы — сертифицированные мастера, работаем со всеми сериями: KGN, KGE, KGV, KAN.",
        "features": [
            "Опыт с системой VitaFresh и NoFrost Multi Airflow",
            "Программирование плат и сброс ошибок",
            "Только оригинальные запчасти BOSCH",
        ],
        "common_issues": [
            "Мигает лампочка температуры — диагностика датчиков",
            "Не работает дисплей — замена платы управления",
            "Слабое охлаждение — поиск утечки фреона",
        ],
        "meta_description": "Ремонт холодильников BOSCH в Минске на дому. VitaFresh, NoFrost, оригинальные запчасти. Гарантия 1 год. +375 (29) 609-54-31.",
    },
    "ariston": {
        "intro": "ARISTON — итальянский дизайн и собственные технологии. Чиним все модели: BCB, EBM, BMBL. Опытные мастера, оригинальные запчасти.",
        "features": [
            "Опыт с системой NaturFresh и Active Oxygen",
            "Аккуратная работа с фасадами Inox",
            "Замена компрессоров, термостатов, плат",
        ],
        "common_issues": [
            "Не охлаждает — диагностика и заправка фреоном",
            "Не работает No Frost — ремонт вентилятора и ТЭНа",
            "Стук и шум — замена компрессора",
        ],
        "meta_description": "Ремонт холодильников ARISTON в Минске на дому. NaturFresh, Active Oxygen, гарантия 1 год. +375 (29) 609-54-31.",
    },
    "liebherr": {
        "intro": "LIEBHERR — премиальная немецкая техника. Требует точной диагностики и оригинальных запчастей. У нас огромный опыт работы с моделями SBSes, CNP, CBNes.",
        "features": [
            "Опыт с системой BioFresh и SmartFrost",
            "Диагностика премиальных моделей LIEBHERR",
            "Только оригинальные запчасти, бережная работа",
        ],
        "common_issues": [
            "Мигает индикатор — диагностика платы",
            "Не работает вентиляция — замена вентиляторов BioFresh",
            "Слабое охлаждение — поиск утечки в контуре",
        ],
        "meta_description": "Ремонт холодильников LIEBHERR в Минске на дому. BioFresh, SmartFrost, оригинальные запчасти, гарантия 1 год. +375 (29) 609-54-31.",
    },
    "aeg": {
        "intro": "AEG — премиальная немецкая марка из группы Electrolux. Работаем со всеми сериями: SCB, SCN, RCB. Опытные мастера, аккуратное обращение с техникой.",
        "features": [
            "Опыт с системой LowFrost и Multi-Air Flow",
            "Замена силовых модулей и компрессоров AEG",
            "Бережная работа с моделями встройки",
        ],
        "common_issues": [
            "Ошибка на дисплее — диагностика и сброс",
            "Не охлаждает — замена компрессора или заправка",
            "Не работает оттайка — ремонт ТЭНа и таймера",
        ],
        "meta_description": "Ремонт холодильников AEG в Минске на дому. LowFrost, Multi-Air Flow, гарантия 1 год. +375 (29) 609-54-31.",
    },
}


def build_brands_seed() -> list:
    """Combine brand list with details."""
    brands = []
    for b in BRAND_LIST:
        d = BRAND_DETAILS.get(b["slug"], {})
        brands.append(
            {
                "slug": b["slug"],
                "name": b["name"],
                "name_en": b["name_en"],
                "country": b["country"],
                "intro": d.get("intro", ""),
                "features": d.get("features", []),
                "common_issues": d.get("common_issues", []),
                "meta_description": d.get("meta_description", ""),
                "price_overrides": [],
            }
        )
    return brands


INITIAL_BRANDS = build_brands_seed()
