# Charge D Hold have different name
def overwrite(key, hint):
    if key == "extend_attack_cnt":
        hint[1] = "attack_land_attack_type_count"
        hint[2] = "attack_land_attack_type{v1}"
        return key, hint