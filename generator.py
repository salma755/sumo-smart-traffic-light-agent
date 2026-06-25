import random
import numpy as np # سنبقيها فقط لتوليد الأرقام العشوائية بسهولة
from constants import (
    ROUTES_FILE,
    ROUTES_FILE_HEADER,
    STRAIGHT_ROUTES,
    TURN_ROUTES,
)

def generate_routefile(seed, n_cars_generated, max_steps, turn_chance):
    """
    دالة بسيطة لتوليد ملف حركة السيارات (XML) لبرنامج SUMO.
    """
    # 1. ضبط العشوائية لضمان نفس النتائج عند استخدام نفس الـ seed
    random.seed(seed)
    np.random.seed(seed)

    # 2. توليد أوقات ظهور السيارات بشكل عشوائي وتمريرها عبر الزمن
    # نختار أوقات عشوائية بين البداية ونهاية المحاكاة
    depart_steps = np.random.randint(0, max_steps, size=n_cars_generated)
    depart_steps.sort() # نرتبهم زمنياً من الأصغر للأكبر

    # 3. فتح ملف المسارات للكتابة (بالطريقة التقليدية)
    # ROUTES_FILE هنا هو نص (String) كما اتفقنا سابقاً
    with open(ROUTES_FILE, "w", encoding="utf-8") as routes_file:
        # كتابة ترويسة ملف الـ XML
        routes_file.write(ROUTES_FILE_HEADER + "\n")

        # 4. لكل سيارة، نحدد مسارها ووقت انطلاقها
        for i, step in enumerate(depart_steps):
            # هل السيارة ستنعطف أم تمشي في خط مستقيم؟
            if random.random() < turn_chance:
                route_id = random.choice(TURN_ROUTES)
            else:
                route_id = random.choice(STRAIGHT_ROUTES)

            # كتابة سطر السيارة بتنسيق SUMO
            car_row = f'    <vehicle id="{route_id}_{i}" type="standard_car" route="{route_id}" depart="{step}" departLane="random" departSpeed="10" />'
            routes_file.write(car_row + "\n")

        # إغلاق وسم الـ XML
        routes_file.write("</routes>")

    print(f"Route file generated successfully: {ROUTES_FILE}")