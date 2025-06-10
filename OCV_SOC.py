import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
 
def voltage_to_soc(voltage):
    soc_lookup = [
        (12.90, 100),
        (12.80, 95),
        (12.70, 90),
        (12.60, 85),
        (12.50, 75),
        (12.40, 60),
        (12.30, 50),
        (12.20, 40),
        (12.10, 30),
        (12.00, 20),
        (11.90, 10),
        (11.80, 0)
    ]
 
    if voltage >= soc_lookup[0][0]:
        return 100.0
    if voltage <= soc_lookup[-1][0]:
        return 0.0
 
    for i in range(len(soc_lookup) - 1):
        v_high, soc_high = soc_lookup[i]
        v_low, soc_low = soc_lookup[i + 1]
        if v_low <= voltage <= v_high:
            soc = soc_low + (voltage - v_low) * (soc_high - soc_low) / (v_high - v_low)
            return round(soc, 1)
    return None
 
st.set_page_config(page_title="Battery SOC Estimator", page_icon="🔋")
st.title("🔋 YUASA NPW45-12 Battery SOC Estimator")
 
voltage = st.number_input("Enter Battery Voltage (V)", min_value=10.0, max_value=13.0, step=0.01, value=12.5)
 
if st.button("Estimate SOC"):
    soc = voltage_to_soc(voltage)
    if soc is not None:
        st.success(f"Estimated State of Charge (SOC): **{soc}%**")
 
        # Data for plotting and table
        soc_lookup = sorted([
            (12.90, 100),
            (12.80, 95),
            (12.70, 90),
            (12.60, 85),
            (12.50, 75),
            (12.40, 60),
            (12.30, 50),
            (12.20, 40),
            (12.10, 30),
            (12.00, 20),
            (11.90, 10),
            (11.80, 0)
        ], key=lambda x: x[0])
 
        voltages, soc_values = zip(*soc_lookup)
 
        # Plot
        plt.figure(figsize=(8, 5))
        plt.plot(voltages, soc_values, marker='o', label='Voltage vs SOC curve')
        plt.scatter(voltage, soc, color='red', label=f'Input Voltage: {voltage} V\nEstimated SOC: {soc}%')
        plt.xlabel("Voltage (V)")
        plt.ylabel("State of Charge (%)")
        plt.title("YUASA NPW45-12 Battery Voltage vs SOC")
        plt.grid(True)
        plt.legend()
        plt.gca().invert_xaxis()  # Voltage decreases as SOC decreases
        st.pyplot(plt)
 
        # Show lookup table
        df = pd.DataFrame(soc_lookup, columns=["Voltage (V)", "SOC (%)"])
        st.subheader("Voltage to SOC Lookup Table")
        st.dataframe(df.style.format({"Voltage (V)": "{:.2f}", "SOC (%)": "{:.0f}"}))
 
    else:
        st.error("Voltage out of valid range (11.8 V – 12.9 V) for estimation.")
