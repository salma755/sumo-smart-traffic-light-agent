import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import os
# كلاس بناء الشبكة العصبية (Multi-Layer Perceptron)
class MLP(nn.Module):
    def __init__(self, input_dim, output_dim, num_layers, width):
        super(MLP, self).__init__()

        layers = []
        # الطبقة الأولى (المدخلات)
        layers.append(nn.Linear(input_dim, width))
        layers.append(nn.ReLU()) # دالة التنشيط

        # الطبقات المخفية (Hidden Layers)
        for _ in range(num_layers):
            layers.append(nn.Linear(width, width))
            layers.append(nn.ReLU())

        # الطبقة الأخيرة (المخرجات - الأفعال)
        layers.append(nn.Linear(width, output_dim))

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


# كلاس إدارة الموديل (التدريب، التوقع، الحفظ)
class Model:
    def __init__(self, num_layers, width, learning_rate, input_dim, output_dim, model_path=None):
        self.input_dim = input_dim
        self.output_dim = output_dim

        # التحقق إذا كان هناك موديل جاهز لتحميله
        if model_path and os.path.exists(model_path):
            print(f"Loading trained model from {model_path}")
            self.model = torch.load(model_path, map_location="cpu", weights_only=False)
        else:
            print("Creating a new neural network model")
            self.model = MLP(input_dim, output_dim, num_layers, width)

        # دالة حساب الخطأ (MSE) والمحسن (Adam)
        self.loss_fn = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def predict_one(self, state):
        """توقع مخرجات لحالة واحدة فقط"""
        state = np.array(state, dtype=np.float32).reshape(1, -1)
        return self.predict_batch(state)

    def predict_batch(self, states):
        """توقع مخرجات لمجموعة من الحالات"""
        self.model.eval() # وضع التقييم
        with torch.no_grad():
            states_t = torch.from_numpy(np.array(states, dtype=np.float32))
            return self.model(states_t).numpy()

    def train_batch(self, states, targets):
        """تدريب الشبكة على مجموعة من البيانات"""
        self.model.train() # وضع التدريب
        
        states_t = torch.from_numpy(np.array(states, dtype=np.float32))
        targets_t = torch.from_numpy(np.array(targets, dtype=np.float32))

        # عملية التحسين وتحديث الأوزان
        self.optimizer.zero_grad()
        predictions = self.model(states_t)
        loss = self.loss_fn(predictions, targets_t)
        loss.backward()
        self.optimizer.step()

    def save_model(self, path):
        """حفظ الموديل في مسار محدد"""
        # التأكد من وجود المجلد
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
            
        torch.save(self.model, path)
        print(f"Model saved to {path}")