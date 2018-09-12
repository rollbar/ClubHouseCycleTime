# Cycle Time

This script calculate the cycle time from ClubHouse stories and report it in the following format. The idea is to sum and average the cycle time of each story that is in work for a specif user in a given week.

The script will generate a report based on the previous 8 weeks:

```
 Member             |   2018 W30 |   2018 W31 |   2018 W32 |   2018 W33 |   2018 W34 |   2018 W35 |   2018 W36 |   2018 W37
--------------------+------------+------------+------------+------------+------------+------------+------------+------------
 Tyler YC           |       7208 |       7208 |       7208 |       7208 |       7208 |       7208 |       7208 |       7208
 Zachary Collins    |       1068 |        575 |        341 |        485 |       1187 |        895 |       1161 |       1161
 Ken Sheppardson    |        444 |        258 |        181 |        577 |        550 |        345 |        231 |        550
 Michael Davis      |       7617 |       7617 |       7617 |       7617 |       7617 |       7617 |       7617 |       7617
 Cory Virok         |       1054 |       1054 |       1188 |        751 |        589 |        788 |        459 |        372
 david karapetyan   |       1149 |       1018 |       1122 |       1261 |       1321 |       1441 |       1201 |       1374
 michael mccullough |      15406 |      15406 |      15406 |      15406 |      15406 |      15406 |      15406 |      15406
 Andrew Ledvina     |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 Joe Bagdon         |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 David Basoco       |        487 |        868 |        426 |        290 |        302 |        501 |        366 |        611
 Rivkah Standig     |       1689 |       1689 |       1250 |       1244 |       1244 |       1244 |       1244 |       1244
 Francesco Crippa   |          0 |          0 |          0 |          0 |          0 |          0 |        140 |         93
 Jesse Gibbs        |       1727 |       1151 |        908 |        408 |        770 |        524 |        878 |        878
 Ali Shakiba        |         60 |         74 |        161 |        177 |        142 |         84 |        129 |         45
 Casie Chen         |        216 |        240 |        240 |          0 |         13 |          0 |          0 |          0
 Rollbar App        |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 Ivan Gomez         |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 Anthony Tran       |       2399 |       2022 |       2528 |       2528 |       2251 |       2528 |       2528 |       2528
 Julie Jones        |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 Megan Anderson     |        232 |        218 |        135 |        272 |        263 |        123 |         49 |        120
 Brian Rue          |          0 |         11 |          7 |          0 |          0 |          0 |          0 |          0
 Jon de Andres      |        129 |        182 |        131 |        160 |         24 |         44 |         24 |          1
 Jason Skowronski   |       2071 |       1108 |        821 |        248 |          0 |          0 |          0 |          0
 Derick Chung       |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 Artur Moczulski    |          0 |          0 |          0 |          0 |          0 |          0 |          0 |          0
 T. Dampier         |       1033 |       1033 |       1847 |       1847 |          0 |          0 |         95 |         95
 Jaee Apte          |       1448 |       1866 |       1399 |       4677 |       4677 |       1596 |       2397 |       2397
 ```


 ## How to run it

 Firts, you need a ClubHouse API Token. You can generate one from ClubHouse directly under ```Settings->Settings->API Tokens```.

  ```bash
 echo 'YOUR_API_TOKEN' > CLUBHOUSE_TOKEN.txt
 ```

 Once you have it, this should be enough to run the script:

 ```bash
 pipenv install
 pipenv shell
 python run.py
 ```
