

# SQLite3 common commands

## Create a table

~~~sqlite
CREATE TABLE table_name(
   column1 datatype,
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype
);
~~~

## Insert a reacord to table 

~~~sqlite
INSERT INTO TABLE_NAME VALUES (value1,value2,value3,...valueN);
~~~

## Display table

~~~sqlite
DISPLAY TABLE_NAME
~~~

~~~
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
~~~

## Query some records with conditions

~~~sqlite
SELECT * FROM COMPANY WHERE ( AGE >= 25 AND SALARY >= 65000 );


~~~

## Delete records 

~~~
DELETE FROM table_name WHERE [condition];
~~~

## Update records

~~~
UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
~~~

