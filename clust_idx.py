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

# Query to find all index names except the primary key
cursor.execute('''
    SELECT INDEX_NAME 
    FROM information_schema.STATISTICS 
    WHERE TABLE_SCHEMA = 'art_database'
    AND TABLE_NAME = 'Artwork'
    AND INDEX_NAME != 'PRIMARY';
''')

# Fetch all index names
indexes = cursor.fetchall()

# Loop through each index and drop it
for index in indexes:
    index_name = index[0]
    if index_name != 'ArtistID':
        drop_index_query = f"DROP INDEX `{index_name}` ON Artwork;"
        cursor.execute(drop_index_query)
        print(f"Index '{index_name}' dropped.")

# Commit the changes
conn.commit()

print("All non-primary indexes have been dropped.")

# Check and drop existing indexes
cursor.execute('''
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE table_schema = 'art_database'
    AND table_name = 'Artwork'
    AND index_name = 'idx_style_price';
''')

if cursor.fetchone()[0] > 0:
    cursor.execute('DROP INDEX idx_style_price ON Artwork;')

# Drop foreign key constraint before dropping index
cursor.execute('''
    SELECT CONSTRAINT_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE table_schema = 'art_database'
    AND table_name = 'Artwork'
    AND column_name = 'ArtistID'
    AND referenced_table_name IS NOT NULL;
''')

constraint_name = cursor.fetchone()
if constraint_name:
    constraint_name = constraint_name[0]
    cursor.execute(f'ALTER TABLE Artwork DROP FOREIGN KEY {constraint_name};')

# Drop the index
cursor.execute('''
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE table_schema = 'art_database'
    AND table_name = 'Artwork'
    AND index_name = 'idx_artist_id';
''')
if cursor.fetchone()[0] > 0:
    cursor.execute('DROP INDEX idx_artist_id ON Artwork;')

# Create the composite index on 'Style' and 'Price' columns
cursor.execute('''
    ALTER TABLE Artwork
    ADD INDEX idx_medium (Medium);
''')

print("Composite index applied on Medium column of 'Artwork' table.")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
