import doctest
import datetime
import matplotlib.pyplot as plt
import numpy as np

class Patient:
    """
    Represent number of patients
    Attributes: num of patients(int),days_diagnosed(int), sex_gender(string), age(int)\
    postal(string), state, temps, days_symptomatic
    """
    #constructor
    def  __init__(self, num, day_diagnosed, age, sex_gender, postal, state, temp, days_symptomatic):
        self.num = int(num)
        self.day_diagnosed = int(day_diagnosed)
        self.age = int(age)
        female_chars = ["W","F"]
        male_chars = ["M", "H"]
        #replace woman/femme/girl with the F (sex)
        if sex_gender[0].upper() in female_chars or sex_gender=="GIRL":
            self.sex_gender = "F"
        #replace man/homme/boy with M
        elif sex_gender[0].upper() in male_chars or sex_gender=="BOY":
            self.sex_gender = "M"
        # else if its non binary we replace it with X
        else:
            self.sex_gender = "X"

        if len(postal) >= 3 and postal[0].upper()== "H" and postal[1].isdigit() and postal[2].isalpha():
            # check the length of the postal and if its 3 the return postal
            if len(postal) == 3:
                self.postal = postal
            #if the lenghth of the postal is more three, slice it and return 1st 3 values
            else:
                self.postal = postal[:3] 
        # check the validity of the postal and replace it with 000 if not valid
        else:
            self.postal = "000"
        
        self.state = state
       
        self.temps = []
        temp = temp.split(" ")[0].replace(",", ".") # make sure the temps is separated with a dot and not a comma
        try:
            temp = float(temp)
        except ValueError: # if the temp cannot be converted into a float that means it is not all digits, record 0.0
            temp = 0.0
        #check whether the temps given is more than 45
        # if not convert to Celscius and append it to the temps list
        if temp > 45:
            self.temps.append(round(((temp - 32) * 5/9), 2))
        else:
            self.temps.append(temp) # append the temp if it is below 45

        self.days_symptomatic = int(days_symptomatic)
    
    #function methods
    def __str__(self):
        """
        return a string of attributes separated by tabs
        >>> p = Patient("0", "0", "42", "Woman", "H3Z2B5", "I", "102.2", "12")
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t12\\t39.0'
        """
        patient_info = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
            str(self.num),
            str(self.age),
            str(self.sex_gender),
            str(self.postal),
            str(self.day_diagnosed),
            str(self.state),
            str(self.days_symptomatic),
            ";".join([str(temp) for temp in self.temps]) 
        )
        return patient_info

    def update(self, other_patient):
        """
        >>> p = Patient("0", "0", "42", "Woman", "H3Z2B5", "I", "102.2", "12")
        >>> p1 = Patient("0", "1", "42", "F","H3Z", "I", "40,0 C", "13")
        >>> p.update(p1)
        >>> (str(p))
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t13\\t39.0;40.0'
        """
        # check If this other object’s number, sex/gender, and postal code are all the same as the current patient:
        if self.num == other_patient.num and self.sex_gender == other_patient.sex_gender and self.postal == other_patient.postal:
            # update the day of symptomatic
            self.days_symptomatic = other_patient.days_symptomatic
            #update state with the current state
            self.state = other_patient.state
            # append the new temp at index zero to the existing list if temps
            self.temps.append(other_patient.temps[0])
        # if the num, sex/gender and postal is not the same, raise an error
        else:
            raise AssertionError("Patient's information not the same.")

def stage_four(input_filename, output_filename):
        
    """
    (str, str)->dict
    want to create a new Patient object for each line on the file
    >>> p = stage_four("stage3.tsv", "stage4.tsv")
    >>> len(p)
    1809
    >>> str(p[0])
    '0\\t43\\tM\\tH2T\\t0\\tD\\t6\\t40.22;0.0;0.0;42.72;0.0'
    """
    # create an empty dictinary
    patients_dict = {}
    input_file = open(input_filename)
    lines = input_file.readlines()
    output_file = open(output_filename,'w', encoding='utf-8')
    for line in lines:
        # split the line into array of columns to access each column
        columns = line.split("\t")
        num = int(columns[1])
        day_diagnosed = columns[2] 
        age = columns[3] 
        sex_gender =  columns[4]
        postal = columns[5]
        state = columns[6]
        temp = columns[7]
        days_symptomatic = columns[8]
        # define the patient information basing on each column by index
        p = Patient(str(num), day_diagnosed, (age), sex_gender, postal, state,temp, days_symptomatic)
        # check whether the num of the patient is already in the dict and update the dict with the new information
        if num in patients_dict.keys():
            patients_dict[num].update(p)
        #if it is not in the dict, append the new patient info into the dict
        else:
            patients_dict[num] = p
    # sort the patients number in increasing order
    for num in sorted(patients_dict.keys()):
        line =str(patients_dict[num])
        output_file.write(line + "\n") # write the details into each line
    output_file.close()

    return patients_dict


def fatality_by_age(p):
    """
    (dict) -> list
    input is dictionary of Patients object 
    want to return list of probability of death by age group
    >>> p = stage_four("stage3.tsv", "stage4.tsv")
    >>> fatality_by_age(p)
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9714285714285714, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    """
    #initialize a new dict of age groups
    age_group_dict = {}
    #loop through p to get the values which is another dict with Death, Infected and recoevred
    for patient in p.values():
        rounded_age = int(round(patient.age)/5)*5 # round the values to the nearest 5
        # check whether the age is already in the dict and if not initialize the empty dict and set keys to 0
        if rounded_age not in age_group_dict:
            age_group_dict[rounded_age] = {"R": 0, "D": 0}
        #check if the state of the patient is recovered or death increase the count
        if patient.state == "R":
            age_group_dict[rounded_age]["R"] += 1
        elif patient.state == "D":
            age_group_dict[rounded_age]["D"] +=1
    # initialize a new list to store the value of fatality probability
    fatality_probability = []
    for status in age_group_dict.values():
        # check whether the sum of the death and recover is 0
        #append 1 instead to avoid zeroDvision error
        if (status["D"] + status["R"]) == 0:
            fatality_probability.append(1)
        # if not 0, then you append the fatality probability
        else:
            fatality_probability.append(status["D"]/(status["D"] + status["R"]))
# plot the graph

    x = (list(age_group_dict.keys())) # the keys of the dict represents the number of people
    y = (fatality_probability)
    plt.plot(x, y)
    plt.ylim((0, 1.2))
    plt.title("Probabilty of death vs age," +"by " + "Gattuoch Kuon")
    plt.xlabel("Age(to nearest 5)")
    plt.ylabel("Deaths/(Deaths + Recoveries)")
    plt.savefig('fatality_by_age.png')

    return fatality_probability



if __name__ == "__main__":
    doctest.testmod()
