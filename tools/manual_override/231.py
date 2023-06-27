# Magnetic have 2 separate forms, red and blue/north and south
# Each form have different attack attribute
def overwrite(key, hint):
    if key == 'max_combo':
        return 0
    elif key == 'extra_dash_max_cnt':
        return 0
    elif key == 'jump_max_combo':
        return 0

def new():
    new_keys = {
        "max_combo": ["Red_Ground_D", "normal_red_n_attack0{v0}_type_count", "normal_red_n_attack0{v0}_type{v1}"],
        "max_combo": ["Blue_Ground_D", "normal_blue_s_attack0{v0}_type_count", "normal_blue_s_attack0{v0}_type{v1}"],
        "dash_red_n_attack_type_count": ["Red_Dash_D", "dash_red_n_attack_type_count", "dash_red_n_attack_type{v0}"],
        "dash_blue_s_attack_type_count": ["Blue_Dash_D", "dash_blue_s_attack_type_count", "dash_blue_s_attack_type{v0}"],
        "extra_dash_max_cnt": ["Red_Dash_Extend_D", "extra_dash_red_n_attack{v0}_type_count", "extra_dash_red_n_attack{v0}_type{v1}"],
        "extra_dash_max_cnt": ["Blue_Dash_Extend_D", "extra_dash_blue_s_attack{v0}_type_count", "extra_dash_blue_s_attack{v0}_type{v1}"],
        "extend_charge_red_n_attack_type_count": ["Red_Dash_Hold_D", "extend_charge_red_n_attack_type_count", "extend_charge_red_n_attack_type{v1}"],
        "extend_charge_blue_s_attack_type_count": ["Blue_Dash_Hold_D", "extend_charge_blue_s_attack_type_count", "extend_charge_blue_s_attack_type{v1}"],
        "jump_max_combo": ["Red_Jump_D", "jump_red_n_attack{v0}_type_count", "jump_red_n_attack{v0}_type{v1}"],
        "jump_max_combo": ["Blue_Jump_D", "jump_blue_s_attack{v0}_type_count", "jump_blue_s_attack{v0}_type{v1}"],
        "jump_charge_red_n_attack_type_count": ["Red_Jump_Hold_D", "jump_charge_red_n_attack_type_count", "jump_charge_red_n_attack_type{v1}"],
        "jump_charge_red_n_land_type_count": ["Red_Landing_Jump_Hold_D", "jump_charge_red_n_land_type_count", "jump_charge_red_n_land_type{v1}"],
        "jump_charge_blue_s_attack_type_count": ["Blue_Jump_Hold_D", "jump_charge_blue_s_attack_type_count", "jump_charge_blue_s_attack_type{v1}"],
        "jump_charge_blue_s_land_type_count": ["Blue_Landing_Jump_Hold_D", "jump_charge_blue_s_land_type_count", "jump_charge_blue_s_land_type{v1}"]
    }
    return new_keys