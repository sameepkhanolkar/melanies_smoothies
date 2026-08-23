# Import Python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response.json())
sf_df =st.dataframe(data=smoothiefroot_response.json(),use_container_width=true)

# App title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Customer name
name_on_order = st.text_input("Name on Smoothie:")

if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Retrieve available fruits
my_dataframe = (
    session
    .table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
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
    max_selections=5
)

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        if not name_on_order.strip():
            st.warning("Please enter a name for your Smoothie.")

        else:

            my_insert_stmt = f"""
                INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (
                    NAME_ON_ORDER,
                    INGREDIENTS
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


# New section to display smoothiefroot nutrition information

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

# st.text(smoothiefroot_response.json())

sf_df = st.dataframe(
    data=smoothiefroot_response.json(),
    use_container_width=True
)