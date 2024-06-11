import sqlite3
import streamlit as st
import pandas as pd
import atexit

# Connect to SQLite database
conn = sqlite3.connect('hotel_management.db')
c = conn.cursor()

# Create the tables
def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS guests (
                    guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()

create_tables()

# Functions to interact with the database
def add_guest(name, phone, email):
    c.execute("INSERT INTO guests (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    return c.lastrowid

def update_guest(guest_id, name, phone, email):
    c.execute("UPDATE guests SET name = ?, phone = ?, email = ? WHERE guest_id = ?", (name, phone, email, guest_id))
    conn.commit()

def delete_guest(guest_id):
    c.execute("DELETE FROM guests WHERE guest_id = ?", (guest_id,))
    conn.commit()

def get_guest_by_id(guest_id):
    c.execute("SELECT * FROM guests WHERE guest_id = ?", (guest_id,))
    return c.fetchone()

def get_all_guests():
    c.execute("SELECT * FROM guests")
    return c.fetchall()

# Streamlit UI
st.title("Hotel Management System")

# Guest Form
st.sidebar.header("Guest Management")
action = st.sidebar.selectbox("Action", ["Add Guest", "Update Guest", "Delete Guest"])

if action == "Add Guest":
    name = st.sidebar.text_input("Name")
    phone = st.sidebar.text_input("Phone")
    email = st.sidebar.text_input("Email")
    
    if st.sidebar.button("Add Guest"):
        if name and phone and email:
            guest_id = add_guest(name, phone, email)
            st.sidebar.success(f"Guest added successfully with Guest ID: {guest_id}")
        else:
            st.sidebar.error("All fields are required")

elif action == "Update Guest":
    guest_id = st.sidebar.text_input("Guest ID")
    
    if guest_id:
        guest = get_guest_by_id(guest_id)
        if guest:
            name = st.sidebar.text_input("Name", guest[1])
            phone = st.sidebar.text_input("Phone", guest[2])
            email = st.sidebar.text_input("Email", guest[3])
            
            if st.sidebar.button("Update Guest"):
                if name and phone and email:
                    update_guest(guest_id, name, phone, email)
                    st.sidebar.success("Guest updated successfully")
                else:
                    st.sidebar.error("All fields are required")
        else:
            st.sidebar.error("Guest not found")

elif action == "Delete Guest":
    guest_id = st.sidebar.text_input("Guest ID")
    
    if st.sidebar.button("Delete Guest"):
        if guest_id:
            delete_guest(guest_id)
            st.sidebar.success("Guest deleted successfully")
        else:
            st.sidebar.error("Guest ID is required")

# Display Guests
st.header("Guest List")
guests = get_all_guests()
if guests:
    guest_df = pd.DataFrame(guests, columns=["ID", "Name", "Phone", "Email"])
    st.dataframe(guest_df)
else:
    st.write("No guests found")

# Close the database connection when the script ends
def close_connection():
    conn.close()

atexit.register(close_connection)
