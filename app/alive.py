from faker import Faker

fake = Faker()


def say_hello():
    return u"Hello World\nFrom : {} ".format(fake.name())
