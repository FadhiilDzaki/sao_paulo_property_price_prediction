from unidecode import unidecode

def create_zone(df_inf):
    # delete "/São Paulo" pada 'District
    df_inf['District'] = df_inf['District'].replace({'/São Paulo':''},regex=True)
    # check
    df_inf.District.unique()

    # Menghapus diakritik
    df_inf['District'] = df_inf['District'].apply(unidecode)

    # check
    df_inf['District'].unique()

    # mengelompokkan district by zone
    district_to_zone = {
        # Downtown
        'Bela Vista': 'Downtown', 'Bom Retiro': 'Downtown', 'Consolacao': 'Downtown', 'Pari': 'Downtown',
        'Liberdade': 'Downtown', 'Republica': 'Downtown', 'Santa Cecilia': 'Downtown', 'Se': 'Downtown', 'Bras': 'Downtown',

        # West
        'Alto de Pinheiros': 'West', 'Barra Funda': 'West', 'Butanta': 'West', 'Jaguare': 'West',
        'Lapa': 'West', 'Perdizes': 'West', 'Pinheiros': 'West', 'Rio Pequeno': 'West',
        'Vila Leopoldina': 'West', 'Vila Madalena': 'West',

        # South Central
        'Campo Belo': 'South Central', 'Ipiranga': 'South Central', 'Itaim Bibi': 'South Central',
        'Jabaquara': 'South Central', 'Jardim Paulista': 'South Central', 'Moema': 'South Central',
        'Morumbi': 'South Central', 'Santo Amaro': 'South Central', 'Saude': 'South Central',
        'Vila Mariana': 'South Central', 'Vila Olimpia': 'South Central', 'Brooklin': 'South Central',

        # Southeast
        'Agua Rasa': 'Southeast', 'Aricanduva': 'Southeast', 'Cambuci': 'Southeast', 'Cursino': 'Southeast',
        'Mooca': 'Southeast', 'Sacoma': 'Southeast', 'Tatuape': 'Southeast', 'Vila Formosa': 'Southeast',
        'Vila Prudente': 'Southeast', 'Carrao': 'Southeast', 'Campo Grande': 'South Central',

        # Northeast
        'Belem': 'Northeast', 'Penha': 'Northeast', 'Sao Lucas': 'Northeast',
        'Sapopemba': 'Northeast', 'Vila Matilde': 'Northeast',

        # Far South
        'Campo Limpo': 'Far South', 'Capao Redondo': 'Far South', 'Cidade Ademar': 'Far South',
        'Cidade Dutra': 'Far South', 'Grajau': 'Far South', 'Jardim Angela': 'Far South',
        'Jardim Sao Luis': 'Far South', 'Pedreira': 'Far South', 'Socorro': 'Far South',
        'Vila Andrade': 'Far South', 'Vila Sonia': 'Far South',

        # Far East
        'Artur Alvim': 'Far East', 'Cangaiba': 'Far East', 'Cidade Lider': 'Far East',
        'Cidade Tiradentes': 'Far East', 'Ermelino Matarazzo': 'Far East', 'Iguatemi': 'Far East',
        'Itaim Paulista': 'Far East', 'Itaquera': 'Far East', 'Jardim Helena': 'Far East',
        'Jose Bonifacio': 'Far East', 'Lajeado': 'Far East', 'Parque do Carmo': 'Far East',
        'Sao Mateus': 'Far East', 'Sao Miguel': 'Far East', 'Sao Rafael': 'Far East',
        'Vila Curuca': 'Far East', 'Vila Jacui': 'Far East', 'Ponte Rasa': 'Far East', 'Guaianazes': 'Far East',

        # Northwest
        'Anhanguera': 'Northwest', 'Brasilandia': 'Northwest', 'Cachoeirinha': 'Northwest',
        'Freguesia do O': 'Northwest', 'Jaragua': 'Northwest',
        'Perus': 'Northwest', 'Pirituba': 'Northwest', 'Raposo Tavares': 'Northwest',
        'Sao Domingos': 'Northwest', 'Tremembe': 'Northwest', 'Limao': 'Northwest', 'Medeiros': 'Northwest',

        # North
        'Casa Verde': 'North', 'Jacana': 'North', 'Mandaqui': 'North', 'Santana': 'North',
        'Tucuruvi': 'North', 'Vila Guilherme': 'North', 'Vila Maria': 'North'
    }

    # kolom zone
    df_inf['Zone'] = df_inf['District'].map(district_to_zone)

    return df_inf