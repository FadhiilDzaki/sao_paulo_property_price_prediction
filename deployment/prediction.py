# Import library
import pandas as pd 
import streamlit as st 
import pickle
from Feature_creation import create_zone

# Load Model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

def run():
    # Title
    st.title('SAO PAULO PROPERTY PRICE PREDICTOR')

    # Pemisah
    st.write('___')

    # Image
    st.image('https://motionarray.imgix.net/motion-array-1683137-l8c7novo30_avenidapaulistasp-1-high_0003.jpg?w=660&q=60&fit=max&auto=format')

    # load data
    df = pd.read_csv('sao-paulo-properties-april-2019.csv')

        # deskripsi
    st.write('''
            #Prediksi Harga Apartment
            ''')

    # Form
    with st.form(key='form parameter'):
        Condo = st.number_input('Biaya Service Bulanan',min_value=0, value=500)
        Size = st.number_input('Ukuran Apartemen',min_value=30, value=65)
        Rooms = st.number_input('Jumlah Ruangan',min_value=1, value=2)
        Toilets = st.number_input('Jumlah Toilet',min_value=1, value=2)
        Suites = st.number_input('Jumlah Ruangan',min_value=0, value=2)
        Parking = st.number_input('Slot Parkir',min_value=0, value=1)
        Elevator = st.selectbox("Apakah Ada Elevator?", [0, 1])
        Furnished = st.selectbox("Apakah Ada Sudah Termasuk Furnitur?", [0, 1])
        Swimming_Pool = st.selectbox("Apakah Ada Kolam Renang?", [0, 1])
        New = st.selectbox("Apakah Apartemen Baru?", [0, 1])
        District = st.selectbox("Distrik", df['District'].unique().tolist())
        Negotiation_Type = st.selectbox("Sewa/Jual", ['sale', 'rent'])
        Property_Type = st.selectbox("Tipe Properti", ['apartment'])
        Longitude = st.number_input('Longitude', min_value=-47.0, max_value=-45.0, value=-46.63, step=0.01)
        Latitude = st.number_input('Latitude', min_value=-24.0, max_value=-23.0, value=-23.55, step=0.01)
        
        submit = st.form_submit_button('Predict') 

    # inference
    data = [{
        'Condo': Condo,
        'Size' : Size,
        'Rooms': Rooms,
        'Toilets': Toilets,
        'Suites': Suites,
        'Parking': Parking,
        'Elevator': Elevator,
        'Furnished': Furnished,
        'Swimming Pool': Swimming_Pool,
        'New': New,
        'District': District,
        'Negotiation Type': Negotiation_Type,
        'Property_Type': Property_Type,
        'Longitude': Longitude,
        'Latitude': Latitude
    }]

    # to dataframe
    df_inf = pd.DataFrame(data)

    # show data
    st.dataframe(df_inf)

    # create zone
    df_inf = create_zone(df_inf)

    # predict
    if submit:
        pred = model.predict(df_inf)
        st.write(f'Prediksi Harga Apartment: {pred[0]:.0f} BRL')

if __name__ == '__main__':
    run()
