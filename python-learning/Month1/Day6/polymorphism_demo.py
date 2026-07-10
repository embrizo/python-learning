class Cat:

    def speak(self):
        print("Meow")

class Dog:
    def speak(self):
        print("Woof")

animals = [Cat(),Dog()]
for animal in animals:
    animal.speak()


class OpenAIModel:

    def prompt(self,msg:str)->str:
        return f"OpenAI: {msg}"

class GeminiModel:
    def prompt(self,msg:str)->str:
        return f"Gemini: {msg}"

class DeepSeekModel:
    def prompt(self,msg:str)->str:
        return f"DeepSeek: {msg}"


models = [OpenAIModel(),GeminiModel(),DeepSeekModel()]

for model in models:
    print(model.prompt("Hello"))

    