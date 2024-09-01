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

# 1. Add Information About 5 New Contemporary Artists

# Add 5 new artists to the User table
cursor.execute('''
    INSERT INTO User (Username, Password, Email, Role) VALUES 
    ('artist5', 'password123', 'artist1@example.com', 'Artist'),
    ('artist6', 'password456', 'artist2@example.com', 'Artist'),
    ('artist7', 'password789', 'artist3@example.com', 'Artist'),
    ('artist8', 'password101', 'artist4@example.com', 'Artist'),
    ('artist9', 'password102', 'artist5@example.com', 'Artist');
''')
print("Added 5 new artists to the User table.")

# Retrieve UserIDs of the newly added artists
cursor.execute('''
    SELECT UserID 
    FROM User 
    WHERE Role = 'Artist' 
    ORDER BY UserID DESC 
    LIMIT 5;
''')
user_ids = cursor.fetchall()

# Add their details to the Artist table
for user_id in user_ids:
    cursor.execute('''
        INSERT INTO Artist (ArtistID, Biography, ProfilePicture) 
        VALUES (%s, %s, %s);
    ''', (user_id[0], f'Biography for Artist {user_id[0]}', f'profile{user_id[0]}.jpg'))
print("Added artist details to the Artist table.")

# 2. Prepare a Report on All Artwork Listings Made in August 2024
cursor.execute('''
    SELECT * 
    FROM Artwork 
    WHERE DateCreated >= '2024-08-01' AND DateCreated < '2024-09-01';
''')
august_listings = cursor.fetchall()

print("Artwork listings for August 2024:")
for listing in august_listings:
    print(listing)

# Done for deleting records from the parent table however we can achieve achieve the same, by first deleting
# dependent records and then parent records.
# Drop the existing foreign key constraint
cursor.execute('''
    ALTER TABLE orderitem
    DROP FOREIGN KEY orderitem_ibfk_2;
''')
print("Dropped the existing foreign key constraint.")

# Add the new foreign key constraint with ON DELETE CASCADE
cursor.execute('''
    ALTER TABLE orderitem
    ADD CONSTRAINT orderitem_ibfk_1
    FOREIGN KEY (OrderID) REFERENCES `Orders` (OrderID)
    ON DELETE CASCADE;
''')
print("Added new foreign key constraint with ON DELETE CASCADE.")


# 3. Remove All Artwork Purchases Made After 7 PM on August 15, 2024
cursor.execute('''
    DELETE FROM `Orders`
    WHERE OrderDate > '2024-08-15 19:00:00';
''')
print("Removed all artwork purchases made after 7 PM on August 15, 2024.")

# Commit changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
