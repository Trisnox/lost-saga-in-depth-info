# Mistyped attribute name
def overwrite(key, hint):
    if key == 'jump_attack_type_count':
        hint += [['50704']]
        return key, hint