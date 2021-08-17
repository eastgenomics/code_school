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

```bash
mysql -p -u kimy
```

```sql
SELECT * FROM table_name;
SELECT column FROM table_name WHERE id = 1;
SELECT * FROM table_name LIMIT 5;
SELECT DISTINCT name FROM table_name;
SELECT * FROM table_name ORDER BY column ASC/DESC;

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
```
