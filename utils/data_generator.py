from faker import Faker

fake = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_word():
        return fake.word()

    @staticmethod
    def generate_random_int():
        return fake.random_int(0,999)