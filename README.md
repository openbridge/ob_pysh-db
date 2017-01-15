# `pysh-db` Docker Image
The `pysh-db` image is intended to jump start someone's efforts in using Python (or Bash) with a pre-configured image containing the needed software packages pre-installed.

# Contents
- [Why `pysh-db`?](#why-pysh-db)
- [What is Included in `pysh-db`?](#what-is-included-in-pysh-db)
	- [Python](#python)
	- [Alpine (OS)](#alpine-os)
- [Requirements](#requirements)
	- [What is Docker?](#what-is-docker)
	- [Install Docker](#install-docker)
	- [Data and Work File Persistence](#data-and-work-file-persistence)
		- [Example: Mounting Host Volume](#example-mounting-host-volume)
	- [Creating Your Own Custom Image](#creating-your-own-custom-image)
- [Getting Setup](#getting-setup)
	- [Step 1: Building an image](#step-1-building-an-image)
	- [Step2: Running The Container](#step2-running-the-container)
	- [Step 3: Getting Your Local Database setup](#step-3-getting-your-local-database-setup)
		- [Postgres and Amazon Aurora (Postgres)](#postgres-and-amazon-aurora-postgres)
		- [MySQL, MariaDB and Amazon Aurora (MySQL)](#mysql-mariadb-and-amazon-aurora-mysql)
			- [Amazon Aurora](#amazon-aurora)
- [Connecting to Postgres, Amazon Auroa or Redshift](#connecting-to-postgres-amazon-auroa-or-redshift)
	- [Connecting With `psql`](#connecting-with-psql)
		- [Example: Listing Schema Tables And Objects](#example-listing-schema-tables-and-objects)
	- [Running Queries Via `psql`](#running-queries-via-psql)
		- [Standard Input Via `-c`](#standard-input-via-c)
		- [File Input Via `-f`](#file-input-via-f)
- [Connecting to MySQL, MariaDB or Amazon Aurora](#connecting-to-mysql-mariadb-or-amazon-aurora)
	- [Connecting With `mysql`](#connecting-with-mysql)
	- [Running Queries Via `mysql`](#running-queries-via-mysql)
- [Exporting Data From Your Database](#exporting-data-from-your-database)
	- [Export CSV from Redshift via `UNLOAD` and `psql`](#export-csv-from-redshift-via-unload-and-psql)
	- [Export Without Using `UNLOAD` command](#export-without-using-unload-command)
- [Connecting Python To Your Database](#connecting-python-to-your-database)
	- [Example: Basic `psycopg2` Usage](#example-basic-psycopg2-usage)
- [Issues](#issues)
- [Contributing](#contributing)
- [References](#references)

# Why `pysh-db`?
This can be valuable for individuals or teams who do not have the time or interest setup up their own development environments. Also, they may have limitations around what they can or cannot install on their corporate laptop. It can be tricky to get all the software packages installed and compiled. Leveraging a Docker image that does that for them can help increase velocity by allowing them time to focus on working with data, not system administration activities.

# What is Included in `pysh-db`?

There are a few Python and OS related items that are pre-installed for convenience

## Python

Sometimes you need helper "packages" and "libraries" to perform various operations. In Python, the typical (simplest) approach is to a Python package manager called `pip`. The image comes with the following packages pre-installed:

- setuptools
- cffi
- psycopg2
- cryptography
- numpy
- matplotlib
- pandas
- python
- dateutil
- sqlalchemy
- mysql-connector
- pytz
- six
- wsgiref
- awscli
- boto
- scipy

Why include these? The two primary reasons for including these packages are;

1. they are commonly used in data science circles so there is an expectation they would be part of a default.
2. they are referenced by [AWS](http://docs.aws.amazon.com/redshift/latest/dg/udf-python-language-support.html) for use in creating User Defined Functions (UDF). However, the versions AWS listed are MUCH older versions than what is installed in this container.

To install the Postgres library for Python we run the `pip install psycopg2 .... -U` command as part of the image build. The `-U` tells pip to upgrade it if it is already installed.

## Alpine (OS)

The included image uses Alpine Linux as the base container OS. This images leverages `alpine:edge` which is the latest release available. In addition to the Python packages, the Alpine `postgres-client` and `mariadb-client` libraries are installed. Without `postgres-client` installed the `psycopg2` package would not work. It also provides the ability to use the Postgres or MySQL command line tools `psql` and `mysql`. More examples on this later.

Here are the install OS packages:

- postgresql-client
- mariadb-client # MySQL
- python
- bash
- curl
- less
- groff
- jq
- py-numpy
- freetype
- libpng

# Requirements

## What is Docker?

This container is used for virtualizing your Python and Postgres development or work environment using Docker. If you don't know what Docker is read "[What is Docker?](https://www.docker.com/what-docker)".

## Install Docker

Once you have a sense of what Docker is, you can then install the software. It is free: "[Get Docker](https://www.docker.com/products/docker)". Select the Docker package that aligns with your environment (ie. OS X, Linux or Windows). If you have not used Docker before, take a look at the guides:

- [Engine: Get Started](* https://docs.docker.com/engine/getstarted/)
- [Docker Mac](https://docs.docker.com/docker-for-mac/)
- [Docker Windows](https://docs.docker.com/docker-for-windows/)

If you already have a Linux instance running as a host or VM, you can install Docker command line. For example, on CentOS you would run `yum install docker -y` and then start the Docker service.

At this point, you should have Docker installed. Now you can get your Python and Postgres services up and running

## Data and Work File Persistence

You may have noticed that once you stop the container, if you previously wrote some data on the DB or some Python script, that data is lost. This is because by default Docker containers are not persistent. We can resolve this problem using a data container. Read about how to persist data: <https://docs.docker.com/engine/tutorials/dockervolumes/>

### Example: Mounting Host Volume

Here is a quick example of mounting a host drive/directory via `VOLUMES`. Note the use of the `-v` command below. This signifies the host volume to be mounted.

In this example, your python app files are located locally at `/src/app`. So you want to make that available to your container. You end up mounting this to `/app` inside the container. This makes available your Python (or anything else) located in `/src/app` to the container.

Let's assume you have a `query.py` script you have worked on. The path to that file on the host would be `/src/app/query.py`. By mounting `/src/app` to `/app`, this will make available `query.py` within the container with a path of `/src/app/query.py`. To run `query.py` the docker command would look like:

```bash
docker run -it -v /src/app:/app openbridge/pysh-db python /app/query.py
```

Per Docker:

_The -v command mounts the host directory, /src/app, into the container at /app. If the path /app already exists inside the container's image, the /src/app mount overlays but does not remove the pre-existing content. Once the mount is removed, the content is accessible again. This is consistent with the expected behavior of the mount command._

## Creating Your Own Custom Image

To persist configurations different than what is in the current Dockerfile, it is best to create your own "docker image". This is done via a custom [Dockerfile](https://docs.docker.com/engine/reference/builder/). You can use this Dockerfile to create a custom image for dev purposes. What you name your image is up to you.

```
docker build -t python-dbdev .
```

Or

```
docker build -t python-my-db-tools .
```

Feel free to modify the Dockerfile as deemed appropriate. You can add and subtract default packages to fit your use case. There are a large number of choices available relating to versions and operating systems. You can see a complete list here: <https://hub.docker.com/_/python/>

# Getting Setup

Once you have Docker running, you can build a Python image and run the container..

## Step 1: Building an image

If you want to build the image from scratch using the Dockefile, the first step is to grab the Dockerfile locally. Then you can execute the build command:

```bash
docker build -t openbridge/pysh-db .
```

Due to the Python packages, the build can take awhile. Pandas, Numpy and Scipy take considerable time to build. When you run the `docker build` command, feel free to grab a cup of coffee.

## Step2: Running The Container

Once you have completed building your image, you can run through some basic checks to make sure it is working as expected. For example, you can test if you can start the bash cli:

```bash
docker run -it openbridge/pysh-db bash
```

Will result in putting you inside the container at the command prompt like this:

```bash
foo@442343470ad0:/#
```

You certainly do not need to enter into the container like that. You can easily run Python "outside" the container. For example, you can run a simple test to have the container echo the current Python version

```bash
docker run -it openbridge/pysh-db python -V
```

Will result in:

```bash
Python 2.7.13
```

Not only does this image have Python, it also has the Postgres libraries. For example, you can run PSQL directly at the prompt:

```bash
docker run -it openbridge/pysh-db psql -V
```

Which will return

```bash
psql (PostgreSQL) 9.5.4
```

You can do the same with the `mysql` client:

```bash
docker run -it openbridge/pysh-db mysql -V
```

Which will return

```bash
mysql Ver 15.1 Distrib 10.1.20-MariaDB, for Linux (x86_64) using readline 5.1
```

Congratulations, you have a working container.

## Step 3: Getting Your Local Database setup
If you havea remote database you will be using, then this section will not be relevant. However, if you want to test or build locally and need a working database, then this will help you get started.

### Postgres and Amazon Aurora (Postgres)

The easiest path is simply to grab the official Postgres image is from Docker hub. Take a look at the options: <https://hub.docker.com/_/postgres/>. To get the image, you can run `docker pull postgres`. This will pull the image locally and allow you to run a local Postgres DB.

You can also create your own custom image if needed. There are some good articles/how-to-guides to follow [here](https://github.com/docker-library/docs/tree/master/postgres) and [here](https://docs.docker.com/engine/examples/postgresql_service/)

### MySQL, MariaDB and Amazon Aurora (MySQL)

Due to the various flavors of MySQL, you have a few choices; MySQL or MariaDB. The best course of action is to align with whatever exists elsewhere in your organization to ensure the broadest capability and reduce any frustrations relating to versioning issues.

- [Getting Started: Docker MySQL](https://hub.docker.com/_/mysql/)
- [Getting Started: Docker MariaDB](https://hub.docker.com/_/mariadb/)

Both links provide an overview on how to get your self up and running. To grab the latest image of either database, simply pull them locally:

- `docker pull mariadb`
- `docker pull mysql`

If you are interested in using MariaDB, this is a detailed guid on setting up a MariaDB environment: [Installing & Using MariaDB](https://mariadb.com/kb/en/mariadb/installing-and-using-mariadb-via-docker/)

Curious what the differences between the MySQL and MariaDB are? Read about it [here](https://mariadb.com/kb/en/mariadb/mariadb-vs-mysql-features/) and [here](http://www.admin-magazine.com/Articles/MariaDB-vs.-MySQL).

#### Amazon Aurora

There is no direct Amazon Aurora Docker container. However, Amazon states that:

_Amazon Aurora database engine is fully compatible with MySQL 5.6 using the InnoDB storage engine. This means the code, applications, drivers, and tools you already use with your MySQL databases can be used with Amazon Aurora with little or no change. This also allows for easy migration of existing MySQL databases using standard MySQL import and export tools or using MySQL binlog replication._

If you are using Amazon Aurora, make sure you are pulling the `5.6` Mysql image locally for development purposes. This will reduce any issues when you are ready to deploy your work and need to interact with Aurora.

To pull a version, specify it in your pull command: `docker pull mysql:5.6`

# Connecting to Postgres, Amazon Auroa or Redshift

The `openbridge/pysh-db` container comes with Python `psycopg2` and `postgres-client`. For connecting to a Postgres or Redshift with Python, the Psycopg2 package is needed. If you want some background on this package, go [here](https://wiki.postgresql.org/wiki/Psycopg2_Tutorial).

## Connecting With `psql`

`psql` is an interactive terminal for working with Postgres. If you want some more background on `psql` you can check [this guide]
(http://postgresguide.com/utilities/psql.html) or [the offical docs](https://www.postgresql.org/docs/current/static/app-psql.html).


Below are some example connections for Redshift using `psql`. It includes the remote host (`-h`), port (`-p`), username (`-U`) and database name (`-d`). You will be prompted for a password assuming your connection parameters are correct.

```bash
docker run -it openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase
```

Replace these values with those for your Redshift cluster.

### Example: Listing Schema Tables And Objects

You can list all tables in your current schema using just `\d`.

```bash
docker run -it openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase \d
```

Specify an additional name and `psql` will tell you details about that named object.

```bash
docker run -it openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase \d mytablename
```

## Running Queries Via `psql`

### Standard Input Via `-c`

```bash
docker run -it openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase -c 'SELECT * FROM mytable'
```

### File Input Via `-f`

Instead of passing the query via `-c` you can also leverage an external file that contains the query you want to execute:

```bash
docker run -it openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase -q -f dump.sql
```

Uisng `-f` reads commands from a file rather than standard input.

# Connecting to MySQL, MariaDB or Amazon Aurora

## Connecting With `mysql`

`mysql` is a _simple SQL shell with input line editing capabilities. It supports interactive and noninteractive use._

Using `mysql` is similar to using to `psql`. To see all the available options for `mysql`, simply run:

```bash
docker run -it openbridge/pysh-db mysql --help
```

Here is a sample connection statement:

```bash
docker run -it openbridge/pysh-db mysql -h 127.0.0.1 -u mysql -D mydatabase -P 3306
```

This will show you all the tables in the specified database

```bash
docker run -it openbridge/pysh-db mysql -h 127.0.0.1 -u mysql -D mydatabase -P 3306 -e "show tables;"
```

## Running Queries Via `mysql`

Use can run `mysql` command to execute local sql file:

```bash
docker run -it openbridge/pysh-db mysql -h 127.0.0.1 -u mysql < "./sql/myqueries.sql"
```

Here is an example command passing the set of commands via `-e`:

```bash
mysql -h 127.0.0.1 -u mysql -e "use mydatabase; INSERT IGNORE INTO users (id, userid, passwd, subscriptionid, uid, gid, homedir, status, shell, count, accessed, modified) VALUES ('', 'bob', '1231232131lkdjadjalj', 'trial', '999', '999', '/home', 'active', '/sbin/nologin', 0, 'NOW()', 'NOW()');"
```

or

```bash
docker run -it openbridge/pysh-db mysql -h 127.0.0.1 -u mysql -e "./sql/myqueries.sql"
```

# Exporting Data From Your Database
There may be times that you want to export data from a database. There are a few methods to accomplish this and we will only cover a few possibilities.

## Export CSV from Redshift via `UNLOAD` and `psql`

We will assume you have a table called `customers` and you want to export it

```sql
    "id" integer NOT NULL,
    "name" varchar(50),
    "email" varchar(50),
    "city" varchar(50) DEFAULT NULL,
    "state" char(2) DEFAULT NULL,
    "created_at" date DEFAULT NULL,
```

Please note that exports from Redshift require a output location on Amazon S3 and that you have the proper permissions to that location.

You will want to connect to your database with your AWS credentials:

```bash
 docker run -it -e AWS_ACCESS_KEY_ID=XXXX -e AWS_SECRET_ACCESS_KEY=XXX openbridge/pysh-db psql -h *****.us-east-1.redshift.amazonaws.com -p 5439 -U username -d mydatabase
```

You will notice the that `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are part of the run command. These reflect the key and secret required for Amazon to store the output from Redshift to a S3 bucket.

At the `psql` command prompt you will want to provide your `UNLOAD` command:

```
UNLOAD ('
  SELECT id, name, email, city, state, created_at  FROM (
    SELECT 1 as ordinal, \'id\' as id, \'name\' as name, \'email\' as email, \'city\' as city, \'state\' as state, \'created_at\' as created_at
    UNION all
    ( SELECT 2 as ordinal, CAST(id as varchar(255)) as id, name, email, city, state, CAST(created_at as varchar(255)) as created_at
    FROM customers )
  ) t ORDER BY ordinal
  TO 's3://mybucket/crm/customer_'
  CREDENTIALS 'aws_access_key_id=X; aws_secret_access_key=X'
  MANIFEST
  ESCAPE
  ADDQUOTES
  DELIMITER ','
  GZIP
  ALLOWOVERWRITE
  ESCAPE
  NULL AS '\\N';
```

The will create an export of files that are stored to S3. Based on the size of the export, it was broken into 3 parts as shown in the manifest file:

```json
{
  "entries": [
    {"url":"s3://mybucket/crm/customer_0000_part_00"},
    {"url":"s3://mybucket/crm/customer_0001_part_00"},
    {"url":"s3://mybucket/crm/customer_0002_part_00"}
  ]
}
```
Each of the files `customer_0000_part_00`, `customer_0001_part_00` and `customer_0002_part_00` reflect the `UNLOAD` command and underlying query used.

If you want to pull those remote S3 files to your local compute, you can use the included `awscli` tools.
```bash
aws s3 cp s3://mybucket/crm /my/local/folder --recursive
```

Notes:

1. UNLOAD by default creates encrypted files using Amazon S3 server-side encryption with AWS-managed encryption keys (SSE) 2.The S3 bucket specified in the command should be in the same region as your cluster. If they are in different regions, you will most likely see an error
2. Rather than specify key-based access control by providing the access key ID and the secret access key, you can also use AWS IAM roles: `CREDENTIALS 'aws_iam_role=arn:aws:iam::<account-id>:role/<role-name>'`


## Export Without Using `UNLOAD` command

A Redshift (only) example

```bash
 docker run -it openbridge/pysh-db psql psql -h *****.eu-west-1.redshift.amazonaws.com -p 5439 -U test -d test -F, -A -c 'select * from  mytable' > mytable.csv
```

A Postgres (only) example:

```bash
 docker run -it openbridge/pysh-db psql -U username -d mydatabase -c "Copy (Select * From mytablename LIMIT 10) To STDOUT With CSV HEADER DELIMITER ',';" > /path/to/store/mytablename.csv
```

# Connecting Python To Your Database

There are hundreds, if not thousands, of articles and guides on how to use Python with databases. Here are a few to get your started:

- [Using psycopg2 with PostgreSQL](https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL)
- [SQLAlchemy quick start with PostgreSQL](https://suhas.org/sqlalchemy-tutorial)
- [How to Execute Raw SQL in SQLAlchemy](https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/)
- [Access PostgreSQL from Python using pscopg2](http://support.datascientistworkbench.com/knowledgebase/articles/835206-access-postgresql-from-python-using-pscopg2)

## Example: Basic `psycopg2` Usage

Here is a basic Postgres connection in Python using `psycopg2`: `

```python
import psycopg2
conn = psycopg2.connect(
    host="datawarehouse.cm4z2iunjfsc.us-west-2.redshift.amazonaws.com",
    user=redshift_user,
    port=port,
    password=redshift_pass,
    dbname=dbname)
cur = conn.cursor()
cursor.execute('select * from customer WHERE purchases < 70000')
for query in cursor:
    print str(query)
```

# Issues

If you have any problems with or questions about this image, please contact us through a GitHub issue.

# Contributing

You are invited to contribute new features, fixes, or updates, large or small; we are always thrilled to receive pull requests, and do our best to process them as fast as we can.

Before you start to code, we recommend discussing your plans through a GitHub issue, especially for more ambitious contributions. This gives other contributors a chance to point you in the right direction, give you feedback on your design, and help you find out if someone else is working on the same thing.

# References

- [10 minutes to Pandas](http://pandas.pydata.org/pandas-docs/stable/10min.html#min)
- [Itroduction to Pandas](http://pandas.pydata.org/pandas-docs/stable/index.html)
- [NumPy Basics](https://docs.scipy.org/doc/numpy-dev/user/quickstart.html)
- [EdX: Introduction to Python for Data Science](https://www.edx.org/course/introduction-python-data-science-microsoft-dat208x-4)
- [Datacamp: Intro to Python for Data Science](https://www.datacamp.com/courses/intro-to-python-for-data-science)
