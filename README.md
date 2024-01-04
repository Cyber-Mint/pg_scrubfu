# pg_scrubfu Data Scrubbing & Obfuscation

## Introduction
Production data should never leave a production environment and yet developers need access to coherent data sets to properly develop and test.  

*pg_scrubfu* is a python3 script that makes creating usable development data from production data a predictable, audit-able and repeatable process. 

It is compatible with Postgres databases and utilizes the COMMENT's on columns to indicate the type of scrubbing & obfuscation required.  The script takes into account foreign-keys and performs obfuscations whilst retaining foreign-key constraint integrity.

The script works by importing the db_dump.sql result from pg_dump and generating db_scrubfu.sql ready for use with pg_import.

### Usage

```
Usage: pg_scrubfu [OPTIONS] [INFILE] [OUTFILE]

  pg_scrubfu v0.1.0, Copyright(c) 2020, Cyber-Mint (Pty) Ltd

     Distributed under the MIT license.

  pg_crubfu is a script that makes creating usable development data from
  production data a predictable, audit-able and repeatable process. The
  script works by scrubbing and /or obsfucating table column data based on
  script-tags in SQL comments stored in the postgres database.

  [INFILE] is the input file obtained by a pg_dump.

  [OUTFILE] is the scrubfu'ed file, ready to be imported with pg_import.

  For further details see: https://github.com/Cyber-Mint/pg_scrubfu

Options:
  -h, --help                      Show this message and exit.
  -v, --version                   Show the version and exit.
  --log TEXT                      Optional LOGFILE, defaults to standard out.
  --log_level [error|info|debug]  Used with [--log=LOGFILE].
  --ref_fk                        Flag: also scrubfu related foreign key data.
```

## Approach
When a DB administrator or developer designs or updates a database schema, they have the opportunity to consciously go through each column in each table and determine if that column contains some sensitive or confidential data such as personally identifiable information or cardholder data etc.

They may then add a *scrubfu script-tag* at the beginning of the comment field associated with each column.

For example:

```
 CREATE TABLE _secret.person (
    id integer NOT NULL,
    first_name text,                -- ~LIST:firstnames.txt, 20, SEQ~
    surname text,                   -- ~LI:surnames.txt, 30, RND~
    age int,                        -- we won't scrubfu this field
    mobile_number text,             -- ~RA:+NNN(NNN) NNN-NNNN~ 
    email text,                     -- ~MA:3,2,#,'@','.'~ The secret person's email address
    description                     -- ~DROP:~ Description of the record
);
```

or the equivalent SQL convention of comments made be used when round tripping is required:

```
COMMENT ON COLUMN _secret.person.first_name IS '~LIST:firstnames.txt, 20, SEQ~';
```

This may result in data of the form:

| id | first_name | surname | age* | mobile_number | email |
| ----- |:------------- |:------------- | ---- | --------------- | ----------------------------- |
| 45 | Adalie | Gadzinksi | 22 | +256(012) 555-8789 | #####@####.##.### |
| 46 | Adalina | Zanders | 35 | +001(211) 555-1526 | ##@#####.#### |
| 47 | Adalind | O'Hare| 19 | +235(240) 555-8756 | ####.####@####.##.## |
etc...

## Script-Tags
*pg_Scrubfu* script-tags should appear at the beginning of the column comment field and be enclosed in an opening and closing ~.  Scrubfu scripts may contain escaped "\" characters if required.  Scrubfu script tags may be abbreviated to be the first two characters of the script required, for example: ~REPLACE could be abbreviated as ~RE. The script parameters follow the script-tag after a colon (:). Scrubfu scripts treat the data obfuscation as if operating on TEXT but data types are honored e.g. if the script resulted in a series of numbers NNNNN but the field type was text rather than numeric then "NNNNN" would be used. It is possible to have multiple scrubfu scripts per comment field, and they will be executed left to right iteratively.

Valid tags would be of these types:

| Script-Tag | Description | Example Script |
| ----- | ----- | ----- |
| ``~``MASK:``~`` | Masks the field | ``~``MA:3,2;#;'@','.'``~`` |
| ``~``REPLACE:``~`` | Replaces non-iteratively using a set of find and replace tuples |  ``~``RE:address,addr;'zone','co.uk' ``~`` |
| ``~``RANDOM:``~`` | Returns random data for N,A,a | ``~``RA:AANa``~`` |
| ``~``LIST:``~`` | Returns data from a supplied list | ``~``LI:firstname.txt``~`` |
| ``~``DROP:``~`` | Returns no/empty data or completely drops the column | ``~``DR:``~`` |

## Implementation
*pg_scrubfu* is implemented using Python3 as a command line application and may easily be run in a docker container as part of any build pipeline.

### Usage
An example usage of *pg_scrubfu* maybe:

```bash
PG_PASSWORD=postgres pg_dump --dbname=<prod_db> -w -u postgres --host=127.0.0.1 --port=5432 --file=pg_dump.sql
pg_scrubfu pg_dump.sql scrubfu_db.sql  --ref-fk --log-level=info -log=-
pg_import -C -d postgres scrubfu_db.sql
```

### Docker
This will build the latest version from source and run a pre-configured demo using the supplied docker-compose.yml file.

```bash
cd ./docker
docker build -t pg_scrubfu:latest .
# docker pull cyber-mint/pg_scrubfu
docker-compose up
docker ps -a
```

### Python3 Environment Tips
```
python3 -m venv pg_scrubfu
source pg_scrubfu/bin/activate
pip3 install --editable .

pg_scrubfu -h

deactivate
```

## Project Documentation

All project documentation is currently available within the /doc folder.

- [User Guide](doc/user-guide.md)
- [Contributing to pg_scrubfu](doc/contributing.md) 
- [Contribution Workflow](doc/contribution-workflow.md) 
- [Coding Style Guide](doc/coding-style.md) 
- [Roadmap](doc/roadmap.md)
- [Copyright & Licenses](doc/copyright.md)

---
&copy; Copyright 2020, Cyber-Mint (Pty) Ltd, and distributed under the MIT License.

