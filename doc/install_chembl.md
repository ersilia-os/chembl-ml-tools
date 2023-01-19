# Instructions to install the ChEMBL database in a local computer

These instructions are valid for Ubuntu Linux.

1. Install postgres.
```
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib
$ sudo apt install postgresql-client
```

2. Start service.

(Note: you will have to run this again if you restart your computer, or alternatively have it run automatically on startup)
```
$ sudo service postgresql start
```

The user "postgres" is created automatically and is the DB administrator. To do any configuration, you need to run as user postgres (sudo -u postgres).

3. Create a database user for our own Linux user, [your_userid], who will be a DB superuser.

```
$ sudo -u postgres createuser --interactive
Enter name of role to add: [your_userid]
Shall the new role be a superuser? (y/n) y
$ sudo -u postgres createdb [your_userid]
```

4. Create database for ChEMBL (make sure to include the semicolon)
```
$ sudo -u postgres psql
postgres=# create database chembl_31;
postgres=# \q
```

5. Download the ChEMBL data in postgres format
From this site: https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/
Download the file: `chembl_31_postgresql.tar.gz`

6. Load database contents using the downloaded file. This takes some time.
```
$ sudo -u postgres pg_restore --no-owner -U postgres -d chembl_31 chembl_31_postgresql.dmp
```

7. Test: Enter the database for querying. Run a test query. You should get the list of assay types.
```
$ psql chembl_31
chembl_31=# select * from assay_type;
chembl_31=# \q
```

So far the database is installed and it works with your own user. For security, we prefer to create a specific DB user, called "chembl_user", 
to use in our programs. The password for this DB user will be "aaa" (this is hard-coded in the data extraction program).

8. Create a specific user for querying this database
```
$ sudo -u postgres createuser --interactive -P
Enter name of role to add: chembl_user
Enter password for new role: aaa
Enter it again: aaa
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

9. Grant access to the chembl_31 tables to user chembl_user
```
$ sudo -u postgres psql chembl_31
chembl_31=# GRANT SELECT ON ALL TABLES IN SCHEMA public TO chembl_user;
```

10. Test: Connect to database as user chembl_user
```
$ psql -h localhost -p 5432 -U chembl_user chembl_31
Password for user chembl_user: (use the password you created before)
psql (12.13 (Ubuntu 12.13-0ubuntu0.20.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.
chembl_31=# select * from assay_type;
chembl_31=> \q
```

**DONE!**

