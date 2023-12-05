# pointCloud2_to_csv
ROS bug で保存したpointCloud2データをCSVファイルに変換するものです。
[sick_scan_xd](https://github.com/SICKAG/sick_scan_xd)で出力されたデータは基本的に適合します。
pointCloud2に付随しているデータ型情報に基づいて型を決める機能は未実装ですべてfloat32でx,y,z,iの4データのみを変換します。
