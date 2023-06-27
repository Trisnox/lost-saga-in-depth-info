---
slug: how-to-read-mercenary
title: How to Read Mercenary Information
authors: trisnox
---

Use image as referece.

![Mercenary Summary](@site/static/img/table1.png)
- `ID` mercenary code. Every mercenary have unique code attached to them
- `Name` mercenary name
- `Sprint` indicates if this mercenary can run
- `Jump` maximum jump this mercenary could do
- `Attack Length` attack length from `Ground` attacks
- `Highest Damage` the most damaging attack this mercenary had
-  `360 Block` indicates if blocking will also protect hits from back
- `Deflect` indicates if mercenary block will deflect enemy (must block at perfect time to deflect)
- `Counter` indicates if mercenary able to perform a counter attack when attack button is pressed when blocking a hit
- `Down Hit` list of attack that are able to hit downed enemy
- `Special` gauge/bullet usage on mercenary
- `Unique Property` unique property this mercenary had
- `Dump` additional info

![Mercenary Attacks](@site/static/img/table2.png)

1. Attacks name
- `Ground` attacks when being done while idling/walking
- `Dash` attacks when being done while running
- `Dash Replace` this mercenary cannot run, if attempting to run, this attack will be used instead
- `Jump` attacks when being done while at air
- `... Jump Hold` attacks when you hold attack button much longer
- `Charged` attacks when you hold attack button much longer during idling/walking
- `... Extend` follow-up attack when you press attack button
- `... Hold` attacks when you hold attack button much longer
- `Counter` attack when you press attack button while blocking a hit from enemy

2. Attacks attribute
- `Damage` damage caused by that attack
- `Defense Break` indicates if this attack break enemy's block
- `Juggle` how high the enemy will be lifted when hit with this attack during some state (eg: faint)
- `Air Juggle` if the enemy is on air, this indicate how much enemy will be lifted with this attack
- `Down Hit` indicates if this attack can hit downed enemy
- `Push Power` indicates how strong this move to push enemy (on ground)
- `Frozen Break` indicates if this attack would break enemy frozen state

3. If this column exist, this means that this attack is a multi-hit (hits more than once)