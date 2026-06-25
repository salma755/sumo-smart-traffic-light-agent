from env import Environment
from agent import Agent
from episode import run_episode
from settings import load_testing_settings
import constants

def test():
    # 1. تحميل إعدادات الاختبار من ملف الـ YAML
    # تأكد أن ملف testing_settings.yaml يحتوي على gui: true لرؤية المحاكي
    settings = load_testing_settings()
    
    if settings is None:
        print("Error: Could not load testing settings.")
        return

    # 2. إنشاء بيئة الاختبار
    env = Environment(
        n_cars_generated=settings['n_cars_generated'],
        max_steps=settings['max_steps'],
        yellow_duration=settings['yellow_duration'],
        green_duration=settings['green_duration'],
        turn_chance=settings['turn_chance'],
        sumocfg_file=settings['sumocfg_file'], # سيقرأه كنص من ملف الـ settings
        gui=settings['gui']
    )
    
    # 3. تحميل العميل (الذكاء الاصطناعي) مع الموديل الجاهز
    # وضعنا epsilon=0.0 لكي لا يتخذ العميل أي قرارات عشوائية أبداً
    agent = Agent(
        settings=settings,
        epsilon=0.0, 
        model_path="trained_model.pt" # المسار الذي تم حفظ الموديل فيه بعد التدريب
    )

    print("--- Starting Testing Simulation ---")
    
    # 4. تشغيل جولة اختبار واحدة
    # نستخدم seed ثابت (مثلاً 42) لضمان تكرار نفس سيناريو الزحام عند كل اختبار
    run_episode(env, agent, seed=settings.get('seed', 42))
    
    print("Testing finished successfully.")

if __name__ == "__main__":
    test()