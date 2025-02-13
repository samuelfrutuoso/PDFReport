from faker import Faker

def generate_fake(model: dict):
  fake = Faker()
  getattr(fake, 'email')
