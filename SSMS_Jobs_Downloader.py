import pyodbc
import os
from datetime import datetime

# Define your SQL Server connection parameters
server = 'server_name'
database = 'database_name'  # msdb database contains SQL Server Agent information
trusted_connection = 'yes'  # Use Windows Authentication
driver = '{ODBC Driver 17 for SQL Server}'  # Update the driver version if necessary

# Create a folder on the desktop with the current date
today = datetime.today().strftime('%Y_%m_%d')
output_folder = f'"file_location_name"/{today}_Jobs'  # Replace drive/file location

# Connect to SQL Server using Windows authentication
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')

# Create a cursor
cursor = conn.cursor()

# Query to retrieve job names, descriptions, and command scripts
query = """
SELECT 
    j.[name] AS job_name, 
    js.[command] AS job_command
FROM 
    msdb.dbo.sysjobs j
INNER JOIN 
    msdb.dbo.sysjobsteps js ON j.job_id = js.job_id
"""

# Execute the query
cursor.execute(query)

# Fetch all rows
jobs = cursor.fetchall()

# Close the cursor and connection
cursor.close()
conn.close()

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each job and save its command to a file
for job in jobs:
    job_name = job.job_name
    job_command = job.job_command

    # Construct the file path
    file_path = os.path.join(output_folder, f"{job_name}.sql")

    # Write the job command to a file
    with open(file_path, 'w') as file:
        file.write(f"-- Job Name: {job_name}\n")
        file.write("-- Job Command:\n")
        file.write(job_command)
        print(f"File created, my leige: {file_path}")
