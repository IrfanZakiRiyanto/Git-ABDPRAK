import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gadget Sales Dashboard", layout="wide")


st.title("📊 Dashboard Laporan Penjualan Gadget Ah Tong")
st.markdown("""
Dashboard ini menampilkan **10 transaksi besar** terakhir di berbagai cabang Ah Tong di Indonesia. 
Data mencakup variasi kategori dari Smartphone, Laptop, hingga Console Game.
""")

st.image(
    "https://images.unsplash.com/photo-1593640408182-31c70c8268f5", 
    caption="Pusat Elektronik & Gadget", 
    use_container_width=True
)

data = pd.DataFrame({
    'Tanggal': pd.date_range(start='2024-11-01', periods=10, freq='D'),
    
    'Nama Produk': [
        'Xiaomi 14',          
        'iPhone 15 Pro',     
        'MacBook Air M4',     
        'Infinix GT 20 Pro',      
        'PlayStation 5',      
        'Samsung S24 Ultra',  
        'iPad Air M3',        
        'ROG Phone 8',        
        'Sony Headphone',     
        'iPhone 15 Pro'
    ],
    
    'Kategori': [
        'Smartphone', 'Smartphone', 'Laptop', 'Smartphone', 'Console',
        'Smartphone', 'Tablet', 'Smartphone', 'Aksesoris', 'Smartphone'
    ],
    
    'Kota Cabang': [
        'Jakarta', 'Surabaya', 'Balikpapan', 'Medan', 'Bandung',
        'Makassar', 'Yogyakarta', 'Samarinda', 'Denpasar', 'Jakarta'
    ],
    
    # Variasi jumlah barang yang terjual
    'Jumlah Terjual': [15, 5, 2, 20, 4, 3, 6, 2, 25, 8],
    
    # Omzet (Harga x Jumlah) -> Sengaja dibuat variatif angkanya
    'Omzet (Juta)': [150, 100, 40, 60, 32, 54, 48, 30, 75, 160],
    
    # Koordinat Peta (Tersebar di Indonesia)
    'lat': [-6.2088, -7.2575, -1.265, 3.5952, -6.9175, -5.1477, -7.7956, -0.502, -8.4095, -6.2088],
    'lon': [106.8456, 112.7521, 116.831, 98.6722, 107.6191, 119.4327, 110.3695, 117.153, 115.1889, 106.8456]
})

st.sidebar.header("🎛️ Panel Kontrol")
pilihan_grafik = st.sidebar.selectbox(
    "Pilih Jenis Visualisasi:",
    [
        "Bar Chart (Omzet per Produk)", 
        "Line Chart (Tren Penjualan Harian)", 
        "Area Chart (Akumulasi Pendapatan)", 
        "Pie Chart (Proporsi Kategori)", 
        "Map (Lokasi Transaksi)"
    ]
)

st.subheader(f"Tampilan: {pilihan_grafik}")

if "Bar Chart" in pilihan_grafik:
    st.write("Perbandingan Total Omzet (Juta Rupiah) setiap produk.")
    st.info("💡 Insight: iPhone 15 Pro dan Xiaomi 14 mendominasi pendapatan.")
    # Group by nama produk agar jika ada produk sama, nilainya dijumlahkan
    bar_data = data.groupby('Nama Produk')['Omzet (Juta)'].sum().sort_values(ascending=False)
    st.bar_chart(bar_data, color="#FF4B4B")

elif "Line Chart" in pilihan_grafik:
    st.write("Tren jumlah unit terjual dari tanggal 1 - 10 November.")
    st.info("💡 Insight: Terjadi lonjakan penjualan pada tanggal 4 dan 9 (Produk Murah & Aksesoris).")
    line_data = data.set_index('Tanggal')['Jumlah Terjual']
    st.line_chart(line_data, color="#0068C9")

elif "Area Chart" in pilihan_grafik:
    st.write("Tren Pendapatan Harian (Omzet).")
    area_data = data.set_index('Tanggal')['Omzet (Juta)']
    st.area_chart(area_data, color="#29B09D")

elif "Pie Chart" in pilihan_grafik:
    st.write("Persentase kontribusi setiap Kategori Barang.")
    
    fig, ax = plt.subplots()
    pie_data = data.groupby('Kategori')['Jumlah Terjual'].sum()
    # Warna custom agar cantik
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal') 
    st.pyplot(fig)

elif "Map" in pilihan_grafik:
    st.write("Peta persebaran lokasi cabang yang melaporkan penjualan.")
    st.map(data[['lat', 'lon']], zoom=4)

st.markdown("---")
st.write("### 📋 Detail Data Transaksi")
with st.expander("Klik untuk melihat tabel data mentah"):
    st.dataframe(data)