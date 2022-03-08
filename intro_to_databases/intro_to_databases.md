# Intro to databases

## Competency thingy

https://curriculumlibrary.nshcs.org.uk/stp/competency/S-BG-S3/3/

## What database is

A database is a specific structure in which you store data. While Excels and JSON could do the job, don't do that for obvious reasons.

It is formed of tables containing columns helping define what data is stored.

```mysql
+----------------+------------------------------------+-----------------+------------------+--------------------+----------------------------------+--------------------------+-------------------+---------------+------------+--------------+------------------------+-------------+
| customerNumber | customerName                       | contactLastName | contactFirstName | phone              | addressLine1                     | addressLine2             | city              | state         | postalCode | country      | salesRepEmployeeNumber | creditLimit |
+----------------+------------------------------------+-----------------+------------------+--------------------+----------------------------------+--------------------------+-------------------+---------------+------------+--------------+------------------------+-------------+
|            103 | Atelier graphique                  | Schmitt         | Carine           | 40.32.2555         | 54, rue Royale                   | NULL                     | Nantes            | NULL          | 44000      | France       |                   1370 |    21000.00 |
|            112 | Signal Gift Stores                 | King            | Jean             | 7025551838         | 8489 Strong St.                  | NULL                     | Las Vegas         | NV            | 83030      | USA          |                   1166 |    71800.00 |
|            114 | Australian Collectors, Co.         | Ferguson        | Peter            | 03 9520 4555       | 636 St Kilda Road                | Level 3                  | Melbourne         | Victoria      | 3004       | Australia    |                   1611 |   117300.00 |
|            119 | La Rochelle Gifts                  | Labrune         | Janine           | 40.67.8555         | 67, rue des Cinquante Otages     | NULL                     | Nantes            | NULL          | 44000      | France       |                   1370 |   118200.00 |
|            121 | Baane Mini Imports                 | Bergulfsen      | Jonas            | 07-98 9555         | Erling Skakkes gate 78           | NULL                     | Stavern           | NULL          | 4110       | Norway       |                   1504 |    81700.00 |
+----------------+------------------------------------+-----------------+------------------+--------------------+----------------------------------+--------------------------+-------------------+---------------+------------+--------------+------------------------+-------------+
```

## Linking stuff together

Storing a lot of data becomes complicated really fast depending on how much information you want to store.

```mysql
+-------------+------------+--------------+-------------+---------+------------------------+----------------+
| orderNumber | orderDate  | requiredDate | shippedDate | status  | comments               | customerNumber |
+-------------+------------+--------------+-------------+---------+------------------------+----------------+
|       10100 | 2003-01-06 | 2003-01-13   | 2003-01-10  | Shipped | NULL                   |            363 |
|       10101 | 2003-01-09 | 2003-01-18   | 2003-01-11  | Shipped | Check on availability. |            128 |
|       10102 | 2003-01-10 | 2003-01-18   | 2003-01-14  | Shipped | NULL                   |            181 |
|       10103 | 2003-01-29 | 2003-02-07   | 2003-02-02  | Shipped | NULL                   |            121 |
|       10104 | 2003-01-31 | 2003-02-09   | 2003-02-01  | Shipped | NULL                   |            141 |
+-------------+------------+--------------+-------------+---------+------------------------+----------------+
```

For example, to link orders to customers, we use primary keys and foreign keys.

Every row has a primary key as an ID. And we can use those IDs to identify the row of data uniquely and unambiguously.

We can link the order to the customer by creating a column (customerNumber) which will contain a foreign key which is a primary key from another table.

## Indexes

Per the [MySQL documentation](https://dev.mysql.com/doc/refman/8.0/en/mysql-indexes.html#:~:text=Indexes%20are%20used%20to%20find,table%2C%20the%20more%20this%20costs.):
> Indexes are used to find rows with specific column values quickly. Without an index, MySQL must begin with the first row and then read through the entire table to find the relevant rows. The larger the table, the more this costs. If the table has an index for the columns in question, MySQL can quickly determine the position to seek to in the middle of the data file without having to look at all the data.

```mysql
mysql> show index from clinical_indication;
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table               | Non_unique | Key_name                       | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| clinical_indication |          0 | PRIMARY                        |            1 | id          | A         |         271 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
| clinical_indication |          1 | clinical_in_name_d871dc_idx    |            1 | name        | A         |         266 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
| clinical_indication |          1 | clinical_in_gemini__a1b42a_idx |            1 | gemini_name | A         |         271 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
```

## Database schema

Creating a database schema is a good design exercise where you have to think about use cases and have good requirements.

Per Microsoft Access <https://support.microsoft.com/en-us/office/database-design-basics-eb2159cf-1e30-401a-8084-bd4f9c9ca1f5#bmpurpose>:

- Determine the purpose of your database
- Find and organize the information required
- Divide the information into tables
- Turn information items into columns
- Specify primary keys
- Set up the table relationships
  - Think about one-to-one/one-to-many/many-to-many relationships
- Refine your design
  - Try and remove redundant information
- Apply the normalization rules

A nice tool to create schemas online: <https://dbdiagram.io/home>

### Normalisation

The rules are the following:

- First normal form (1NF)

Every column should have atomic values.

Wrong:
|ISBN#|Title|Format|Author|Author Nationality|Price|Subject|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Hardcover|Chad Russell|American|49.99|MySQL, Database, Design|520|Thick|Tutorial|

Right:
|ISBN#|Title|Format|Author|Author Nationality|Price|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Hardcover|Chad Russell|American|49.99|520|Thick|Tutorial|

|ISBN#|Subject name|
|---|---|
|1590593324|MySQL|
|1590593324|Database|
|1590593324|Design|

- Second normal form (2NF)
  - Should be in 1NF
  - Should not have partial dependency

ISBN, Title and Format form a key as they are needed to identify a row. However price depends on format which is a partial dependency.

To fix that we create another table with the format and the price.

Wrong:
|ISBN#|Title|Format|Author|Author Nationality|Price|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Hardcover|Chad Russell|American|49.99|520|Thick|Tutorial|
|1590593324|Beginning MySQL Database Design and Optimization|E-book|Chad Russell|American|22.34|520|Thick|Tutorial|
|8594308655|The Relational Model for Database Management: Version 2|Hardcover|E.F.Codd|British|39.99|538|Thick|Popular science|
|8594308655|The Relational Model for Database Management: Version 2|E-book|E.F.Codd|British|13.88|538|Thick|Popular science|

Right:
|ISBN#|Title|Author|Author Nationality|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Chad Russell|American|520|Thick|Tutorial|
|8594308655|The Relational Model for Database Management: Version 2|E.F.Codd|British|538|Thick|Popular science|

|Title|Format|Price|
|---|---|---|
|Beginning MySQL Database Design and Optimization|Hardcover|49.99|
|Beginning MySQL Database Design and Optimization|E-book|22.34|
|The Relational Model for Database Management: Version 2|E-book|13.88|
|The Relational Model for Database Management: Version 2|Paperback|39.99|

- Third normal form (3NF)
  - Should be in 2NF
  - Should not have transitive dependency

Author nationality depends on the author which is vulnerable to logical inconsistencies i.e. same author could have another nationality.

Wrong:
|ISBN#|Title|Author|Author Nationality|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Chad Russell|American|520|Thick|Tutorial|
|8594308655|The Relational Model for Database Management: Version 2|E.F.Codd|British|538|Thick|Popular science|

Right:
|ISBN#|Title|Author|Pages|Thickness|Genre Name|
|---|---|---|---|---|---|
|1590593324|Beginning MySQL Database Design and Optimization|Chad Russell|520|Thick|Tutorial|
|8594308655|The Relational Model for Database Management: Version 2|E.F.Codd|538|Thick|Popular science|

|Author|Author Nationality|
|---|---|
|Chad Russell|American|
|E.F.Codd|British|

## Data integrity

Per <https://www.talend.com/resources/what-is-data-integrity/> :

Physical integrity is the protection of the wholeness and accuracy of that data as it’s stored and retrieved. When natural disasters strike, power goes out, or hackers disrupt database functions, physical integrity is compromised. Human error, storage erosion, and a host of other issues can also make it impossible for data processing managers, system programmers, applications programmers, and internal auditors to obtain accurate data.

Logical integrity keeps data unchanged as it’s used in different ways in a relational database. Logical integrity protects data from human error and hackers as well, but in a much different way than physical integrity does. There are four types of logical integrity:

- Entity integrity relies on the creation of primary keys — the unique values that identify pieces of data — to ensure that data isn’t listed more than once and that no field in a table is null.
- Referential integrity refers to the series of processes that make sure data is stored and used uniformly. Rules embedded into the database’s structure about how foreign keys are used ensure that only appropriate changes, additions, or deletions of data occur.
- Domain integrity is the collection of processes that ensure the accuracy of each piece of data in a domain. In this context, a domain is a set of acceptable values that a column is allowed to contain i.e. phone numbers, email addresses...
- User-defined integrity involves the rules and constraints created by the user to fit their particular needs. Sometimes entity, referential, and domain integrity aren’t enough to safeguard data. Often, specific business rules must be taken into account and incorporated into data integrity measures.

## Data backup strategy

Have your data in 3 copies:

- Original data
- Backup on an external hard drive
- Off site backup
