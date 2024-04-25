import pandas as pd
from faker import Faker
import random

fake = Faker()

employee_fields = ["SN", "First Name", "Last Name", "Middle name", "Date", "Employment Type", "Employment Status",
                   "Email", "Phone Number", "Address", "Employee ID", "Department", "Designation", "Level", "Salary"]

dataset = []
num = 10

for i in range(num):
    dataset.append([i+1, fake.first_name(), fake.last_name(), fake.first_name(), fake.date_of_birth(minimum_age=20, maximum_age=70), 
                    random.choice(["Full-time", "Part-time"]), random.choice(["Active", "Inactive"]), 
                    fake.email(), fake.phone_number(), fake.address(), fake.random_int(1000, 9999), 
                    fake.job(), fake.random_element(["Manager", "Supervisor", "Assistant", "Director"]), 
                    random.randint(1, 10), fake.random_int(30000, 100000)])

df = pd.DataFrame(dataset, columns=employee_fields)
# print(df)
verify_names = [row["First Name"] for _,row in df.iterrows()]
# print(verify_names)
unique_id = [row.get('Employee IID') if pd.notna(row.get('Employee IID')) else "Nothing" for _, row in df.iterrows()]
print(list(zip(verify_names, unique_id)))