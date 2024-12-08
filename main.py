import streamlit as st
import heapq
from collections import deque

# Initialize session state
if "users" not in st.session_state:
    st.session_state["users"] = []  # List of all users added so far
if "vip_queue" not in st.session_state:
    st.session_state["vip_queue"] = []  # Priority queue for VIP users
if "regular_queue" not in st.session_state:
    st.session_state["regular_queue"] = deque()  # Regular queue
if "booking_order" not in st.session_state:
    st.session_state["booking_order"] = []  # Order of booking


# Helper function to add users
def add_user(user_id, is_vip):
    # Check if the user_id already exists
    if any(user["User ID"] == user_id for user in st.session_state["users"]):
        return "Error: User ID already exists!"

    # Add user to the appropriate queue and the users list
    if is_vip:
        heapq.heappush(st.session_state["vip_queue"], (len(st.session_state["users"]), user_id))
        st.session_state["users"].append({"User ID": user_id, "VIP": "Yes"})
    else:
        st.session_state["regular_queue"].append(user_id)
        st.session_state["users"].append({"User ID": user_id, "VIP": "No"})
    return "User added successfully!"


# Helper function to generate booking order
def generate_booking_order():
    booking_order = []
    vip_queue_copy = st.session_state["vip_queue"][:]
    regular_queue_copy = list(st.session_state["regular_queue"])

    while vip_queue_copy:
        _, user_id = heapq.heappop(vip_queue_copy)
        booking_order.append({"User ID": user_id, "VIP": "Yes"})

    while regular_queue_copy:
        user_id = regular_queue_copy.pop(0)
        booking_order.append({"User ID": user_id, "VIP": "No"})

    st.session_state["booking_order"] = booking_order


# Streamlit App
st.title("Priority Queue-Based Ticket Booking System")

# Section for adding users
st.header("Add Users")
user_id = st.text_input("Enter User ID")
is_vip = st.checkbox("VIP User")
if st.button("Add User"):
    if user_id.strip():
        result = add_user(user_id.strip(), is_vip)
        if "Error" in result:
            st.error(result)
        else:
            st.success(result)
    else:
        st.error("Please enter a valid User ID.")

# Display the list of users who want to book tickets
st.header("Users Who Want to Book Tickets")
if st.session_state["users"]:
    st.table(st.session_state["users"])
else:
    st.write("No users added yet.")

# Button to generate booking order
if st.button("Book Tickets"):
    generate_booking_order()

# Display the booking order table
st.header("Order of Booking")
if st.session_state["booking_order"]:
    st.table(st.session_state["booking_order"])
else:
    st.write("No booking order generated yet.")

