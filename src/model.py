from src.recipe_data.scraper import Recipe, import_data
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

RECIPE_DATA = import_data("src/recipe_data/recipes.csv")
UNIQUE_KEYWORDS = get_unique_db_keywords()

CONVERSATION_LEADS = {
    "find_recipe": ["find", "recipe", "hungry", "want", "make", "food", "meal", "dish", "eat", "craving", "dinner", "lunch", "breakfast", "snack", "dessert"],
    "different_recipe": ["next", "another", "different", "new", "more", "else", "alternative", "other", "change", "switch"],
    "yes": ["yes", "sure", "okay", "fine", "good", "great", "awesome", "cool", "nice", "alright", "yep", "yup", "yea", "yeah", "correct", "right", "affirmative", "positive", "true", "accurate", "indeed", "absolutely", "definitely", "certainly", "of course", "obviously", "clearly", "undoubtedly", "surely", "truly"],
    "no": ["no", "nah", "nope", "negative", "wrong", "incorrect", "false", "untrue"],
    "thanks": ["thanks", "thank", "thankyou", "thank you", "appreciate", "grateful", "gratitude", "blessed", "bless", "blessing", "blessings", "blessed", "blessed"],
    "cookbook": ["cookbook", "cook book", "recipe list", "recipe book", "collection", "list", "database", "add", "append", "insert", "include", "store", "save", "favourite", "favorite", "fav", "favourites", "favorites"]
}

def conversation_lead_found(prompt: str, lead: str) -> bool:
    for keyword in CONVERSATION_LEADS[lead]:
        if keyword in prompt:
            return True
    return False


class ChatModel(ChatBot):
    def __init__(self):
        super().__init__('Recommender')
        if not SQLStorageAdapter().count():
            trainer = ChatterBotCorpusTrainer(self)
            trainer.train("chatterbot.corpus.english.food")
            trainer.train("chatterbot.corpus.english.greetings")
            trainer.train("chatterbot.corpus.english.conversations")
            trainer.train("chatterbot.corpus.english.emotion")
        self.COOKBOOK_MENTIONED = False
        self.CONVERSATION_PHASE = 'casual'
        self.current_recipes = RECIPE_DATA
        self.current_keywords = []

    def reset_recipe_search(self) -> None:
        self.current_recipes = RECIPE_DATA
        self.current_keywords = []
    
    def set_cookbook_mention(self, prompt: str) -> bool:
        self.COOKBOOK_MENTIONED = (True if self.COOKBOOK_MENTIONED else conversation_lead_found(prompt, "cookbook"))
        return self.COOKBOOK_MENTIONED

    def get_casual_response(self, prompt: str) -> str:
        return super().get_response(prompt)
    
                                        # Think about those optional arguments, u need to return them
    def find_recipe(self, prompt: str) -> Recipe:
        self.current_keywords = list(set(self.current_keywords + get_important_keywords(prompt)))

        scored_recipes = []
        for recipe in self.current_recipes:
            recipe_keywords = get_recipe_keywords(recipe)
            score = list_similarity(self.current_keywords, recipe_keywords)
            if score > 0.15:
                scored_recipes.append((recipe, score))

        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        self.current_recipes = [x[0] for x in scored_recipes]

        print("a")
        print([d.name for d in self.current_recipes])
        print("b")
        print(self.current_keywords)

        if self.current_recipes:
            return self.current_recipes[0]
        else:
            self.reset_recipe_search()
            return None
    
    def next_recipe(self, prompt: str) -> Recipe:
        self.current_recipes = self.current_recipes[1:]
        return self.find_recipe(prompt)
    
    def is_recipe_in_cookbook(self, recipe: Recipe) -> bool:
        with open("cookbook.txt", "r", encoding='cp1252') as file:
            return recipe.__str__().strip("====================================") in file.read().split("====================================")

    def save_recipe(self, recipe: Recipe) -> None:
        with open("cookbook.txt", "a", encoding='utf-8') as file:
            if self.is_recipe_in_cookbook(recipe):
                return "This recipe is already in your cookbook."
            else:
                file.write(recipe.__str__().lstrip("===================================="))
                return f"Recipe: {recipe.name} saved to your cookbook."
        
    # TODO: eat italian > thanks
    def get_response(self, prompt: str) -> str:
        prompt = prompt.lower()
        result = None
        print(prompt, self.CONVERSATION_PHASE, self.COOKBOOK_MENTIONED)

        if self.CONVERSATION_PHASE == 'casual':
            if conversation_lead_found(prompt, "find_recipe"):
                self.COOKBOOK_MENTIONED = conversation_lead_found(prompt, "cookbook")
                self.CONVERSATION_PHASE = 'mention_recipe'
                result = self.find_recipe(prompt)
            else:
                return self.get_casual_response(prompt)

        if self.CONVERSATION_PHASE == 'mention_recipe':
            self.COOKBOOK_MENTIONED = conversation_lead_found(prompt, "cookbook")
            self.CONVERSATION_PHASE = 'first_recipe'
            if result == None:
                return "Tell me more about the dish you're looking for."
            
        if self.CONVERSATION_PHASE == 'first_recipe':
            result = self.find_recipe(prompt) #self changed

        if self.COOKBOOK_MENTIONED and self.CONVERSATION_PHASE != 'first_recipe':
            if conversation_lead_found(prompt, "yes") or conversation_lead_found(prompt, "no"):
                self.CONVERSATION_PHASE = 'casual'
                self.COOKBOOK_MENTIONED = False
                result = self.current_recipes[0]
                self.reset_recipe_search()

            if conversation_lead_found(prompt, "yes"):
                return self.save_recipe(result)
            elif conversation_lead_found(prompt, "no"):
                return "Operation cancelled."

        if self.CONVERSATION_PHASE == 'next_recipe':
            self.set_cookbook_mention(prompt)
            print(self.COOKBOOK_MENTIONED)
            if conversation_lead_found(prompt, "different_recipe"):
                result = self.next_recipe(prompt)
            elif self.COOKBOOK_MENTIONED:
                return "Would you like me to save this recipe to your cookbook?"
        
        if self.CONVERSATION_PHASE == 'first_recipe':
            self.set_cookbook_mention(prompt)
            self.CONVERSATION_PHASE = 'next_recipe'

        if result == None:
            self.CONVERSATION_PHASE = 'casual'
            self.COOKBOOK_MENTIONED = False
            self.reset_recipe_search()
            return "I can't find anything in the database. Can I help you with anything else?"

        print(self.COOKBOOK_MENTIONED)
        if self.COOKBOOK_MENTIONED:
            result = result.__str__() + "\nWould you like me to save this recipe to your cookbook?"
        
        if isinstance(result, Recipe):
            result = "I found a recipe for you!\n" + result.__str__()

        return result
