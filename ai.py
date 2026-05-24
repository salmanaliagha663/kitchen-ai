import streamlit as st
import os
from google import genai

# --- 1. PAGE SETUP (Wide Layout for Multi-Column Grid) ---
st.set_page_config(
    page_title="My Fridge Food AI",
    page_icon="🍳",
    layout="wide"
)

# --- 2. API KEY INTEGRATION ---
# Bhai, jab aap new key banayein toh bas is quotes ke andar daal dena.
API_KEY = "AIzaSyB0EYJXgR4IYqF-OB5SO_m_7TbYEnmbrqk"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"🔑 API Key Issue: {str(e)}")
    st.stop()

# --- 3. CUSTOM CSS FOR CLEAN GRID & CARD LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333333; }
    
    /* Box titles */
    .section-title {
        color: #e67e22;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    /* Sticky Selected Ingredients Bar */
    .pantry-bar {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. ALL INGREDIENTS LIST (Screenshot Style Flat List) ---
# Saari common cheezain aik sath taake 3 ya 4 columns mein fit ho sakein
ALL_INGREDIENTS = [
    "Apples", "Baking Powder", "Bread", "Brown Sugar", "Butter / Margarine",
    "Chicken / Turkey", "Cheddar Cheese", "Cream Cheese", "Eggs", "Flour",
    "Garlic", "Garlic Powder", "Ginger", "Green Onions", "Honey", "Lemon",
    "Milk", "Mushrooms", "Mustard", "Mutton", "Beef", "Olive Oil", "Cooking Oil",
    "Onions / Shallots", "Pasta Noodles", "Potatoes (Aloo)", "Rice (Chawal)",
    "Tomatoes (Tamatar)", "Yogurt (Dahi)", "Hari Mirch", "Salt", "Red Chilli Powder"
]

# --- 5. APP LAYOUT ---
st.markdown('<p class="section-title">WHAT\'S IN YOUR FRIDGE?</p>', unsafe_allow_html=True)
st.caption("Select the ingredients you have right now to find matched recipes instantly.")
st.write("---")

# Split screen: Left side 75% for Grid Checkboxes, Right side 25% for Results & Action
col_left, col_right = st.columns([3, 1], gap="large")

selected_ingredients = []

# --- LEFT COLUMN: 3-COLUMN CHECKBOX GRID (Screenshot Style) ---
with col_left:
    st.write("**QUICK KITCHEN LIST:**")
    
    # 3 equal columns mein checkboxes divide karne ke liye
    grid_col1, grid_col2, grid_col3 = st.columns(3)
    
    # Pure ingredients list ko barabar 3 hisson mein divide kar ke columns mein fit karna
    for index, item in enumerate(ALL_INGREDIENTS):
        if index % 3 == 0:
            with grid_col1:
                if st.checkbox(item, key=f"item_{index}"):
                    selected_ingredients.append(item)
        elif index % 3 == 1:
            with grid_col2:
                if st.checkbox(item, key=f"item_{index}"):
                    selected_ingredients.append(item)
        else:
            with grid_col3:
                if st.checkbox(item, key=f"item_{index}"):
                    selected_ingredients.append(item)

    # Custom item input box at the end of the grid
    st.write("---")
    custom_item = st.text_input("➕ Any other ingredient? Type here (e.g. Capsicum):")
    if custom_item:
        custom_clean = custom_item.strip()
        if custom_clean and custom_clean not in selected_ingredients:
            selected_ingredients.append(custom_clean)

# --- RIGHT COLUMN: ACTIONS AND LIVE RESULTS ---
with col_right:
    st.write("**YOUR SELECTION:**")
    
    if selected_ingredients:
        # User ko live dikhana ke kya select hua hai
        st.markdown(
            f"""
            <div class="pantry-bar">
                <strong>📦 Selected ({len(selected_ingredients)}):</strong><br>
                {", ".join(selected_ingredients)}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Centralized action button inside right panel
        find_recipe_btn = st.button("🔍 Find Recipes", type="primary", use_container_width=True)
    else:
        st.info("You don't have any selected ingredients yet. Please check some items from the left side!")
        find_recipe_btn = False

# --- RECIPE OUTPUT SECTION (BELOW THE MAIN SCREEN WHEN BUTTON IS CLICKED) ---
if find_recipe_btn and selected_ingredients:
    st.write("---")
    st.markdown("## 🍽️ Matched Recipes For You")
    
    with st.spinner("⏳ Mixing ingredients and cooking recipes with Gemini AI..."):
        ingredients_str = ", ".join(selected_ingredients)
        
        prompt = f"""
        You are an expert chef analyzing ingredients available in a home kitchen.
        The user has checked these items: {ingredients_str}.
        
        Task:
        Provide exactly 3 practical recipes that can be quickly prepared using primarily these items.
        
        Format each recipe cleanly: