import os
if __name__ == '__main__':
    with open('valid_mercenaries.txt', 'r') as f:
        valid_mercenaries = f.readlines()
        valid_mercenaries = [_.strip() for _ in valid_mercenaries]
    
    valid_images = {}
    for x, y, z in os.walk("D:\\codes\\lso_in-depth_info\\ls-data-scrape-project\\static\\img"):
        _, constant, remaining = x.partition("static\\img")
        image_location = "@site/" + constant.replace('\\', '/') + remaining.replace('\\', '/')
        for a in z:
            valid_images[a] = image_location + '/' + a
    
    for x in valid_mercenaries:
        image1 = valid_images.get(f"thum_char_view_n_{x}.jpg", '')
        image2 = valid_images.get(f"thum_char_view_o_{x}.jpg", '')
        if not image1 == '':
            image1 = f"<Image img={{require('{image1}')}}/>"
        if not image2 == '':
            image2 = f"<Image img={{require('{image2}')}}/>"
        text = f"""---
id: {x}
slug: {x}
---

import Image from "@theme/IdealImage";
import {{ TableComponent }} from "@site/src/components/SortableTable";
import {{ mercenary_{x}, mercenary_{x}_attacks, mercenary_info_{x}, mercenary_attack_{x} }} from "@site/src/table/mercenaries_individual";

# {x}

<div style = {{{{ display: "flex" }}}}>
    {image1}
    {image2}
</div>

## Mercenary Summary

<TableComponent
  columns={{ mercenary_info_{x} }}
  data={{ mercenary_{x} }}
/>

## Mercenary Attacks

<TableComponent
  columns={{ mercenary_attack_{x} }}
  data={{ mercenary_{x}_attacks }}
/>"""
        with open(f'{x}.mdx', 'w+') as f:
            f.write(text)