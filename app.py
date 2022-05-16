import pandas as pd
import streamlit as st
import os


st.set_page_config(page_title="Data Visualisation",
                   page_icon=":chart_with_upwards_trend:",
                   layout="wide")
curr_path = os.path.dirname(os.path.realpath(__file__))

df=pd.read_csv(curr_path + "/credit_data.csv")




#Side Bar
st.sidebar.header("Please Select filter here:")

check_acc=st.sidebar.multiselect("Select the checking account type",
                                 options=df['Checking_Amt'].unique(),
                                 default=df['Checking_Amt'].unique()
                                 )

Credit_His=st.sidebar.multiselect("Select the Credit History type",
                                 options=df['Credit_History'].unique(),
                                  default=df['Credit_History'].unique()
                                 )

Purpose=st.sidebar.multiselect("Select the Purpose",
                                 options=df['Purpose'].unique(),
                               default=df['Purpose'].unique()
                                 )

Savings_acc=st.sidebar.multiselect("Select the Saving account type",
                                 options=df['Savings_Amt'].unique(),
                               default=df['Savings_Amt'].unique()
                                 )

sex=st.sidebar.multiselect("Select the Saving account type",
                                 options=df['Personal_status'].unique(),
                                    default=df['Personal_status'].unique()
                                 )
CR=st.sidebar.multiselect("Select the Risk type",
                                 options=df['Credit_Risk'].unique(),
                                default=df['Credit_Risk'].unique()
                                 )
#Duration=st.sidebar.number_input("Enter duration:")


df_select=df.query(
    "Checking_Amt == @check_acc & Credit_History == @Credit_His & Purpose == @Purpose & Savings_Amt == @Savings_acc & Personal_status == @sex & Credit_Risk == @CR"
)



# ---- MAINPAGE ----
st.title(":bar_chart: Credit Risk Dashboard")
st.markdown("##")

# TOP KPI's
total= int(df_select["Credit_Risk"].sum())
average_Amount = round(df_select["Credit_Amt"].mean(), 1)

left_column, middle_column = st.columns(2)
with left_column:
    st.subheader("Average Credit Amount:")
    st.subheader(f"DM € {average_Amount:}")
with middle_column:
    st.subheader("Total Records:")
    st.subheader(f"{total}")


st.markdown("""---""")

st.dataframe(df_select)


#visualization
import plotly.express as px
fig=px.histogram(df_select, x='Personal_status', color="Credit_Risk", barmode='group',title="Personal status/sex Distribution with Risk")

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

fig2 = px.box(df_select, x="Credit_Risk", y="Age", color="Personal_status",title="Age Distribution with Risk")
fig2.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default


lf_col,rt_col=st.columns(2)
lf_col.plotly_chart(fig,use_container_width=True)
rt_col.plotly_chart(fig2,use_container_width=True)


fig3 = px.box(df_select, x="Credit_Risk", y="Credit_Amt", color="Credit_Risk",title="Credit Amount (in Deutsch Mark) Distribution with Risk")
fig3.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default

fig4 = px.box(df_select, x="Credit_Risk", y="Duration", color="Credit_Risk",title="Duration (in month) Distribution with Risk")
fig4.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default


lft_col,rgt_col=st.columns(2)
lft_col.plotly_chart(fig3,use_container_width=True)
rgt_col.plotly_chart(fig4,use_container_width=True)

fig5=px.histogram(df_select, x='Housing', color="Credit_Risk", barmode='group',title="Housing Distribution with Risk")
fig6=px.histogram(df_select, x='Savings_Amt', color="Credit_Risk", barmode='group',title="Saving Account Quality Distribution with Risk")

lbtm_col,rbtm_col=st.columns(2)
lbtm_col.plotly_chart(fig5,use_container_width=True)
rbtm_col.plotly_chart(fig6,use_container_width=True)