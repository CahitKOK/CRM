#-------------------------------
#-- CRM ANALITIGINE GIRIS
#-------------------------------

#CRM Müsteri iliskileri Yonetimi olarakta gecmektedir.

#KPI - Sirket departman ya da calisanlarin performanslarini degerlendirek icin kullanilan
##  matematiksel gosterlere denir. Temel performans gostergeleri olarak bilinmektedir.

## KPI Ornekleri
# Customer Acquistion Rate  (Musteri Kazanma Orani)
# Customer Retention Rate   (Musteri Elde Tutma Orani)
# Customer Churn Rate       (Musteri Terk Etme Orani)
# Conversion Rate           (Donusum Orani)
# Growth Rate               (Buyume Orani)

#-- Cohort Analizi
# Cohort : Ortak ozelliklere sahip bir grup insan demektir.
# Cohort Analizi :Ortak ozelliklere sahip insanlarin davranislarinin analizidir.

#-------------------------------
#-- RFM ile Musteri Segmentasynu
#-------------------------------

# RFM : Receny,Frequency,Monetary
# RFM Analizi Musteri segmentasyonu icin kullanilan bir tekniktir.
# Musterilerin satin alma aliskanliklari uzerinden gruplara ayrilmasi ve bu gruplar uzerinden ozel stratejiler gelistirmesidir
# CRM calismalari bircok baslikta veriye dayali aksiyon almayi saglar
#Recency  = Yenilik ,  Frequency  =  Siklik , Monetary  =   Parasal Değer anlamlarina gelmektedir.

#-------------------------------
#-- Is Problemi
#-------------------------------

#Bir e ticaret sirketinin musterilerini segmentlere ayirip bu segmentlere gore
## pazarlama stratejisi belirlemek isteniyor.

#Veri Seti İngilteredeki bir e ticaret sirketinin veri setidir
## https://archive.ics.uci.edu/ml/datasets/Online+Retail+II veri setinin buradan indirebilirsiniz.

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
## 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

#-- Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

#-------------------------------
#-- Veriyi Anlama
#-------------------------------

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None) # tum sutunlari goster
# pd.set_option('display.max_rows', None) # tum satirlari goster
pd.set_option('display.float_format', lambda x: '%.3f' % x) # Virgulden sonra kac sayiyi gormek icin yapilan ayar
df_ = pd.read_excel("C:/Users/trcah/PycharmProjects/pythonProject4/online_retail_II.xlsx" , sheet_name="Year 2009-2010")
#verimizi bilgisayarda bulundugu yerin idsini alarak okutuyoruz
df = df_.copy() #buyuk bir veri oldugu icin uzun surede tekrar tekrar veriyi cekmek yerine
## kopyasi uzerinde islem yaparak daha kisa surede veriyi cekebiliyoruz.
#Simdi veriyi incelemeye baslayabiliriz
df.head()
df.shape
df.isnull().sum() # Tum degiskenlerde toplam kac tane eksik deger ver
df["Description"].nunique() #Essiz urun deger sayisini bu komutla elde edebiliriz.

df["Description"].value_counts().head() # hangi urunden kacar tane oldugu
# Her bir urunden toplam kac tane siparis verildigine bakmak icin
df.groupby("Description").agg({"Quantity" : "sum" }).sort_values("Quantity",ascending=False).head()
#Urun isimlerinde kirilim yani gruplasma yaptiktan sonra  satilan urun adedine gore
## sum komutuyla toplam sayisini degerlerin ise ascending = False ile buyukten
### kucuge siralanmasini saglariz

df["Invoice"].nunique() # Toplam kac tane fatura kesildigini gosterir.
#Nunique komutunu hatirlayacak olursak bize kac farkli sinif oldugunu gosteriyordu
## Burada su yorumu yapmaliyiz ki her sinif bir faturayi temsil etmektedir.

#Veride bize bir faturaya toplam verilen parayi vermemisir.
##Bunu bulmak icin urun adedi ve fiyatini her fatura icin carpmamiz gerekir.
df["total_price"] = df["Quantity"]*df["Price"]
#Burada yeni bir degisken olusturup dataframede eklemis oluyoruz.
#Fatura basina dusen toplam miktari ogrenmek istersekde İnvoice degiskenini
## gruplastirmamiz gerekir cunku veride her urun icin ayri deger verilmistir.
df.groupby("Invoice").agg({"total_price":"sum"}).head(10)

from forex_python.converter import CurrencyRates

c = CurrencyRates()

print(c.get_rate('GBP', 'TRY'))
trycevir = c.get_rate('GBP', 'TRY')
df["total_price"] = df["total_price"]*trycevir
df.groupby("Invoice").agg({"total_price":"sum"}).head(10)

#-------------------------------
#-- Veriyi Hazirlama
#-------------------------------

#Veriyi okunabilir ve kullanibilir bir hale getirecegimiz kisimdir.
df.shape
df.isnull().sum() # Aykiri degerlerin direkt toplam sayisini gosterir
#CustomerID lerdeki eksikler direkt olarak silinir cunku fatura uzerınde isim yoksa ise yaramaz
##mantiginda olaya bakilmalidir.
df.dropna(inplace=True)#Aykiri degerleri siler inplace ile kalici olmasini saglar
#İadelerinde veriden cikarilmasi lazim
##İnvoice bolumunde basinda c olan degerler iadeleri temsil etmekteydi.
df.describe().T # Burada sayisal olarak degiskenlerin degerlerini incelerken
## İadelerden kaynakli aykiri degerlerin sonuclari etkiledigini negatif degerlerden
### anlayabiliriz.
#İade olan faturalari cikarmak icin
df = df[~df["Invoice"].str.contains("C", na=False)] #Burada koydugumuz tilda isareti ile
## yazdigimiz yerin haricindekileri getir islemi yapmis olduk

#-------------------------------
#-- RFM Metriklerinin Hesaplanmasi(Calculating RFM Metrics)
#-------------------------------

#Recency, Frequency, Monetary

df.head()
# Oncelikle bizim verinin tarih araligini bilip yapacagimiz tahmin icin bu tarihten
##sonraki bir zaman icin tahminde bulunulmasi gerekir.
# İlk olarak verinin alindigi son tarihe bir bakalim
df["InvoiceDate"].max()

today_date = dt.datetime(2010,12,11)
type(today_date)
#today_date kutuphanesinden tahmin edecegimiz tarihi bugunmus gibi almasini istiyoruz

rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda date : (today_date -date.max()).days,
                                     "Invoice" : lambda num : num.nunique(),
                                     "total_price" : lambda total_price: total_price.sum()})
#Burada yazmis oldugumuz fonksiyonun ilk maddesiyle aslinda Receny
##Yani musterinin en son ne zaman alisveris yaptigini
### Nunique invoice ile toplam kac tane faturasini oldugunu yani Frequency
#### total_price.sum() ile toplam yaptigi alisveris tutarini
##### Musterilerin idlerine gore gruplastirmis oluyoruz.

rfm.columns = ["Recency","Frequency","Monetary"] #Bu komut ile degisken isimlerini
## Bulmaya calistigimiz degerlerle degistiriyoruz.
### Bu tercihen yapilan bir seydir. Verinin okunabilirligini artirir.

rfm.head()
rfm.describe().T#Artik sayisal degerlerimizdeki negatif durum kalkmis durumda
##Boylece veriyi daha mantikli bir hale getirmis olduk
#Tekrar veriyi inceledigimizde monetary degerinin min degerinin 0 oldugunu goruyoruz
## 0 degerinde bir fatura olamayacagi icin bunlarida veriden kaldirammiz gerekir

rfm = rfm[rfm["Monetary"] > 0]

#-------------------------------
#-- RFM Skorlarinin Hesaplanmasi(Calculating RFM Scores)
#-------------------------------

#Receny Skoru
import pandas as pd
rfm["recency_score"] = pd.qcut(rfm["Recency"],5,labels=[5,4,3,2,1])
#Burada qcut fonksiyonu ile buyukten kucuge 5 e bolup
## Boldukten sonra labels = kismi ile isimlendiriyor.
#Monetary icinde 1 den puanlamaya baslamamiz yeterli
#Monetary Skoru
rfm["monetary_score"] = pd.qcut(rfm["Monetary"],5,labels=[1,2,3,4,5])

#Frequencyde verilen birbirine cok yakin oldugu ve degerlerin fazla oldugu icin
## qcut ile direkt olarak yukaridakiler gibi yaptigimizda hata aliriz
#Frequency Skoru
rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"),5,labels=[1,2,3,4,5])
#rank ile gordugun ilk degeri birinci olarak ata komutu vererek hatayi duzeltiyoruz.

rfm.head()

#RFM skoru icin receny ve frequency degerlerini bir arada yazmamiz gerekmektedir.

rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str)+
                    rfm["frequency_score"].astype(str))

rfm.describe().T #Yeni olusturulan degerler burada string ifadeler oldguu icin gozukmez

rfm[rfm["RFM_SCORE"] == "55"]

rfm[rfm["RFM_SCORE"] == "11"]

#-------------------------------
#-- RFM Segmentlerinin Olusturulmasi ve Analiz Edilmesi (Creating & Analysing RFM Segments)
#-------------------------------

#Regex ?

#RFM İsimlendirmesini nasıl yapıyoruz ?

seg_map = {
    r'[1-2][1-2]': 'hibernating',#1. elemanda 1-2 2.elemanda 1-2 gorursen bu isimlendirme
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising', #1. elemanda 4 2.elemanda 1. elemani gorursen diye ifade edilir.
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
#Oncelikle bu kisimda bir kutuphane olusturup genel skorda karsiliginda
## Bize elimizdeki degerin neyi ifade ettigini belirliyorz.
### Burada kullandigimiz regex bizim degere karsilik yapiyi yakalamamizi sagliyor.
# Her r' ifadesi regexi sembolize ediyor.

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map,regex=True)
#Bu ifade ile segment olarak atamasi yapilan deger
## rfm scorelara gore string komutu olan replace ile
### regex olacak ve seg_mapdaki degerler yakalanacak diye ifade edilmektedir.
#### Yani burada isimlendirmek istedigimiz kutuphaneyi replace ilk kismina yaziyoruz.

rfm[["segment","Recency","Frequency","Monetary"]].groupby("segment").agg(["mean","count"])
#Degiskenlerimizin segment degerlerini ortalama ve toplam sayi acisindan inceledik
## Artik is gelistirme anlaminda hitap etmemiz yani kaybetmemek icin calismamiz gereken
### musteri siniflarina yonelik pazarlama stratejileri gelistirmek icin
#### bu musterileri tespit etmeliyiz. Peki Bu islemi nasil yapiyoruz

rfm[rfm["segment"] == "cant_loose"].head()
# bunun gibi segmentler icinde string degeri buna esit olanlari cagirabiliriz.
## bu musterilerin sadece idlerine erismek istersek

rfm[rfm["segment"] == "cant_loose"].index #bu sekilde idleri alabiliriz.

new_df =pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["segment"] == "cant_loose"].index
#Yeni olusturdugumuz bir dataframe'in icine bu degerleri atiyoruz.
#Daha sonra daha okuabilir olmasi icin astype ile int olarak atamasini yapabiliriz.
new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)
#Bir Excel veya csv olarak almamiz gerektiginde
new_df.to_csv("new_customers.csv")

#-------------------------------
#-- Tüm Sürecin Fonksiyonlastirilmasi
#-------------------------------

def create_rfm(dataframe, csv=False):

    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=True)

