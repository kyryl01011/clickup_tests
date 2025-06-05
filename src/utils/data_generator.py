from faker import Faker

from src.data_models.tasks import CreationTaskModel


fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_word():
        return fake.word()

    @staticmethod
    def generate_random_int():
        return fake.random_int(0, 999)

    @classmethod
    def generate_task_data(cls):
        return CreationTaskModel(
            name=f'{cls.generate_random_word()}{cls.generate_random_int()}'
        )
