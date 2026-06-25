import yaml

def load_settings(file_path):
    # فتح الملف وقراءته فوراً
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_training_settings():
    return load_settings("training_settings.yaml")

def load_testing_settings():
    return load_settings("testing_settings.yaml")