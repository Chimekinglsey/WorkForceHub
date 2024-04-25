import csv
import random
from faker import Faker

# Initialize Faker to generate random data
fake = Faker()

# Function to generate fake date of birth
def generate_dob():
    return fake.date_of_birth(minimum_age=18, maximum_age=65)

# Function to generate fake gender
def generate_gender():
    return random.choice(['Male', 'Female'])

# Function to generate fake marital status
def generate_marital_status():
    return random.choice(['Single', 'Married', 'Divorced', 'Widowed'])

# Function to generate fake email address
def generate_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}@example.com"

# Function to generate fake address
def generate_address():
    return fake.address()

# Function to generate fake phone number
def generate_phone_number():
    return fake.phone_number()

# Function to generate fake department/division
def generate_department():
    return fake.job()

# Function to generate fake job role
def generate_job_role():
    return fake.job()

# Function to generate fake date employed
def generate_date_employed():
    return fake.date_this_decade()

# Function to generate fake employment type
def generate_employment_type():
    return random.choice(['Full-time', 'Part-time', 'Contract', 'Internship'])

# Function to generate fake employment status
def generate_employment_status():
    return random.choice(['Active', 'Resigned', 'Terminated'])

# Function to generate fake designation
def generate_designation():
    return fake.job()

# Function to generate fake level
def generate_level():
    return random.randint(1, 10)

# Function to generate fake salary
def generate_salary():
    return fake.random_number(digits=5)

# Function to generate fake bank name
def generate_bank_name():
    return fake.company()

# Function to generate fake account number
def generate_account_number():
    return fake.random_number(digits=10)

# Function to generate fake account name
def generate_account_name():
    return fake.name()

# Function to generate fake emergency contacts
def generate_emergency_contacts():
    return fake.name(), fake.phone_number()

# Function to generate fake highest qualification
def generate_highest_qualification():
    return fake.job()

# Function to generate fake skills/qualifications
def generate_skills():
    return fake.words(nb=3)

# Function to generate fake next of kin name
def generate_next_of_kin():
    return fake.name(), random.choice(['Spouse', 'Child', 'Parent', 'Sibling'])

# Function to generate fake next of kin phone number
def generate_next_of_kin_phone():
    return fake.phone_number()

# Number of employees to generate
num_employees = 50

# Open CSV file for writing
with open('employees/tests/files/csv/employees.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write header
    writer.writerow(["SN", "First Name", "Last Name", "Middle name", "Date of birth", "Gender", "Marital status",
                     "email address", "Address", "Nationality", "State of origin", "Phone number", "Employee ID",
                     "Department/division", "Job role", "Date employed", "Employment type", "Employment status",
                     "Designation", "Level", "Last promotion date", "Next promotion date", "Salary", "bank name",
                     "account number", "account name", "pension ID", "tax ID", "Emergency contacts",
                     "Date of termination/resignation", "Highest qualification", "Skills/qualifications",
                     "Next of kin name", "Next of kin relationship", "Next of kin phone number"])

    # Generate employees
    for i in range(num_employees):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.first_name_male() if generate_gender() == 'Male' else fake.first_name_female()
        dob = generate_dob()
        gender = generate_gender()
        marital_status = generate_marital_status()
        email = generate_email(first_name, last_name)
        address = generate_address()
        nationality = fake.country()
        state = fake.state()
        phone_number = generate_phone_number()
        department = generate_department()
        job_role = generate_job_role()
        date_employed = generate_date_employed()
        employment_type = generate_employment_type()
        employment_status = generate_employment_status()
        designation = generate_designation()
        level = generate_level()
        salary = generate_salary()
        bank_name = generate_bank_name()
        account_number = generate_account_number()
        account_name = generate_account_name()
        pension_id = fake.random_number(digits=6)
        tax_id = fake.random_number(digits=9)
        emergency_contacts = generate_emergency_contacts()
        termination_date = fake.date_this_decade() if employment_status != 'Active' else ''
        highest_qualification = generate_highest_qualification()
        skills = generate_skills()
        next_of_kin_name, next_of_kin_relation = generate_next_of_kin()
        next_of_kin_phone = generate_next_of_kin_phone()

        # Write employee data to CSV file
        writer.writerow([i+1, first_name, last_name, middle_name, dob, gender, marital_status, email, address,
                         nationality, state, phone_number, '', department, job_role, date_employed, employment_type,
                         employment_status, designation, level, '', '', salary, bank_name, account_number,
                         account_name, pension_id, tax_id, emergency_contacts, termination_date, highest_qualification,
                         skills, next_of_kin_name, next_of_kin_relation, next_of_kin_phone])

print("Employees generated successfully.")
