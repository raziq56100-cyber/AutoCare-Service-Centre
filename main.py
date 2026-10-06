import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from vehicle_module import Vehicle, PremiumVehicle


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoCare Service Centre",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# SERVICE LIST
# ============================================================

SERVICES = {
    "Engine Oil Change": 80.00,
    "Brake Service": 120.00,
    "Tire Replacement": 200.00,
    "Air Conditioning Service": 100.00,
    "Full Service": 250.00
}


# ============================================================
# SESSION STATE
# ============================================================

if "service_records" not in st.session_state:
    st.session_state.service_records = []


# ============================================================
# FUNCTION 1
# REGISTER CUSTOMER AND VEHICLE
# ============================================================

def register_customer_vehicle(
    customer_name,
    phone,
    registration_no,
    model,
    vehicle_type
):
    if vehicle_type == "Premium":
        return PremiumVehicle(
            customer_name,
            phone,
            registration_no,
            model
        )

    return Vehicle(
        customer_name,
        phone,
        registration_no,
        model,
        vehicle_type
    )


# ============================================================
# FUNCTION 2
# CALCULATE SERVICE CHARGE
# DEFAULT PARAMETER = FUNCTION OVERLOADING CONCEPT
# ============================================================

def calculate_service_charge(
    service_charge,
    quantity=1
):
    return service_charge * quantity


# ============================================================
# FUNCTION 3
# DISPLAY CUSTOMER AND VEHICLE INFORMATION
# ============================================================

def display_customer_vehicle_info(vehicle):

    st.subheader("Customer and Vehicle Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(
            f"**Customer Name:** {vehicle.customer_name}"
        )

        st.write(
            f"**Phone Number:** {vehicle.phone}"
        )

        st.write(
            f"**Registration Number:** "
            f"{vehicle.registration_no}"
        )

    with col2:
        st.write(
            f"**Vehicle Model:** {vehicle.model}"
        )

        st.write(
            f"**Vehicle Type:** {vehicle.vehicle_type}"
        )


# ============================================================
# MAIN GUI
# ============================================================

st.title("🚗 AutoCare Service Centre")

st.write(
    "Smart Car Service Centre Management "
    "and Analysis System"
)

st.divider()


# ============================================================
# CUSTOMER INFORMATION
# ============================================================

st.header("👤 Customer Information")

customer_name = st.text_input(
    "Customer Name",
    placeholder="Enter customer name"
)

phone = st.text_input(
    "Phone Number",
    placeholder="Example: 0123456789"
)


# ============================================================
# VEHICLE INFORMATION
# ============================================================

st.header("🚘 Vehicle Information")

col1, col2 = st.columns(2)

with col1:

    registration_no = st.text_input(
        "Vehicle Registration Number",
        placeholder="Example: ABC1234"
    )

    model = st.text_input(
        "Vehicle Model",
        placeholder="Example: Honda Civic"
    )

with col2:

    vehicle_type = st.selectbox(
        "Vehicle Type",
        [
            "Normal",
            "Premium"
        ]
    )


# ============================================================
# SERVICE SELECTION
# ============================================================

st.header("🔧 Service Selection")

selected_services = st.multiselect(
    "Select vehicle services:",
    list(SERVICES.keys())
)


# ============================================================
# DISPLAY SERVICE CHARGES
# ============================================================

if selected_services:

    st.subheader("Selected Services and Charges")

    service_preview = []

    for service in selected_services:

        charge = SERVICES[service]

        service_preview.append(
            {
                "Service": service,
                "Service Charge (RM)": charge
            }
        )

    preview_df = pd.DataFrame(
        service_preview
    )

    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CALCULATE BUTTON
# ============================================================

st.divider()

calculate_button = st.button(
    "Calculate Service Charge",
    type="primary"
)


# ============================================================
# CALCULATION AND VALIDATION
# ============================================================

if calculate_button:

    try:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not customer_name.strip():
            raise ValueError(
                "Customer name cannot be empty."
            )

        if not phone.strip():
            raise ValueError(
                "Phone number cannot be empty."
            )

        if not registration_no.strip():
            raise ValueError(
                "Vehicle registration number cannot be empty."
            )

        if not model.strip():
            raise ValueError(
                "Vehicle model cannot be empty."
            )

        if not selected_services:
            raise ValueError(
                "Please select at least one service."
            )

        if not phone.isdigit():
            raise ValueError(
                "Phone number must contain digits only."
            )

        if len(phone) < 10 or len(phone) > 11:
            raise ValueError(
                "Phone number must contain 10 or 11 digits."
            )

        # ----------------------------------------------------
        # CREATE VEHICLE OBJECT
        # ----------------------------------------------------

        vehicle = register_customer_vehicle(
            customer_name,
            phone,
            registration_no,
            model,
            vehicle_type
        )

        # ----------------------------------------------------
        # CALCULATE SERVICE CHARGES
        # ----------------------------------------------------

        total_charge = 0

        current_records = []

        for service in selected_services:

            charge = calculate_service_charge(
                SERVICES[service]
            )

            vehicle.add_service(
                service,
                charge
            )

            total_charge += charge

            current_records.append(
                {
                    "Customer": customer_name,
                    "Vehicle": model,
                    "Registration": registration_no,
                    "Vehicle Type": vehicle_type,
                    "Service": service,
                    "Service Charge (RM)": charge
                }
            )

        # Store current calculation
        st.session_state.service_records = current_records

        # ----------------------------------------------------
        # DISPLAY CUSTOMER INFORMATION
        # ----------------------------------------------------

        display_customer_vehicle_info(
            vehicle
        )

        # ----------------------------------------------------
        # DISPLAY SELECTED SERVICES
        # ----------------------------------------------------

        st.subheader("🔧 Selected Services")

        for service, charge in vehicle.service_charges:

            st.write(
                f"**{service}**: RM {charge:.2f}"
            )

        # ----------------------------------------------------
        # TOTAL CHARGE
        # ----------------------------------------------------

        st.success(
            f"💰 Total Service Charge: "
            f"RM {total_charge:.2f}"
        )

        # ----------------------------------------------------
        # PREMIUM VEHICLE DEMONSTRATION
        # ----------------------------------------------------

        st.subheader("OOP Demonstration")

        st.write(
            "Current object created:"
        )

        st.code(
            str(vehicle)
        )

        # Demonstrate PremiumVehicle inheritance
        premium_demo = PremiumVehicle(
            "Demo Customer",
            "0123456789",
            "DEMO123",
            "Toyota Camry"
        )

        premium_demo.add_service(
            "Engine Oil Change",
            80
        )

        combined_charge = (
            vehicle + premium_demo
        )

        st.write(
            f"Operator Overloading "
            f"(Vehicle + PremiumVehicle): "
            f"RM {combined_charge:.2f}"
        )

    except ValueError as error:

        st.error(
            f"⚠️ {error}"
        )


# ============================================================
# DATA ANALYSIS
# ============================================================

if st.session_state.service_records:

    st.divider()

    st.header(
        "📊 Vehicle Service Data Analysis"
    )

    # ========================================================
    # PANDAS DATAFRAME
    # ========================================================

    st.subheader(
        "1. Pandas DataFrame"
    )

    service_df = pd.DataFrame(
        st.session_state.service_records
    )

    st.dataframe(
        service_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # NUMPY ARRAY
    # ========================================================

    st.subheader(
        "2. NumPy Array"
    )

    charge_array = np.array(
        service_df[
            "Service Charge (RM)"
        ]
    )

    st.write(
        "Service Charge Array:"
    )

    st.write(
        charge_array
    )

    # ========================================================
    # ARRAY ATTRIBUTES
    # ========================================================

    st.subheader(
        "3. Array Attributes"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Shape",
            str(charge_array.shape)
        )

    with col2:

        st.metric(
            "Data Type",
            str(charge_array.dtype)
        )

    # ========================================================
    # INDEXING AND SLICING
    # ========================================================

    st.subheader(
        "4. Indexing and Slicing"
    )

    if len(charge_array) > 0:

        st.write(
            "First Service Charge:"
        )

        st.write(
            charge_array[0]
        )

        st.write(
            "First Two Service Charges:"
        )

        st.write(
            charge_array[:2]
        )

    # ========================================================
    # MATHEMATICAL ANALYSIS
    # ========================================================

    st.subheader(
        "5. Mathematical Analysis"
    )

    total_charges = np.sum(
        charge_array
    )

    average_charge = np.mean(
        charge_array
    )

    highest_charge = np.max(
        charge_array
    )

    lowest_charge = np.min(
        charge_array
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Charges",
            f"RM {total_charges:.2f}"
        )

    with col2:

        st.metric(
            "Average Charge",
            f"RM {average_charge:.2f}"
        )

    with col3:

        st.metric(
            "Highest Charge",
            f"RM {highest_charge:.2f}"
        )

    with col4:

        st.metric(
            "Lowest Charge",
            f"RM {lowest_charge:.2f}"
        )

    # ========================================================
    # FILTERING
    # ========================================================

    st.subheader(
        "6. Filtered Services"
    )

    filtered_df = service_df[
        service_df["Service Charge (RM)"] >= 100
    ]

    if not filtered_df.empty:

        st.write(
            "Services with charge RM100 and above:"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No service has a charge of RM100 or above."
        )

    # ========================================================
    # SORTING
    # ========================================================

    st.subheader(
        "7. Services Sorted by Charge"
    )

    sorted_df = service_df.sort_values(
        by="Service Charge (RM)",
        ascending=False
    )

    st.dataframe(
        sorted_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # MATPLOTLIB GRAPH
    # ========================================================

    st.subheader(
        "8. Service Charge Graph"
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    ax.bar(
        service_df["Service"],
        service_df["Service Charge (RM)"]
    )

    ax.set_title(
        "Vehicle Service Charges"
    )

    ax.set_xlabel(
        "Service"
    )

    ax.set_ylabel(
        "Service Charge (RM)"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    st.pyplot(fig)