from env import Environment
from agent import Agent
from memory import Memory, Sample
from episode import run_episode
from settings import load_training_settings
import constants

def main():
    # 1. تحميل الإعدادات من ملف الـ YAML
    settings = load_training_settings() 
    if settings is None:
        return

    # 2. إنشاء بيئة المحاكاة
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
        # طباعة رقم الجولة وقيمة Epsilon الحالية (نسبة العشوائية)
        print(f"--- Episode {episode + 1}/{settings['total_episodes']} (Exploration: {agent.epsilon:.2f}) ---")
        
        # تشغيل الجولة وجمع التاريخ (history)
        # لاحظ هنا حذفنا (_) لأننا لغينا EnvStats
        history = run_episode(env, agent, seed=episode)
        
        # تخزين ما حدث في هذه الجولة داخل الذاكرة
        for i in range(len(history) - 1):
            sample = Sample(
                state=history[i].state,
                action=history[i].action,
                reward=history[i].reward,
                next_state=history[i+1].state
            )
            memory.add_sample(sample)

            print(f"Current Memory Size: {len(memory)} / {settings['memory_size_min']}")

        # بدء عملية التعلم (Replay) إذا جمعنا تجارب كافية
        if len(memory) >= settings['memory_size_min']:
            print("Learning from experience...")
            agent.replay(
                memory, 
                gamma=settings['gamma'], 
                batch_size=settings['batch_size']
            )


            
            # تقليل العشوائية (Epsilon Decay) بعد كل جولة يتعلم فيها
            # لكي يبدأ العميل بالاعتماد على ذكائه أكثر من الحظ
            if agent.epsilon > 0.01:
                agent.set_epsilon(agent.epsilon * 0.96)

            
    # 5. حفظ النموذج المدرب (استخدمنا نص عادي للمسار)
    save_path = "/home/sofyan/Desktop/ML_project/trained_model.pt"
    agent.save_model(save_path)
    print(f"Success! Model saved to: {save_path}")

if __name__ == "__main__":
    main()