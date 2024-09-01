import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="2004-2002-1979",
    database="art_database"
)
cursor = conn.cursor()

# Apply a secondary index on the 'Title' column
cursor.execute('''
    CREATE INDEX idx_title ON Artwork (Title);
''')
print("Secondary index 'idx_title' applied on 'Title' column.")

# Apply a secondary index on the 'DateCreated' column
cursor.execute('''
    CREATE INDEX idx_date_created ON Artwork (DateCreated);
''')
print("Secondary index 'idx_date_created' applied on 'DateCreated' column.")

# Apply a composite secondary index on 'Medium' and 'Availability' columns
cursor.execute('''
    CREATE INDEX idx_medium_availability ON Artwork (Medium, Availability);
''')
print("Composite secondary index 'idx_medium_availability' applied on 'Medium' and 'Availability' columns.")

# Commit changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
