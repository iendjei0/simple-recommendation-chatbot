from src.model import ChatModel
import os
import shutil
import pytest

model = ChatModel()

COOKBOOK_PATH = "cookbook.txt"
TEMP_PATH = "temp.txt"

def backup_cookbook():
    if os.path.exists(COOKBOOK_PATH):
        shutil.copy(COOKBOOK_PATH, TEMP_PATH)
        os.remove(COOKBOOK_PATH)

def restore_cookbook():
    if os.path.exists(COOKBOOK_PATH):
        os.remove(COOKBOOK_PATH)
    if os.path.exists(TEMP_PATH):
        shutil.move(TEMP_PATH, COOKBOOK_PATH)

ASK_FOR_INFO = "Tell me more about the dish you're looking for."
RECIPE_FOUND = "I found a recipe for you!"      # use startswith
NOTHING_FOUND = "I can't find anything in the database. Can I help you with anything else?"
ASK_COOKBOOK = "Would you like me to save this recipe to your cookbook?"
YES_COOKBOOK_NEW = " saved to your cookbook."   # use endswith
YES_COOKBOOK_OLD = "This recipe is already in your cookbook."
NO_COOKBOOK = "Operation cancelled."

def test_backup_cookbook():
    backup_cookbook()

def test_eat_italian_thanks():
    assert (model.get_response
            ("I would love to eat something") == 
            ASK_FOR_INFO)
    assert (model.get_response
            ("I want to try something italian").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("Thank you very much") == 
            NOTHING_FOUND)

def test_eat_italian_cookbook_yes():
    assert (model.get_response
            ("What can I make?") ==
            ASK_FOR_INFO)
    assert (model.get_response
            ("Right now i just have pasta").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("This is great! Can you save it?") ==
            ASK_COOKBOOK)
    assert (model.get_response
            ("Yes, please").endswith
            (YES_COOKBOOK_NEW))

def test_eat_italian_cookbook_no():
    assert (model.get_response
            ("What can I make?") ==
            ASK_FOR_INFO)
    assert (model.get_response
            ("Right now i just have pasta").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("This is great! Can you save it?") ==
            ASK_COOKBOOK)
    assert (model.get_response
            ("Actually no I changed my mind") ==
            NO_COOKBOOK)

def test_save_duplicate_recipe():
    assert (model.get_response
            ("What can I make?") ==
            ASK_FOR_INFO)
    assert (model.get_response
            ("Right now i just have pasta").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("This is great! Can you save it?") ==
            ASK_COOKBOOK)
    assert (model.get_response
            ("Yes, please").endswith
            (YES_COOKBOOK_OLD))

def test_EatItalianCookbook_yes():
    response = model.get_response(
        "I wanna eat something italian. Can you add it to the list?")
    assert (response.startswith(RECIPE_FOUND) and
            response.endswith(ASK_COOKBOOK))
    assert (model.get_response
            ("Sure, add it").endswith
            (YES_COOKBOOK_NEW))
    
def test_EatPolish_NextCabbage_cookbook_yes():
    assert (model.get_response
            ("I want to eat something polish").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("Show me something else. I have cabbage").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("Can you save it?") ==
            ASK_COOKBOOK)
    assert (model.get_response
            ("Hell yeah!").endswith
            (YES_COOKBOOK_NEW))

def test_EatBBQ_next_NextCookbook_NextMeat_yes():
    assert (model.get_response
            ("A bbq meal would be great").startswith
            (RECIPE_FOUND))
    assert (model.get_response
            ("Any other alternatives?").startswith
            (RECIPE_FOUND))
    response = model.get_response(
        "I want something different. Also is there a way to store the recipe?")
    assert (response.startswith(RECIPE_FOUND) and
            response.endswith(ASK_COOKBOOK))
    response = model.get_response(
        "Im looking for something with more meat")
    assert (response.startswith(RECIPE_FOUND) and
            response.endswith(ASK_COOKBOOK))
    assert (model.get_response
            ("That's the one! I want to save it for sure!").endswith
            (YES_COOKBOOK_NEW))
    
def test_restore_cookbook():
    restore_cookbook()