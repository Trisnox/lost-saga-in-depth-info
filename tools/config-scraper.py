import argparse
import importlib
import io
import json
import os
import re
import traceback
import sys
from ext.modified_parser import ModConfigParser
from configparser import NoOptionError, DuplicateSectionError, MissingSectionHeaderError
"""
basic_information = [
		'id',
		# 'icon', #it will use mercenary ID as the icon later on
		'name', # all alternative name including in-file name will be included
		'rarity', # 2 = premium, 3 = rare, 4 = unique, 6 = idol... idfk what is 5???
		'basic_attack_length', # self explanatory, the data is provided
		'dash_attack_replacement', # if dash type is EXTEND_ASSAULT_DASH, then yes
        'highest_damage', # highest damage in single attack
		'max_jump', # self explanatory, the data is provided
        '360_defend', # self explanatory, the data is provided
		'can_deflect', # it is named 'cancel', some deflect may doesn't have counter
		'can_counter', # some are named 'cancel' and the rest are 'counter', refer to the deflect info
		'have_down_hit', # self explanatory
		'have_gauge',
		'unique_property'
        ]

        attack_information = [
            'damage',
            'defense_break', # if defense_break_type is 1, then yes
            'down_hit', # if enable_down_attack = 1, it can hit downed enemy
            'juggle', # if blow power is > 1.0, then it will juggle the enemy, 0.5 doesn't seem do though. RE: if it's 1, then it's conditional, means it either push them or juggle them, above that will make them float slightly higher, else doesn't
            # 'piercing', # if char_piercing = 0, it means it can only hit single target re: seems only available for dummy character
            # 'target_debuff', # not yet
            'push_power',
            'frozen_break',
            'air_push_power',
            'downed_push_power',
            'defense_push_power',
            'ball_push',
            'gangxi_push'
        ]

# dev note: let's try check for dash_attack_type_count instead of analyzing every dash to check wherever it can sprint or not
indicators = [
        "max_combo", # Normal #normal_attack0{0}_type1
        "dash_type", # Dash #dash_attack_type1 #attack_type1 for assault
        "dash_attack_type_count", # ~D1 #dash_attack_type{0}
        "extra_dash_max_cnt", # ~D2 #extra_dash_attack{0}_type_count #extra_dash_attack{0}_type{1}
        # "extra_dash_attack1_type_count", # ~D2 #extra_dash_attack{0}_type1 actually recursive
        "extend_dash_max_cnt", # alt D~ #extend_dash_attack{0}_type_count #extend_dash_attack{0}_type{1}
        "max_jump_cnt", # Jump #jump_type for some
        "jump_max_combo", # Jump +D #jump_attack{0}_type_count #jump_attack{0}_type{1}
        "extend_jump_max_cnt", # Jump D~ #extend_jump_attack{0}_type_count #extend_jump_attack{0}_type{1}
        "enable_jump_dash", # # Jump >> #dash_jump_attack_type_count #dash_jump_attack_type{1}
        "dash_action_attack_type_count", # >> for those dash are replaced
        "dash_jump_attack_add_attack_cnt", # >>+D #dash_jump_attack_add_attack{0}_type_count #dash_jump_attack_add_attack{0}_type{1}
        "defense_weak_attack_push", # Deflect
        "enable_counter_attack", # Counter #counter_attack_type_count #counter_attack_type{1}
        "enable_defence_counter_attack", # can deflect and counter, dayum #defence_counter_attack_type_count #defence_counter_attack_type{1}
        "charge_time", # Charge #extend_attack_cnt #extend_attack0{0}_type_count #extend_attack0{0}_type{1}
        "extra_gauge_enable", # Gauge
        "max_gauge", # Gauge...
        "max_bullet" # Bullet
    ]
"""

class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class Mercenary_Config_Parser():
    def __init__(self, **kwargs):
        """
        kwargs:
            - method: Generation method for mercenaries. 1. Mercenaries per individual table. 2. Mercenaries for all table
            - text: text_?.txt, where ? is the language, can be found inside xml/text_?.txt
            - override: the folder location that contains python script that override/add new methods
            - images: Images folder containing mercenaries illustration and mini icon. The file name is the same as you would download them directly from the lostsaga.com site. It should be located at static/img
        """
        self.folder_location = kwargs.get('mercenary_folder', None)

        # I'm telling you, I tried really hard just to try get my tables working without separating them
        # Basically, I could access it by just mercenaries.keys().map(key), but I figured it's too hard
        # that I spend 3 hours, and still no result. So I figured, "hey, just separate it, I mean, the total mercenary size is only about 1mb though"
        self.method = kwargs.get('method', 1)

        self.mercenary_code = None
        self.mercenary_config = ModConfigParser(allow_no_value=True)
        self.mercenary_keys = None
        self.attack_config = ModConfigParser(allow_no_value=True)
        self.buff_config = ModConfigParser(allow_no_value=True)

        self.max_combo = None
        self.max_jump = '1'
        self.mercenary_name = ''
        self.mercenary_file_comment_name = ''
        self.highest_damage = None
        self.can_sprint = '✗'
        self.can_deflect = '✗'
        self.can_counter = '✗'
        self.gauge_bullet = '✗'
        self.unique_property = []
        self.down_hits = []

        self.valid_mercenaries = []
        self.heroes_name = None
        self.previous = None

        # I'm telling you, the files are literally messy, it uses up to 3 different encoding system!
        # For some reason, it took up to 4 encoders to work around with confiparser
        # It also has strange error that I can't be bothered with
        self.encoder = None

        # text_-.txt, where - is the language
        self.client_text = kwargs.get('text', None)

        # I've planned to place it on the same folder as the script, but that is not possible
        # because I choose to place the manual override at the wiki repository for ease of use in case people want to commit pull requests
        # so yeah, that means you have to download both the wiki and the tool if you ever want to request pull
        self.override_folder = kwargs.get('override', None)
        self.override_all = None
        self.new_all = None

        # Unfortunately, the json override only apply to the basic general information
        # This is because you can pretty much override the attack attributes using the script
        self.json_override = False

        # Folder containing the images. The image link for jsx will always be from './src/images'... unless you want to modify it
        self.images = kwargs.get('images', None)

        if self.override_folder:
            sys.path.append(self.override_folder)
            override_all_file = self.override_folder + '\\' + 'all' + '.py'
            if os.path.isfile(override_all_file):
                try:
                    modules = importlib.import_module(os.path.basename(override_all_file))
                    try:
                        self.override_all = getattr(modules, 'overwrite')
                    except AttributeError:
                        pass
                    try:
                        self.new_all = getattr(modules, 'new')
                    except AttributeError:
                        pass
                except ModuleNotFoundError:
                    pass
        
        if self.images:
            valid_images = {}
            for x, y, z in os.walk(self.images):
                _, constant, remaining = x.partition("static\\img")
                image_location = "@site/" + constant.replace('\\', '/') + remaining.replace('\\', '/')
                for a in z:
                    valid_images[a] = image_location + '/' + a

            if valid_images:
                self.images = valid_images

        self.any_regex = r"(;-*\/*\s)(.*)"
        self.charge_attack_regex = r"(;-*\s)(Charge)"
        self.weapon_regex = r";-*\/*\sWeapon"
        self.comment_mercenary_regex = r";-*\/*\s\d*\.?(.*)\.?"

        is_invalid = False
        # I don't know if this is a bad practice because I'm not a programmer, but it does its job well
        # Anyways, I have 3 methods to retrieve names
        # Method 1: retrieve name from literal translation file, which is xml/text_id.txt
        # beyond 218 is quite challenging because:
        # - Some heroes only mention their translated name on single line only, eg: Paparazzi
        # - Some heroes have name mention on their gear, but not everyone have it, eg: tyr
        #   > While theorically it's possible to retrieve it from other gear, I'm afraid that is not possible because
        #   > not all heroes have their gear on the same folder, which requires extra work to check which file does the gear belong to
        # - Some heroes doesn't mention any translated name: eg Tae Eul Jin, it is named as "Taoist" on file
        #
        # In that case, I have 2 fallback method
        # Fallback method 1: check from training text. This one mentions their literal English name, eg: Yukime became Ice God
        # Fallback method 2: read from item.ini sub_type value. This one is the worst because it takes their literal in-file name, and have no space
        if self.client_text:
            invalid_mercenaries = []
            with open(self.client_text, 'r', encoding='ansi') as f:
                self.client_text = f.readlines()
                names = [_ for _ in self.client_text if '|INI_sp2_setitem_info::set_item' in _]
                self.heroes_name = {}
                for x in names:
                    res_num = re.findall(r'.*item(\d*)_1', x)[0]
                    res_name = re.findall(r'.*\|(.*)\|', x)[0]
                    if not res_name.startswith('Hero '):
                        self.heroes_name[res_num] = res_name
                    else:
                        invalid_mercenaries = [_ for _ in invalid_mercenaries + [res_num]]
                        is_invalid = True

        if is_invalid:
            practice_names = self.iter_practice(invalid_mercenaries)
            self.heroes_name.update(practice_names)

    
    def iter_practice(self, invalid_mercenaries):
        def one_line_find(pattern, text):
            res = re.findall(pattern, text)
            if res:
                return res[0]
            else:
                return None

        mercenaries = {}
        practice_names = [_ for _ in self.client_text if re.search(rf"\|INI_sp2_practice_help::Set\d*\_1\|(.*)-", _)]
        for x in practice_names:
            for y in invalid_mercenaries:
                if not f'|INI_sp2_practice_help::Set{y}' in x:
                    continue
                name = one_line_find(rf"\|INI_sp2_practice_help::Set{y}\_1\|(.*)-", x)
                if name:
                    mercenaries[y] = name

        # yet_invalid_mercenaries = [_ for _ in invalid_mercenaries if not _ in mercenaries.keys()]
        return mercenaries

    def is_mercenary(self, code):
        for _, _, x in os.walk(self.folder_location + '\\' + code):
            if f'{code}_item.ini' in x:
                return True
            else:
                return False
    
    # we should reformat the ini file first, this is because of mutiple reason
    # 1 : dupe options
    #       This is because the mercenary weapon attribute may contain the same option that is somewhat the game handles it separately
    #       this is proven because each attribute have comments on top of it.
    # 2 : comments
    #       In contradictory on the first point, some useful information are actually on the comment
    #       like the mercenary in-file name, the attribute name, hints, etc.
    #       This makes it easier to make table with.

    # RE: fuck that shit, I had more errors that what's it worth
    # def reformat_mercenary(self, mercenary: str):
    #     def convert(mercenary):
    #         l = []
    #         for x in mercenary:
    #             y = re.sub(self.mercenary_regex, '', x)
    #             y = re.sub(self.weapon_regex, '', y)
    #             y = re.sub(self.any_regex, '', y)
    #             y = re.sub(self.charge_attack_regex, r'[\2d attack]', y)
    #             l.append(y)
    #         return l

    #     with open(mercenary, 'r') as f:
    #         mercenary = f.readlines()

    #     raw_mercenary = convert(mercenary)
    #     buffer = io.StringIO(''.join(raw_mercenary))
    #     self.mercenary_config.read_file(buffer)

    #     # I'm aware that this will remove the gears data, that doesn't matter because gears script might differ from mercenary
    #     filtered_item = []
    #     for x in self.mercenary_config.sections():
    #         if x.lower() == 'armor':
    #             break
    #         filtered_item.append(x)
    #     self.mercenary_keys = filtered_item
    #     return
    
    
    def reformat_attack(self, mercenary: str):
        def reformat():
            with open(mercenary, 'r+', encoding=self.encoder) as f:
                lines = f.readlines()

            seen = set()
            result = []
            for x in lines:
                if x not in seen or not x.startswith('['):
                    seen.add(x)
                    result = [_ for _ in result + [x]]
                else:
                    if not x == result[-1]:
                        result.remove(x)

            buffer = io.StringIO(''.join(result))
            self.attack_config.read_file(buffer)
            return
        
        try:
            self.attack_config.read(mercenary)
            self.encoder = None
        except UnicodeDecodeError:
            try:
                try:
                    self.encoder = 'utf-8'
                    self.attack_config.read_file(open(mercenary, 'r', encoding='utf-8'))
                except MissingSectionHeaderError:
                    self.encoder = 'utf-8-sig'
                    self.attack_config.read_file(open(mercenary, 'r', encoding='utf-8-sig'))
                except UnicodeDecodeError:
                    self.encoder = 'euc-kr'
                    self.attack_config.read_file(open(mercenary, 'r', encoding='euc-kr'))
                except DuplicateSectionError:
                    reformat()
            except UnicodeDecodeError:
                self.encoder = 'ansi'
                self.attack_config.read_file(open(mercenary, 'r', encoding='ansi'))
            except DuplicateSectionError:
                reformat()
        except DuplicateSectionError:
            reformat()
        return

    def attack_data(self):                    
        def process_attribute_attack(hint: list, attack_number = 0):
            pre_defined = False
            if len(hint) > 3:
                attribute_id = hint[3][attack_number-1]
                if attribute_id:
                    pre_defined = True
                    self.previous = attribute_id

            if not pre_defined:
                try:
                    attribute_id = self.mercenary_config.get('item1', hint[2])
                    self.previous = attribute_id
                except NoOptionError as e:
                    # "could've sworn it counts more than 1, but how could it be possible?"
                    # For mercenaries attack that uses the same attribute as before
                    attribute_id = self.previous
                    
            if attribute_id:
                attribute = dict(self.attack_config.items('attribute'+attribute_id))
            else:
                return
            
            if self.encoder == 'euc-kr' and isinstance(attribute['type'], list):
                new_attribute = {}
                for x, y in attribute.items():
                    new_attribute[x] = y[0]
                attribute = new_attribute
            damage = attribute.get('damage_rate', '0.0').replace('f', '')

            if not self.highest_damage or '' in self.highest_damage:
                self.highest_damage = [hint[0] + str(attack_number), float(damage)]
            elif self.highest_damage[1] == float(damage):
                self.highest_damage += [hint[0] + str(attack_number), float(damage)]
            elif self.highest_damage[1] < float(damage):
                self.highest_damage = [hint[0] + str(attack_number), float(damage)]

            if attribute.get('defense_break_type', '0') == '1':
                defense_break = '✓'
            else:
                defense_break = '✗'

            if attribute.get('enable_down_attack', '0') == '1':
                down_hit = '✓'
                atk = f'{hint[0]}{attack_number}'
                if not atk in self.down_hits:
                    self.down_hits.append(atk)
            else:
                down_hit = '✗'

            blow_power = float(attribute.get('blow_power', '0').replace('f', ''))
            if blow_power > 1.5:
                juggle = '✓✓, ' + str(blow_power)
            elif blow_power >= 1.0:
                juggle = '✓, ' + str(blow_power)
            else:
                juggle = '✗, ' + str(blow_power)
            
            air_blow_power = float(attribute.get('air_blow_power', '0').replace('f', ''))
            if air_blow_power > 1.5:
                air_juggle = '✓✓, ' + str(air_blow_power)
            elif air_blow_power >= 1.0:
                air_juggle = '✓, ' + str(air_blow_power)
            else:
                air_juggle = '✗, ' + str(air_blow_power)

            push_power = attribute.get('push_power', '0.0').replace('f', '')

            frozen_break = attribute.get('frozen_break', '✗').replace('1', '✓')
            data = {
                'damage': damage,
                'defense_break': defense_break,
                'juggle': juggle,
                'air_juggle': air_juggle,
                'down_hit': down_hit,
                'push_power': push_power,
                'frozen_break': frozen_break
            }
            return data
            
        def process_attack(key, hint, modify_func = None):
            inputs = []
            recursive_inputs = []
            option = False
            is_recursive = False
            skip = False
            already_set = False
            is_int = False

            # Positive lookahead, appearantly some data are inconsistent
            if key == 'extend_dash_max_cnt':
                try:
                    # Does this mercenary missing a number on their value?
                    self.mercenary_config.get('item1', "extend_dash_attack1_type1")
                except NoOptionError:
                    try:
                        # Which value is incorrect? Is this a harmless dash or mistyped value?
                        self.mercenary_config.get('item1', "extend_dash_attack_type1")
                        hint[1] = "extend_dash_attack_type_count"
                        hint[2] = "extend_dash_attack_type{v1}"
                    except NoOptionError:
                        # ok, it's a harmless dash, we'll just skip the first value as they might have attack attribute on their dash
                        skip = True
            # I'm sensing a pattern here, I'll just make one time solution instead of manual override
            elif key == 'extend_attack_cnt':
                try:
                    # Is this mistyped or doesn't exist?
                    self.mercenary_config.get('item1', 'extend_attack01_type_count')
                except NoOptionError:
                    try:
                        # ok, maybe it was mistyped
                        self.mercenary_config.get('item1', 'extend_attack1_type_count')
                        hint[1] = "extend_attack{v0}_type_count"
                        hint[2] = "extend_attack{v0}_type{v1}"
                    except NoOptionError:
                        try:
                            # mistyped no.2
                            self.mercenary_config.get('item1', 'extend_attack_type_count')
                            hint[1] = "extend_attack_type_count"
                            hint[2] = "extend_attack_type{v1}"
                        except NoOptionError:
                            # the attribute exist yet the attack does not
                            option = 0
                            already_set = True
            elif key == "enable_counter_attack":
                try:
                    option = int(self.mercenary_config.get('item1', "counter_combo_cnt"))
                    hint[1] = "counter_combo_attack{v0}_type_count"
                    hint[2] = "counter_combo_attack{v0}_type{v1}"
                    already_set = True
                except NoOptionError:
                    pass
            
            if self.override_all:
                res = self.override_all(key, hint)
                if res is not None:
                    if isinstance(res, int):
                        option = res
                        already_set = True
                    elif isinstance(res, tuple | list):
                        if isinstance(res[0], int):
                            option = res[0]
                            hint = res[1]
                    else:
                        key, hint = res

            if modify_func:
                res = modify_func(key, hint)
                if res is not None:
                    if isinstance(res, int):
                        option = res
                        already_set = True
                    elif isinstance(res, tuple | list):
                        if isinstance(res[0], int):
                            option = res[0]
                            hint = res[1]
                            already_set = True
                    else:
                        key, hint = res

            if isinstance(hint[1], int) and not already_set:
                check = int(self.mercenary_config.get('item1', key))
                if check != 0:
                    option = hint[1]
                    is_int = True
                    already_set = True
                else:
                    option = 0
                    is_int = True
                    already_set = True

            if not option and not already_set:
                option = int(self.mercenary_config.get('item1', key))

            if option == 0:
                if not self.highest_damage:
                    self.highest_damage = ['', '']
                return
            
            if key == 'max_combo':
                self.max_combo = option
            elif key == 'dash_attack_type_count':
                if int(option) >= 1:
                    self.can_sprint = '✓'
            elif key == 'enable_defence_counter_attack':
                self.can_deflect = '✓'
                self.can_counter = '✓'
            elif key == 'enable_counter_attack':
                self.can_counter = '✓'

            for x in range(option):
                if skip:
                    skip = False
                    continue
                x += 1
                if not isinstance(hint[1], int):
                    recursive_option = int(self.mercenary_config.get('item1', hint[1].format_map(SafeDict(v0=x))))
                    if not recursive_option == 1:
                        is_recursive = True
                elif not already_set or any(keyword == key for keyword in ("dash_action_attack_type_count", "dash_attack_type_count", "dash_charging_attack_type_count", "jump_attack_type_count", "dash_jump_attack_type_count", "jump_charge_attack_type_count", "jump_charge_land_type_count")):
                    recursive_option = int(self.mercenary_config.get('item1', key))
                    if not recursive_option == 1:
                        is_recursive = True

                if is_recursive:
                    for y in range(recursive_option):
                        y += 1
                        if is_int:
                            formatted_hint = [*hint]
                            formatted_hint[2] = hint[2].format_map(SafeDict(v0=x, v1=y))
                        else:
                            formatted_hint = [*hint]
                            formatted_hint[1] = hint[1].format_map(SafeDict(v0=x))
                            formatted_hint[2] = hint[2].format_map(SafeDict(v0=x, v1=y))
                        attribute_dict = process_attribute_attack(formatted_hint, x)
                        if not attribute_dict:
                            return
                        data = f"""
                "{y}": {{
                    "Damage": "{attribute_dict['damage']}",
                    "Defense Break": "{attribute_dict['defense_break']}",
                    "Juggle": "{attribute_dict['juggle']}",
                    "Air Juggle": "{attribute_dict['air_juggle']}",
                    "Down Hit": "{attribute_dict['down_hit']}",
                    "Push Power": "{attribute_dict['push_power']}",
                    "Frozen Break": "{attribute_dict['frozen_break']}",
                }},"""
                        recursive_inputs = [_ for _ in recursive_inputs + [data]]
                    combined = '\n'.join(recursive_inputs)
                    if not combined:
                        recursive_inputs = []
                        is_recursive = False
                        return
                    data = f"""
            {hint[0]}{x}: {{
                {combined}
            }},"""
                    inputs = [_ for _ in inputs + [data]]
                    recursive_inputs = []
                    is_recursive = False
                else:
                    if is_int:
                        formatted_hint = [*hint]
                        formatted_hint[2] = hint[2].format_map(SafeDict(v0=x, v1=1))
                    else:
                        formatted_hint = [*hint]
                        formatted_hint[1] = hint[1].format_map(SafeDict(v0=x))
                        formatted_hint[2] = hint[2].format_map(SafeDict(v0=x, v1=1))

                    attribute_dict = process_attribute_attack(formatted_hint, x)
                    if not attribute_dict:
                            return
                    data = f"""
    {hint[0]}{x}: {{
        "Damage": "{attribute_dict['damage']}",
        "Defense Break": "{attribute_dict['defense_break']}",
        "Juggle": "{attribute_dict['juggle']}",
        "Air Juggle": "{attribute_dict['air_juggle']}",
        "Down Hit": "{attribute_dict['down_hit']}",
        "Push Power": "{attribute_dict['push_power']}",
        "Frozen Break": "{attribute_dict['frozen_break']}",
        }},"""
                    inputs = [_ for _ in inputs + [data]]
            return inputs[::-1]

        # The 'type' is just tells you how many attack it caused from that single button press
        # Alt keyword: multi-hit from single attack, eg: Jinrah semi d-hold, Nang in D3
        key = {
            "max_combo": ["Ground_D", "normal_attack0{v0}_type_count", "normal_attack0{v0}_type{v1}"],
            "dash_action_attack_type_count": ['Dash_Replace', 1, "dash_action_attack_type{v1}"],
            "dash_attack_type_count": ["Dash_D", 1, "dash_attack_type{v1}"],
            "extra_dash_max_cnt": ["Dash_Extend_D", "extra_dash_attack{v0}_type_count", "extra_dash_attack{v0}_type{v1}"],
            "extend_dash_max_cnt": ["Dash_Hold_D", "extend_dash_attack{v0}_type_count", "extend_dash_attack{v0}_type{v1}"],
            # "enable_extra_dash_attack": ["Dash_Hold_D", "dash_charging_attack_type_count", "dash_charging_attack_type{v1}"], #
            "dash_charging_attack_type_count": ["Dash_Hold_D", 1, "dash_charging_attack_type{v1}"],
            "jump_max_combo": ["Jump_D", "jump_attack{v0}_type_count", "jump_attack{v0}_type{v1}"],
            "jump_attack_type_count": ["Jump_D", 1, "jump_attack_type{v1}"],
            "extend_jump_max_cnt": ["Jump_Hold_D", "extend_jump_attack{v0}_type_count", "extend_jump_attack{v0}_type{v1}"],
            #dash_jump_attack_type_count #dash_jump_attack_type{v1}
            # "enable_jump_dash": ["Jump_Dash_Extend_D", "dash_jump_attack_type_count", "dash_jump_attack_type{v1}"],
            "dash_jump_attack_type_count": ["Jump_Dash_Extend_D", 1, "dash_jump_attack_type{v1}"],
            "dash_jump_attack_add_attack_cnt": ["Jump_Dash_D", "dash_jump_attack_add_attack{v0}_type_count", "dash_jump_attack_add_attack{v0}_type{v1}"],
            "jump_charge_attack_type_count": ["Jump_Hold_D", 1, "jump_charge_attack_type{v1}"],
            "jump_charge_land_type_count": ["Landing_Jump_Hold_D", 1, "jump_charge_land_type{v1}"],
            "enable_counter_attack": ["Counter_D", "counter_attack_type_count", "counter_attack_type{v1}"],
            # "counter_attack_type_count": ["Counter_D", 1, "counter_attack_type{v1}"],
            "counter_combo_cnt": ["Counter_D", "counter_combo_attack{v0}_type_count", "counter_combo_attack{v0}_type{v1}"],
            "enable_defence_counter_attack": ["Counter_D", "defence_counter_attack_type_count", "defence_counter_attack_type{v1}"],
            "extend_attack_cnt": ["Charged_D", "extend_attack0{v0}_type_count", "extend_attack0{v0}_type{v1}"],
            "charge_combo_max_cnt": ["Charged_D", "charge_combo_attack{v0}_type_count", "charge_combo_attack{v0}_type{v1}"],
            "max_charge_attack": ["Charged_D", "charge_attack0{v0}_type_count", "charge_attack0{v0}_type{v1}"]

        }
        # separating this because some options are required to be looped, some are only for checks
        key_check = {
            "max_jump_cnt": "Jump",
            # "enable_jump_dash":  "Jump",
            "defense_weak_attack_push": "Deflect",
            "charge_time": "Charged",
            "extra_gauge_enable": "Gauge",
            "max_gauge":  "Gauge",
            "max_bullet": "Bullet",
            "jump_defense_push_rate": "Air Block"
        }

        override_method = None
        new_method = None

        override_file = self.override_folder + '\\' + self.mercenary_code

        if os.path.isfile(override_file + '.py'):
            try:
                modules = importlib.import_module(os.path.basename(override_file))
                try:
                    override_method = getattr(modules, 'overwrite')
                except AttributeError:
                    pass
                try:
                    new_method = getattr(modules, 'new')
                except AttributeError:
                    pass
            except ModuleNotFoundError:
                pass
        
        if os.path.isfile(override_file + '.json'):
            with open(override_file + '.json', 'r') as f:
                self.json_override = json.load(f)

        datas = []
        
        # Not recommended, but I implemented it anyway
        # Since you can also use manual override, I think you should have no probelm with this one
        if self.new_all:
            all_new_keys = self.new_all()
            try:
                if isinstance(all_new_keys, tuple | list):
                    data = process_attack(*all_new_keys)
                    self.previous = None
                    if data:
                        datas = [_ for _ in datas + [data]]
                elif isinstance(all_new_keys, dict):
                    for x, y in all_new_keys.items():
                        data = process_attack(x, y, override_method)
                        self.previous = None
                        if data:
                            datas = [_ for _ in datas + [data]]
            except NoOptionError as e:
                traceback.print_exc()

        # Since you're responsible with whatever you're doing,
        # I'm going to assume that the key exist
        if new_method:
            new_keys = new_method()
            if isinstance(new_keys, tuple | list):
                data = process_attack(*new_keys)
                self.previous = None
                if data:
                    datas = [_ for _ in datas + [data]]
            elif isinstance(new_keys, dict):
                for x, y in new_keys.items():
                    data = process_attack(x, y)
                    self.previous = None
                    if data:
                        datas = [_ for _ in datas + [data]]

        for x, y in key.items():
            try:
                self.mercenary_config.get('item1', x)
            except NoOptionError as e:
                continue
            data = process_attack(x, y, override_method)
            self.previous = None
            if data:
                datas = [_ for _ in datas + [data]]

        for x, y in key_check.items():
            try:
                self.gauge_bullet = '✗'
                value = self.mercenary_config.get('item1', x)
                if y == 'Jump':
                    self.max_jump = value
                elif x == 'enable_jump_dash':
                    pass
                elif y == 'Deflect':
                    self.can_deflect = '✓'
                elif y == 'Gauge':
                    self.gauge_bullet = 'Gauge'
                elif y == 'Bullet':
                    self.gauge_bullet = 'Bullet'
                elif y == 'Air Block':
                    self.unique_property.append('Can guard mid-air')
            except NoOptionError:
                continue
        return datas[::-1]
                

    # def attack_convert(self):
    #     pass

    def buff_convert(self):
        pass

    def get_down_hit_inputs(self):
        pass

    def table_convert(self, inputs):
        rarity = int(dict(self.mercenary_config.items('item1')).get('grade_type', 1))
        rarity_table = {
            0: 'Undefined',
            1: 'Normal',
            2: 'Premium',
            3: 'Rare',
            4: 'Unique',
            5: 'Unknown',
            6: 'Idol'
        }
        try:
            if self.mercenary_config.get('item1', 'defense_backside') == '1':
                defend_360 = '✓'
            else:
                defend_360 = '✗'
        except NoOptionError:
            defend_360 = '✗'

        # NO! Do not do this here, instead do this on attack, for efficiency. Just set them to 'x' or None so you don't have to redefine it
        # If the variable do not get iterated on attack loop, then it should be defined here instead
        # try:
        #     can_sprint = int(self.mercenary_config.get('item1', 'dash_attack_type_count'))
        #     if can_sprint >= 1:
        #         can_sprint = '✓'
        #     else:
        #         can_sprint = '✗'
        # except NoOptionError:
        #     can_sprint = '✗'

        with open(self.folder_location + '\\' + self.mercenary_code + '\\' + self.mercenary_code + '_item.ini', 'r') as f:
            self.mercenary_file_comment_name = re.findall(self.comment_mercenary_regex, f.read())
            if self.mercenary_file_comment_name:
                self.mercenary_file_comment_name = self.mercenary_file_comment_name[0]

        if self.heroes_name:
            self.mercenary_name = self.heroes_name.get(self.mercenary_code.lstrip('0'), None)
        
        if not self.mercenary_name:
            self.mercenary_name = self.mercenary_config.get('item1', 'sub_type').capitalize().replace('_item', '')

        self.mercenary_name = self.mercenary_name.strip()

        if self.down_hits:
            down_inputs = ', '.join(self.down_hits).replace('_', ' ')
        else:
            down_inputs = '✗'

        self.valid_mercenaries.append(self.mercenary_code)

        def recursive_reversed(items):
            if isinstance(items, list):
                return [recursive_reversed(item) for item in reversed(items)]
            return items

        inputs = '\n'.join(_ for __ in recursive_reversed(inputs) for _ in __)
        if len(self.highest_damage) > 2:
            paired = []
            self.highest_damage = self.highest_damage[::-1]
            for x in range(0, len(self.highest_damage), 2):
                if x + 1 == len(self.highest_damage):
                    paired.append(', '.join(str(_) for _ in self.highest_damage[x:]))
                else:
                    paired.append(', '.join(str(_) for _ in self.highest_damage[x:x + 2]))
            dmg = ' | '.join(paired[::-1]).replace('_', ' ')
        else:
            dmg = f'{self.highest_damage[1]}, {self.highest_damage[0]}'

        icons = '""'
        if self.images.get(f'thum_char_{self.mercenary_code}_n.jpg', None):
            image = self.images[f'thum_char_{self.mercenary_code}_n.jpg']
            icons = f'"{image}"'

        if self.images.get(f'thum_char_{self.mercenary_code}_o.jpg', None):
            image = self.images[f'thum_char_{self.mercenary_code}_o.jpg']
            if not icons == '""':
                icons = f'[{icons}, "{image}"]'
            else:
                icons = f'"{image}"'

        if self.method == 1:
    # Icon: {icons},
            data = f"""
export const mercenary_{self.mercenary_code} = [{{
    ID: "{self.mercenary_code}",
    Name: "{self.mercenary_name}",
    Rarity: "{rarity_table[rarity]}",
    Sprint: "{self.can_sprint}",
    Jump: "{self.max_jump}",
    Attack_Length: "{self.max_combo}",
    Highest_Damage: "{dmg}",
    "360_Block": "{defend_360}",
    Deflect: "{self.can_deflect}",
    Counter: "{self.can_counter}",
    Down_Hit: "{down_inputs}",
    Special: "Not yet added",
    Unique_Property: "{', '.join(self.unique_property)}",
    Dump: {{
        file_comment_name: "{self.mercenary_file_comment_name}",
    }},
}}];
export const mercenary_{self.mercenary_code}_attacks = [{{
        {inputs}
}}];"""
        else:
        # Icon: {icons},
            data = f"""
    {{
        ID: "{self.mercenary_code}",
        Name: "{self.mercenary_name}",
        Rarity: "{rarity_table[rarity]}",
        Sprint: "{self.can_sprint}",
        Jump: "{self.max_jump}",
        Attack_Length: "{self.max_combo}",
        Highest_Damage: "{dmg}",
        "360_Block": "{defend_360}",
        Deflect: "{self.can_deflect}",
        Counter: "{self.can_counter}",
        Down_Hit: "{down_inputs}",
        Special: "Not yet added",
        Unique_Property: "{', '.join(self.unique_property)}",
        Dump: {{
            File_Comment_Name: "{self.mercenary_file_comment_name}",
        }},
    }},"""

        return data
    
    def parse(self):
        datas = []
        for x in os.listdir(self.folder_location):
            self.mercenary_code = None
            self.mercenary_config = ModConfigParser(allow_no_value=True)
            self.mercenary_keys = None
            self.attack_config = ModConfigParser(allow_no_value=True)
            self.buff_config = ModConfigParser(allow_no_value=True)

            self.max_combo = None
            self.max_jump = '1'
            self.mercenary_file_comment_name = None
            self.highest_damage = None
            self.can_sprint = '✗'
            self.can_deflect = '✗'
            self.can_counter = '✗'
            self.gauge_bullet = '✗'
            self.unique_property = []
            self.down_hits = []

            if not self.is_mercenary(x) or x == '000' or int(x) >= 550 and int(x) <= 600:
                continue
            print('processing: ', x)
            self.mercenary_code = x
            try:
                self.mercenary_config.read(self.folder_location + '\\' + x + '\\' + x + '_item.ini')
                self.encoder = None
            except UnicodeDecodeError:
                try:
                    try:
                        self.encoder = 'utf-8'
                        self.mercenary_config.read_file(open(self.folder_location + '\\' + x + '\\' + x + '_item.ini', 'r', encoding='utf-8'))
                    except MissingSectionHeaderError:
                        self.encoder = 'utf-8-sig'
                        self.mercenary_config.read_file(open(self.folder_location + '\\' + x + '\\' + x + '_item.ini', 'r', encoding='utf-8-sig'))
                    except UnicodeDecodeError:
                        self.encoder = 'euc-kr'
                        self.mercenary_config.read_file(open(self.folder_location + '\\' + x + '\\' + x + '_item.ini', 'r', encoding='euc-kr'))
                except UnicodeDecodeError:
                    self.encoder = 'ansi'
                    self.mercenary_config.read_file(open(self.folder_location + '\\' + x + '\\' + x + '_item.ini', 'r', encoding='ansi'))

            # self.reformat_mercenary(self.folder_location + '\\' + x + '\\' + x + '_item.ini')
            self.reformat_attack(self.folder_location + '\\' + x + '\\' + x + '_attack.ini')

            inputs = self.attack_data()

            data = self.table_convert(inputs)
            datas = [_ for _ in datas + [data]]
            columns = ''
        if self.method == 2:
            location = './mercenaries_table.js'
            columns += """export const column = Object.keys(mercenaries[0]).map((key) => ({
    Header: key.replace("_", " "),
    accessor: key,
}));"""
        else:
            location = './mercenaries_individual.js'
            for x in self.valid_mercenaries:
                columns += f"""
export const mercenary_info_{x} = Object.keys(mercenary_{x}[0]).map((key) => ({{
    Header: key.replace("_", " "),
    accessor: key,
}}));

export const mercenary_attack_{x} = Object.keys(mercenary_{x}_attacks[0]).map((key) => ({{
    Header: key.replace("_", " "),
    accessor: key,
}}));
"""
        with open(location, 'w+', encoding='utf-8') as f:
            combined = '\n'.join(datas)
            if self.method == 1:
                file = f"""
import React from "react";

// -------------------------------------------------------------------------------------------------------------
// Manually editing this file is not recommended since most mercenary data are automated.
// If you wish to edit individual mercenary, please use the manual override and use the provided tools to do so.
// -------------------------------------------------------------------------------------------------------------

{combined}

{columns}"""
            else:
                file = f"""import React from "react";

// -------------------------------------------------------------------------------------------------------------
// Manually editing this file is not recommended since most mercenary data are automated.
// If you wish to edit individual mercenary, please use the manual override and use the provided tools to do so.
// -------------------------------------------------------------------------------------------------------------
export const mercenaries = [
{combined}
];

{columns}"""
            f.write(file)
        with open('valid_mercenaries.txt', 'w+') as f:
            f.writelines(_ + '\n' for _ in self.valid_mercenaries)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='config-scraper',
        description='Python script to scrape the mercenary data from config/mercenary folder',
        formatter_class=argparse.RawTextHelpFormatter
        )
    required = argparser.add_argument_group('Required')
    optional = argparser.add_argument_group('Optional')
    required.add_argument('mercenary_folder', type=str, help="Folder containg the mercenaries (config/mercenary). Use the mercenary folder, not the config")
    optional.add_argument('-m', '--method', type=int, required=True, help="The mercenary generation method for table.\n1. Mercenaries per individual table\n2. Mercenaries for all table")
    optional.add_argument('-t', '--text', type=str, required=False, help="The Lost Saga text file. It is usually found on xml/text_id.txt\nWithout this, mercenary name won't be provided.")
    optional.add_argument('-o', '--override', type=str, required=False, help="The override folder location. It is found at the docs repository at the root folder.")
    optional.add_argument('-i', '--images', type=str, required=False, help="Images folder containing mercenaries illustration and mini icon. The file name is the same as you would download them directly from the lostsaga.com site")
    args = vars(argparser.parse_args())
    parser = Mercenary_Config_Parser(**args)
    parser.parse()