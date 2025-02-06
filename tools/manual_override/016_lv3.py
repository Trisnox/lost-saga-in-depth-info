# Charge D Combo have different name
def overwrite(key, hint):
    if key == "charge_combo_max_cnt":
        hint[1] = "charge_combo_attack0{v0}_type_count"
        hint[2] = "charge_combo_attack0{v0}_type{v1}"
        return key, hint

# !!!
# data is incomplete, you need to supply extend combo as well