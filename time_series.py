import doctest
import datetime
#import matplotlib.pyplot as plt
#import numpy as np

def date_diff(date1, date2):
    """
    (str, str)-> int
    The dates formatted in ISO format
    If the ﬁrst date is earlier than the second date, the number should be positive;
     otherwise the number should be negative
    Want to return how many days apart the two days are, as an integer
    >>> date_diff("2019-10-31","2019-11-2") 
    2
    >>> date_diff("2020-5-3","2020-6-30") 
    58
    >>> date_diff("2019-12-31","2019-11-27") 
    -34
    """
    # striptime change the string date to an integer and the second
    # argument is the fomrat of the date
    date1_object = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2_object = datetime.datetime.strptime(date2, '%Y-%m-%d')
    time_delta =  date2_object - date1_object

    return time_delta.days

def get_age(date1, date2):
    """
    (str, str)-> int
    The dates formatted in ISO format
    If the ﬁrst date is earlier than the second date, the number should be positive;
     otherwise the number should be negative
    Want to return how many years apart the two dates are, as an integer
    take 1 year = 365.2425 days
    >>> get_age("2018-10-31","2019-11-2") 
    1
    >>> get_age("2018-10-31","2000-11-2") 
    -18
    >>> get_age("2016-12-31","2019-11-2") 
    2
    """
    date1_object = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2_object = datetime.datetime.strptime(date2, '%Y-%m-%d')
    time_delta =  date2_object - date1_object #gives the number of days
    years = int(time_delta.days//365.2425) #convert into years

    return years

def stage_three(input_filename, output_filename):
    
    """
     (str, str)->dict
     The changes to make to the data:
     1. Replace the date of each record with the date diﬀ of that date and the index date
     2. Replace the date of birth with age at the time of the index date
     3. Replace the status with one of I, R and D.(Representing Infected, Recovered, and Dead;
     the French words are infect´e(e), r´ecup´er´e(e) and mort(e).)
     >>> stage_three("stage2.tsv", "stage3.tsv") 
     {0: {'I': 1, 'D': 0, 'R': 0}, 1: {'I': 3, 'D': 0, 'R': 0}, 2: {'I': 4, 'D': 2, 'R': 0}}
    """
    days_dict = {}
    input_file = open(input_filename)
    lines = input_file.readlines()
    output_file = open(output_filename,'w', encoding='utf-8')
    first_line = lines[0]
    index_date = first_line.split("\t")[2]
    for line in lines:
        columns = line.split("\t")
        columns[2] = (date_diff(index_date, columns[2]))
        columns[3] = str(get_age(columns[3],index_date))
        status = columns[6][0].upper()
        if status == "M":
            status = "D"
        columns[6]=status
        if columns[2] not in days_dict.keys():
            days_dict[columns[2]] = {"I": 0, "D": 0, "R": 0}
        days_dict[columns[2]][columns[6]] += 1
        columns[2] = str(columns[2])
        line = "\t".join(columns)
        output_file.write(line)
    return days_dict

if __name__ == '__main__':
    doctest.testmod()
