import yaml

def load_settings(file_path):
    # تم إضافة encoding='utf-8' لضمان قراءة الملفات بشكل صحيح على ويندوز
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_training_settings():
    return load_settings("training_settings.yaml")

def load_testing_settings():
    return load_settings("testing_settings.yaml")