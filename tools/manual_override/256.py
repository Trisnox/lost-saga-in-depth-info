# Priest have 2 different charged D state, minimum and maximum
def overwrite(key, hint):
    if key == 'max_charge_attack':
        return 0

def new():
    new_keys = {
        "charge_attack_type_count": ["Charged_D_Min", "charge_attack_type_count", "charge_attack_type{v1}"],
        "max_charge_attack_type_count": ["Charged_D_Max", "max_charge_attack_type_count", "max_charge_attack_type{v1}"]
    }
    return new_keys