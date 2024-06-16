import requests
import csv
import sys

class Recipe:
    def __init__(self): #empty
        self.id = None
        self.name = None
        self.category = None
        self.area = None
        self.instructions = None
        self.tags = []
        self.ingredients = []
        self.measures = []    

    def set_data_from_api(self, data: dict):
        self.id = data['idMeal']
        self.name = data['strMeal']
        self.category = data['strCategory']
        self.area = data['strArea']
        self.instructions = data['strInstructions'].rstrip()
        self.tags = (data['strTags'] or '').split(',')
        self.ingredients = []
        self.measures = []
        for i in range(1, 21):
            ingredient = data[f'strIngredient{i}']
            measure = data[f'strMeasure{i}']
            if ingredient:
                self.ingredients.append(ingredient.rstrip())
                self.measures.append(measure.rstrip())
            else:
                break
        return self

    def set_data_from_csv(self, data: dict):
        self.id = data['idMeal']
        self.name = data['strMeal']
        self.category = data['strCategory']
        self.area = data['strArea']
        self.instructions = data['strInstructions'].rstrip()
        self.tags = (data['strTags'] or '').split(',')
        self.ingredients = (data['strIngredient'] or '').split(',')
        self.measures = (data['strMeasure'] or '').split(',')
        return self
    
    def __str__(self):
        result = "====================================\n"
        result += f"{self.name} ({self.category})\n"
        result += f"Area: {self.area}\n"
        result += f"Tags: {', '.join(self.tags)}\n"
        result += "Ingredients:\n"
        for i, (ingredient, measure) in enumerate(zip(self.ingredients, self.measures), 1):
            result += f"{i}. {ingredient.rstrip()} ({measure.rstrip()})\n"
        result += f"Instructions: {self.instructions}\n"
        result += "===================================="
        return result
    
    def to_row(self):
        return [self.name, self.category, self.area, self.instructions, ','.join(self.tags), ','.join(self.ingredients), ','.join(self.measures)]

def get_data():
    result = []
    for i in range(319):
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={52764+i}"
        response = requests.get(url)
        data = response.json()
        print(f"Getting data for recipe {i+1}/{319}")
        if data['meals'] is not None:
            result.append(Recipe().set_data_from_api(data['meals'][0]))
        else:
            print(f"Recipe {i+1} is null")
    return result

def export_data(data):
    with open('recipes.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Category', 'Area', 'Instructions', 'Tags', 'Ingredients', 'Measures'])
        for recipe in data:
            writer.writerow(recipe.to_row())

def import_data():
    result = []
    with open('recipes.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data = {
                'idMeal': None,  # or provide a default value
                'strMeal': row[0],
                'strCategory': row[1],
                'strArea': row[2],
                'strInstructions': row[3],
                'strTags': row[4],
                'strIngredient': row[5],
                'strMeasure': row[6]
            }
            recipe = Recipe().set_data_from_csv(data)
            result.append(recipe)
    return result

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'get':
        data = get_data()
        export_data(data)
    elif len(sys.argv) > 1 and sys.argv[1] == 'show':
        data = import_data()
        for recipe in data:
            print(recipe)
    else:
        print("Bad argument (use 'get' or 'show')")
