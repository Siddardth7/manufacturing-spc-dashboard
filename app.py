import streamlit as st

st.set_page_config(
    page_title="SPC Manufacturing Quality Dashboard",
    layout="wide",
)

st.title("SPC Manufacturing Quality Dashboard")
st.markdown(
    "Statistical Process Control for composites and aerospace manufacturing. "
    "Use the sidebar to navigate between dashboard pages."
)

left, center, right = st.columns(3)

with left:
    st.subheader("Control Charts")
    st.write("Explore variables and attributes chart workflows.")

with center:
    st.subheader("Process Capability")
    st.write("Review capability indices and distribution views.")

with right:
    st.subheader("Live Simulation")
    st.write("Preview real-time disturbance and rule-violation flows.")

st.sidebar.success("Select a page above.")
