import streamlit as st
from data_collection import fetch_active_satellites

st.title("Live Satellite Link Budget")

@st.cache_resource(ttl=60 * 60)  # refresh hourly
def load_satellite_data():
    return fetch_active_satellites()

sat_dict = load_satellite_data()

mode = st.radio("Link Direction", ("Uplink (Earth to Sat)", "Downlink (Sat to Earth)"))

# Satellite selection (orbit only)
st.header("Satellite Parameters")
sat_name = st.selectbox("Select a Satellite to Track", list(sat_dict.keys()))
selected_sat = sat_dict[sat_name]  # Skyfield EarthSatellite object

# Ground station
st.header("Ground Station Parameters")
gs_lat = st.number_input("Ground Station Latitude (degrees)", value=78.22875)
gs_lon = st.number_input("Ground Station Longitude (degrees)", value=15.39964)
gs_alt = st.number_input("Ground Station Altitude (meters)", value=458)
gs_min_elevation = st.number_input("Minimum Elevation Angle (degrees)", value=5.0)

# rf params based of link direction
st.header("Link RF Parameters")

if mode == "Uplink (Earth to Sat)":
    uplink_mhz = st.number_input("Uplink Frequency (MHz)", value=7200.0)

    # Ground TX
    st.subheader("Ground Station Transmit")
    gs_tx_power = st.number_input("Ground Station Transmit Power (dBW)", value=17.0)
    gs_tx_gain  = st.number_input("Ground Station TX Antenna Gain (dBi)", value=52.0)
    gs_tx_loss  = st.number_input("Ground Station TX Loss (dB)", value=1.5)

    # Satellite RX
    st.subheader("Satellite Receive")
    sat_rx_bandwidth_khz = st.number_input("Satellite Receive Bandwidth (kHz)", value=5000.0)
    sat_rx_bandwidth_hz  = sat_rx_bandwidth_khz * 1000.0
    sat_rx_noise_figure  = st.number_input("Satellite Receive Noise Figure (dB)", value=2.0)
    sat_rx_gain          = st.number_input("Satellite RX Antenna Gain (dBi)", value=0.0)
    sat_rx_loss          = st.number_input("Satellite Receive Loss (dB)", value=2.0)

    # frequency conversion
    gs_tx_frequency = uplink_mhz
    sat_rx_frequency = uplink_mhz

else:
    downlink_mhz = st.number_input("Downlink Frequency (MHz)", value=8200.0)

    # Satellite TX
    st.subheader("Satellite Transmit")
    sat_tx_power = st.number_input("Satellite Transmit Power (dBW)", value=10.0)
    sat_tx_gain  = st.number_input("Satellite TX Antenna Gain (dBi)", value=30.0)
    sat_tx_loss  = st.number_input("Satellite Transmit Loss (dB)", value=2.0)

    # Ground RX
    st.subheader("Ground Station Receive")
    gs_rx_bandwidth_khz = st.number_input("Ground Station Receive Bandwidth (kHz)", value=5000.0)
    gs_rx_bandwidth_hz  = gs_rx_bandwidth_khz * 1000.0
    gs_rx_noise_figure  = st.number_input("Ground Station Receive Noise Figure (dB)", value=1.2)
    gs_rx_gain          = st.number_input("Ground Station RX Antenna Gain (dBi)", value=52.0)
    gs_rx_loss          = st.number_input("Ground Station Receive Loss (dB)", value=1.0)

    # frequency conversion
    sat_tx_frequency = downlink_mhz
    gs_rx_frequency  = downlink_mhz
