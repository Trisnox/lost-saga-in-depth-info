---
slug: how-to-read-mercenary
title: Cara Baca Informasi Hero
authors: trisnox
---

Gunakan gambar sebagai acuan.

![Mercenary Summary](@site/static/img/table1.png)
- `ID` kode hero. Biasanya setiap hero memiliki kode unik
- `Name` nama hero
- `Sprint` indikasi jika hero ini bisa lari
- `Jump` maksimal lompatan yang bisa dilakukan
- `Attack Length` jumlah serangan dari serangan `Ground`
- `Highest Damage` serangan yang paling sakit yang dimiliki hero tersebut
-  `360 Block` indikasi jika tangkisan hero tersebut juga menangkis serangan dari belakang
- `Deflect` indikasi jika tangkisan kita memantulkan musuh (jika menangkis tepat waktu)
- `Counter` indikasi jika hero tersebut bisa menyerang balik jika menekan tombol serang saat menangkis serangan musuh
- `Down Hit` daftar serangan yang bisa menyerang musuh yang jatuh/down
- `Special` kegunaan gauge/bullet pada hero
- `Unique Property` properti unik yang dimiliki hero tersebut
- `Dump` informasi tambahan

![Mercenary Attacks](@site/static/img/table2.png)

1. Nama serangan
- `Ground` serangan ketika dalam keadaan diam/jalan
- `Dash` serangan ketika dalam keadaan lari
- `Dash Replace` hero ini tidak bisa lari, jika mencoba untuk lari, maka serangan ini akan dipakai
- `Jump` serangan ketika sedang di udara
- `... Jump Hold` serangan ketika tombol serang ditekan lebih lama
- `Charged` serangan ketika tombol serang ditekan lebih lama ketika dalam keadaan diam/jalan
- `... Extend` serangan lanjutan ketikan menekan tombol serang
- `... Hold` serangan ketika tombol serang ditekan lebih lama
- `Counter` serangan ketika menekan tombol serang saat menangkis serangan dari musuh

2. Attribut serangan
- `Damage` damage yang disebabkan oleh serangan itu
- `Defense Break` indikasi jika serangan ini menyebabkan hancur tangkis
- `Juggle` seberapa tinggi musuh akan diangkat ke udara jika diserang dalam keadaan tertentu (seperti: faint)
- `Air Juggle` jika musuh berada di udara, ini mengindikasikan seberapa tinggi musuh akan diangkat
- `Down Hit` indikasi jika serangan ini bisa mengenai musuh yang sedang jatuh/down
- `Push Power` seberapa kuat serangan tersebut mendorong musuh
- `Frozen Break` indikasi jika serangan ini menghancurkan state musuh yang sedang frozen

3. Jika ada kolom seperti ini, ini berarti serangan ini multi-hit (serangan ini menyebabkan dua atau lebih serangan)