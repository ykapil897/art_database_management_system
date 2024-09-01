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

# Drop existing tables if any (clean start)
tables = ['Review', 'OrderItem', 'Orders', 'Cart', 'Artwork', 'Buyer', 'Artist', 'User']
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Role ENUM('Artist', 'Buyer') NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Artist (
    ArtistID INT PRIMARY KEY,
    Biography TEXT,
    ProfilePicture VARCHAR(255),
    FOREIGN KEY (ArtistID) REFERENCES User(UserID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Buyer (
    BuyerID INT PRIMARY KEY,
    ShippingAddress TEXT,
    FOREIGN KEY (BuyerID) REFERENCES User(UserID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Artwork (
    ArtworkID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    Description TEXT,
    Medium VARCHAR(255),
    Style VARCHAR(255),
    Image VARCHAR(255),
    DateCreated DATE,
    Availability BOOLEAN,
    Price DECIMAL(10, 2),
    ArtistID INT,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Cart (
    ArtworkID INT,
    BuyerID INT,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID),
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    Status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') NOT NULL,
    BuyerID INT,
    PaymentMethod ENUM('Credit Card', 'PayPal') NOT NULL,
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS OrderItem (
    Quantity INT,
    OrderID INT,
    ArtworkID INT,
    FOREIGN KEY (OrderID) REFERENCES `Orders`(OrderID),
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comment TEXT,
    ReviewDate DATE,
    BuyerID INT,
    ArtworkID INT,
    FOREIGN KEY (BuyerID) REFERENCES Buyer(BuyerID),
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID)
);
''')

# Insert Dummy Records
# Insert Users
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('artist1', 'pass123', 'artist1@example.com', 'Artist')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('buyer1', 'pass123', 'buyer1@example.com', 'Buyer')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('artist2', 'pass456', 'artist2@example.com', 'Artist')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('buyer2', 'pass456', 'buyer2@example.com', 'Buyer')")

# Insert Artist (linked to user)
cursor.execute("INSERT INTO Artist (ArtistID, Biography, ProfilePicture) VALUES (1, 'Bio of artist 1', 'path/to/profile1.jpg')")
cursor.execute("INSERT INTO Artist (ArtistID, Biography, ProfilePicture) VALUES (3, 'Bio of artist 2', 'path/to/profile2.jpg')")

# Insert Buyer (linked to user)
cursor.execute("INSERT INTO Buyer (BuyerID, ShippingAddress) VALUES (2, '1234 Elm Street')")
cursor.execute("INSERT INTO Buyer (BuyerID, ShippingAddress) VALUES (4, '5678 Oak Avenue')")

# Insert Artwork
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Sunset', 'Beautiful sunset painting', 'Oil', 'Realism', 'path/to/image1.jpg', '2024-08-01', TRUE, 250.00, 1)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Abstract Dreams', 'Abstract artwork with vibrant colors', 'Acrylic', 'Abstract', 'path/to/image2.jpg', '2024-07-15', TRUE, 300.00, 1)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('The Sea', 'Painting of a serene seascape', 'Watercolor', 'Seascape', 'path/to/image3.jpg', '2024-08-10', TRUE, 200.00, 3)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Night Sky', 'Depiction of a starry night sky', 'Oil', 'Landscape', 'path/to/image4.jpg', '2024-06-20', TRUE, 180.00, 3)")

# Insert Cart
cursor.execute("INSERT INTO Cart (ArtworkID, BuyerID) VALUES (1, 2)")
cursor.execute("INSERT INTO Cart (ArtworkID, BuyerID) VALUES (3, 4)")

# Insert OrderTable
cursor.execute("INSERT INTO `Orders` (OrderDate, TotalAmount, Status, BuyerID, PaymentMethod) \
VALUES ('2024-08-15', 250.00, 'Pending', 2, 'Credit Card')")
cursor.execute("INSERT INTO `Orders` (OrderDate, TotalAmount, Status, BuyerID, PaymentMethod) \
VALUES ('2024-08-20', 200.00, 'Shipped', 4, 'PayPal')")

# Insert OrderItem
cursor.execute("INSERT INTO OrderItem (Quantity, OrderID, ArtworkID) VALUES (1, 1, 1)")
cursor.execute("INSERT INTO OrderItem (Quantity, OrderID, ArtworkID) VALUES (2, 2, 3)")

# Insert Review
cursor.execute("INSERT INTO Review (Rating, Comment, ReviewDate, BuyerID, ArtworkID) \
VALUES (5, 'Amazing artwork!', '2024-08-16', 2, 1)")
cursor.execute("INSERT INTO Review (Rating, Comment, ReviewDate, BuyerID, ArtworkID) \
VALUES (4, 'Beautiful but expensive.', '2024-08-17', 4, 3)")

# Insert Users
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('artist3', 'pass789', 'artist3@example.com', 'Artist')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('buyer3', 'pass789', 'buyer3@example.com', 'Buyer')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('artist4', 'pass101', 'artist4@example.com', 'Artist')")
cursor.execute("INSERT INTO User (Username, Password, Email, Role) VALUES ('buyer4', 'pass101', 'buyer4@example.com', 'Buyer')")

# Insert Artist (linked to user)
cursor.execute("INSERT INTO Artist (ArtistID, Biography, ProfilePicture) VALUES (5, 'Bio of artist 3', 'path/to/profile3.jpg')")
cursor.execute("INSERT INTO Artist (ArtistID, Biography, ProfilePicture) VALUES (7, 'Bio of artist 4', 'path/to/profile4.jpg')")

# Insert Buyer (linked to user)
cursor.execute("INSERT INTO Buyer (BuyerID, ShippingAddress) VALUES (6, '9876 Pine Road')")
cursor.execute("INSERT INTO Buyer (BuyerID, ShippingAddress) VALUES (8, '5432 Maple Street')")

# Insert Artwork
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Golden Sunset', 'A sunset painting with golden hues', 'Oil', 'Impressionism', 'path/to/image5.jpg', '2024-08-21', TRUE, 320.00, 5)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Serenity', 'Peaceful abstract art', 'Acrylic', 'Abstract', 'path/to/image6.jpg', '2024-08-22', TRUE, 350.00, 5)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Mountain Range', 'Landscape of majestic mountains', 'Watercolor', 'Landscape', 'path/to/image7.jpg', '2024-08-23', TRUE, 220.00, 7)")
cursor.execute("INSERT INTO Artwork (Title, Description, Medium, Style, Image, DateCreated, Availability, Price, ArtistID) \
VALUES ('Urban Jungle', 'Vibrant cityscape', 'Mixed Media', 'Urban', 'path/to/image8.jpg', '2024-08-24', TRUE, 290.00, 7)")

# Insert Cart
cursor.execute("INSERT INTO Cart (ArtworkID, BuyerID) VALUES (2, 6)")
cursor.execute("INSERT INTO Cart (ArtworkID, BuyerID) VALUES (4, 8)")

# Insert OrderTable
cursor.execute("INSERT INTO `Orders` (OrderDate, TotalAmount, Status, BuyerID, PaymentMethod) \
VALUES ('2024-08-25', 320.00, 'Pending', 6, 'Credit Card')")
cursor.execute("INSERT INTO `Orders` (OrderDate, TotalAmount, Status, BuyerID, PaymentMethod) \
VALUES ('2024-08-30', 290.00, 'Shipped', 8, 'PayPal')")

# Insert OrderItem
cursor.execute("INSERT INTO OrderItem (Quantity, OrderID, ArtworkID) VALUES (1, 3, 2)")
cursor.execute("INSERT INTO OrderItem (Quantity, OrderID, ArtworkID) VALUES (2, 4, 4)")

# Insert Review
cursor.execute("INSERT INTO Review (Rating, Comment, ReviewDate, BuyerID, ArtworkID) \
VALUES (5, 'Incredible piece of art!', '2024-08-26', 6, 2)")
cursor.execute("INSERT INTO Review (Rating, Comment, ReviewDate, BuyerID, ArtworkID) \
VALUES (4, 'Really like the colors.', '2024-08-27', 8, 4)")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
print("Dummy data inserted into all tables successfully.")
