import streamlit as st
import pandas as pd
import os

# --- Configuration and Initial Data ---

# Set page to wide mode for better table display
st.set_page_config(layout="wide")

st.title("Editable Excel Tracker")

# Define the path for the data file to persist changes
DATA_FILE = "tracker_data.csv"

# The list of columns that should be editable by the user.
# Note: The original 'Gear' column from the JSON is different from the new editable 'Gear'.
# To avoid conflict, I've renamed the new one 'Gear (Editable)'.
EDITABLE_COLUMNS = ["bnk-no", "Mk-Art of Die", "Ups", "Gear (Editable)", "Machine no"]

# --- Data from the HTML file ---
# This is the same data object from your original file's <script> tag.
INITIAL_SHEETS_DATA = {
    "ALL": [{"Customer": "A S ESSENTTIALS", "PRODUCT NAME": "JAMUNA MILK KHOVA & SWEETS W 1000ML BOTTOM IML LBL", "MK-ART": "IML-5922", "GEAR ": 134}, {"Customer": "AKSHAR PLASTIC", "PRODUCT NAME": "AKSHAR PLASTIC SWEET BOX NAGESHWAR LID 250ML + 500 ML", "MK-ART": "IML 8791 / 8792", "GEAR ": 123}, {"Customer": "BLOW PACKAGING", "PRODUCT NAME": "GULF AL ADBLUE 20 LTR 921.74*331.10MM-KANCHIPURAM", "MK-ART": "IML-8510", "GEAR ": 295}, {"Customer": "BMRAJ INDUSTRIES PVT LTD", "PRODUCT NAME": "AMUL CHEESE SPREAD YUMMY PLAIN 200G BOTTOM ( BARODA )", "MK-ART": "IML-3367-1", "GEAR ": 115}, {"Customer": "EMAAR POLYMER", "PRODUCT NAME": "MK-ART-IML8363 EMAAR POLYMERS FEPCON SS BUCKET BIRYANI 7 KG LID", "MK-ART": "IML-8363", "GEAR ": 205}, {"Customer": "ESSEE METAL CONTAINERS PVT LTD\t", "PRODUCT NAME": "ESSEE METAL GEETHAM LOGO LID", "MK-ART": "0", "GEAR ": 134}, {"Customer": "Eco Energy ", "PRODUCT NAME": "SKU:R500 BOTTOM / LID PADMA", "MK-ART": "IML-7683", "GEAR ": 111}, {"Customer": "GDK SOLUTIONS", "PRODUCT NAME": "MK-ART-IML8753 GDK SOLUTIONS BANSAL 250G TUB/ LID", "MK-ART": "IML-8753", "GEAR ": 99}, {"Customer": "J&L ENTERPRISE", "PRODUCT NAME": "MK-ART-IML8868 JK PLASTIC AMBUR BIRYANI 500-750G", "MK-ART": "IML-8868", "GEAR ": 144}, {"Customer": "JOLLY CONTAINERS KALARIA", "PRODUCT NAME": "1030005513-IML-7.5LTR KIRLOSKAR SUPER GENU OIL BPCL WITH INVISIBLE SECURITY CODE", "MK-ART": "IML-8354", "GEAR ": 218}, {"Customer": "JOLLY CONTAINERS-DAMAN", "PRODUCT NAME": "MK-ART-IML8936 JOLLY CONTAINER BUTTER PACK 200G ( TOP AND BOTTOM )", "MK-ART": "IML-8936", "GEAR ": 99}, {"Customer": "JOLLY CONTAINERS-MALANPUR", "PRODUCT NAME": "1030004340-IML - 20LTR ADBLUE ASHOK LEYLAND GULF WITH QR CODE", "MK-ART": "IML-8366-1", "GEAR ": 288}, {"Customer": "JOLLY PLAST PACKAGING PRIVATE LIMITED", "PRODUCT NAME": "1060000270-IML- 20LTR ADBLUE ASHOK LEYLAND GULF-LUDHIYANA", "MK-ART": "IML8366-1", "GEAR ": 288}, {"Customer": "JOLLY TECH PACKAGING PVT LTD ", "PRODUCT NAME": "IML-200ML ONE PURE ELEGANCE (NP) GRASIM", "MK-ART": "IML-7840", "GEAR ": 102}, {"Customer": "KANTAM KONTAINER", "PRODUCT NAME": "I-FLY MILKA MALAI BAR BOTTOM + TOP IML LBL MK-ART-IML7574-1", "MK-ART": "IML-7574-1", "GEAR ": 162}, {"Customer": "KANTAM KONTAINERS LLP / SHAZ ", "PRODUCT NAME": "MK-ART-IML5658-1 AMUL 1 LTR VANILLA MAGIC BOTTOM LABEL", "MK-ART": "IML-5658-1", "GEAR ": 162}, {"Customer": "KAY PLAST PRODUCT PVT.LTD.", "PRODUCT NAME": "RAJ FRESH IML 1 KG-BOTTOM (GEAR 124)", "MK-ART": "IML-3852", "GEAR ": 123}, {"Customer": "KAYVEE ENTERPRISE", "PRODUCT NAME": "MK-ART-IML6058 JK PLASTIC ANAND BHAVAN SWEET 250ML", "MK-ART": "6058", "GEAR ": 108}, {"Customer": "KRIPA PALSTOPACK LLP", "PRODUCT NAME": "KRIPA PLASTIC MAA'S CHOICE CASHEW STICKER 15 KG", "MK-ART": "IML-8944", "GEAR ": 288}, {"Customer": "KUMAR PAINTS & INSULATE INDUSTRIES", "PRODUCT NAME": "1 LTR ROUND 1ML RALLISON SURPRISE HIGH GLOSS EMULSION", "MK-ART": "IML-4291-1", "GEAR ": 111}, {"Customer": "LONG THAMES ENTERPRISE", "PRODUCT NAME": "WETECH COMERICH-75T NLGI", "MK-ART": "IML-8257", "GEAR ": 108}, {"Customer": "MAYURI KUMKUM LTD", "PRODUCT NAME": "BY-01 IML STICKER NO-01 DARK KISS + COCONUT", "MK-ART": "9022 / 2023", "GEAR ": 134}, {"Customer": "NAKODA PLAST INDUSTRIES PRIVATE LIMITED", "PRODUCT NAME": "NAKODA NITRO LB BIG IML", "MK-ART": "IML-5316", "GEAR ": 139}, {"Customer": "SAI BABA POLYMER TECHNOLOGIES PVT LTD-UNIT-VI (MUMBAI)", "PRODUCT NAME": "20 LTR IML GULF AL ADBLUE-KHALAPUR", "MK-ART": "IML-8434", "GEAR ": 295}, {"Customer": "SENTHIL PLASTIC", "PRODUCT NAME": "RKG AGMARK GHEE 5 LTR", "MK-ART": "IML-8654", "GEAR ": 200}, {"Customer": "SENTHIL PLASTIC CONTAINERS PVT LTD", "PRODUCT NAME": "20 LTR NIPPON PAINT WEATHERBOND ADVANCE WITH LAMINATION IML LBL", "MK-ART": "IML-7469", "GEAR ": 295}, {"Customer": "SENTHIL PLATIC CONTAINERS PVT LTD", "PRODUCT NAME": "4 LITRE NIPPON WEATHERBOND ADVANCE WITH LAMINATION IML LBL", "MK-ART": "IML-7467", "GEAR ": 205}, {"Customer": "SHREE JAGDISH PLASTIC", "PRODUCT NAME": "MK-ART-IML5830-3 SHRI JAGDISH MILTOP JAGGERY NEW DESIGN 900G", "MK-ART": "IML-5830-3", "GEAR ": 128}, {"Customer": "SHREE SHYAM PACKAGING", "PRODUCT NAME": "RECENT CHAM CHAM", "MK-ART": "IML-8682", "GEAR ": 282}, {"Customer": "SSF PLASTIC", "PRODUCT NAME": "SSF AACHI TWINKLE DISHWASH 500 G LID (GEAR 115)", "MK-ART": "IML-9095", "GEAR ": 102}, {"Customer": "SSF PLASTIC INDIA PVT LTD BADDI UNIT II", "PRODUCT NAME": "LABEL TUB IML VIM BAR 500G KURALI -64969841-RM-7061 PKD 05/2025", "MK-ART": "0", "GEAR ": 128}, {"Customer": "SSF PLASTICS INDIA PVT LTD-BADDI UNIT-2", "PRODUCT NAME": "LABEL : KISSAN MIXED FRUIT JAM 90 G -LABEL : KISSAN MIXED FRUIT JAM 90 G -", "MK-ART": "IML-6930-1", "GEAR ": 134}, {"Customer": "TERRA TECH PACKS ", "PRODUCT NAME": "HAIRBHAVAM ORANGE PEEL + FOIL IML LABEL-500 ML ROUND TUB", "MK-ART": "IML-7758", "GEAR ": 108}, {"Customer": "TRIMURTI IML SOLUTION PVT LTD", "PRODUCT NAME": "DLECTA CREAM CHEESE 180 SQUARE TUB + LID IML 825-5", "MK-ART": "825-5", "GEAR ": 102}, {"Customer": "YASH POLYMERS ", "PRODUCT NAME": "NIPPON PAINTS 4 LTR", "MK-ART": "IML-8296", "GEAR ": 181}]}


# --- Data Loading and Processing Functions ---

def get_initial_df():
    """
    Loads the initial hardcoded data into a Pandas DataFrame and prepares it.
    """
    df = pd.DataFrame(INITIAL_SHEETS_DATA["ALL"])
    
    # Clean up column names (e.g., remove trailing spaces)
    df.columns = df.columns.str.strip()

    # Add the new editable columns if they don't already exist
    for col in EDITABLE_COLUMNS:
        if col not in df.columns:
            df[col] = "" # Initialize with empty strings
    
    return df

def load_data():
    """
    Loads data from the CSV file if it exists, otherwise, loads the initial data.
    This function provides persistence.
    """
    if os.path.exists(DATA_FILE):
        try:
            # Load from CSV and ensure editable columns are treated as strings
            dtype_map = {col: 'str' for col in EDITABLE_COLUMNS}
            df = pd.read_csv(DATA_FILE, dtype=dtype_map)
            # Fill any potential NaN values in editable columns with empty strings
            for col in EDITABLE_COLUMNS:
                 if col in df.columns:
                    df[col] = df[col].fillna('')
            return df
        except Exception as e:
            st.error(f"Error loading data file: {e}. Loading initial data instead.")
            return get_initial_df()
    else:
        return get_initial_df()

# --- Main App Logic ---

# Load the data and store it in Streamlit's session state to prevent reloading on every interaction
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Create tabs (though there is only one sheet in the data)
tab1, = st.tabs(["ALL"])

with tab1:
    st.subheader("Data Table")
    
    # --- Column Filters ---
    st.text("Filter data by typing below each column header:")
    
    # Create a layout with one column for each filter input
    filter_cols = st.columns(len(st.session_state.df.columns))
    
    # Make a copy of the dataframe to apply filters
    filtered_df = st.session_state.df.copy()

    # Iterate over each column to create a text input for filtering
    for i, col_name in enumerate(filtered_df.columns):
        with filter_cols[i]:
            # Each filter widget needs a unique key
            filter_val = st.text_input(f"Filter {col_name}", key=f"filter_{col_name}")
            if filter_val:
                # Apply filter to the dataframe
                filtered_df = filtered_df[filtered_df[col_name].astype(str).str.contains(filter_val, case=False, na=False)]

    # --- Editable Data Table ---
    st.markdown("---")
    st.write("You can edit the cells in the columns: " + ", ".join(EDITABLE_COLUMNS))

    # Identify which columns should be disabled in the data editor
    all_columns = st.session_state.df.columns.tolist()
    disabled_cols = [col for col in all_columns if col not in EDITABLE_COLUMNS]

    # Display the data editor
    edited_df = st.data_editor(
        filtered_df,
        key="data_editor",
        num_rows="fixed", # "dynamic" would allow adding/deleting rows
        disabled=disabled_cols,
        use_container_width=True
    )

    # --- Save Changes ---
    # Check if any changes were made in the data editor
    if not filtered_df.equals(edited_df):
        # Update the main dataframe (in session state) with the changes from the edited (and possibly filtered) view.
        # The .update() method uses the dataframe's index to match rows, which is perfect for this.
        st.session_state.df.update(edited_df)
        
        # Save the updated main dataframe to the CSV file
        st.session_state.df.to_csv(DATA_FILE, index=False)
        st.toast("✅ Changes saved successfully!")