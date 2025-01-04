# import library
import pandas as pd 
import streamlit as st 

# library for visualization
import matplotlib.pyplot as plt 
import seaborn as sns

# stats
from scipy.stats import spearmanr, kendalltau, mannwhitneyu, f_oneway

# create zone
from Feature_creation import create_zone

def run():
    # OVERALL
    # fungsi cek deskriptif stats
    def check_deskriptif(df, kolom):
        '''
        Fungsi ini digunakan untuk mengetahui statistik deskriptif.

        Argumen:
        - df = DataFrame
        - kolom = List dari kolom numerik

        Return:
        - DataFrame yang berisi deskriptif statistik data.
        '''
        # deskriptif stats
        deskriptif = df[kolom].describe().T

        # List untuk menyimpan nilai
        skewness_values = []
        jenis_skewness = []

        # Loop untuk menghitung skewness dan kurtosis setiap kolom
        for i in kolom:
            # Menghitung skewness
            skew = df[i].skew()
            skewness_values.append(skew)
            
            # Menentukan jenis skewness
            if -0.5 <= skew <= 0.5:
                jenis_skewness.append('normal')
            else:
                jenis_skewness.append('skewed')

        # Membuat kolom baru dalam deskriptif
        deskriptif['skewness'] = skewness_values
        deskriptif['jenis_skewness'] = jenis_skewness

        return deskriptif

    # STATS
    # fungsi uji anova
    def uji_anova(df, group_col, value_col):
        '''
        Fungsi ini digunakan untuk melakukan uji ANOVA (Analysis of Variance).

        Argumen:
        - df = DataFrame
        - group_col = Nama kolom yang berisi grup/kategori
        - value_col = Nama kolom yang berisi nilai yang akan dianalisis
        
        output:
        - F-statistic, p-value, eta squared dari uji ANOVA
        '''
        # define unique value dari kolom kategorik
        unique = df[group_col].unique()
        
        # Mengelompokkan data berdasarkan kategori dalam group_col
        groups = [df[df[group_col] == i][value_col] for i in unique]
        
        # Melakukan uji ANOVA
        F_stat, p_value = f_oneway(*groups)

        # Menghitung SS_between
        grand_mean = df[value_col].mean()
        ss_between = sum([len(group) * ((group.mean() - grand_mean) ** 2) for group in groups])
        
        # Menghitung SS_total
        ss_total = sum((df[value_col] - grand_mean) ** 2)
        
        # Menghitung eta squared
        eta_squared = ss_between / ss_total
        
        # Tampilkan hasil
        print(f'F-statistic: {F_stat}')
        st.write(f'p-value: {p_value}')
        st.write(f'eta squared: {eta_squared}')

        # interpretasi pvalue
        if p_value < 0.05:
            st.write(f'H0 berhasil ditolak: terdapat perbedaan yang signifikan pada {value_col} terhadap {group_col}')
                # interpretasi korelasi
            if eta_squared < 0.01:
                st.write("Small effect size")
            elif eta_squared < 0.06:
                st.write("Medium effect size")
            else:
                st.write("Large effect size")
        else:
            st.write(f'H0 gagal ditolak: TIDAK terdapat perbedaan yang signifikan pada {value_col} terhadap {group_col}\n')
        
        return F_stat, p_value, eta_squared

    # uji mann whitney
    def uji_mannwhitney(df,kolom_1,kolom_2):
        '''
        argumen:
        kolom_1 = kolom yang ingin dibandingkan
        kolom_2 = kolom pembanding
        '''
        # list unique value
        unique = df[kolom_1].unique()

        # filtering per unique value
        df_a = df.loc[df[kolom_1] == unique[0], kolom_2]
        df_b = df.loc[df[kolom_1] == unique[1], kolom_2]

        # Mann-Whitney U Test
        stat, p_value = mannwhitneyu(df_a, df_b)
        print(f"U-Statistic: {stat}, P-Value: {p_value}")

        # hasil
        print(f'tstat = {stat}')
        st.write(f'pvalue = {p_value}')

        # kondisi tolak H0
        if p_value < 0.05:
            st.write(f'H0 berhasil ditolak: terdapat perbedaan yang signifikan pada {kolom_1} dan {kolom_2}\n')
        # kondisi gagal tolak H0
        else:
            st.write(f'H0 gagal ditolak: TIDAK terdapat perbedaan yang signifikan pada {kolom_1} dan {kolom_2}\n')
        
        # mengembalikan stat dan p value
        return stat,p_value

    # uji spearman
    def uji_spearman(df,kolom_1,kolom_2):
        '''
        Fungsi ini digunakan ketika igni melakukan uji korelasi dengan metode spearman (distribusi tidak normal)

        Argumen:
        - df = dataset
        - kolom_1 = kolom pertama yang ingin diuji korelasi
        - kolom_2 = kolom kedua yang ingin diuji korelasi
        '''
        # uji spearman
        corr_coef, p_value = spearmanr(df[kolom_1],df[kolom_2])

        # hasil
        st.write(f'koefisien corr = {corr_coef}')
        st.write(f'pvalue = {p_value}')

        # kondisi tolak H0
        if p_value < 0.05:
            st.write(f'H0 berhasil ditolak: {kolom_1} berkorelasi dengan {kolom_2}\n')
        # kondisi gagal tolak H0
        else:
            st.write(f'H0 gagal ditolak {kolom_1}  TIDAK berkorelasi dengan {kolom_2}\n')
        
        return corr_coef, p_value

    # fungsi uji kendall
    def uji_kendall(df,kolom_1, kolom_2):
        '''
        argumen:
        df = dataset
        kolom_1 = kolom fitur
        kolom_2 = kolom target
        '''    
        #uji stats
        stat, p_value = kendalltau(df[kolom_1],df[kolom_2])

        # hasil
        st.write(f'koefisien corr = {stat}')
        st.write(f'pvalue = {p_value}')

        # kondisi tolak H0
        if p_value < 0.05:
            st.write(f'H0 berhasil ditolak: {kolom_1} berkorelasi dengan {kolom_2}\n')
        # kondisi gagal tolak H0
        else:
            st.write(f'H0 gagal ditolak: {kolom_1} TIDAK berkorelasi dengan {kolom_2}\n')

        return stat, p_value


    # Title
    st.title("Sao Paulo Apartment Price Analysis")

    # garis pembatas
    st.write('___')

    # add image
    st.image('https://www.civitatis.com/f/brasil/sao-paulo/sao-paulo.jpg')

    # garis pembatas
    st.write('___')

    # load data
    df = pd.read_csv('sao-paulo-properties-april-2019.csv')

    # create zone
    df = create_zone(df)

    # show data
    st.dataframe(df)

    # overview data
    st.write('''
    **Dataset Overview:**\n
    Dataset memiliki 13640 baris dan 16 kolom:\n
        - Kategorik: 'Elevator', 'Furnished', 'Swimming Pool', 'New', 'District', 'Negotiation Type', 'Property Type', 'Latitude', 'Longitude'.
        - Numerik: 'Price', 'Condo', 'Size', 'Rooms', 'Toilets', 'Suites', 'Parking'.
    ''')

    # define numerik-kategorik
    num = ['Price', 'Condo', 'Size', 'Rooms', 'Toilets', 'Suites', 'Parking']
    cat = df.drop(columns=num).columns.to_list()

    # descriptive
    # numerik
    st.write('## Descriptive Statistik Numerik')

    # check descriptive
    desc = check_deskriptif(df,num)

    # show data
    st.dataframe(desc)

    # insight
    st.write('''
    **Price:**
    - *Median*: Median harga apartment adalah 8100 BRL.
    - *Standar Deviasi*: Standar deviasi yang sangat tinggi menunjukkan bahwa harga appartment sangat beragam (480 BRL - 10 juta BRL)
    - *Distribusi*: Distribusi data highly positive skew, menunjukkan bahwa mayoritas harga apartment berada di bawah 287737.8 dan beberapa berada di atasnya (hingga 10 juta BRL).

    **Condo:**
    - *Median*: Median biaya operasional apartment adalah 500 BRL.
    - *Standar Deviasi*: walaupun jauh lebih kecil dari 'Price', Standar deviasi 'Condo' juga dapat dikatakan sangat tinggi, menunjukkan bahwa biaya service appartment sangat beragam.
    - *Distribusi*: Distribusi data highly positive,menunjukkan bahwa mayoritas biaya operasional apartment berada di bawah 689.9 BRL dan beberapa berada di atasnya (hingga 9500 BRL).

    **Size**:
    - *Median*: Median ukuran apartment adalah  65m<sup>2</sup>. Median ini relatif kecil, yang menunjukkan kemungkinan sebagian besar apartment berpusat pada pasar perkotaan (compact).
    - *Standar Deviasi*: Standar deviasi kolom ini termasuk tinggi, menunjukkan ukuran apartment yang dijual memiliki variasi yang beragam (30m<sup>2</sup> - 880m<sup>2</sup>).
    - *Distribusi*: Distribusi data highly positive,menunjukkan bahwa mayoritas luas apartment berada di bawah 84.3m</sup>2<sup> dan beberapa berada di atasnya.

    **Rooms, Toilets, Suites dan Parking**:
    - *Median*: Sebagian besar apartment memiliki 2 kamar tidur, 2 toilet, 1 kamar tidur utama dan/atau 1 tempat parkir.
    - *Standar Deviasi*: Standar deviasi ke-empat kolom kecil menunjukkan bahwa variasinya yang tidak banyak.
    - Properti yang memiliki lebih dari 3 kamar tidur dan/atau lebih dari 5 mungkin menargetkan kalangan atas atau kelauarga besar.
    - Dengan sebagian besar porperty memiliki suites dapat mencerminkan apartment yang dijual kebanyakan modern.
    ''')

    # kategorik
    st.write('## Deskriptive statistik Kategorik')

    # define kolom yang tidak akan di plot
    skipped = ['Longitude', 'Latitude', 'District']

    # remove skipped column from list
    for i in skipped:
        # remove list
        cat.remove(i)

    # create canvas
    fig = plt.figure(figsize=(20,20))

    # loop histogram
    for idx,i in enumerate(cat):
        # urut dari terbanyak
        urut = df[i].value_counts(ascending=False).index
        
        # subplot 3x3
        plt.subplot(3,3,idx+1)
        
        # plot histogram
        ax=sns.countplot(x=df[i],order=urut)

        # add gridline
        plt.grid(True, linestyle = '--', color = 'grey', alpha = 0.3)
        # add title
        plt.title(i)
        # perlakuan kolom job
        if i=='job':
            # rotate x label 90 derajat
            plt.xticks(rotation=90)

        # menghitung panjang tiap bar
        total = float(len(df[i]))

        # loop untuk add persentase tiap kategori
        for p in ax.patches:
            # menghitung persentase per kategori
            percentage = '{:.1f}%'.format(100 * p.get_height() / total)
            
            # menghitung lebar x dan y
            x = p.get_x() + p.get_width() / 2 - 0.05
            y = p.get_height()

            # add persentase per kategori
            ax.annotate(percentage, (x, y), ha='center', va='bottom')

    # show plot
    st.pyplot(fig)

    # add skipped column to list
    for i in skipped:
        # add to list
        cat.append(i)

    # insight
    st.write('''
    **Elevator**:\n
    Sebagian besar (64.6%) apartment memiliki elevator. Hal in mengindikasikan bahwa sebagian besar apartment tidak berada di lantai dasar atau memiliki lebih dari 1 lantai, sehingga membutuhkan elevator untuk menuju ke apartment tersebut.

    **Furnished**:\n 
    Sekitar 85% apartment yang dijual telah memiliki furnitur di dalamnya.

    **Swimming Pool**:\n 
    Distribusi antara property yang memiliki kolam renang dan yang tidak relatif setara dengan property dengan kolam renang sedikit lebih banyak. Hal ini menandakan bahwa kepemilikian kolam renang tidak menjadi faktor yang memiliki pengaruh besar pada keputusan orang-orang dalam memilih property.

    **New**:\n 
    Hampir seluruh property (98.4%) berada dalam kondisi baru. Hal ini dapat mengindikasikan tingginya minat orang-orang dalam bisnis property di kota metropolitan seperti Sao Paulo ini.

    **Negotiation Type**:\n 
    Distribusi yang hampir setara antara apartment dijual dan disewa menandakan adanya pasar yang kompetitif antar keduanya. Namun, jumlah apartment disewakan yang sedikit lebih banyak dapat mengindikasikan demand yang tinggi atau ketersediaan yang lebih banyak.

    **Zone**:\n
    South Central São Paulo memiliki banyak unit apartemen yang dijual atau disewa karena berdasarkan [Wikitravel](https://wikitravel.org/en/S%C3%A3o_Paulo) daerah ini adalah pusat perusahaan dan memiliki banyak fasilitas yang menarik, seperti pusat perbelanjaan, restoran, dan transportasi yang mudah dijangkau. Selain itu, Daerah ini lebih strategis karena berdekatan dengan West Area yang merupakan pusat pemerintahan dan Downtown yang merupakan pusat pendidikan dan perkantoran.
    Sementara itu, daerah Northeast São Paulo memiliki jumlah unit apartemen yang paling sedikit untuk dijual atau disewa karena daerah ini lebih terfokus pada komunitas lokal dan memiliki lebih sedikit fasilitas komersial dan infrastruktur yang menarik bagi pendatang atau penghuni baru.
    ''')

    # inferential
    st.write('## Korelasi Target Dengan Setiap Fitur')

    st.write('''
            H0: Fitur-fitur tidak berkorelasi dengan Target.\n
            H1: Fitur-fitur berkorelasi dengan Target.
            ''')

    # loop uji korelasi
    for i in df:
        # exclude Price
        if i != 'Price':
            # kondisi jika price vs numerik
            if num:
                # nama kolom yang diuji
                st.write('')
                st.write(i)
                # uji spearmann
                uji_spearman(df,'Price',i)
                
            # kondisi jika price vs kategori
            else:
                # jika zone atau district
                if i == 'Zone' or i == 'District' or i == 'Longitude' or i == 'Latitude':
                    # nama kolm yang diuji
                    st.write('')
                    st.write(i)
                    # uji anova
                    uji_anova(df,i,'Price')

                # jika selain district dan zone
                else:
                    # nama kolomyang diuji
                    st.write('')
                    st.write(i)
                    # uji kendall
                    uji_kendall(df,'Price',i)

    # insight
    st.write("Hasil uji korelasi menunjukkan bahwa seluruh fitur memiliki korelasi dengan target. Fitur-fitur selain 'Zone', 'District', 'Longitude' dan 'Latitude' memiliki korelasi positif terhadap target. Ini menunjukkan bahwa tidak ada fitur yang benar-benar noise atau tidak penting.")


    # Harga
    st.write('## Distribusi Harga Apartment')

    # create canvas
    fig = plt.figure(figsize=(15,10))

    # visualization
    sns.histplot(df['Price'],kde=True,bins=40)

    # show plot
    st.pyplot(fig)

    # insight
    st.write('''
    Berdasarkan distribusi harga, tampak bahwa distribusi data highly positive skew, menunjukkan mayoritas properti berada dalam rentang harga yang lebih rendah/terjangkau, sementara beberapa properti dengan harga sangat tinggi.

    Terdapat 2 tipe penjualan properti dalam data, yaitu jual dan sewa dimana biasanya harga sewa lebih rendah daripada harga jual. Mayoritas properti bedara dalam rentang harga yang lebih rendah dapat disebabkan oleh hal tersebut.
            ''')

    # distribusi harga berdasarkan negotiation type
    st.write('### Distribusi Harga Berdasarkan Negotiation Type')

    # create canvas
    fig = plt.figure(figsize=(10,5))

    # histogram rent price vs sale price
    sns.histplot(x=df['Price'],
                hue=df['Negotiation Type'],
                bins=30)

    # add title
    plt.title('Rent Price vs Sale Price Distribution')

    # show plot
    st.pyplot(fig)

    # insight
    st.write('''
    Berdasarkan grafik, diketahui bahwa harga sewa kebanyakan berkumpul pada harga-harga rendah. Hal ini menunjukkan bahwa sebagian besar properti sewaan cenderung memiliki harga yang lebih terjangkau. Menyewa apartemen dapat menjadi alternatif bagi orang-orang yang ingin tinggal di sao paulo dengan biaya yang lebih terjangkau.

    Sebagian besar harga jual juga terkonsentrasi di kisaran harga rendah, tetapi distribusi harga jual lebih meluas dibandingkan harga sewa. Properti jual memiliki variasi harga yang jauh lebih besar, termasuk sejumlah kecil properti yang dijual dengan harga tinggi (hingga mendekati 10 juta).
    ''')

    # filter Negotiation Type = sell
    sale = df[df['Negotiation Type']=='sale']

    # filter Negotiation Type = rent
    rent = df[df['Negotiation Type']=='rent']

    # deskriptive apartment for sale
    desc = check_deskriptif(sale,['Price'])

    # show df
    st.dataframe(desc)

    # deskriptice apartment for rent
    desc = check_deskriptif(rent,['Price'])

    # show df
    st.dataframe(desc)

    # insight
    st.write('''
    Rata-rata harga properti yang dijual jauh lebih tinggi dari properti yang disewakan. Hal ini memperkuat bahwa market properti di Sao Paulo memiliki karakteristik yang sangat berbeda antara penjualan dan penyewaan apartemen.

    Rata-rata harga jual yang jauh lebih tinggi dibanding harga sewa menunjukkan bahwa kepemilikan apartemen mungkin hanya dapat diakses oleh segmen masyarakat dengan daya beli tinggi, sementara segmen lainnya lebih mengandalkan pasar sewa untuk memenuhi kebutuhan hunian mereka.
    ''')

    # Top 5 Area Dengan Median Harga Tertinggi
    st.write('## Top 5 Area Dengan Median Harga Tertinggi')

    # define top 5 columns
    top_5_col = ['Zone', 'District']

    # set figure
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    # loop barplot
    for idx, i in enumerate(top_5_col):
        # Sales Data
        # group by col & calculate median
        median_prices_sale = sale.groupby(i).agg({'Price': 'median'}).reset_index()
        # top 5 apart for sale
        top_5_sale = median_prices_sale.sort_values(by='Price', ascending=False).head(5)

        # axes Sale plot
        ax_sale = axes[0, idx]
        # bar plot
        sns.barplot(x='Price', y=i, data=top_5_sale, palette='pastel', ax=ax_sale)

        # add title
        ax_sale.set_title(f'Top 5 {i} with Highest median Sales Prices')
        # set x label
        ax_sale.set_xlabel('median Price (BRL)')
        # set y label
        ax_sale.set_ylabel(i)

        # loop Add annotations
        for p in ax_sale.patches:
            # get width
            width = p.get_width()
            # get height
            height = p.get_height()
            # add annotation
            ax_sale.text(width, p.get_y() + height / 2, f'{int(width)} BRL',
                        ha='right', va='center', color='white', weight='bold', fontsize=20)

        # Rent Data
        # group by col & calculate median
        median_prices_rent = rent.groupby(i).agg({'Price': 'median'}).reset_index()
        # top 5 apart for sale
        top_5_rent = median_prices_rent.sort_values(by='Price', ascending=False).head(5)

        # axes Sale plot
        ax_rent = axes[1, idx]
        # bar plot
        sns.barplot(x='Price', y=i, data=top_5_rent, palette='pastel', ax=ax_rent)

        # add title
        ax_rent.set_title(f'Top 5 {i} with Highest median Rent Prices')
        # set x label
        ax_rent.set_xlabel('median Price (BRL)')
        # set y label
        ax_rent.set_ylabel(i)

        # loop Add annotations
        for p in ax_rent.patches:
            # get width
            width = p.get_width()
            # get height
            height = p.get_height()
            # add annotation
            ax_rent.text(width, p.get_y() + height / 2, f'{int(width)} BRL',
                        ha='right', va='center', color='white', weight='bold', fontsize=20)

    # show plot
    st.pyplot(fig)

    # insight
    st.write('''
    - Zona Pusat Selatan dan Distrik Itaim Bibi serta Jardim Paulista menunjukkan potensi investasi yang kuat dengan harga yang konsisten tinggi.

    - Pengembangan Infrastruktur: Perkembangan infrastruktur dan fasilitas yang baik di area ini mungkin terus mendorong harga ke atas, menjadikannya pilihan utama untuk investasi jangka panjang.
    ''')

    # Top 5 Area Dengan Median biaya service Tertinggi
    st.write('## Top 5 Area Dengan Median biaya service Tertinggi')

    # define top 5 columns
    top_5_col = ['Zone', 'District']

    # set figure
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    # loop barplot
    for idx, i in enumerate(top_5_col):
        # Sales Data
        # group by col & calculate median
        median_Condos_sale = sale.groupby(i).agg({'Condo': 'median'}).reset_index()
        # top 5 apart for sale
        top_5_sale = median_Condos_sale.sort_values(by='Condo', ascending=False).head(5)

        # axes Sale plot
        ax_sale = axes[0, idx]
        # bar plot
        sns.barplot(x='Condo', y=i, data=top_5_sale, palette='pastel', ax=ax_sale)

        # add title
        ax_sale.set_title(f'Top 5 {i} with Highest median Sales Condos')
        # set x label
        ax_sale.set_xlabel('median Condo (BRL)')
        # set y label
        ax_sale.set_ylabel(i)

        # loop Add annotations
        for p in ax_sale.patches:
            # get width
            width = p.get_width()
            # get height
            height = p.get_height()
            # add annotation
            ax_sale.text(width, p.get_y() + height / 2, f'{int(width)} BRL',
                        ha='right', va='center', color='white', weight='bold', fontsize=20)

        # Rent Data
        # group by col & calculate median
        median_Condos_rent = rent.groupby(i).agg({'Condo': 'median'}).reset_index()
        # top 5 apart for sale
        top_5_rent = median_Condos_rent.sort_values(by='Condo', ascending=False).head(5)

        # axes Sale plot
        ax_rent = axes[1, idx]
        # bar plot
        sns.barplot(x='Condo', y=i, data=top_5_rent, palette='pastel', ax=ax_rent)

        # add title
        ax_rent.set_title(f'Top 5 {i} with Highest median Rent Condos')
        # set x label
        ax_rent.set_xlabel('median Condo (BRL)')
        # set y label
        ax_rent.set_ylabel(i)

        # loop Add annotations
        for p in ax_rent.patches:
            # get width
            width = p.get_width()
            # get height
            height = p.get_height()
            # add annotation
            ax_rent.text(width, p.get_y() + height / 2, f'{int(width)} BRL',
                        ha='right', va='center', color='white', weight='bold', fontsize=20)

    # show plot
    st.pyplot(fig)

    # insight
    st.write('''
    - Konsistensi Zona: Zona Selatan Tengah menunjukkan biaya service yang tinggi baik untuk jual maupun sewa, menunjukkan bahwa ini adalah area yang mungkin sangat ekslusif.
    - Ketertinggalan Distrik: Distrik Itaim Bibi dan Jardim Paulista menunjukkan biaya service yang sangat tinggi, menunjukkan bahwa ini adalah area yang sangat eksklusif dan mungkin memiliki banyak fasilitas yang menarik.
    ''')

    # Perbandingan Harga Apartment dengan Furnished dan Tidak
    st.write('## Perbandingan Harga Apartment dengan Furnished dan Tidak')

    # hipotesis
    st.write('H0: Tidak terdapat perbedaan yang signifikan pada Furnished dan Price.')
    st.write('H1: Terdapat perbedaan yang signifikan pada Furnished dan Price.')

    # uji mannhitney
    uji_mannwhitney(df,'Furnished','Price')

    # insight
    st.write('''
    Hasil uji mannwhitney menunjukkan bahwa rata-rata apparttemen yang sudah terisi furnitur dan yang belum signifikan berbeda. Untuk lebih jelasny, perhatikan grafik dibawah:
    ''')

    # set figure
    fig =plt.figure(figsize=(10, 6))

    # histogram  Furnished
    sns.kdeplot(df.loc[df['Furnished'] == 1, 'Price'], shade=True, label='Furnished', color='green')
    # histogram unfurnished
    sns.kdeplot(df.loc[df['Furnished'] == 0, 'Price'], shade=True, label='Unfurnished', color='orange')

    # set title
    plt.title('Distribusi Harga Apartment: Furnished vs Tidak')
    # set x label
    plt.xlabel('Harga (R$)')
    # add legend
    plt.legend()

    # show plot
    st.pyplot(fig)

    # group by
    grup = df.groupby('Furnished')['Price'].describe()

    # show
    st.dataframe(grup)

    # insight
    st.write('''
    Dapat dilihat bahwa Kedua kurva menunjukkan bahwa mayoritas apartemen berada di kisaran harga rendah. Puncak distribusi untuk apartemen unfurnished (oranye) lebih tinggi dibandingkan apartemen furnished (hijau), menunjukkan lebih banyak apartemen unfurnished yang tersedia di harga rendah.

    banyaknya apartemen yang dijual/disewa mungkin dapat mencerminkan Pembeli atau penyewa yang cenderung memilih apartemen unfurnished di kisaran harga yang lebih rendah, mungkin karena biaya awal yang lebih terjangkau atau preferensi untuk menata ruang mereka sendiri.
    ''')

    # Perbandingan Harga Apartment Baru dan Bekas
    st.write('## Perbandingan Harga Apartment Baru dan Bekas')

    # hipotesis
    st.write('H0: Tidak terdapat perbedaan yang signifikan pada harga apartemen baru dan tidak baru.')
    st.write('H1: Terdapat perbedaan yang signifikan pada  baru dan tidak baru.')

    # uji signifikansi
    uji_mannwhitney(df,'New','Price')

    # insight
    st.write('Hasil uji mannwhitney menunjukkan bahwa rata-rata harga apparttemen dengan kondisi baru dan tidak signifikan berbeda. Untuk lebih jelasnya, perhatikan grafik dibawah:')

    # set figure
    fig = plt.figure(figsize=(10, 6))

    # histogram  New
    sns.kdeplot(df.loc[df['New'] == 1, 'Price'], shade=True, label='New', color='green')
    # histogram Used
    sns.kdeplot(df.loc[df['New'] == 0, 'Price'], shade=True, label='Used', color='orange')

    # set title
    plt.title('Distribusi Harga Apartment: New vs Tidak')
    # set x label
    plt.xlabel('Harga (R$)')
    # add legend
    plt.legend()

    # show plot
    st.pyplot(fig)

    # Statistik deskriptif berdasarkan Furnished
    grup = df.groupby('New')['Price'].describe()

    # show
    st.dataframe(grup)

    # insight
    st.write('''
    - Puncak distribusi untuk apartemen bekas (oranye) lebih tajam di harga yang lebih rendah dibandingkan apartemen baru (hijau), menunjukkan bahwa lebih banyak apartemen bekas yang tersedia di harga rendah.
    - meskipun puncaknya lebih rendah, kurva apartemen baru menunjukkan distribusi harga yang lebih lebar, menunjukkan adanya variasi harga yang lebih besar.
    ''')



if __name__ == '__main__':
    run()