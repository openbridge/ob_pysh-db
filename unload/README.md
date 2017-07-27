# Unload
This script is meant to simplify running a [Redshift UNLOAD command](http://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html). The script automatically retrieves and adds headers to the file before output.

## Configuration file
The script requires a configuration file named ``config.json`` in the same directory. It uses parameters set here to obtain database connection info, AWS credentials and any UNLOAD options you wish to use.

A sample configuration file is below.

```
{
    "db": {
        "host": "test.redshift.io",
        "port": "5439",
        "database": "db1",
        "user": "username",
        "password": "password"
    },
    "aws_access_key_id": "myawsaccesskeyid",
    "aws_secret_access_key": "myawssecretaccesskey",
    "unload_options": [
    	"ADDQUOTES",
    	"PARALLEL OFF",
    	"ALLOWOVERWRITE",
    	"GZIP",
    	"DELIMITER ','"
    ]
}
```

## Runtime parameters
* ``-t``: The table you wish to UNLOAD
* ``-f``: The S3 key at which the file will be placed
* ``-s`` (Optional): The file you wish to read a custom valid SQL WHERE clause from. This will be sanitized then inserted into the UNLOAD command. 
* ``-d`` (Optional): The date column you wish to use to constrain the results  
* ``-d1`` (Optional): The desired start date to constrain the result set
* ``-d2`` (Optional): The desired end date to constrain the result set  
Note:  ``-s`` and ``-d`` are mutually exlusive and cannot be used together. If neither is used, the script will default to not specifying a WHERE clause and output the entire table.

## Examples
This command will unload the data in the table ``mytable`` which the ``datecol`` is between to the specified S3 location.
```
python unload.py -t mytable -f s3://dest-bucket/foo/bar/output_file.csv -d datecol -d1 2017-01-01 -d2 2017-06-01
```

## Optional WHERE clause
As mentioned previously, it is possible to supply your own WHERE clause to be used in the UNLOAD command.

Note that this is the WHERE clause **only**. For example, to use this functionality to UNLOAD only new users, the SQL file will contain ``WHERE is_new = true``.

Note: It may be wise to create a read-only user on the database for the script to use. This will improve the security of the script by further protecting against SQL injection. For more information on how to do this, check the manual for your database type.

