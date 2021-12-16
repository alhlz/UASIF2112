import matplotlib.pyplot as plt
import pandas as pd
import json
import streamlit as st
from PIL import Image
import numpy as np

# read and load json file 
readjson = open("kode_negara_lengkap.json")
dictjson = json.load(readjson)

# read csv file
readcsv = pd.read_csv("produksi_minyak_mentah.csv")

# print dan nampilin grafik produksi minyak
def prodMinyak():
    countryCode = 0
    dic = {}
    key_li = list(dictjson[0].keys())
    for key in key_li:
        dic[key] = []
    for i in dictjson:
        for key in key_li:
            dic[key].append(i[key])

    dfJson = pd.DataFrame(dic)
    dfCsv = readcsv
    countryList = dfJson["name"].tolist()
    n = st.selectbox("Pilih negara : ",countryList) 
    n = n.upper() # biar gampang divalidasi nanti

    for i in dictjson:
        countryName = str(i["name"]) # get nama negara di json
        if countryName.upper() == n: # validasi nama negara sama yang tadi diinput
            countryCode = str(i["alpha-3"]) # get kode_negara
            break
    
    showProd = readcsv.loc[readcsv["kode_negara"] == countryCode] # loc tempat si kode_negara di csv
    showProd.plot(kind="line", x="tahun", y="produksi", xlabel="Tahun", ylabel="Produksi", grid=True, title=("Grafik Produksi Tahunan " + n.capitalize())) # plotting
    st.pyplot(plt)

# global variabel buat efisiensi
st.set_option('deprecation.showPyplotGlobalUse', False)
global bigT, lowT, big, low

# print dan nampilin grafik produksi terbesar
def biggestProd(frommenu):
    global bigT, lowT
    sumprod = new_func()

    dic = {}
    key_li = list(dictjson[0].keys())
    for key in key_li:
        dic[key] = []
    for i in dictjson:
        for key in key_li:
            dic[key].append(i[key])

    dfJson = pd.DataFrame(dic)
    dfCsv = readcsv
    yearList = dfCsv["tahun"].tolist()
    t = st.selectbox("Pilih tahun: ",yearList)
    
    dfCsv = dfCsv[dfCsv["tahun"]==t] # spesifik ke tahunnnya
    kode_negara = dfCsv[dfCsv["tahun"]==t]["kode_negara"].tolist() # ambil kode negara dari tahun tsb jadiin list
    kode_negara = list(dict.fromkeys(kode_negara))# abis jadiin list, ambil yang unik aja jadi gaada duplikat

    produksi_maks = []
    negara_pertahun = []

    for kode in kode_negara:
        try:
            produksi = dfCsv[dfCsv["kode_negara"]==kode]["produksi"].tolist()#sekarang ambil data produksi per kode per tahun
            negara = dfJson[dfJson["alpha-3"]==kode]["name"].tolist()[0]#ambil negara nya sesuaiin sama kode negara nya
            produksi_maks.append(max(produksi))#ambil produksi maksimalnya ,masukin ke list produksi maks
            negara_pertahun.append(negara)#masukin nama negaranya ke list negara_pertahun
        except:
            continue
    
    dic = {"negara":negara_pertahun,"produksi_maks":produksi_maks}#jadiin dict
    lowT = pd.DataFrame(dic)#ubah ke dataframe pandas
    bigT = lowT.sort_values("produksi_maks",ascending=False).reset_index()#sort nilai produksi dari besar ke kecil
    
    if frommenu: # boolean buat penanda kalo ini emang panggilan dari menu
        numbList = list(range(1, 101))
        b = st.selectbox("Masukkan jumlah negara yang ingin ditampilkan: ",numbList)
        BigT = bigT[0:b] # cut sesuai jumlah b
        BigT.plot(kind="bar", x="negara", y="produksi_maks", xlabel="Kode Negara", ylabel="Produksi", grid=True, title=("Grafik " + str(b) + " Negara dengan Produksi Minyak Terbanyak Tahun " +str(t))) # plotting
        graph = plt.show()
        st.pyplot(graph)

def new_func():
    sumprod = dict() # dict baru buat bikin data baru
    return sumprod

# print dan nampilin grafik produksi terbesar kumulatif
def biggestCumul(frommenu):
    global big, low # panggil variabel global buat di overwrite
    
    sumcumul = dict() # dict baru buat bikin data

    for i in dictjson:
        countryCode = str(i["alpha-3"]) # get kode_negara
        found = False
        for j in range(len(readcsv)):
            if readcsv.iloc[(j), (0)] == countryCode: # di csv ada yang sesuai kode_negara
                found = True
                break
        if found: # proses buat masukin ke dict
            getCountryCode = readcsv.loc[readcsv["kode_negara"] == countryCode] # loc sesuai kode_negara
            sumcumul[countryCode] = getCountryCode.sum()["produksi"] # masukin ke dict

            newData = list(sumcumul.items()) # buat list dari dict tadi
            low = pd.DataFrame(data=newData, columns=["kode_negara", "produksi"]) # jadiin ke dataframe

    big = low.sort_values(["produksi"], ascending=[0]) # urutin dari yang paling besar produksinya
    
    if frommenu: # boolean buat penanda kalo ini emang dari panggilan menu
        numbList = list(range(1, 101))
        b = st.selectbox("Masukkan jumlah negara yang ingin ditampilkan: ",numbList)
        Big = big[0:b] # cut sesuai b
        #print(showBig)
        Big.plot(kind="bar", x="kode_negara", y="produksi", xlabel="Kode Negara", ylabel="Produksi", grid=True, title=("Grafik " + str(b) + " Negara dengan Produksi Minyak Kumulatif Terbanyak\n")) # plotting
        #plt.show()
        graphic = plt.show()
        st.pyplot(graphic)

# nampilin info negara produksi terbesar
def infoBigProd(choice, frommenu):
    global bigT, big 

    if choice == "T": # ini pada tahun X
        biggestProd(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        biggest = bigT.iloc[(0), (0)] # get row 0 col 0
        resultProd = bigT.iloc[(0), (1)] # get row 0 col 1
        
        for i in dictjson:
            if i["name"] == resultProd: # ketemu sesuai kode_negara
                st.write("Negara: ", str(i["name"]))
                st.write("Kode negara: ", str(i["country-code"]))
                st.write("Benua : ", str(i["region"]))
                st.write("Subbenua : ", str(i["sub-region"]))
                st.write("Total produksi : ", biggest)

    elif choice == "A": # ini kumulatif
        biggestCumul(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        biggest = big.iloc[(0), (0)] # get row 0 col 0
        resultProd = big.iloc[(0), (1)] # get row 0 col 1

        for i in dictjson:
            if str(i["alpha-3"]) == biggest: # ketemu sesuai kode_negara
                st.write("Negara: ", str(i["name"]))
                st.write("Kode negara: ", str(i["country-code"]))
                st.write("Benua : ", str(i["region"]))
                st.write("Subbenua : ", str(i["sub-region"]))
                st.write("Total produksi : ", resultProd)

    else:
        st.write("Masukkan tidak sesuai!")

# nampilin info negara produksi terkecil
def infoSmallProd(choice, frommenu):
    global lowT, low

    if choice == 'T': # tahun X
        biggestProd(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        sortLowest = lowT.sort_values(["produksi_maks"], ascending=[1]) # sort dari urutan produksi terkecil
        sortLowest = sortLowest.loc[sortLowest["produksi_maks"] > 0] # delete yang nilai produksinya 0
        lowest = sortLowest.iloc[(0), (0)] # get row 0 col 0
        resultProd = sortLowest.iloc[(0), (1)] # get row 0 col 1
    
        for i in dictjson:
            if i["name"] == lowest: # ketemu sesuai kode_negara
                st.write("Negara: ", str(i["name"]))
                st.write("Kode negara: ", str(i["country-code"]))
                st.write("Benua : ", str(i["region"]))
                st.write("Subbenua : ", str(i["sub-region"]))
                st.write("Total produksi : ", resultProd)

    elif choice == 'A': # kumulatif
        biggestCumul(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        sortLowest = low.sort_values(["produksi"], ascending=[1]) # sort dari urutan produksi terkecil
        sortLowest = sortLowest.loc[sortLowest["produksi"] > 0] # delete yang nilai produksinya 0
        lowest = sortLowest.iloc[(0), (0)] # get row 0 col 0
        resultProd = sortLowest.iloc[(0), (1)] # get row 0 col 1

        for i in dictjson:
            if str(i["alpha-3"]) == lowest: # ketemu sesuai kode_negara
                st.write("Negara: ", str(i["name"]))
                st.write("Kode negara: ", str(i["country-code"]))
                st.write("Benua : ", str(i["region"]))
                st.write("Subbenua : ", str(i["sub-region"]))
                st.write("Total produksi : ", resultProd)

    else:
        st.write("Masukkan tidak sesuai!")

# nampilin info negara produksinya nol
def infoNilProd(choice, frommenu):
    global lowT, low

    if choice == 'T': # tahun X
        biggestProd(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        searchNil = lowT.sort_values(["produksi_maks"], ascending=[1]) # sort dari urutan produksi terkecil
        searchNil = searchNil.loc[searchNil["produksi_maks"] == 0] # hanya yang nilai produksinya 0

        Nil = [] # deklarasi list
        for i in range(len(searchNil)):
            Nil.append(searchNil.iloc[(i), (0)]) # append list yang isinya kode_negara
    
        for j in range(len(Nil)): # iterasi sepanjang list Nil
            for i in dictjson:
                if Nil[j] == i["name"]: # ketemu sesuai kode_negara
                    st.write(str(i["name"]), "|", str(i["country-code"]), "|", str(i["region"]), "|", str(i["sub-region"]), "| 0")

    elif choice == 'A': # kumulatif
        biggestCumul(frommenu) # selalu set false biar ga execute yang if condition di fungsi tujuan
        searchNil = low.sort_values(["produksi"], ascending=[1]) # sort dari urutan produksi terkecil
        searchNil = searchNil.loc[searchNil["produksi"] == 0] # hanya yang nilai produksinya 0
        Nil = [] # deklarasi list
        for i in range(len(searchNil)):
            Nil.append(searchNil.iloc[(i), (0)]) # append list yang isinya kode_negara

        for j in range(len(Nil)): # iterasi sepanjang list Nil
            for i in dictjson:
                if Nil[j] == str(i["alpha-3"]): # ketemu sesuai kode_negara
                    st.write(str(i["name"]), "|", str(i["country-code"]), "|", str(i["region"]), "|", str(i["sub-region"]), "| 0")

    else:
        st.caption("Masukkan tidak sesuai!")

def aboutApp():
    st.caption("Aplikasi ini memberikan informasi mengenai data produksi minyak mentah dari berbagai negara di seluruh dunia. Melalui aplikasi ini, Anda dapat melihat dan menganalisis secara langsung data-data produksi minyak mentah tersebut, termasuk di antara tren produksi tahun ke tahun di negara pilihan Anda.")

# laman utama
def mainProgram():
    st.write("Alya Nissa Haliza 12220074 | UAS IF2112 Pemrograman Komputer")
    imageitb = Image.open("header.png")
    st.image(imageitb)
    image = Image.open("judul.png")
    st.image(image)

    #sidebar
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password")
    button_was_clicked = st.sidebar.button("\nSUBMIT")
    rate = st.sidebar.slider("Puaskah Anda dengan aplikasi kami?")
    st.sidebar.write("Tingkat kepuasan Anda: ", rate, "/100")

    st.subheader("Selamat datang di aplikasi informasi data produksi minyak mentah!")
    choice = st.selectbox("Silakan pilih menu aplikasi:", ("Tentang Kami", "Melihat Grafik Produksi Tahunan per Negara", "Melihat Daftar Negara dengan Produksi Terbanyak pada per Tahun",
                                                           "Melihat Daftar Negara dengan Produksi Kumulatif Terbanyak", "Melihat Informasi per Negara"))

    if choice == "Melihat Grafik Produksi Tahunan per Negara":
        prodMinyak() # cara manggil soal a
    elif choice == "Melihat Daftar Negara dengan Produksi Terbanyak pada per Tahun":
        biggestProd(True) # cara manggil soal b
    elif choice == "Melihat Daftar Negara dengan Produksi Kumulatif Terbanyak":
        biggestCumul(True) # cara manggil soal c
    elif choice == "Melihat Informasi per Negara":
        getChoice = st.selectbox("Pilih ketentuan pencarian informasi",("Produksi Terbanyak per Tahun", "Produksi Terbanyak Kumulatif", "Produksi Terkecil per Tahun",
                                                                        "Produksi Terkecil Kumulatif", "Produksi Nol per Tahun", "Produksi Nol Kumulatif"))
        if getChoice == "Produksi Terbanyak per Tahun":
            infoBigProd("T", False) # cara manggil soal d
        elif getChoice == "Produksi Terbanyak Kumulatif":
            infoBigProd("A", False) # cara manggil soal d
        elif getChoice == "Produksi Terkecil per Tahun":
            infoSmallProd("T", False) # cara manggil soal d
        elif getChoice == "Produksi Terkecil Kumulatif":
            infoSmallProd("A", False) # cara manggil soal d
        elif getChoice == "Produksi Nol per Tahun":
            infoNilProd("T", False) # cara manggil soal d
        elif getChoice == "Produksi Nol Kumulatif":
            infoNilProd("A", False) # cara manggil soal d

    elif choice == "Tentang Kami":
        aboutApp()
        
mainProgram()
