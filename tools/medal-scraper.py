import argparse
import importlib
import io
import json
import os
import re
import sys
import traceback
from configparser import (DuplicateSectionError, MissingSectionHeaderError,
                          NoOptionError)

from ext.modified_parser import ModConfigParser


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class Medal_Config_Parser():
    def __init__(self, **kwargs):
        self.medal_location = kwargs.get('medal_file', None)
        # text_-.txt, where - is the language
        self.text_location = kwargs.get('text', None)

        self.medal = ModConfigParser(allow_no_value=True)
        self.text = {}

        if self.medal_location:
            self.medal.read_file(open(self.medal_location, encoding='ansi'))
            self.medal.remove_section('sell_info')
            self.medal.remove_section('slot_info')
            self.medal.remove_section('item_info_common')
        
        if self.text_location:
            with open(self.text_location, 'r', encoding='ansi') as f:
                entries = f.readlines()
                entries = [_ for _ in entries if '|INI_sp2_medalitem_info::item_info_' in _]
                for x in entries:
                    res = re.findall(r'.*_(\d*)_\d\|(.*)\|.*', x)[0]
                    self.text[res[0]] = res[1]
    
    def parse(self):
        datas = []
        for x in self.medal.sections():
            medal_type = self.medal[x]['item_type']
            medal_id = medal_type.zfill(5)
            medal_name = self.text.get(medal_type, '<No Name>')

            medal_level = self.medal[x].get('limit_level', '0')
            medal_hero = self.medal[x].get('use_class_1', '0')

            medal_dump = re.search(r'#(.*)', self.medal[x]['icon'])[1]

            if not medal_dump.endswith('custommedal'):
                weapon = self.medal[x].get('item_growth_1', '0')
                armor = self.medal[x].get('item_growth_2', '0')
                helm = self.medal[x].get('item_growth_3', '0')
                trinket = self.medal[x].get('item_growth_4', '0')
                
                medal_weapon = '+' + weapon if not weapon == '0' and not weapon.startswith('-') else weapon
                medal_armor = '+' + armor if not armor == '0' and not armor.startswith('-') else armor
                medal_helm = '+' + helm if not helm == '0' and not helm.startswith('-') else helm
                medal_trinket = '+' + trinket if not trinket == '0' and not trinket.startswith('-') else trinket

                attack = self.medal[x].get('char_growth_1', '0')
                defense = self.medal[x].get('char_growth_2', '0')
                speed = self.medal[x].get('char_growth_3', '0')
                dexterity = self.medal[x].get('char_growth_4', '0')

                medal_attack = '+' + attack if not attack == '0' and not attack.startswith('-') else attack
                medal_defense = '+' + defense if not defense == '0' and not defense.startswith('-') else defense
                medal_speed = '+' + speed if not speed == '0' and not speed.startswith('-') else speed
                medal_dexterity = '+' + dexterity if not dexterity == '0' and not dexterity.startswith('-') else dexterity

                stats = f""""Weapon  {medal_weapon}": "Attack    {medal_attack}",
            "Armor   {medal_armor}": "Defense   {medal_defense}",
            "Helmet  {medal_helm}": "Speed     {medal_speed}",
            "Trinket {medal_trinket}": "Dexterity {medal_dexterity}","""
            else:
                medal_point = self.medal[x]['total_point']
                medal_select = self.medal[x]['enable_select_stat']

                medal_min_stat = self.medal[x]['min_stat_point']
                medal_max_stat = self.medal[x]['max_stat_point']
                stats = f""""Max Point: {medal_point}": "Max Stat Choice: {medal_select}",
            "Minimum Stat: {medal_min_stat}": "Maximum Stat: {medal_max_stat}",
"""


            if medal_level == '0' and medal_hero == '0':
                restrictions = """Restriction: "-","""
            else:
                if medal_level == '0':
                    level = ''
                else:
                    level = f'Level: "{medal_level}",'
                if medal_hero == '0':
                    hero = ''
                else:
                    hero = f'Hero: "{medal_hero}",'

                restrictions = f"""Restriction: {{
                {level}
                {hero}
                }},"""

            data = f"""
    {{
        ID: "{medal_id}",
        Icon: "",
        Name: "{medal_name}",
        Stats: {{
            {stats}
        }},
        {restrictions}
        Dump: "{medal_dump}",
    }},"""
            datas = [_ for _ in datas + [data]]
        
        combined = '\n'.join(datas)
        with open('./medal_table.js', 'w+', encoding='utf-8') as f:
            f.write(f"""import React from "react";

// -------------------------------------------------------------------------------------------------------------
// Manually editing this file is not recommended since most mercenary data are automated.
// If you wish to edit individual mercenary, please use the manual override and use the provided tools to do so.
// -------------------------------------------------------------------------------------------------------------
export const medals = [
{combined}
];

export const column = Object.keys(medals[0]).map((key) => ({{
    Header: key.replace(/_/g, " "),
    accessor: key,
}}));""")

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='config-scraper',
        description='Python script to scrape the medal data through sp2_medalitem_info.ini file',
        formatter_class=argparse.RawTextHelpFormatter
        )
    required = argparser.add_argument_group('Required')
    optional = argparser.add_argument_group('Optional')
    required.add_argument('medal_file', type=str, help="File containg the medal info. Not the folder")
    required.add_argument('text', type=str, help="The text_[lang].txt file, which contains information about medal names and other stuffs")
    args = vars(argparser.parse_args())
    parser = Medal_Config_Parser(**args)
    parser.parse()