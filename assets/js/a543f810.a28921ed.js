"use strict";(self.webpackChunkls_data_scrape_project=self.webpackChunkls_data_scrape_project||[]).push([[4271],{49:a=>{a.exports=JSON.parse('{"blogPosts":[{"id":"how-to-read-mercenary","metadata":{"permalink":"/lost-saga-in-depth-info/blog/how-to-read-mercenary","editUrl":"https://github.com/trisnox/lost-saga-in-depth-info/tree/main/blog/2023-06-27-how-to-read.md","source":"@site/blog/2023-06-27-how-to-read.md","title":"Cara Baca Informasi Hero","description":"Gunakan gambar sebagai acuan.","date":"2023-06-27T00:00:00.000Z","formattedDate":"27 Juni 2023","tags":[],"readingTime":1.645,"hasTruncateMarker":false,"authors":[{"name":"Trisnox","title":"Wiki Author","url":"https://github.com/trisnox","imageURL":"https://github.com/trisnox.png","key":"trisnox"}],"frontMatter":{"slug":"how-to-read-mercenary","title":"Cara Baca Informasi Hero","authors":"trisnox"},"nextItem":{"title":"Author\'s Note","permalink":"/lost-saga-in-depth-info/blog/init-release"}},"content":"Gunakan gambar sebagai acuan.\\r\\n\\r\\n![Mercenary Summary](@site/static/img/table1.png)\\r\\n- `ID` kode hero. Biasanya setiap hero memiliki kode unik\\r\\n- `Name` nama hero\\r\\n- `Sprint` indikasi jika hero ini bisa lari\\r\\n- `Jump` maksimal lompatan yang bisa dilakukan\\r\\n- `Attack Length` jumlah serangan dari serangan `Ground`\\r\\n- `Highest Damage` serangan yang paling sakit yang dimiliki hero tersebut\\r\\n-  `360 Block` indikasi jika tangkisan hero tersebut juga menangkis serangan dari belakang\\r\\n- `Deflect` indikasi jika tangkisan kita memantulkan musuh (jika menangkis tepat waktu)\\r\\n- `Counter` indikasi jika hero tersebut bisa menyerang balik jika menekan tombol serang saat menangkis serangan musuh\\r\\n- `Down Hit` daftar serangan yang bisa menyerang musuh yang jatuh/down\\r\\n- `Special` kegunaan gauge/bullet pada hero\\r\\n- `Unique Property` properti unik yang dimiliki hero tersebut\\r\\n- `Dump` informasi tambahan\\r\\n\\r\\n![Mercenary Attacks](@site/static/img/table2.png)\\r\\n\\r\\n1. Nama serangan\\r\\n- `Ground` serangan ketika dalam keadaan diam/jalan\\r\\n- `Dash` serangan ketika dalam keadaan lari\\r\\n- `Dash Replace` hero ini tidak bisa lari, jika mencoba untuk lari, maka serangan ini akan dipakai\\r\\n- `Jump` serangan ketika sedang di udara\\r\\n- `... Jump Hold` serangan ketika tombol serang ditekan lebih lama\\r\\n- `Charged` serangan ketika tombol serang ditekan lebih lama ketika dalam keadaan diam/jalan\\r\\n- `... Extend` serangan lanjutan ketikan menekan tombol serang\\r\\n- `... Hold` serangan ketika tombol serang ditekan lebih lama\\r\\n- `Counter` serangan ketika menekan tombol serang saat menangkis serangan dari musuh\\r\\n\\r\\n2. Attribut serangan\\r\\n- `Damage` damage yang disebabkan oleh serangan itu\\r\\n- `Defense Break` indikasi jika serangan ini menyebabkan hancur tangkis\\r\\n- `Juggle` seberapa tinggi musuh akan diangkat ke udara jika diserang dalam keadaan tertentu (seperti: faint)\\r\\n- `Air Juggle` jika musuh berada di udara, ini mengindikasikan seberapa tinggi musuh akan diangkat\\r\\n- `Down Hit` indikasi jika serangan ini bisa mengenai musuh yang sedang jatuh/down\\r\\n- `Push Power` seberapa kuat serangan tersebut mendorong musuh\\r\\n- `Frozen Break` indikasi jika serangan ini menghancurkan state musuh yang sedang frozen\\r\\n\\r\\n3. Jika ada kolom seperti ini, ini berarti serangan ini multi-hit (serangan ini menyebabkan dua atau lebih serangan)"},{"id":"init-release","metadata":{"permalink":"/lost-saga-in-depth-info/blog/init-release","editUrl":"https://github.com/trisnox/lost-saga-in-depth-info/tree/main/blog/2023-06-20-dev-note.md","source":"@site/blog/2023-06-20-dev-note.md","title":"Author\'s Note","description":"Catatan inisial rilis. Wiki ini dibuat dengan tujuan edukasi. Biasanya game/website Lost Saga tidak/kurang mencakupi informasi tentang suatu gear/hero, maka terbuatlah wiki ini dengan tujuan untuk meng-scrape semua data hero dan gear agar kita dapat memahami mekanisme game lebih baik.","date":"2023-06-20T00:00:00.000Z","formattedDate":"20 Juni 2023","tags":[],"readingTime":1.11,"hasTruncateMarker":false,"authors":[{"name":"Trisnox","title":"Wiki Author","url":"https://github.com/trisnox","imageURL":"https://github.com/trisnox.png","key":"trisnox"}],"frontMatter":{"slug":"init-release","title":"Author\'s Note","authors":"trisnox"},"prevItem":{"title":"Cara Baca Informasi Hero","permalink":"/lost-saga-in-depth-info/blog/how-to-read-mercenary"}},"content":"Catatan inisial rilis. Wiki ini dibuat dengan tujuan edukasi. Biasanya game/website Lost Saga tidak/kurang mencakupi informasi tentang suatu gear/hero, maka terbuatlah wiki ini dengan tujuan untuk meng-scrape semua data hero dan gear agar kita dapat memahami mekanisme game lebih baik.\\r\\n\\r\\nSaat ini saya hanya bekerja sendiri saja, jika ingin berkontribusi/sugesti/fix (typo, informasi salah, informasi kurang), bisa kontak via `discord: trisnox`, submit [pull request](https://google.com), submit [issue](https://google.com). Untuk discord, bisa lewat dm atau server discord langsung, dihimbau agar tidak berdiskusi tentang subjek ini di discord lso valofe, terima kasih.\\r\\n\\r\\n---\\r\\n\\r\\nSedikit lore, semuanya berawal ketika saya gabut ingin ekstrak model dari Lost Saga, yang kemudian [saya buat animasi dari model tersebut](https://youtu.be/DLYl9QIcmUM). Setelah berpikir-pikir, ternyata hampir seluruh resource Lost Saga tersedia didalam arsip tersebut, ini termasuk data hero, gear, shop, mode pvp/pve, dan lain-lain.\\r\\n\\r\\nFile ini menyediakan informasi yang lengkap terhadap barang tersebut, ketika saya melihat data-data tersebut, saya terkejut karena ada banyak sekali informasi yang tidak satu orang pun tau secara detail tentang informasi tersebut.\\r\\n\\r\\nSebagai contoh: helm scientist lvl 3 tidak memberi efek damage bonus, tetapi membuat player tersebut mengaplikasikan efek poison pada setiap hit kepada musuh. Poison ini berlangsung selama .1s, dan setiap .05s darah musuh berkurang sebanyak 2%.\\r\\n\\r\\nBahkan developer/GM saja tidak menjelaskan informasi secara detail begitu, maka dari itu, terbuatlah wiki ini untuk menyediakan informasi kepada seluruh player Lost Saga."}]}')}}]);