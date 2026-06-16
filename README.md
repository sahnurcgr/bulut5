# ☁️ Bulut Tabanlı Akıllı Şehir Çevre İzleme ve Erken Uyarı Sistemi

Bu proje, akıllı şehir konseptleri (örneğin Ankara/Kızılay bölgesi) için tasarlanmış; çevresel faktörlerin gerçek zamanlı izlenmesini, sunucusuz (serverless) mimari ile depolanmasını ve kritik durumlarda otonom e-posta uyarıları üretilmesini sağlayan uçtan uca bir AWS IoT projesidir.

## 🚀 Proje Özellikleri

* **Gerçek Zamanlı Sensör Simülasyonu:** Edge (uç) cihazları simüle etmek amacıyla Python ile geliştirilmiş sistem. Ana akışı bloklamamak ve kesintisiz veri akışı sağlamak için veri üretimi ve gönderimi bağımsız bir **thread** üzerinde çalıştırılmıştır.
* **Güvenli Haberleşme (IoT & MQTT):** Cihazlar ve bulut arasındaki iletişim, 2048-bit TLS/SSL sertifikalarıyla şifrelenmiş MQTT protokolü üzerinden sağlanarak veri güvenliği (Confidentiality) maksimum seviyede tutulmuştur.
* **Sunucusuz Veritabanı Mimarisi (Serverless NoSQL):** Yüksek frekanslı zaman serisi verilerinin geleneksel ilişkisel veritabanlarında (RDBMS) yaratacağı darboğazları önlemek için, otomatik ölçeklenebilir (auto-scaling) Amazon DynamoDB tercih edilmiştir.
* **Canlı İzleme Paneli (Dashboard):** AWS CloudWatch üzerinde sıcaklık, nem ve karbonmonoksit seviyelerinin anlık olarak takip edilebildiği (Gauge ve Line grafikli) komuta kontrol paneli.
* **Otonom Alarm ve Uyarı (SNS):** Karbonmonoksit (CO) seviyesinin belirlenen statik kritik eşiği (50 ppm) aşması durumunda, CloudWatch Alarms ve Amazon SNS entegrasyonu ile yetkili birimlere saniyeler içinde otomatik acil durum e-postası iletilmesi.

## 🏗️ Sistem Mimarisi

1. **Uç Katman (Python):** Sensör verileri (Sıcaklık, Nem, CO) rastgele üretilir ve JSON formatına çevrilir.
2. **Mesajlaşma Katmanı (AWS IoT Core):** Mesajlar `sehir/cevre/kizilay` kanalı (topic) üzerinden AWS'ye ulaşır ve IoT Kural Motoru (Rule Engine) ile ayrıştırılır.
3. **Depolama Katmanı (Amazon DynamoDB):** Ayrıştırılan veriler kalıcı depolama için NoSQL tablosuna yazılır.
4. **İzleme ve Tepki Katmanı (CloudWatch & SNS):** Metrikler grafiğe dökülür; anomali durumunda SNS üzerinden e-posta tetiklenir.
