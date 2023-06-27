# Mistyped attribute
def overwrite(key, hint):
    if key == 'extra_dash_max_cnt':
        hint[1] = 'extra_dash_attack_type_count'
        hint[2] = 'extra_dash_attack_type{v1}'
        return key, hint
    elif key == 'jump_max_combo':
        hint[1] = 'jump_attack_type_count'
        hint[2] = 'jump_attack_type{v1}'
        return key, hint