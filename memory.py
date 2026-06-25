import random

# كلاس بسيط لتمثيل "تجربة" واحدة
class Sample:
    def __init__(self, state, action, reward, next_state):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state

class Memory:
    def __init__(self, size_max, size_min):
        self.samples = []      # قائمة لتخزين التجارب
        self.size_max = size_max # أقصى عدد تجارب ممكن تخزينه
        self.size_min = size_min # أقل عدد تجارب لازم يتوفر قبل ما نبدأ تدريب

    def add_sample(self, sample):
        """إضافة تجربة جديدة للذاكرة"""
        self.samples.append(sample)
        
        # إذا زاد عدد التجارب عن الحد الأقصى، نحذف أقدم تجربة
        if len(self.samples) > self.size_max:
            self.samples.pop(0)

    def get_samples(self, n):
        """سحب مجموعة (Batch) عشوائية من التجارب للتدريب"""
        # إذا كان عدد التجارب أقل من الحد الأدنى المطلوب، لا نسحب شيء
        if len(self.samples) < self.size_min:
            return []

        # سحب n من التجارب بشكل عشوائي
        num_to_sample = min(n, len(self.samples))
        return random.sample(self.samples, num_to_sample)

    def __len__(self):
        """دالة تعطينا عدد التجارب الموجودة حالياً"""
        return len(self.samples)