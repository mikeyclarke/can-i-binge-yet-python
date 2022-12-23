from random import SystemRandom
import string


safe_random = SystemRandom()


class AlphaNumericIdGenerator:
    def generate(self, length: int) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(safe_random.choices(characters, k=length))
