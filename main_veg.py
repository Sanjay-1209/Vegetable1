import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io


# Set page configuration for wide mode
st.set_page_config(layout="wide")


# Cache the function to improve performance for repeated operations
@st.cache
def load_data(filepath):
    """Load the Excel data from the specified sheet."""
    return pd.read_excel(filepath, sheet_name="8-1-2024")

def main():
    # Set the app title
    st.title("Welcome, Siddarth")

    # Upload the Excel file
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Load the DataFrame and clone it to ensure immutability
        df = load_data(uploaded_file).fillna(0)

        # Display the DataFrame
        # st.write("Data Overview:")

        with st.expander('View Uploaded Data'):

            # st.write("**View Raw Data**")
            st.dataframe(df)

            # Add a download button to export the DataFrame as Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                # writer.save()

            st.download_button(
                label="Download data as Excel",
                data=excel_buffer,
                file_name='vegetable_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

        # Create tabs for different sections
        tabs = st.tabs(['Data Vizualization', 'Compare Price', 'Price Rec.'])

        with tabs[0]:
            data_visualization(df)

        with tabs[1]:
            profit_analysis(df)

        with tabs[2]:
            st.subheader("Price Recommendation")
            price_recommendation(df)

def data_visualization(df):
    """Visualize data using bar and line charts."""
    # Select multiple vegetables to visualize
    all_vegetables = df['NAME'].unique()

    with st.sidebar:
        st.write("**𝑨𝒑𝒑𝒍𝒚 𝑭𝒊𝒍𝒕𝒆𝒓**")
        selected_vegs = st.multiselect("Select Vegetables", all_vegetables, default=all_vegetables)

        # Select websites
        all_websites = df.columns[2:].tolist()
        selected_websites = st.multiselect("Select Websites", all_websites, default=all_websites)

    if selected_vegs and selected_websites:
        # Filter the data for the selected vegetables and websites
        veg_data = df[df['NAME'].isin(selected_vegs)][['ID', 'NAME'] + selected_websites]

        # Melt DataFrame to work with Plotly
        melted_data = veg_data.melt(id_vars=['ID', 'NAME'], var_name='Website', value_name='Price')
        melted_data = melted_data[melted_data['Website'].isin(selected_websites)]

        # Bar graph using Plotly
        bar_fig = px.bar(
            melted_data,
            x='NAME',
            y='Price',
            color='Website',
            barmode='group',
            title="Price Comparison Across Selected Websites"
        )
        st.plotly_chart(bar_fig)

        # Line graph using Plotly
        line_fig = px.line(
            melted_data,
            x='NAME',
            y='Price',
            color='Website',
            markers=True,
            title="Price Trend Across Selected Websites"
        )
        st.plotly_chart(line_fig)

        # Additional insights or statistics
        if st.button('Show Statistics for Selected Vegetables'):
            st.write(veg_data.describe())

def profit_analysis(df):
    """Calculate and display profit margins."""
    # Calculate the profit for each vendor
    df["FAMILY_GARDEN_PROFIT"] = df["FAMILY_GARDEN_PRICE"] - df["VEGETABLE_MARKET_PRICE"]
    df["GRACE_SUPERMARKET_PROFIT"] = df["GRACE_SUPERMARKET_PRICE"] - df["VEGETABLE_MARKET_PRICE"]
    df["FRESH2DAY_PROFIT"] = df["FRESH2DAY_PRICE"] - df["VEGETABLE_MARKET_PRICE"]

    # Create a summary DataFrame
    summary_df = df[["NAME", "FAMILY_GARDEN_PROFIT", "GRACE_SUPERMARKET_PROFIT", "FRESH2DAY_PROFIT"]]

    # Display the summary DataFrame
    st.write("### Vegetable Price Comparison")
    st.dataframe(summary_df)

    # Add a download button to export the DataFrame as Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        summary_df.to_excel(writer, index=False, sheet_name='Sheet1')
        # writer.save()

    st.download_button(
        label="Download data as Excel",
        data=excel_buffer,
        file_name='Profit_Summary.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    plot_profit_margins_plotly(summary_df)

def plot_profit_margins_plotly(summary_df):
    """Plot profit margins using Plotly."""
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
        template="plotly_white",
        width=1300,   # Set the width of the chart
        height=900    # Set the height of the chart
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)


def price_recommendation(df):
    """Find the lowest price of each vegetable across different shops."""
    # Select relevant columns for comparison
    price_columns = ['FAMILY_GARDEN_PRICE', 'GRACE_SUPERMARKET_PRICE', 'FRESH2DAY_PRICE']

    # Calculate the minimum price for each vegetable across the selected columns
    lowest_price_df = df[['NAME'] + price_columns].copy()
    lowest_price_df['LOWEST_PRICE'] = lowest_price_df[price_columns].min(axis=1)

    # Create a DataFrame with the lowest price for each vegetable
    result_df = lowest_price_df[['NAME', 'LOWEST_PRICE']]

    # Display the DataFrame with the lowest prices
    st.write("### Lowest Price for Each Vegetable")
    st.dataframe(result_df)

    # Add a download button to export the DataFrame as Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()

    st.download_button(
        label="Download lowest price data as Excel",
        data=excel_buffer,
        file_name='Lowest_Price.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )

if __name__ == "__main__":
    main()
