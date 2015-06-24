# csvupdate
Script in python for update data from two files in format CSV.


With this script you can:

 - `Update the data row`
 - `Add new row`



# Help

    # python csvupdate.py
    Usage: example usage: csvupdate.py -p primary.csv -s secondary.csv -o output.csv [-k key] [-n] [-f arg1,arg2,arg3...] [-d ';']
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -p PRIMARY_FILE, --primary_file=PRIMARY_FILE
                            input: primary file
      -s SECONDARY_FILE, --secondary_file=SECONDARY_FILE
                            input: secondary file
      -o OUTPUT_FILE, --output=OUTPUT_FILE
                            output: file
      -k KEY, --key=KEY     puts key name, the default is the first data (first
                            column of primary input)
      -n, --no-add          do not add the secondary input data does not exist if
                            the primary input, by default data add
      -f OUTPUT_FIELDS, --output-fields=OUTPUT_FIELDS
                            format output fields
      -d DELIMITER, --delimiter=DELIMITER
                            delimiter



# Examples:
Basic, In this example you can obtain all data from 2 files: output.csv

    python ./csvupdate.py -p primary.csv -s secondary.csv -o output.csv

Select Fields, "-f": output_fields.csv
    
    python ./csvupdate.py -p primary.csv -s secondary.csv -o output_fields.csv -f first_name,last_name,email
    
No add new row, but updating data, "-n": output_fields.csv
    
    python ./csvupdate.py -p primary_example_no_add.csv -s secondary_example_no_add.csv -o output_no_add.csv -n
    
Key, "-k": output_key.csv
    
    python ./csvupdate.py -p primary_example_key.csv -s secondary_example_key.csv -o output_key.csv -k email
    
    
    
