class FileReader:
    def read(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            content = file.read()

        return content
