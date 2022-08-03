[Установка]

Перед использованием рекомендуется проверить наличие требуемых модулей python.

Это можно сделать с помощью запуска скрипта check_modules.py

Если модуль отсутствует в системе будет запущена его установка.

Для запуска проверки необходимо выполнить:

$ Win+R -> cmd

[cmd] cd C:\Users\and_andreev\Desktop\git_repos\mac_arp\analyzer_arp

[cmd] python ./check_modules.py


[Описание работы]

Инструмент состоит из двух компонент.

analyzer_arp - предназначен для сравнения состава записей в рамках одной единицы оборудования до и после работ. 
описание детальное описание выходных файлов и работы находится в директории инструмента.

analyzer_arp_move - предназначен для сравнения состава записей в рамках двух единиц оборудования (исходное и подменное) до и после работ. 
описание детальное описание выходных файлов и работы находится в директории инструмента.
