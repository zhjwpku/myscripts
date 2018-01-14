#!/bin/bash

MYSQL_USERNAME=root
MYSQL_PASSWORD=rootpassword
MYSQL_HOST=10.0.63.6
MYSQL_CONN="-h${MYSQL_HOST} -u${MYSQL_USERNAME} -p${MYSQL_PASSWORD}"
EXCLUSIVE_DBS="'mysql', 'information_schema', 'performance_schema'"

#
# Collect all database names except for EXCLUSIVE_DBS
#

SQL="SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN (${EXCLUSIVE_DBS})"

DBLIST=""
for DB in `mysql ${MYSQL_CONN} -ANe"${SQL}"` ; do DBLIST="${DBLIST} ${DB}" ; done

# --triggers option is enabled by default
# --routines 选项会把所有的存储过程和存储函数dump到sql文件
# --single-transaction 保证在备份的过程中得到一致性的备份
MYSQLDUMP_OPTIONS="--routines --single-transaction"

mysqldump ${MYSQL_CONN} ${MYSQLDUMP_OPTIONS} --databases ${DBLIST} > all-dbs.sql
