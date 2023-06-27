# Mistyped attribute
def overwrite(key, hint):
    if key == 'extend_attack_cnt':
        hint[1] = "extend_attack{v0}_type_count"
        hint[2] = "extend_attack{v0}_type{v1}"
        return key, hint