# scrubfu User Guide

## Introduction

Production data should never leave a production environment and yet developers need access to coherent data sets to properly develop and test.  

*scrubfu* is a .NET CLI tool that makes creating usable development data from production data a predictable, audit-able and repeatable process. 

It is compatible with Postgres databases and utilizes the COMMENT's on table columns to indicate the type of scrubbing & obfuscation required.  

``` bash
Usage: scrubfu [OPTIONS] [INFILE] [OUTFILE]

  [INFILE] is the input file obtained by a pg_dump.
           This can also be standard out stream.

  [OUTFILE] is the scrubfu'ed file, ready to be imported with pg_import.
            This can also be the standard out stream.

Options:
  -h, --help                      Show this message and exit.
  -v, --version                   Show the version and exit.
  --log TEXT                      Optional LOGFILE, defaults to standard out.
  --log_level [error|info|debug]  Used with [--log=LOGFILE].
```

## Approach

When a DB administrator or developer designs or updates a database schema, they have the opportunity to consciously go through each column in each table and determine if that column contains some sensitive or confidential data such as personally identifiable information or cardholder data etc.

They may then add a *scrubfu tag* at the beginning of the comment field associated with each column.

**For example:**

```sql
 CREATE TABLE _secret.person (
    id integer NOT NULL,
    first_name text,                -- ~MA:4,0;*~
    surname text,                   -- ~FZ~
    age int,                        -- we won't scrubfu this field
    mobile_number text,             -- ~RA:+NNN(NNN) NNN-NNNN~ 
    email text,                     -- ~MA:3,2;#;@,.~ The secret person's email address
    description text,               -- we won't scrubfu this field
    city text,                      -- ~RE:Johannesburg,Tokyo;Cape Town,London;Durban,New York City;Pretoria,S�o Paulo;Bloemfontein,Sydney~
    residencies text[]              -- ~FZ[0]~
);
```

or the equivalent SQL convention of comments may be used when round tripping is required.

**For example:**

```sql
COMMENT ON COLUMN _secret.person.first_name IS '~MA:3,1;*~';

COMMENT ON COLUMN _secret.person.surname IS '~FZ~';

COMMENT ON COLUMN _secret.person.mobile_number IS '~RA:+NNN(NNN) NNN-NNNN~';

COMMENT ON COLUMN _secret.person.email IS '~MA:3,2;#;@,.~';

COMMENT ON COLUMN _secret.person.city IS '~RE:Johannesburg,Tokyo;Cape Town,London;Durban,New York City;Pretoria,S�o Paulo;Bloemfontein,Sydney~';

COMMENT ON COLUMN _secret.person.residencies IS '~FZ[0]~';
```

**This may result in data transformed as follows:**

Before:

| id | first_name | surname | age* | mobile_number | email | city | residencies |
| ----- |------------- |------------- | ---- | --------------- | ----------------------------- |  --------------- |  --------------- | 
| 45 | Adalie | Gadzinksi | 22 | +256(012) 555-8789 | adalie@gadzinksi.za.net | Johannesburg | '{"St, James Court","Waverly Village","Sandton Suites"}'
| 46 | Adalina | Zanders | 35 | +001(211) 555-1526 | az@domain.com | Pretoria | '{"Waverly Court","Mandela Square"}'
| 47 | Adalind | O'Hare| 19 | +23(24) 555-8756 | a.ohare@companyname.co.za | Cape Town |'{"Alexander Hill","V&A Apartments"}'

After:

| id | first_name | surname | age* | mobile_number | email | city | residencies |
| ----- | ------------- | ------------- | ---- | --------------- | ----------------------------- |  --------------- |  --------------- | 
| 45 | Ada**e | Rxbsyaqpk | 22 | +256(012) 555-8789 | ######@#########.##.### | Tokyo | '{"Pz. Mxuis Npewb","Waverly Village","Sandton Suites"}'
| 46 | Ada***a | Avfewzq | 35 | +001(211) 555-1526 | ##@#####.### | S�o Paulo | '{"Jtyicvbq Lsxze","Mandela Square"}'
| 47 | Ada***d | X'Cjal| 19 | +023(724) 555-8756 | #.#####@###########.##.## | London |'{"Giuttybxe Kbci","V&A Apartments"}'
| 48 | etc... | | | | | |

## Scrubfu Tags

Scrubfu tags are used to declaratively specifiy what scrubbing actions Scrubfu should take when it scrubs SQL text from a `pg_dump`.  

### Tag Syntax:

Every Scrubfu tag has an associated action, but may also include options that may be used to configure the behaviour of the Scrubfu action.

Scrubfu tags typically consist of three main sections, namely the **```action name```**, the **```field content location```** and the **```action options```**. 
The **```action name```** is required (for obvious reasons), but both the **```field content location```** and **```action options```** may be optional depending on the action type.

![Scrubfu-Tag Syntax Diagram](images/scrubfu-tag-syntax-diagram.jpg)

* The tag action must be specified before the first ":".  

* The tag action options must be specified after the first ":".  

* Scrubfu tags may contain escaped "\\" characters if required.  

* Scrubfu tags may be abbreviated to be the first two characters of the tag required, for example REPLACE could be abbreviated as RE. 

* Scrubfu treats the data obfuscation as if operating on TEXT, but data types are honored. For example, if the scrubfu action resulted in the series of numbers NNNNN, but the field type was text rather than numeric then "NNNNN" would be used. 

* Scrubfu tags should appear at the beginning of the column comment field and be enclosed in an opening and closing tilde (~).  

* It is possible to have multiple scrubfu scripts per comment field, and they will be executed left to right iteratively.

#### Valid Tags:

| Tag |  Abbreviation | Description | Example Declaration |
| ----- | ----- | ----- | ----- |
| MASK | MA |  Masks the field. | ``~MA:3,2;#;'@','.'~`` |
| REPLACE | RE | Replaces non-iteratively using a set of find and replace tuples. |  ``~RE:address,addr;'zone','co.uk'~`` |
| RANDOM | RA | Returns random data. | ``~RA:AAAANN~`` |
| FUZZ | FZ | Returns pseudo-random data. | ``~FZ~`` |

 
### MASK script
 > ```~MASK: start, end, mask character, 'ignored','characters',<>,<>~```

**Information:**
- The MASK script tag should have a minimum of 3 parameters, the first 2 parameters should be digits or numbers. After every parameter there should be a comma.

**Usage:**
 - The MASK script starts with a digit / number, which determines at what position the masking should start.
 - The **end** or second position (must be a digit / number) determines how many digits that are not masked from the back of the value.
 - The **mask character** is the applied mask for each character in the field.
 - The **'ignored','characters'** are a comma separated string of quoted characters which will be ignored during the masking.

![MASK2](https://github.com/Cyber-Mint/pg_scrubfu/assets/102973452/e57ce475-42d2-4d16-af66-abb6563d594d) 

**Example:** Mask an email address by leaving two characters on each end, while masking the rest of the email address with # but ignoring '@' and '.' characters.
<pre>
~MA:3,2,#,'@','.'~
email.address@domain.zone becomes ema##.#######@######.##ne
</pre>


### REPLACE script
> ```~RE:find,replace;<>,<>~```

**Information:**
- The REPLACE script tag should have a minimum of 2 parameters, the first parameter is what needs to be replaced, and the second parameter is the value that will replace the first. After every even parameter there should be a comma. Values have to be found and replaced in pairs, so the requirement is to have an even number of parameters, with a semi colon (;) after every even number.
  
**Usage:**
The REPLACE script will non-iteratively find and replace each of the tuples provided with the ``~``RE: tag.
The find & replace strings may be 'quoted' for clarity (optional).

![Replace](https://github.com/Cyber-Mint/pg_scrubfu/assets/102973452/ef04c0a7-9734-44cf-8131-4f6b60970df2)

**Example:** Replace 'com' with 'co.za' in a web address.
<pre>
~RE:'com','co.za'~
www.example.com becomes www.example.co.za
</pre>


### RANDOM script
> ```~RA:<format>~```

**Information:**
- The RANDOM script can only have 1 parameter.
  
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
List selects from a provided list file called list-name (one entry per line), either sequentially (SEQ) or randomly (RND) and replaces the field with that entry truncated to the truncation length (for example 20).

![List](https://github.com/Cyber-Mint/pg_scrubfu/assets/102973452/2c9b7364-74f2-4981-88f8-f6dda2b47a4b)

**Example:** 
<pre>
~LI:firstnames.txt,20,RND~
The field value is changed to a random TRUNC(firstname,20) from the supplied firstnames.txt file.
</pre>

### DROP script
> ```~DR~```

**Usage:**
Drop script drops the the column.

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

---
&copy; Copyright 2020, Cyber-Mint (Pty) Ltd, and distributed under the MIT License.

