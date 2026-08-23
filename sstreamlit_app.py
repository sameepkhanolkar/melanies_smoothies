# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response.json())
sf_df =st.dataframe(data=smoothiefroot_response.json(),use_container_width=true)

# App title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Customer name
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Get active Snowflake session
session = get_active_session()

# Retrieve available fruits
my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

fruit_options = [
    row["FRUIT_NAME"]
    for row in my_dataframe.collect()
]

# Fruit selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=6
)

# Only show the button after ingredients are selected
if ingredients_list:

    # Join selected fruits without a trailing space
    ingredients_string = " ".join(ingredients_list)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if not name_on_order.strip():
            st.warning("Please enter a name for your Smoothie.")

        else:
            my_insert_stmt = f"""
                INSERT INTO smoothies.public.orders
                (
                    name_on_order,
                    ingredients
                )
                VALUES
                (
                    '{name_on_order}',
                    '{ingredients_string}'
                )
            """

            session.sql(my_insert_stmt).collect()

            st.success(
                f"Your Smoothie is ordered, {name_on_order}!",
                icon="✅"
            )
