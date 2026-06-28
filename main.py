from env import Environment
from agent import Agent
from memory import Memory, Sample
from episode import run_episode
from settings import load_training_settings
import constants
import os

def main():
    # 1. تحميل الإعدادات من ملف الـ YAML
    settings = load_training_settings() 
    if settings is None:
        print("Error: Could not load settings.")
        return

    # 2. إنشاء بيئة المحاكاة
    # ملاحظة: تأكد من ضبط gui: True في ملف training_settings.yaml لتظهر الخريطة
    env = Environment(
        n_cars_generated=settings['n_cars_generated'],
        max_steps=settings['max_steps'],
        yellow_duration=settings['yellow_duration'],
        green_duration=settings['green_duration'],
        turn_chance=settings['turn_chance'],
        sumocfg_file=settings['sumocfg_file'],
        gui=settings['gui']
    )
    
    # 3. إنشاء العميل (الذكاء الاصطناعي) والذاكرة
    agent = Agent(settings=settings)
    memory = Memory(size_max=settings['memory_size_max'], size_min=settings['memory_size_min'])

    # 4. حلقة التدريب (الجولات)
    for episode in range(settings['total_episodes']):
        # طباعة رقم الجولة وقيمة Exploration (نسبة العشوائية في اتخاذ القرار)
        print(f"--- Episode {episode + 1}/{settings['total_episodes']} (Exploration: {agent.epsilon:.2f}) ---")
        
        # تشغيل الجولة وجمع البيانات
        history = run_episode(env, agent, seed=episode)
        
        # تخزين الخبرات في الذاكرة ليتعلم منها العميل لاحقاً
        for i in range(len(history) - 1):
            sample = Sample(
                state=history[i].state,
                action=history[i].action,
                reward=history[i].reward,
                next_state=history[i+1].state
            )
            memory.add_sample(sample)

        # عرض حجم الذاكرة الحالي
        print(f"Current Memory Size: {len(memory)} / {settings['memory_size_min']}")

        # بدء عملية التعلم (Experience Replay) إذا امتلأت الذاكرة بالحد الأدنى
        if len(memory) >= settings['memory_size_min']:
            print("Learning from experience...")
            agent.replay(
                memory, 
                gamma=settings['gamma'], 
                batch_size=settings['batch_size']
            )
            
            # تقليل العشوائية (Epsilon Decay) لزيادة اعتماد العميل على خبرته
            if agent.epsilon > 0.01:
                agent.set_epsilon(agent.epsilon * 0.96)

    # 5. حفظ النموذج المدرب
    # تم تعديل المسار ليتم الحفظ في نفس مجلد المشروع الحالي بدلاً من مسار جهاز زميلك
    save_path = "trained_model.pt"
    agent.save_model(save_path)
    print(f"Success! Model saved to: {os.path.abspath(save_path)}")

if __name__ == "__main__":
    main()