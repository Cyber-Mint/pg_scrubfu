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
| 47 | Adalind | O'Hare| 19 | +23(24) 555-8756 | ####.####@####.##.## |
etc...

## Script-Tags
*pg_Scrubfu* script-tags should appear at the beginning of the column comment field and be enclosed in an opening and closing ~.  Scrubfu scripts may contain escaped "\" characters if required.  Scrubfu script tags may be abbreviated to be the first two characters of the script required, for example: ~REPLACE could be abbreviated as ~RE. The script parameters follow the script-tag after a ":".  Field types are maintained or the scrubfu script is not executed.  Scrubfu scripts treat the data obfuscation as if operating on TEXT but data types are honored e.g. if the script resulted in a series of numbers NNNNN but the field type was text rather than numeric then "NNNNN" would be used. It is possible to have multiple scrubfu scripts per comment field, and they will be executed left to right iteratively.

Valid tags would be of these types:

| Script-Tag | Description | Example Script |
| ----- | ----- | ----- |
| ``~``MASK:``~`` | Masks the field | ``~``MA:3,2;#;'@','.'``~`` |
| ``~``REPLACE:``~`` | Replaces non-iteratively using a set of find and replace tuples |  ``~``RE:address,addr;'zone','co.uk' ``~`` |
| ``~``RANDOM:``~`` | Returns random data | ``~``RA:A3N2``~`` |
| ``~``LIST:``~`` | Returns data from a supplied list | ``~``LI:firstname.txt``~`` |
| ``~``DROP:``~`` | Returns no/empty data or completely drops the column | ``~``DR:``~`` |

 
### MASK script
 > ```~MASK: start, end, mask character, 'ignored','characters',<>,<>~```

**Usage:**
 - The MASK script starts at the **start** position in the field, and ends **end** characters from the end of the field.
 - The **mask character** is the applied mask for each character in the field.
 - The **'ignored','characters'** are a comma separated string of quoted characters which will be ignored during the masking. 

**Example:** Mask an email address by leaving two characters on each end, while masking the rest of the email address with # but ignoring '@' and '.' characters.
<pre>
~MA:3,2,#,'@','.'~
email.address@domain.zone becomes ema##.#######@######.##ne
</pre>

### REPLACE script
> ```~RE:find,replace;<>,<>~```

**Usage:**
The REPLACE script will non-iteratively find and replace each of the tuples provided with the ``~``RE: tag.
The find & replace strings may be 'quoted' for clarity (optional) and escape `\,` characters may be used to include a comma or a single-quotes in the find/replace string. 

### RANDOM script
> ```~RA:<format>~```

**Usage:**
Random generates a random value of the given type and formats it according to the provided format.
Random types include:
 - N - Numeric
 - A - Capital alpha characters
 - a - Lowercase alpha characters

**Example:** 
The Random script below s an example of using Numeric's to create a valid but random telephone style number.
 
```
~RA:+NNN(NNN) NNN-NNNN~
This would for example yield +612(342) 555-9786
```


### LIST script
> ```~LI:list-name,truncation,SEQ|RND~```

**Usage:**
List selects from a provided list file called list-name (one entry per line), either sequentially (SEQ) or randomly (RND) and replaces the field with that entry truncated to the truncation length (for example 21).

**Example:** 

<pre>
~LI:firstnames.txt,20,RND~
the field value is changed to a random TRUNC(firstname,20) from the supplied firstnames.txt file.
</pre>

### Alias's
Alias's are added after the ":" delimiter instead of the script as follows ``~``MASK:EMAIL``~``
Where EMAIL would a pre-configured alias being EMAIL=2,#,@
Other alias's could conceivably be CARD=4,#
Alias's are kept in the *scrubfu.alias* file one per line.


## Referential Integrity Maintained
If the --ref-integrity command line parameter is set to "true" and a tagged field is referenced in a foreign_key then *scrubfu* follows the foreign_key back and replaces the matching foreign_key in the reference column with the *scrubfu* data by applyting the same script there.

## Errors
Errors are recorded into the default *scrubfu.log* if the *--log_level=* command line parameter is present.  Valid values are: info, error, debug.  The log file name may be changed using the *--log_file=* parameter.


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

### Tests
> Future feature


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

