import random
import numpy as np

# استيراد الثوابت والموديل
from constants import NUM_ACTIONS, STATE_SIZE
from model import Model

class Agent:
    def __init__(self, settings, epsilon=1.0, model_path=None):
        """
        تعريف العميل (الذكاء الاصطناعي)
        """
        self.epsilon = epsilon # نسبة العشوائية في البداية
        
        # إنشاء الموديل (الشبكة العصبية) باستخدام الإعدادات
        self.model = Model(
            num_layers=settings['num_layers'],
            width=settings['width_layers'],
            learning_rate=settings['learning_rate'],
            input_dim=STATE_SIZE,
            output_dim=NUM_ACTIONS,
            model_path=model_path  # سيكون نص (String) أو None
        )

    def set_epsilon(self, epsilon):
        """تحديث قيمة العشوائية"""
        self.epsilon = epsilon

    def choose_action(self, state):
        """
        اختيار حركة: إما عشوائياً (للتعلم) أو بناءً على الموديل (للذكاء)
        """
        # إذا كان الرقم العشوائي أقل من epsilon، نختار حركة عشوائية (Exploration)
        if random.random() < self.epsilon:
            return random.randrange(NUM_ACTIONS)

        # غير ذلك، نستخدم الموديل لتوقع أفضل حركة (Exploitation)
        q_values = self.model.predict_one(state)
        return int(np.argmax(q_values))

    def replay(self, memory, gamma, batch_size):
        """
        عملية التعلم من الذاكرة (Experience Replay)
        """
        # سحب عينة عشوائية من الذاكرة
        batch = memory.get_samples(batch_size)
        if not batch:
            return

        # تحويل البيانات لمصفوفات numpy للمعالجة السريعة
        states = np.array([sample.state for sample in batch])
        next_states = np.array([sample.next_state for sample in batch])

        # الحصول على توقعات الموديل الحالية
        q_values = self.model.predict_batch(states)
        next_q_values = self.model.predict_batch(next_states)

        x = states # المدخلات للتدريب
        y = q_values.copy() # الأهداف (Targets) التي نريد الوصول لها

        # تحديث قيمة Q بناءً على معادلة Bellman
        for i, sample in enumerate(batch):
            # الهدف الجديد = المكافأة + (معامل الخصم * أعلى توقع للمستقبل)
            target = sample.reward + gamma * np.max(next_q_values[i])
            y[i, sample.action] = target

        # تدريب الموديل على البيانات الجديدة
        self.model.train_batch(x, y)

    def save_model(self, out_path):
        """حفظ الموديل المدرب في المسار المحدد"""
        self.model.save_model(out_path)