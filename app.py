# app.py
import streamlit as st
import mysql.connector
from mysql.connector import Error


# # Adding CSS styling with background images using st.markdown
# st.markdown(
#     """
#     <style>
#     body {
#         font-family: 'Arial', sans-serif;
#         background-color: #f4f4f4;
#         margin: 0;
#         padding: 0;
#     }

#     /* Title Styling */
#     .main > .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         position: relative; /* Position relative to contain absolute elements */
#     }

#     /* Background Images Styling */
#     .bg-image1, .bg-image2, .bg-image3 {
#         position: absolute;
#         z-index: -1; /* Behind all other content */
#         opacity: 0.7; /* Transparency for effect */
#     }

#     /* Specific Background Images with Rotation and Positioning */
#     .bg-image1 {
#         content: url('https://i.etsystatic.com/21806975/r/il/318807/4160800982/il_570xN.4160800982_7et3.jpg');
#         width: 30vw; /* 30% of the viewport width */
#         height: auto;
#         top: 10vh; /* 10% from the top */
#         left: -5vw; /* 5% to the left of the viewport */
#         transform: rotate(15deg); /* Artistic rotation */
#     }

#     .bg-image2 {
#         content: url('https://m.media-amazon.com/images/I/61bOqUZRSPL.jpg');
#         width: 20vw; /* 20% of the viewport width */
#         height: auto;
#         bottom: 20vh; /* 20% from the bottom */
#         right: 0; /* Align to the right of the viewport */
#         transform: rotate(-10deg); /* Artistic rotation */
#     }

#     .bg-image3 {
#         content: url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSubBhdZEN66Hk6tk0-Q2769-4ZiNqYhGRcsdrHCy-YwB_-zFB8byxiI6fB7Q6y2Bu8Lcs&usqp=CAU');
#         width: 25vw; /* 25% of the viewport width */
#         height: auto;
#         top: 40vh; /* 40% from the top */
#         right: 15vw; /* 15% from the right of the viewport */
#         transform: rotate(25deg); /* Artistic rotation */
#     }

#     /* General Content Styling */
#     .stApp {
#         background: none;
#     }

#     button[data-baseweb="button"] {
#         background-color: #4CAF50;
#         color: white;
#         border: none;
#         padding: 10px 24px;
#         text-align: center;
#         text-decoration: none;
#         display: inline-block;
#         font-size: 16px;
#         margin: 4px 2px;
#         cursor: pointer;
#         border-radius: 4px;
#         transition-duration: 0.4s;
#     }

#     button[data-baseweb="button"]:hover {
#         background-color: white;
#         color: black;
#         border: 2px solid #4CAF50;
#     }

#     h1, h2, h3 {
#         color: #333;
#         text-align: center;
#     }

#     .dataframe {
#         border-collapse: collapse;
#         width: 100%;
#         margin: 20px 0;
#         font-size: 18px;
#         text-align: left;
#     }

#     .dataframe th, .dataframe td {
#         padding: 12px;
#         border: 1px solid #ddd;
#     }

#     .dataframe th {
#         background-color: #f2f2f2;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Adding the background images to the Streamlit app
# st.markdown(
#     """
#     <div class="bg-image1"></div>
#     <div class="bg-image2"></div>
#     <div class="bg-image3"></div>
#     """,
#     unsafe_allow_html=True
# )


# Connect to MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="2004-2002-1979",  # Replace with your password
            database="art_database"
        )
        return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to execute SQL query
def execute_query(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)
         # Execute the query with parameters if provided
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    # Fetch all results if it is a SELECT query
    if query.strip().upper().startswith("SELECT"):
        results = cursor.fetchall()  # Fetch all results to clear any unread data
    else:
        results = None
        conn.commit()  # Commit the transaction for non-SELECT queries

    cursor.close()  # Close the cursor after fetching results
    conn.close()  # Close the connection
    return results

# Main Streamlit Application
st.title('Interactive Art Database Application')

# User selection for operation type
operation = st.selectbox("Choose an operation:", ["Select Table", "Add Record", "Generate Report", "Delete Record"])

# If user selects "Select Table"
if operation == "Select Table":
    table = st.selectbox("Select a table to view data:", ["Artist", "Artwork", "Orders"])

    if st.button("Fetch Data"):
        query = f"SELECT * FROM {table};"
        results = execute_query(query)
        if results:
            st.write(results)

# If user selects "Add Record"
elif operation == "Add Record":
    st.header("Add New Record")
    add_to_table = st.selectbox("Select the table to add a record:", ["Artist", "Artwork", "Orders"])

    if add_to_table == "Artist":
        # Input fields for adding artist
        artist_id = st.text_input("Artist ID")
        username = artist_id
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        role = "Artist"
        biography = st.text_area("Biography")
        profile_picture = st.text_input("Profile Picture URL")

        if st.button("Add Artist"):
            if not (username and password and email and biography and profile_picture):
                st.error("Please provide all artist details perfectly")
            
            # Insert user into the User table
            user_query = '''
            INSERT INTO User (Username, Password, Email, Role)
            VALUES (%s, %s, %s, %s);
            '''
            execute_query(user_query, (username, password, email, role))

            query = "INSERT INTO Artist (ArtistID, Biography, ProfilePicture) VALUES (%s, %s, %s)"
            params = (artist_id, biography, profile_picture)
            execute_query(query, params)
            st.success("Artist added successfully!")

    elif add_to_table == "Artwork":
        # Input fields for adding artwork
        title = st.text_input("Title")
        artist = st.text_input("Artist")
        medium = st.text_input("Medium")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        availability = st.selectbox("Availability", ["Available", "Sold"])

        if st.button("Add Artwork"):
            query = "INSERT INTO Artwork (Title, Artist, Medium, Price, Availability) VALUES (%s, %s, %s, %s, %s)"
            params = (title, artist, medium, price, availability)
            execute_query(query, params)
            st.success("Artwork added successfully!")

    # Add similar options for Orders...

# If user selects "Generate Report"
elif operation == "Generate Report":
    report_type = st.selectbox("Select a report type:", ["Artwork Listings for a Month", "Sales at Specific Date"])
    
    if report_type == "Artwork Listings for a Month":
        month = st.selectbox("Select month:", ["January", "February", "March", "August"]) # Add more months as needed
        year = st.text_input("Year", value="2024")

        # Dictionary to map month names to numbers
        month_mapping = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        # Get the corresponding month number
        month_number = month_mapping[month]

        if st.button("Generate Report"):
            query = "SELECT * FROM Artwork WHERE MONTH(DateCreated) = %s AND YEAR(DateCreated) = %s"
            params = (month_number, year)
            results = execute_query(query, params)
            if results:
                st.write(results)

    elif report_type == "Sales at Specific Date":
        date = st.date_input("Date", value=None)
        # time = st.time_input("Time", value=None)

        if st.button("Generate Report"):
            query = "SELECT * FROM Orders WHERE OrderDate = %s"
            params = (date, )
            execute_query(query, params)

# If user selects "Delete Record"
elif operation == "Delete Record":
    table_to_delete = st.selectbox("Select the table to delete from:", ["Artist", "Artwork", "Orders"])
    record_id = st.text_input(f"Enter the ID of the record to delete from {table_to_delete}:")

    if st.button("Delete Record"):
        query = f"DELETE FROM {table_to_delete} WHERE ID = %s"
        params = (record_id,)
        execute_query(query, params)
        st.success("Record deleted successfully!")

### **2. CSS Styling (Optional)**

# To customize the look and feel of your Streamlit app, you can add custom CSS. However, Streamlit itself has limited support for directly embedding HTML/CSS in its interface. You can use `st.markdown` to embed simple CSS.

#### **3. Running the Application**

# To run your Streamlit app, use the following command in your terminal:

# ```sh
# streamlit run app.py
