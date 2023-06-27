# Maximum combo is mismatched
def overwrite(key, hint):
    if key == 'charge_combo_max_cnt':
        return 2
    elif key == 'extend_attack_cnt':
        return 0

# Have special charged
def new():
    key = "charge_special_combo_max_cnt"
    hint = ["Charged_Special_D", "charge_special_combo_attack{v0}_type_count", "charge_special_combo_attack{v0}_type{v1}"]
    return key, hint