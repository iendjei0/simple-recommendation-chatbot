from recipe_data.scraper import Recipe, import_data
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter
from difflib import SequenceMatcher

# Maybe swap with semantic similarity
def string_similarity(str1: str, str2: str) -> float:
    return SequenceMatcher(None, str1, str2).ratio()

def get_recipe_keywords(recipe: Recipe) -> list:
    result = f"{recipe.name} {recipe.category} {recipe.area} {' '.join(recipe.tags + recipe.ingredients)}"
    return [r.lstrip("(").rstrip(")") for r in result.lower().split()]

def get_unique_db_keywords() -> list:
    result = []
    for recipe in RECIPE_DATA:
        result += get_recipe_keywords(recipe)
    return list(set(result))

def get_important_keywords(prompt: str) -> list:
    result = set()
    prompt_keywords = prompt.lower().split()
    for keyword in UNIQUE_KEYWORDS:
        for prompt_keyword in prompt_keywords:
            if string_similarity(keyword, prompt_keyword) > 0.95:
                result.add(keyword)
    result = list(result)
    print(result)
    return result

def list_similarity(list1: list, list2: list) -> float:
    if [] in [list1, list2]:
        return 0

    count = 0
    for item in list1:
        if item in list2:
            count += 3
    for item in list2:
        if item in list1:
            count += 1
    return count / len(list1*3+list2)

RECIPE_DATA = import_data("recipe_data/recipes.csv")
UNIQUE_KEYWORDS = get_unique_db_keywords()

class ChatModel(ChatBot):
    def __init__(self):
        print(RECIPE_DATA[0])
        super().__init__('Recommender')
        if not SQLStorageAdapter().count():
            trainer = ChatterBotCorpusTrainer(self)
            trainer.train("chatterbot.corpus.english.food")
            trainer.train("chatterbot.corpus.english.greetings")
            trainer.train("chatterbot.corpus.english.conversations")
            trainer.train("chatterbot.corpus.english.emotion")

    def get_casual_response(self, prompt: str) -> str:
        return super().get_response(prompt)
    
    def find_recipe(self, prompt: str) -> str:
        good_recipes = []
        prompt_keywords = get_important_keywords(prompt)
        for recipe in RECIPE_DATA:
            recipe_keywords = get_recipe_keywords(recipe)
            score = list_similarity(prompt_keywords, recipe_keywords)
            if score > 0.2:
                good_recipes.append((recipe, score))
        good_recipes.sort(key=lambda x: x[1], reverse=True)
        good_recipes = [x[0] for x in good_recipes]
        if good_recipes:
            RECIPE_CONVERSATION = True
            return good_recipes[0]
        else:
            RECIPE_CONVERSATION = False
            return self.get_casual_response(prompt)
