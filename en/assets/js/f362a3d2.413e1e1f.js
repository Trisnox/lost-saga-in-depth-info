"use strict";(self.webpackChunkls_data_scrape_project=self.webpackChunkls_data_scrape_project||[]).push([[7797],{61870:(e,a,t)=>{t.r(a),t.d(a,{assets:()=>d,contentTitle:()=>s,default:()=>_,frontMatter:()=>r,metadata:()=>o,toc:()=>l});var n=t(87462),i=(t(67294),t(3905));const r={id:"HP and Damage",slug:"char_info",sidebar_position:3},s=void 0,o={unversionedId:"HP and Damage",id:"HP and Damage",title:"HP and Damage",description:"By default, player have 196.0 HP and 300.0 Speed.",source:"@site/i18n/en/docusaurus-plugin-content-docs/current/2_hp_and_damage.mdx",sourceDirName:".",slug:"/char_info",permalink:"/en/docs/char_info",draft:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/2_hp_and_damage.mdx",tags:[],version:"current",sidebarPosition:3,frontMatter:{id:"HP and Damage",slug:"char_info",sidebar_position:3},sidebar:"tutorialSidebar",previous:{title:"Individual Gear Data",permalink:"/en/docs/data/gear/gear_list"}},d={},l=[],c={toc:l},p="wrapper";function _(e){let{components:a,...t}=e;return(0,i.kt)(p,(0,n.Z)({},c,t,{components:a,mdxType:"MDXLayout"}),(0,i.kt)("p",null,"By default, player have 196.0 HP and 300.0 Speed."),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-ini",metastring:'title="sp2_char.ini"',title:'"sp2_char.ini"'},";------------------------// \uccb4\ub825, \uc774\ub3d9\uc18d\ub3c4\ndefault_hp    = 196.0f\ndefault_speed = 300.0f\n")),(0,i.kt)("p",null,"Here is also table that shows how much damage player would receive during specific conditions."),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-ini",metastring:'title="sp2_char.ini"',title:'"sp2_char.ini"'},"; // \ud53c\ud574\uc728 (\ud6c4\uba74 / \ub2e4\uc6b4 / \uacf5\uc911 / \ube59\uacb0) (1 = 100%)\nback_attack_damage_rate     = 1.0f\nback_attack_gap_time        = 0\nblow_state_damage_rate      = 0.5f\nblow_state_push_power_rate  = 0.1f\nblow3_state_push_power_rate = 0.3f\nblow_state_blow_power_rate  = 1.0f\nfloat_state_damage_rate     = 0.5f\nfrozen_damage_rate          = 0.5f\n")),(0,i.kt)("p",null,"This means that, if the enemy is on air, they only receive 50% of usual damage (",(0,i.kt)("inlineCode",{parentName:"p"},"blow_state_damage_rate"),"). But, if\nthe enemy is down, they receive 100% damage."),(0,i.kt)("p",null,"Even though back attacks (",(0,i.kt)("inlineCode",{parentName:"p"},"back_attack_damage_rate"),") was written as ",(0,i.kt)("inlineCode",{parentName:"p"},"1.0f"),", the damage enemy would receive is still the same as is (no damage bonus)."))}_.isMDXComponent=!0}}]);