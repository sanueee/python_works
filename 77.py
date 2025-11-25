import requests
import re

class MyFile:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode
        self.content = None

    def read(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def write(self, text):
        try:
            mode = 'w' if self.mode == 'write' else 'a' #либо write либо append
            with open(self.path, mode, encoding='utf-8') as f:
                f.write(text)
            return True
        except PermissionError:
            print(f"Ошибка: нет прав для записи в файл '{self.path}'")
            return False
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
            return False

    def write_url(self, filename):
        try:
            if self.content is None:
                self.read_url()
            if self.content is None:
                print("Ошибка: не удалось получить содержимое страницы")
                return False
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"Содержимое сохранено в файл '{filename}'")
            return True
        except PermissionError:
            print(f"Ошибка: нет прав для записи в файл '{filename}'")
            return False
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")
            return False

    def read_url(self):
        try:
            response = requests.get(self.path, timeout=10)
            response.raise_for_status()
            self.content = response.text
            return self.content
        except requests.exceptions.ConnectionError:
            print(f"Ошибка: не удалось подключиться к {self.path}")
            return None
        except requests.exceptions.Timeout:
            print(f"Ошибка: превышено время ожидания для {self.path}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка HTTP: {e}")
            return None
        except Exception as e:
            print(f"Ошибка при чтении URL: {e}")
            return None

    def count_urls(self):
        try:
            if self.content is None:
                self.read_url()
            if self.content is None:
                return 0
            urls = re.findall(r'https?://[^\s<>"]+', self.content)
            return len(urls)
        except Exception as e:
            print(f"Ошибка при подсчете URL: {e}")
            return 0
