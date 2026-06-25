from agent import Agent
from env import Environment

# كلاس بسيط لتخزين بيانات كل خطوة (الحالة، القرار، المكافأة)
class Record:
    def __init__(self, state, action, reward):
        self.state = state
        self.action = action
        self.reward = reward

def run_episode(env, agent, seed):
    # 1. توليد ملف سيارات جديد لهذه الجولة
    env.generate_routefile(seed=seed)

    previous_total_wait = 0.0
    history = [] # قائمة لتخزين سجل الجولة للتدريب

    # 2. بدء تشغيل المحاكي
    env.activate()

    # 3. حلقة المحاكاة (تستمر حتى ينتهي الوقت المحدد)
    while not env.is_over():
        # الحصول على حالة الشوارع الحالية
        state = env.get_state()
        
        # اطلب من العميل (الذكاء الاصطناعي) اختيار قرار (أكشن)
        action = agent.choose_action(state)

        # تنفيذ القرار في البيئة
        env.execute(action)

        # حساب المكافأة (Reward) بناءً على تحسن وقت الانتظار
        current_total_wait = env.get_cumulated_waiting_time()
        reward = previous_total_wait - current_total_wait
        previous_total_wait = current_total_wait

        # حفظ هذه الخطوة في السجل (History)
        record = Record(state=state, action=action, reward=reward)
        history.append(record)

    print(f"DEBUG: Episode finished. Steps recorded: {len(history)}")

    # 4. إغلاق المحاكي بعد انتهاء الجولة
    env.deactivate()

    # إرجاع السجل فقط (بدون EnvStats)
    return history