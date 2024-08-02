
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the Excel data
@st.cache
def load_data(filepath):
    return pd.read_excel(filepath, sheet_name="8-1-2024")

# Upload the Excel file
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Display the DataFrame
    st.write("Data Overview:")
    df = df.fillna(0)
    df

    tabs = st.tabs(['Data Viz', 'Test'])
    with tabs[0]:
        # Select multiple vegetables to visualize
        all_vegetables = df['NAME'].unique()
        selected_vegs = st.multiselect("Select Vegetables", all_vegetables, default=all_vegetables)

        # Select websites
        all_websites = df.columns[2:].tolist()
        selected_websites = st.multiselect("Select Websites", all_websites, default=all_websites)

        if selected_vegs and selected_websites:
            # Filter the data for the selected vegetables and websites
            veg_data = df[df['NAME'].isin(selected_vegs)][['ID', 'NAME'] + selected_websites]

            # Melting DataFrame to work with Plotly
            melted_data = veg_data.melt(id_vars=['ID', 'NAME'], var_name='Website', value_name='Price')

            # Filter for selected websites in melted data
            melted_data = melted_data[melted_data['Website'].isin(selected_websites)]

            # Bar graph using Plotly
            fig = px.bar(melted_data, x='NAME', y='Price', color='Website', barmode='group',
                        title="Price Comparison Across Selected Websites")
            st.plotly_chart(fig)

            # Line graph using Plotly
            fig2 = px.line(melted_data, x='NAME', y='Price', color='Website', markers=True,
                        title="Price Trend Across Selected Websites")
            st.plotly_chart(fig2)

            # Additional insights or statistics
            if st.button('Show Statistics for Selected Vegetables'):
                st.write(veg_data.describe())

    with tabs[1]:
        st.title("yet to Code")
        # Calculate the profit
        df["FAMILY_GARDEN_PROFIT"] = df["FAMILY_GARDEN_PRICE"] - df["VEGETABLE_MARKET_PRICE"]
        df["GRACE_SUPERMARKET_PROFIT"] = df["GRACE_SUPERMARKET_PRICE"] - df["VEGETABLE_MARKET_PRICE"]
        df["FRESH2DAY_PROFIT"] = df["FRESH2DAY_PRICE"] - df["VEGETABLE_MARKET_PRICE"]

        # Create a summary DataFrame
        summary_df = df[["NAME", "FAMILY_GARDEN_PROFIT", "GRACE_SUPERMARKET_PROFIT", "FRESH2DAY_PROFIT"]]

        # Display the DataFrame
        st.write("### Vegetable Price Comparison")
        st.dataframe(summary_df)

        # Plot the profit margins
        fig, ax = plt.subplots(figsize=(10, 6))
        summary_df.set_index("NAME").plot(kind="bar", ax=ax)
        plt.title("Profit Margin of Vegetables Across Websites")
        plt.ylabel("Profit (₹)")
        plt.xlabel("Vegetables")
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Websites')
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(fig)


        # Transform the DataFrame to a long format for Plotly
        melted_df = summary_df.melt(id_vars="NAME", var_name="Website", value_name="Profit")

        # Create a Plotly bar chart
        fig = px.bar(
            melted_df,
            x="NAME",
            y="Profit",
            color="Website",
            title="Profit Margin of Vegetables Across Websites",
            labels={"Profit": "Profit (₹)", "NAME": "Vegetables"},
            barmode="group",
            template="plotly_white"
        )

        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig)
