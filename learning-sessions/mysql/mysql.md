# SQL

## Structured Query Language

It's a programming language designed to manipulate databases.

There are different databases managers the most known ones being:

- MySQL
- SQLite
- MariaDB

## Commands

```sql
# database level operations
CREATE DATABASE database_name;
SHOW DATABASES;
USE database_name;
SHOW TABLES;
DROP DATABASE database_name;

# user level operations
CREATE USER username IDENTIFIED BY password;
GRANT ALL ON table_name . column TO "user"@"host";
DROP USER "user"@"host";
```

```sql
mysql> create user panel_ro identified by "panelreadonly";
Query OK, 0 rows affected (0.04 sec)

mysql> grant select on panel_database . * to "panel_ro"
    -> @"localhost";
Query OK, 0 rows affected (0.02 sec)

mysql> show grants for panel_ro;
+--------------------------------------+
| Grants for panel_ro@%                |
+--------------------------------------+
| GRANT USAGE ON *.* TO `panel_ro`@`%` |
+--------------------------------------+
1 row in set (0.00 sec)

mysql -ppanelreadonly -u panel_ro

mysql> insert into reference values (test_ref);
ERROR 1142 (42000): INSERT command denied to user 'panel_ro'@'localhost' for table 'reference'
```

```sql
SELECT * FROM table_name;
SELECT column FROM table_name WHERE id = 1;
SELECT * FROM table_name LIMIT 5;
SELECT DISTINCT name FROM table_name;
SELECT * FROM table_name ORDER BY column ASC/DESC;

CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
    ....
);
INSERT INTO table_name VALUES (value1, value2, value3);
UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;

DROP TABLE table_name;
ALTER TABLE table_name DROP COLUMN column_name;
```

## Keys

Keys are special columns in databases. They add constraints on that column.

2 types of keys in databases:

- Primary keys
- Foreign keys

Primary keys are columns used to uniquely identify every row.

Foreign keys are columns used to reference other tables using their primary keys. This allows linking of tables together:

```sql
mysql> describe genes2transcripts;
+---------------------+------------+------+-----+---------+----------------+
| Field               | Type       | Null | Key | Default | Extra          |
+---------------------+------------+------+-----+---------+----------------+
| id                  | int        | NO   | PRI | NULL    | auto_increment |
| clinical_transcript | tinyint(1) | NO   |     | NULL    |                |
| date                | date       | NO   |     | NULL    |                |
| gene_id             | int        | NO   | MUL | NULL    |                |
| reference_id        | int        | NO   | MUL | NULL    |                |
| transcript_id       | int        | NO   | MUL | NULL    |                |
+---------------------+------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)

mysql> select * from genes2transcripts limit 5;
+----+---------------------+------------+---------+--------------+---------------+
| id | clinical_transcript | date       | gene_id | reference_id | transcript_id |
+----+---------------------+------------+---------+--------------+---------------+
|  1 |                   1 | 2021-05-18 |       1 |            1 |             1 |
|  2 |                   1 | 2021-05-18 |       2 |            1 |             2 |
|  3 |                   0 | 2021-05-18 |       2 |            1 |             3 |
|  4 |                   0 | 2021-05-18 |       2 |            1 |             4 |
|  5 |                   1 | 2021-05-18 |       3 |            1 |             5 |
+----+---------------------+------------+---------+--------------+---------------+
5 rows in set (0.00 sec)

mysql> select * from gene where id=2;
+----+------------+
| id | hgnc_id    |
+----+------------+
|  2 | HGNC:22140 |
+----+------------+
1 row in set (0.01 sec)
```

Creating primary keys and foreign keys create constraints. For example, deleting a gene in the database above would send an error message saying that the row references a foreign key.

To delete the gene row, you would first deleting the reference or beforehand, allow the foreign key to be NULL.

## Join

Joins are used to link tables together. There are 4 types of joins:

- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- OUTER/CROSS JOIN

![MySQL joins](UI25E.jpg)

```sql
mysql> SELECT gene.hgnc_id, hgnc_current.approved_symbol FROM gene INNER JOIN hgnc_current ON gene.hgnc_id = hgnc_current.hgnc_id LIMIT 5;
+------------+-----------------+
| hgnc_id    | approved_symbol |
+------------+-----------------+
| HGNC:3680  | FGF23           |
| HGNC:22140 | FAM20C          |
| HGNC:8918  | PHEX            |
| HGNC:3356  | ENPP1           |
| HGNC:11019 | SLC34A1         |
+------------+-----------------+
5 rows in set (0.01 sec)

mysql> SELECT hgnc_current.hgnc_id, hgnc_current.approved_symbol, gene.id FROM hgnc_current LEFT JOIN gene ON gene.hgnc_id = hgnc_current.hgnc_id limit 10;
+------------+-----------------+------+
| hgnc_id    | approved_symbol | id   |
+------------+-----------------+------+
| HGNC:1     | A12M1           | NULL |
| HGNC:10    | A2MRAP          | NULL |
| HGNC:100   | ASIC1           | NULL |
| HGNC:1000  | BCL5            | NULL |
| HGNC:10000 | RGS4            | NULL |
| HGNC:10001 | RGS5            | NULL |
| HGNC:10002 | RGS6            | NULL |
| HGNC:10003 | RGS7            | NULL |
| HGNC:10004 | RGS9            | 2745 |
| HGNC:10005 | RH              | NULL |
+------------+-----------------+------+
10 rows in set (0.00 sec)

mysql> SELECT hgnc_current.hgnc_id, hgnc_current.approved_symbol, gene.id FROM hgnc_current LEFT JOIN gene ON gene.hgnc_id = hgnc_current.hgnc_id WHERE gene.id IS NULL LIMIT 10;
+------------+-----------------+------+
| hgnc_id    | approved_symbol | id   |
+------------+-----------------+------+
| HGNC:1     | A12M1           | NULL |
| HGNC:10    | A2MRAP          | NULL |
| HGNC:100   | ASIC1           | NULL |
| HGNC:1000  | BCL5            | NULL |
| HGNC:10000 | RGS4            | NULL |
| HGNC:10001 | RGS5            | NULL |
| HGNC:10002 | RGS6            | NULL |
| HGNC:10003 | RGS7            | NULL |
| HGNC:10005 | RH              | NULL |
| HGNC:10007 | RHBDL1          | NULL |
+------------+-----------------+------+
10 rows in set (0.01 sec)
```

## Indexes

Indexes are a data structure improving speed of operations. You can use one or more columns when creating indexes and you should consider which columns are going to be used most when doing operations.

Indexes are also invisible from the user.

```sql
CREATE UNIQUE INDEX index_name ON table_name ( column1, column2,...);

mysql> show index from clinical_indication;
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table               | Non_unique | Key_name                       | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| clinical_indication |          0 | PRIMARY                        |            1 | id          | A         |         271 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
| clinical_indication |          1 | clinical_in_name_d871dc_idx    |            1 | name        | A         |         266 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
| clinical_indication |          1 | clinical_in_gemini__a1b42a_idx |            1 | gemini_name | A         |         271 |     NULL |   NULL |      | BTREE      |         |               | YES     | NULL       |
+---------------------+------------+--------------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
3 rows in set (0.03 sec)

```
