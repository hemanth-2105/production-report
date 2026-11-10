import streamlit as st
import plotly.express as px
import pandas as pd
from report import datas

st.set_page_config(
    page_title="Manufacturing Production Report",
    layout="wide"
)


left,right = st.columns([3,2])

with right:
    number_format= st.radio(
        "Display Format",
        ["Full","Thousands(K)","Lakhs(L)"],
        horizontal=True,
        index=0
    )

st.title("Manufacturing Production ")

file1 = datas(r"C:\Users\Hemnath Raj\Downloads\manufacturing_production_data.xlsx")

data = file1.f_path

file2 = datas(r"C:\Users\Hemnath Raj\Downloads\product_names.xlsx",process_date=False)

product_names = file2.f_path

data = pd.merge(
    data,
    product_names,
    on="Product",
    how="left"
)

data["Product Filter"] = (
    data["Product"].astype(str)+" - "+data["Product Description"].astype(str)
)

min_date = data["Date"].min().date()
max_date = data["Date"].max().date()


if st.sidebar.button("Reset filters"):
    st.session_state["start_date"] = min_date
    st.session_state["end_date"] = max_date
    st.session_state["products"] = data["Product Filter"].unique().tolist()
    st.session_state["departments"] = data["Department"].unique().tolist()
    st.session_state["shifts"] = data["Shift"].unique().tolist()

    st.rerun()

start_date = st.sidebar.date_input(
    "Pick a Starting Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="start_date"
)

end_date = st.sidebar.date_input(
    "Pick a Ending Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="end_date"
)


select_products = data["Product Filter"].unique().tolist()

select_products = st.sidebar.multiselect(
    "Select Products",
    options=select_products,
    default=select_products,
    key="products"  
)

select_department = data["Department"].unique().tolist()

select_department = st.sidebar.multiselect(
    "Select Department",
    options=select_department,
    default=select_department,
    key="departments"
)

select_shift = data["Shift"].unique().tolist()

select_shift = st.sidebar.multiselect(
    "Select Shift",
    options=select_shift,
    default=select_shift,
    key="shifts"
)


def format(value):
    if number_format =="Full":
        return f"{value:,.0f}"

    elif number_format =="Thousands(K)":
        return f"{value/1_000:,.1f}K"

    elif number_format =="Lakhs(L)":
        return f"{value/100_000:,.2f}L"

if select_department and select_products and select_shift and start_date<=end_date:

    data_filter = data[
        (data["Date"].dt.date >= start_date) &
        (data["Date"].dt.date <= end_date) &
        (data["Product Filter"].isin(select_products)) &
        (data["Department"].isin(select_department)) &
        (data["Shift"].isin(select_shift))
    ]

    col1,col2,col3,col4,col5 = st.columns(5)

    total_production = data_filter["Production"].sum()
    total_defects = data_filter["Defects"].sum()
    target_production = data_filter["Target Production"].sum()
    production_difference = total_production - target_production
    production_archievement = (total_production/target_production)*100
    data_filter["Production Difference"] = data_filter["Production"] - data_filter["Target Production"]

    col2.metric("Total Production",format(total_production))
    col1.metric("Target Production",format(target_production))
    col3.metric("Production Difference",format(production_difference))
    col5.metric("Defects",format(total_defects))
    col4.metric("Archievement",f"{production_archievement:.2f}%")

    tab1,tab2,tab3,tab4 = st.tabs([
        "Product",
        "Department",
        "Shift",
        "Daily Trend"
    ])

    with tab1:
        file1.f_path = data_filter
        product = file1.product_data()

        st.subheader("Product-wise Production")

        fig1 = px.bar(
            product,
            x="Product Description",
            y="Target_production",
            title="Target Production by Product",
            text="Target_production",
            color="Product",
            color_discrete_map={
                "Product A":"#E21717",
                "Product B":"#08A9D1",
                "Product C":"#B42565",
                "Product D":"#C9CC19"
            }
        )   
        fig1.update_traces(
            textposition = "outside"
        )

        fig1.update_layout(
            template = "plotly_white",
            xaxis_title = "Product",
            yaxis_title = "Target Production"
        )

        st.plotly_chart(fig1,use_container_width=True)

        file1.f_path = data_filter
        product = file1.product_data()

        st.subheader("Target Production vs Actual Proudction")

        fig9 = px.bar(
            product,
            x="Product Description",
            y=["Target_production","Production"],
            title="Target Production vs Actual Proudction",
            barmode="group",
            text_auto=True
        )

        fig9.update_traces(
            texttemplate="%{y:d}",
            textposition = "outside"
        )

        fig9.update_layout(
            template = "plotly_white",
            xaxis_title = "Product",
            yaxis_title = "Total Production and Actual Production",
            yaxis_tickformat="d",
        )

        st.plotly_chart(fig9,use_container_width=True)

        file1.f_path = data_filter
        product = file1.product_data()
        st.subheader("Product-wise Defects")        

        fig2 = px.bar(
            product,
            x="Product Description",
            y="Defect",
            title="Defects by Product",
            text="Defect",
            color="Product",
            color_discrete_map={
                "Product A": "#2563EB",
                "Product B": "#16A34A", 
                "Product C": "#7C3AED",
                "Product D": "#090514"
            }
        )

        fig2.update_traces(
            textposition = "outside"
        )

        fig2.update_layout(
            template = "plotly_white",
            xaxis_title = "Product",
            yaxis_title = "Defects"
        )

        st.plotly_chart(fig2,use_container_width=True)

        file1.f_path = data_filter
        product = file1.product_data()

        st.subheader("Product-wise Production")

        fig3 = px.pie(
            product,
            names="Product Description",
            values="Production",
            title="Production Archieved by Product",
            hole=0.2
        )

        fig3.update_traces(
            textinfo = "value+percent+label",
            textposition = "inside"
        )

        st.plotly_chart(fig3,use_container_width=True)

        st.write("Product Table")
        st.dataframe(product,hide_index=True)

    with tab2:
        file1.f_path = data_filter
        department = file1.department_data()

        st.subheader("Department-wise Production")
        fig4 = px.bar(
            department,
            x="Department",
            y="Target_production",
            title="Target Production by Department",
            text="Target_production",
            color="Department",
            color_discrete_map={
                "Assembley":"#DC2626",
                "Packaging":"#0891B2",
                "Quality Control":"#B95984",
                "Testing":"#CFD13F"
            }
        )
        fig4.update_traces(
            textposition = "outside"
        )

        fig4.update_layout(
            template = "plotly_white",
            xaxis_title = "Department",
            yaxis_title = "Target Production"
        )

        st.plotly_chart(fig4,use_container_width=True)

        file1.f_path = data_filter
        product = file1.department_data()
        
        st.subheader("Department-wise Defects")
        fig5 = px.bar(
            department,
            x="Department",
            y="Defect",
            title="Defects by Department",
            text="Defect",
            color="Department",
            color_discrete_map={
                "Assembly": "#2563EB",
                "Packaging": "#16A34A", 
                "Quality Control": "#7C3AED",
                "Testing": "#EA580C"
            }
        )

        fig5.update_traces(
            textposition = "outside"
        )

        fig5.update_layout(
            template = "plotly_white",
            xaxis_title = "Department",
            yaxis_title = "Defects"
        )

        st.plotly_chart(fig5,use_container_width=True)

        file1.f_path = data_filter
        product = file1.department_data()

        st.subheader("Department-wise Production")

        fig6 = px.pie(
            department,
            names="Department",
            values="Production",
            title="Production Archieved by Department",
            hole=0.4
        )

        fig6.update_traces(
            textinfo = "value+percent+label",
            textposition = "inside"
        )

        st.plotly_chart(fig6,use_container_width=True)

        st.write("Department Table")
        st.dataframe(department,hide_index=True)

    with tab3:
        file1.f_path = data_filter
        shift = file1.shift_data()

        fig7 = px.bar(
            shift,
            x="Shift",
            y="Production",
            title="Production by Shift",
            color="Shift",
            text="Production",
            color_discrete_map={
                "Morning": "#1555DF",
                "Afternoon": "#0FA5CA", 
                "Night": "#451E88"
            }
        )
        fig7.update_traces(
            textposition = "outside"
        )

        fig7.update_layout(
            template = "plotly_white",
            xaxis_title = "Shift",
            yaxis_title = "Production"
        )

        st.plotly_chart(fig7,use_container_width=True)
        st.write("Shift Table")

        st.dataframe(shift,hide_index=True)

    with tab4:
        file1.f_path = data_filter
        date = file1.daily_data()

        fig8 = px.line(
            date,
            x="Date",
            y=["Target_production","Production"],
            title="Target Production vs Actual Production",
            markers=True,
            hover_data=["Defect"],
            color_discrete_map={
                "Target_production":"#18D5DB",
                "Production":"#082BCA"
            }
        )
        fig8.update_layout(
            template = "plotly_white",
            xaxis_title = "Date",
            yaxis_title = "Target Production and Actual Production"
        )

        st.plotly_chart(fig8,use_container_width=True)

        file1.f_path = data_filter
        date = file1.daily_data()
        date["Cumulative"] = date["Production"].cumsum()

        fig11 = px.line(
            date,
            x="Date",
            y=["Cumulative","Production"],
            title="Daily Trend of Production",
            markers=True,
            hover_data=["Defect"],
            color_discrete_map={
                "Cumulative":"#18D5DB",
                "Production":"#082BCA"
            },
            line_dash="variable",
            line_dash_map={
                "Cumulative":"solid",
                "Production":"dot"
            }
        )

        fig11.update_layout(
            template = "plotly_white",
            xaxis_title = "Date",
            yaxis_title = "Production"
        )

        st.plotly_chart(fig11,use_container_width=True)

        st.dataframe(date,hide_index=True,height=300)

    fig10 = px.scatter(
    data_filter,
    x="Production",
    y="Defects",
    color="Department",
    hover_data=["Date"]
    )

    st.plotly_chart(fig10,use_container_width=True)

elif not select_department or not select_shift or not select_products:
    st.warning("Please select atleast one department, product and shift")

else:
    st.warning("Start date and End date must be between Jan-1 2024 to June-30 2024")

show_table = st.selectbox(
    "Pick a one",
    ["None","Data"]
)

try:
    if show_table == "Data":
        st.dataframe(data_filter,use_container_width=True,hide_index=True)
    else:
        st.caption("Please select the value")
except:
    exit()
