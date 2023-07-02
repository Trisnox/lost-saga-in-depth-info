# For evolution heroes, use  `000_lv?.py`, where ? is the evolution level
# There is no 'ultimate' keyword, please use number instead
#
# The function name must be `overwrite` for overwriting variables
# You will be given key and hint variables
#   - key: str. The key indicator, please refer to the config scraper key dictionary
#   - hint: list. A list that contains the input hint, type count, and the attack.
#
# You can also return an int, this is used if the maximum combo a mercenary using is incorrect
# You don't need to return int if you return key, the script will assume if it was incorrect combo or incorrect key/hint
# It is also possible to return option + hint, just simply `return x, hint`
def overwrite(key, hint):
    # This means that the maximum combo of key `extra_dash_max_cnt` (Dash D) should be 2, but written as 3 on file
    if key == 'extra_dash_max_cnt':
        return 2
    # This means that the variable is using incorrect value. This is usually valid because the file provide the files
    # v0 is for the attack number, v1 is for the type count, it's kinda hard to explain in text.
    # I'm afraid you have to figure it out yourself
    elif key == 'extend_attack_cnt':
        key = "charge_combo_max_cnt"
        hint[1] = "charge_combo_attack{v0}_type_count"
        hint[2] = "charge_combo_attack{v0}_type{v1}"
        return key, hint

# This is used if the mercenary missing an attack attribute, this is likely because it contain neither data of the keys dictionary. Rarely used.
def new():
    # Kinda self explanatory, you need to provide the missing data
    key = "???"
    hint = ["???_D", "???{v0}", "???{v0}???{v1}"]
    # You need to return key and hint like so
    return key, hint

# This is used if you want to use pre-defined attack attribute
# Only used for Kaito and R-Robin because their attack attribute mismatched, and had to be defined manually
def new():
    key = "???"
    # The amount of pre-defined attributes has to match with maximum combo, and if the attribute is already correct, just supply None
    hint = ["Pre_defined_D", "???{v0}", "???{v0}???{v1}", [None, '000000']]
    return key, int

# Or if you want to add multiple keys
def new():
    keys = {
        "key1": ["???_D", "???{v0}", "???{v0}???{v1}"],
        "key2": ["???_D", "???{v0}", "???{v0}???{v1}"]
    }
    return keys