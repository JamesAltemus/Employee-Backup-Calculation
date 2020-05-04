# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:32:46 2020

@author: James Altemus
"""

import pandas as pd
import numpy as np

# Select an availability calculation
# linear gives more weight to employees that are allowed more backups
# flat weights all as 1 if they have backup slots available
# inverse gives more weight to employees that are allowed less backups
method = ['linear', 'flat', 'inverse']
method = method[1]

# Load the bias matrix, current employee/customer coverage infromation, and
# the amount of customers each employee is allowed to have as backup
bias_matrix = pd.read_csv('BiasMatrix.csv')
assignments = pd.read_csv('AssignmentTable.csv')

## extract the data from the default format
accepted_backups = np.array(assignments[assignments.columns[1]], dtype = np.float32)
customers = assignments[assignments.columns[2:]]
backup_block = np.zeros(len(accepted_backups), dtype = np.float32)
unique_block = np.array([np.ones(len(accepted_backups))]*len(accepted_backups),
                         dtype = np.float32)

full_cust = list(bias_matrix[bias_matrix.columns[0]])
emp_names = list(assignments[assignments.columns[0]])

save_dict = {}
for name in emp_names:
    save_dict[name] = []


# Define functions for the actual calculation
def get_order(array):
    # Randomly assigns order to an array
    array_idx = np.array(range(len(array)), dtype = np.float32)
    array_order = np.random.sample(len(array))
    return array_idx, array_order


def calc_fill(fill, block, method):
    # Calcualtes the amount of available backup slots for each employees.
    # Check the first notes for details on method
    calc = fill - block
    if method == 'linear':
        return calc
    elif method == 'flat':
        calc[calc > 0] =1
        return calc
    elif method == 'inverse':
        calc[calc > 0] = 1/calc[calc > 0]
        return calc


def calc_bias(row_pos, bias):
    # Extracts the bias row for the customer
    return np.array(bias[.columns[1:]].iloc[selected_customer],dtype = np.float32)


# Get max amount of customers to add titles to CSV
max_cust = 0

# Randomly order and select an employee
emp_idx, emp_order = get_order(accepted_backups)
for emp in emp_idx:
    selected_emp = int(emp_idx[emp_order == max(emp_order)])
    
    # Randomly order and select a customer. Also check max customers
    cust_names = customers.iloc[selected_emp].dropna()
    if len(cust_names) > max_cust:
        max_cust = len(cust_names)
    cust_idx, cust_order = get_order(cust_names)
    for cust in cust_idx:
        selected_customer = int(cust_idx[cust_order == max(cust_order)])
        cust_name = list(cust_names)[selected_customer]
        selected_customer = full_cust.index(cust_name)
        
        # Calculate who will take charge as backup
        full = calc_fill(accepted_backups, backup_block, method)
        bias = calc_bias(cust_name, bias_matrix)
        inval = unique_block[selected_emp]
        rng = np.random.sample(size = len(emp_idx))/100
        a_mat = full*inval*(bias+rng)
        
        # Update selected employee's restrictions
        unique_block[selected_emp][a_mat == max(a_mat)] = 0
        backup_block[a_mat == max(a_mat)] += 1
        
        # Save the selected employee and the customer they'll serve as backup for
        name = emp_names[int(emp_idx[a_mat == max(a_mat)])]
        save_dict[name].append(cust_name)
        
        # Set the customer to 0 to select the next customer
        cust_order[cust_order == max(cust_order)] = 0
    # Set the employee to 0 to select the next employee
    emp_order[emp_order == max(emp_order)] = 0


# Save the final backup list to a CSV file
with open('Backup_Personnel.csv', 'w+') as file:
    ## Write titles
    file.write('Employee_Name')
    for i in range(max_cust):
        file.write(',Backup_for_'+str(i))
    file.write('\n')
    ## Write data
    for key in save_dict.keys():
        file.write(key)
        for item in save_dict[key]:
            file.write(',' + item)
        file.write('\n')
