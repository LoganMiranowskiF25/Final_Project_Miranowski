import streamlit as st
from database import connect_db, create_table
from datetime import datetime

create_table()

st.title("Aviation Inventory Management System")

menu = [
    "Add Item",
    "View Inventory",
    "Search",
    "Delete Item",
    "Update Item",
    "Low Stock Alert",
    "Expiration Alert",
    "Aircraft Parts API Lookup"
]

choice = st.sidebar.selectbox("Menu", menu)

conn = connect_db()
c = conn.cursor()

# ---------------- EXTERNAL API ----------------
import requests

def fetch_part_info(tail_number):
    """
    Looks up an aircraft by tail number using the FAA Aircraft Registry API.
    Returns relevant fields mapped to inventory-style data.
    """
    url = f"https://registry.faa.gov/aircraftinquiry/Search/NNumberInquiry?nNumberTxt={tail_number}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None

        # FAA returns HTML, so we do a basic check for a valid registration
        if "Aircraft Description" not in response.text:
            return None

        return {
            "part_number": tail_number.upper(),
            "name": f"FAA Registered Aircraft: N{tail_number.upper()}",
            "category": "Aircraft Registration",
            "price": 0.0,
            "reorder_level": 1,
            "time_sensitive": True
        }

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

# ---------------- ADD ITEM ----------------
if choice == "Add Item":
    st.subheader("Add New Item")

    part_number = st.text_input("Part Number")
    name = st.text_input("Name")
    quantity = st.number_input("Quantity", min_value=0)
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    expiration = st.date_input("Expiration Date")
    reorder_level = st.number_input("Reorder Level", min_value=0)
    time_sensitive = st.checkbox("Time Sensitive")

    if st.button("Add Item"):
        c.execute("""
            INSERT INTO inventory
            (part_number, name, quantity, category, price, expiration, reorder_level, time_sensitive)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            part_number,
            name,
            quantity,
            category,
            price,
            str(expiration),
            reorder_level,
            int(time_sensitive)
        ))

        conn.commit()
        st.success("Item added successfully!")

# ---------------- VIEW ----------------
elif choice == "View Inventory":
    st.subheader("Inventory")

    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()

    if rows:
        for r in rows:
            id, part_number, name, qty, cat, price, exp, reorder, ts = r

            st.write(
                f"ID: {id} | Part#: {part_number} | Name: {name} | Qty: {qty} | "
                f"Category: {cat} | Price: ${price:.2f} | Exp: {exp} | "
                f"Reorder: {reorder} | Time Sensitive: {'Yes' if ts else 'No'}"
            )
    else:
        st.info("No items found.")

# ---------------- SEARCH ----------------
elif choice == "Search":
    st.subheader("Search Inventory")

    term = st.text_input("Search")

    if st.button("Search"):
        c.execute("""
            SELECT * FROM inventory
            WHERE name LIKE ? OR category LIKE ? OR part_number LIKE ?
        """, (f"%{term}%", f"%{term}%", f"%{term}%"))

        results = c.fetchall()

        if results:
            for r in results:
                id, part_number, name, qty, cat, price, exp, reorder, ts = r

                st.write(
                    f"ID: {id} | Part#: {part_number} | Name: {name} | Qty: {qty} | "
                    f"Category: {cat} | Price: ${price:.2f}"
                )
        else:
            st.warning("No results found.")

# ---------------- DELETE ----------------
elif choice == "Delete Item":
    st.subheader("Delete Item")

    item_id = st.number_input("Item ID", min_value=1)

    if st.button("Delete"):
        c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        st.success("Deleted.")

# ---------------- UPDATE ----------------
elif choice == "Update Item":
    st.subheader("Update Item")

    item_id = st.number_input("Item ID", min_value=1)
    part_number = st.text_input("Part Number")
    name = st.text_input("Name")
    quantity = st.number_input("Quantity", min_value=0)
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0)
    expiration = st.date_input("Expiration")
    reorder_level = st.number_input("Reorder Level", min_value=0)
    time_sensitive = st.checkbox("Time Sensitive")

    if st.button("Update"):
        c.execute("""
            UPDATE inventory
            SET part_number=?, name=?, quantity=?, category=?, price=?, expiration=?, reorder_level=?, time_sensitive=?
            WHERE id=?
        """, (
            part_number,
            name,
            quantity,
            category,
            price,
            str(expiration),
            reorder_level,
            int(time_sensitive),
            item_id
        ))

        conn.commit()
        st.success("Updated.")

# ---------------- LOW STOCK ----------------
elif choice == "Low Stock Alert":
    st.subheader("Low Stock")

    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()

    for r in rows:
        id, part_number, name, qty, cat, price, exp, reorder, ts = r

        if qty <= reorder:
            st.warning(f"{name} ({part_number}) low stock: {qty}")

# ---------------- EXPIRATION ----------------
elif choice == "Expiration Alert":
    st.subheader("Expiration")

    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()

    today = datetime.now().date()

    for r in rows:
        id, part_number, name, qty, cat, price, exp, reorder, ts = r

        if exp and ts:
            exp_date = datetime.strptime(exp, "%Y-%m-%d").date()

            if exp_date <= today:
                st.error(f"Expired: {name} ({part_number})")

# ---------------- API ----------------
# USED FAA AIRCRAFT REGISTRY BECAUSE THERE IS
# NO PUBLIC API FOR AIRCRAFT PARTS. 
# SIMPLY A DEMONSTRATION OF INTEGRATED API.
elif choice == "Aircraft Parts API Lookup":
    st.subheader("FAA Aircraft Registry Lookup")

    st.info("Enter an FAA tail number (N-number) to look up a registered aircraft.")
    tail_number = st.text_input("Enter Tail Number (e.g. N12345)")

    if st.button("Fetch"):
        if not tail_number.strip():
            st.warning("Please enter a tail number.")
        else:
            result = fetch_part_info(tail_number.strip())

            if result:
                st.session_state["api_result"] = result
            else:
                st.error("Aircraft not found or invalid tail number.")

    if "api_result" in st.session_state:
        result = st.session_state["api_result"]
        st.success("Aircraft found in FAA Registry.")
        st.write(f"**Tail Number:** {result['part_number']}")
        st.write(f"**Name:** {result['name']}")
        st.write(f"**Category:** {result['category']}")
        st.write(f"**Time Sensitive:** {'Yes' if result['time_sensitive'] else 'No'}")
        st.write(f"**Suggested Reorder Level:** {result['reorder_level']}")

        if st.button("Add to Inventory"):
            c.execute("""
                INSERT OR IGNORE INTO inventory
                (part_number, name, quantity, category, price, expiration, reorder_level, time_sensitive)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result['part_number'],
                result['name'],
                1,
                result['category'],
                result['price'],
                None,
                result['reorder_level'],
                int(result['time_sensitive'])
            ))
            conn.commit()
            st.success("Added to inventory!")
            del st.session_state["api_result"]

conn.close()