# COMP 202 A4 PART 1
# NAME: GATTUOCH KUON
# STUDENT ID : 260-877-635

import doctest

def which_delimiter(string):
    """
    (str)->s tr
    Want to return delimiter(space/comma/tab) in the input string
    >>> which_delimiter("0 1 2,3")
    ' '
    >>> which_delimiter("hello")
    Traceback (most recent call last):
    AssertionError: Should have at least one delimiter.
    >>> which_delimiter("cat\\tdog\\trat")
    '\\t'
    >>> which_delimiter("0,1,2,3")
    ','
    """
    delimiters = [",", " ", "\t"]
    most_common = None
    max_occurence = 0
    for delimiter in delimiters:
        total_count = string.count(delimiter)
        if string.count(delimiter) > max_occurence:
            most_common = delimiter
            max_occurence = total_count
    if most_common:
        return most_common
    else:
        raise AssertionError("Should have at least one delimiter.")
        #to revisit
    """    
    delimiters = [",", " ", "\t"]
    first_occurence = float("inf") # i assign my first occurence the highest value
    while delimiters:
        char = delimiters.pop(0) # i get the delimiter at the first index
        i = string.find(char) # find index of the first occurrence
        if i != -1: # if no index found i.e find return -1
            i < first_occurence #compare the index of delimiter at the value of first occurrence
            first_occurence = i
    if first_occurence == float("inf"): # if delimiter not found, i raise an error
        raise AssertionError("Should have at least one delimiter.")
    else:
        #first occurrence store lowest index and return the value at this index
       return string[first_occurence]
    """
def stage_one(input_filename, output_filename):
    """
    (str, str)-> int
    The changes to make to the data: 
    1. Change the most common delimiter to tab (if it is not already tab-delimited) 
    2. Change all text to be upper case
    3. Change any / or . in the dates to hyphens(-) 
    Want to return how many lines were written to output filename
    >>> stage_one("input_filename.txt", "stage1.tsv")
    10
    """
    input_file = open(input_filename)
    lines = input_file.readlines() # want to read line by line
    output_file = open(output_filename,"w", encoding='utf-8')
    count_lines = 0
    for line in lines:
        most_common = which_delimiter(line)
        if most_common != "\t":
            line = line.replace(most_common, "\t")
        line = line.replace(".", "-")
        line = line.replace("/","-")
        line.upper() # change everything into uppercase
        output_file.write(line)
        count_lines += 1
    output_file.close()
    
    return count_lines
   

def stage_two(input_filename, output_filename):
    """
    (str, str)-> int
    The changes to make to the data: 
    1. All lines should have 9 ccleanolumns
    2. Any lines with more than 9 columns should be cleaned so the line is now 9 columns. 
    Want to return how many lines were written to output filename
    >>> stage_two("stage1.tsv", "stage2.tsv")
    10
    """
    input_file = open(input_filename)
    lines = input_file.readlines()
    output_file = open(output_filename,'w', encoding='utf-8')
    count = 0
    for line in lines:
        columns = line.split("\t")
        if len(columns) != 9:# check if the length of the line is exactly 9.
            # then we simply write on the outputfile
            if len(columns[5])==3:
                columns[5]+=columns[6]
                columns.pop(6)
            if len(columns) > 9:
                columns[7] = columns[7] + "." + columns[8]
                columns.pop(8)

        line = "\t".join(columns)
        output_file.write(line)
        count += 1

    return count


if __name__ == '__main__':
    doctest.testmod()
