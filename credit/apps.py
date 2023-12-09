from django.apps import AppConfig
import os
import pickle
from django.conf import settings

class CreditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'credit'


class ModelConfig(AppConfig):
    model_file_path = os.path.join(settings.MODEL, "score_model.pkl")

    with open(model_file_path, 'rb') as model_file:
        model = pickle.load(model_file)

