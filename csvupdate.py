import optparse
import sys
import os
import csv  # work in python 2.6+


# Global
PROGRAM_VERSION = "%prog 15.21.02"


def validate_input_file(file_name):
    if not os.path.exists(file_name):
        sys.exit('file %s, dont exists' % file_name)
    elif not os.access(file_name, os.R_OK):
        sys.exit('file %s, not access to read' % file_name)


def validate_output_file(file_name):
    dirname_file = os.path.dirname(os.path.abspath(file_name))
    if not os.path.isdir(dirname_file):
        sys.exit('dirname %s, dont exists' % dirname_file)
    elif not os.access(dirname_file, os.W_OK):
        sys.exit('file %s, not access to write' % file_name)


def update_data(primary_file, secondary_file, output_file, key, flag_add):
    # list where store data
    DATA_PRIMARY = []
    DATA_SECONDARY = []

    # read file and obtain headers and data
    data_p = csv.DictReader(open(primary_file, 'rb'), delimiter=';', quotechar='"')
    data_s = csv.DictReader(open(secondary_file, 'rb'), delimiter=';', quotechar='"')
    header_p = data_p.fieldnames
    header_s = data_s.fieldnames

    # validation no string in header
    if '' in header_p: sys.exit('key \'\', is not valid in %s' % primary_file)
    if '' in header_s: sys.exit('key \'\', is not valid in %s' % secondary_file)

    # if not exist key argument, is first value of header
    if not key: key = header_p[0]

    # validation of key
    if key not in header_p: sys.exit('key %s, not exist in %s' % (key, primary_file))
    if key not in header_s: sys.exit('key %s, not exist in %s' % (key, secondary_file))

    # save data in global var DATA_PRIMARY as a list
    try:
        for row_p in data_p:
            DATA_PRIMARY.append(row_p)
            if None in row_p: del row_p[None]
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (primary_file, data_p.line_num, e))

    # save data in global var DATA_SECONDARY as a list
    try:
        for row_s in data_s:
            DATA_SECONDARY.append(row_s)
            if None in row_s: del row_s[None]
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (secondary_file, data_s.line_num, e))

    # update data
    for row_s in DATA_SECONDARY:
        exist_in_primary = False
        for row_p in DATA_PRIMARY:
            # update value in primary input
            if row_s[key] != '' and row_s[key] != '' and row_p[key].lower().strip() == row_s[key].lower().strip():
                exist_in_primary = True
                key_original_value = {key: row_p[key].strip()}
                row_p.update(row_s)
                row_p.update(key_original_value)
        if exist_in_primary == False and flag_add == True:
            DATA_PRIMARY.append(row_s)

    # obtain header of output
    header_diff = list(set(header_s).difference(set(header_p)))
    header_output = header_p + header_diff

    # save data to file
    writer = csv.DictWriter(open(output_file, 'w'), delimiter=';', fieldnames=header_output)
    writer.writeheader()
    try:
        for row_p in DATA_PRIMARY:
            writer.writerow(row_p)
    except csv.Error, e:
        sys.exit('file %s' % output_file)
    print('All OK, please view file: %s' % os.path.abspath(output_file))


def main():
    parser = optparse.OptionParser(usage="Usage: %prog -p primary.csv -s secondary.csv -o output.csv [-k key] [-n]",
                                   version=PROGRAM_VERSION)
    parser.add_option('-p', '--primary_file', help='input: primary file', dest='primary_file', type='string')
    parser.add_option('-s', '--secondary_file', help='input: secondary file', dest='secondary_file', type='string')
    parser.add_option('-o', '--output', help='output: file', dest='output_file', type='string')
    parser.add_option('-k', '--key',
                      help='puts key name, the default is the first data (first column of primary input)', dest='key',
                      type='string')
    parser.add_option('-n', '--no-add',
                      help='do not add the secondary input data does not exist if the primary input, by default data add',
                      dest='add', default=True, action='store_false')
    (opts, args) = parser.parse_args()

    if opts.primary_file and opts.secondary_file and opts.output_file:
        validate_input_file(opts.primary_file)
        validate_input_file(opts.secondary_file)
        validate_output_file(opts.output_file)

        # validate same name input:
        if opts.primary_file == opts.secondary_file:
            sys.exit(
                'primary file \'%s\' is same than secondary file \'%s\'' % (opts.primary_file, opts.secondary_file))

        ## validate ouput
        if opts.output_file == opts.primary_file:
            sys.exit('output file \'%s\' is same than primary file \'%s\'' % (opts.output_file, opts.primary_file))
        elif opts.output_file == opts.secondary_file:
            sys.exit('output file \'%s\' is same than secondary file \'%s\'' % (opts.output_file, opts.secondary_file))

        update_data(opts.primary_file, opts.secondary_file, opts.output_file, opts.key, opts.add)
    else:
        parser.print_help()
        sys.exit(-1)


if __name__ == '__main__':
    main()
