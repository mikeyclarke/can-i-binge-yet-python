from slugify import slugify


class SlugGenerator:
    def generate(self, text_to_slugify: str, max_length: int = 120) -> str:
        result = slugify(text_to_slugify, max_length=max_length)

        if len(result) == 0:
            raise RuntimeError(f'{text_to_slugify} cannot be slugified')

        return result
