# Employee-Backup-Calculation
Calculates a 'fair' distribution for employee backups based on given constraints. Employees will not be allowed to backup more than one of another employee's customers.

Data Inputs:
AssignmentTable: A sheet containing employee information. The first column must be employee name. The second column must be the amount of people they're allowed/are willing to backup. All remaining columns are the names of customers that employee usually supports

Bias Matrix: A sheet containing employee preferences. May be set to all the same number to ignore. First column must be customer name. First row must be employee name. Below each employee name should be a preference rating. This rating may be on any scale that exists in the natural numbers excluding 0, for the example I used 1 - 10. Employees must enter 0 for a customer that is thier primary responsability.


RedistributionCalculation was used to make the sample data.


Running:
Before running Employee_Backup_Assignment.py, be sure to select your desired calculation method. The default is flat.

This script will output a CSV file called Backup_Personnel.csv containing the new employee backups. The first column is the name of the employee. The remaining columns are the customers the employee will serve as backup for.

This script may be compiled, executed in the console, or however you prefer to run python code. Some formatting may be required to fit your desired running style.
