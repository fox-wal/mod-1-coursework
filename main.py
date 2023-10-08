#==============#
# MEAL PLANNER #
#==============#

from recipe import Recipe
from enum import Enum

# Global variables
EXIT_CHAR = "X"
EXIT_VALUE = -1

#                   #
# Generic Functions #
#                   #

# Display an error message.
def print_error(error_message: str):
    print("Error:", error_message)

# Display a menu with an index (starting from 1) before each item.
def display_menu(menu: list[str]):
    ERROR_NO_MENU = "No menu to display."

    # Check if there are any items in the menu.
    if menu.__len__() == 0:
        print(ERROR_NO_MENU)
        return

    # Display each item in the menu preceded by an index (starting from 1).
    for i in range(0, menu.__len__()):
        print(f"{i + 1}. {menu[i]}")

# Display a menu and prompt user to select an item.
# >> Return: the index selected, or -1 if the user entered "X".
def display_selection_menu(menu: list[str]) -> int:
    display_menu(menu)
    return user_selects_menu_item(menu.__len__())

# Display a section heading.
def print_heading(heading: str, new_line: bool = True):
    print("\n---", heading, "---")

# Prompt the user to enter an integer to select an item from a menu until they
# enter a valid number.
# >> Return: the index selected, or -1 if the user entered "X".
def user_selects_menu_item(menu_size: int) -> int:
    MIN = 1
    MAX = menu_size - 1

    PROMPT = f"Select an item from the menu using the index. Enter {EXIT_CHAR} to exit.\n"

    selection = input_int(PROMPT, MIN, MAX)

    return selection - 1

#--------------#
# View Recipes #
#--------------#

# Add the index of each recipe that satisfies the given filter condition to a list.
# >> Returns: list of indexes of recipes that satisfy the given filter condition.
def filter_recipes(recipes: list[Recipe], check_fits_filter: function(Recipe)) -> list[int]:
    filtered_recipe_indexes = []
    for i in range(recipes.__len__()):
        if check_fits_filter(recipes[i]):
            filtered_recipe_indexes.append(i)

class FilterConditions(Enum):
    CONTAINS_TAGS_UNION = 0
    CONTAINS_TAGS_INTERSECT = 1
    CONTAINS_KEYWORDS_UNION = 2
    CONTAINS_KEYWORDS_INTERSECT = 3
    DURATION_LESS_THAN = 4

all_tags: list[str] = ["breakfast", "lunch", "dinner"]

def load_files(path: str):
    # TODO: write file loading function
    load_recipes()
    pass

def load_recipes() -> list[Recipe]:
    # TODO: write recipe loading function
    RECIPE_PATH = "recipes.json"
    pass

def check_contains_tags(recipe: Recipe, tags: list[str], union: bool = True) -> bool:
    contains_at_least_one_tag = False
    contains_all_tags = True
    for tag in tags:
        if recipe.get_tags().__contains__(tag):
            contains_at_least_one_tag = True
        else:
            contains_all_tags = False
    return contains_all_tags or (contains_at_least_one_tag and union)

def check_contains_keywords(recipe: Recipe, keywords: list[str], union: bool = True) -> bool:
    contains_at_least_one_keyword = False
    contains_all_keywords = True
    for keyword in keywords:
        if recipe.get_keywords().__contains__(keyword):
            contains_at_least_one_keyword = True
        else:
            contains_all_keywords = False
    return contains_all_keywords or (contains_at_least_one_keyword and union)

# Check the given recipe against each active filter.
# >> Return: True if the recipe satisfies every active filter.
#            False if it does not.
def apply_selected_filters(recipe: Recipe, active_filters: dict[FilterConditions, bool],
                           tags: list[str], keywords: list[str], max_duration: int) -> bool:
    return ((active_filters.__contains__(FilterConditions.CONTAINS_TAGS_UNION)         and check_contains_tags(recipe, tags, union=True)) 
        and (active_filters.__contains__(FilterConditions.CONTAINS_TAGS_INTERSECT)     and check_contains_tags(recipe, tags, union=False))
        and (active_filters.__contains__(FilterConditions.CONTAINS_KEYWORDS_UNION)     and check_contains_keywords(recipe, keywords, union=True))
        and (active_filters.__contains__(FilterConditions.CONTAINS_KEYWORDS_INTERSECT) and check_contains_keywords(recipe, keywords, union=False))
        and (active_filters.__contains__(FilterConditions.DURATION_LESS_THAN)          and (recipe.get_prep_time <= max_duration)))

def format_time(minutes: int):
    # EXTENSION: can toggle between just minutes or hours and minutes format
    MINUTES_PER_HOUR = 60
    output = ""
    if minutes > MINUTES_PER_HOUR:
        output += f"{minutes // MINUTES_PER_HOUR} h "
    output += f"{minutes % MINUTES_PER_HOUR} m"
    return output

# Display a single recipe and all of its attributes and values.
def display_recipe(recipe: Recipe):
    print(recipe.get_name(), "|", "Preparation time:", format_time(recipe.get_prep_time()))
    print()
    print_heading("Ingredients")
    for ingredient, amount in recipe.get_ingredients().items():
        print(amount.get_amount, amount.get_unit(), ingredient)
    print()
    print_heading("Method")
    for i in range(recipe.get_steps().__len__()):
        print(f"{i + 1}: {recipe.get_steps()[i]}")
    print()
    print("Tags:", " ".join(recipe.get_tags()))

class SortingOptions(Enum):
    NAME = 0
    DURATION = 1
    # EXTENSION: LAST_OPENED = 2

# gets input until it is between the (inclusive) min and max
def input_int(prompt: str = "", min: int = None, max: int = None) -> int:
    ERROR_GENERIC =  "Invalid selection."
    ERROR_OUT_OF_RANGE = f"Please enter a whole number between {min} and {max}."
    ERROR_NOT_INTEGER = "Please ensure you enter a whole number."

    valid = False
    print(prompt)

    # Continue prompting user for input using relevant error messages until they
    # enter a valid integer within the appropriate range.
    valid = False
    while not valid:
        try:
            str_input = input()
            number = int(str_input)
            valid = ((min is None) or (min <= number)) and ((max is None) or (number <= min))
            if not valid:
                print_error(ERROR_OUT_OF_RANGE)
        except ValueError:
            # If the user entered the exit character, return the exit value so the
            # user can exit the menu.
            if str_input.upper() == EXIT_CHAR:
                return EXIT_VALUE
            # Otherwise, the user must have entered an invalid non-integer.
            print_error(ERROR_NOT_INTEGER)
        # except:
        #     print_error(ERROR_GENERIC)
    return number
     

# The view recipes menu option: select a recipe to view it
def view_recipes(recipes: list[Recipe]):
    active_filters: list[FilterConditions] = []
    active_tags = list[int] = []
    keywords: list[str] = []
    max_prep_time: int
    sort_by: SortingOptions

    # TODO: Display filtering and sorting settings
    print_heading("Sorting")
    print("Sort by", sort_by.name.lower().replace('_', ' ') + '.')
    print_heading("Filters")
    print("Search term(s):", ' '.join(keywords))
    print("Tags:", ", ".join(active_tags))
    print("Max preparation time:", max_prep_time)

    choice = input("Would you like to change these filtering and sorting settings? [Y/N]")
    if choice.upper() == "Y":
        # TODO: Allow user to edit filter options --> perhaps do this in settings
        # Display menu of each element (i.e. tag, term, etc.)
        # User can select one to edit
        FILTER_MENU = [
            "Sort by"
            "Search terms"
            "Tags"
            "Max preparation time"
        ]

        choice = display_selection_menu(FILTER_MENU)

        # They enter a menu with a table with all the possible, current, and new options.
        match choice:
            
            # For sort by, user selects from the available options.
            case 0:
                choice = display_selection_menu(sort_option.capitalize().replace('_', ' ') for sort_option in SortingOptions._member_names_)
                if choice != EXIT_VALUE:
                    sort_by = choice
            
            # For search term(s), user types in the new search term(s).
            case 1:
                user_input = input("Search: ")
                if user_input != "":
                    keywords = user_input.split(' ')
            
            # The cursor jumps from line to line.
            # - [Enter] = keep the same
            # - a = add
            # - r = remove
            # - c = clear all
            case 2:
                MAX_TAG_LENGTH = 20
                print("Command  | Function")
                print("---------|-------------------------------------------------")
                print("a        | activate current tag")
                print("d        | deactivate)")
                print("da       | deactivate all tags")
                print("1        | activate the current tag and deactivate the rest")
                print("anything | do nothing")
                print("else     |")
                print()
                print(f"{'Tag'.ljust(MAX_TAG_LENGTH)}    {'Status'.ljust(MAX_SYMBOL_LENGTH)}    Command")
                for tag in all_tags:
                    # NOTE: max char amount for tag is:
                    MAX_SYMBOL_LENGTH = "Active".__len__()
                    if active_tags.__contains__(tag):
                        status = "Active"
                    else:
                        status = ""
                    user_input = input(f"{tag.ljust(MAX_TAG_LENGTH)}    {status.ljust(MAX_SYMBOL_LENGTH)}    ")
                    match user_input:
                        case "a":
                            if status != "Active":
                                active_tags.append(tag)
                        case "d":
                            if status == "Active":
                                active_tags.remove(tag)
                        case "da":
                            active_tags.clear()
                        case "1":
                            active_tags = [tag]
            
            # For max prep time, user enters a value in minutes, or 0 to remove the constraint.
            case 3:
                if max_prep_time == 0:
                    output += "none"
                else:
                    output += format_time(max_prep_time)
                print("Current max prep time:", output)
                value = input_int(f"Enter new max prep time in minutes (or {EXIT_CHAR} to exit): ", 0)
                if value != EXIT_VALUE:
                    max_prep_time = value
                
        # TODO: remove union and intersect variations in enum and create a separate variable for it


    # Filter recipes
    check_recipe_satisfies_filters = lambda recipe: apply_selected_filters(recipe, active_filters, active_tags, keywords, max_prep_time)
    filtered_recipes = filter_recipes(recipes, check_recipe_satisfies_filters)
    
    # Display recipes (filtered)
    while recipe_to_display != -1:
        display_menu([recipes[i].get_name() for i in filtered_recipes])
        recipe_to_display = user_selects_menu_item(filtered_recipes.__len__())
        if recipe_to_display == -1:
            break
        display_recipe(recipes[filtered_recipes[recipe_to_display]])
        input("Enter any key to exit: ")

#-------------------#
# Main Code Section #
#-------------------#

# Load files
recipes: list[Recipe]
load_files(recipes)

# Main menu
class MenuOptions(Enum):
    VIEW_RECIPES = 0
    ADD_RECIPES = 1
    ADD_UNITS = 2
    VIEW_MEAL_PLANS = 3
    CREATE_MEAL_PLANS = 4
    EXIT = -1
MAIN_MENU = [
    "View recipes",
    "Add/edit recipe",
    "Add/edit units",
    "View meal plans",
    "Create/edit meal plan",
]
display_menu(MAIN_MENU)
choice = user_selects_menu_item(MAIN_MENU.__len__())
match choice:
    case MenuOptions.VIEW_RECIPES:
        view_recipes(recipes)
    # case Menu_options.ADD_RECIPES:
    #     add_recipes(recipes)
    # case Menu_options.ADD_UNITS:
    #     add_units(units)
    # case Menu_options.VIEW_MEAL_PLANS:
    #     view_meal_plans(meal_plans)
    # case Menu_options.CREATE_MEAL_PLANS:
    #     create_meal_plans(meal_plans)
    case MenuOptions.EXIT:
        print("Exiting...")
    case other:
        print(f"[{MAIN_MENU[choice]}] selected.")
