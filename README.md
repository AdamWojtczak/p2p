# p2p

Siec dziala poprzez serwer,
odpal server i clientow zeby zobaczyc,
w klientach mozna wpisywac stringi i dojda do wszystkich innych klientow + siebie samego

chinolClient na ten moment nie potrafi korzystac z sieci, 
jak powinien dzialac:
  w funkcji start() petla while ktora sprawdza komunikaty i odpala rozczytanieKomunikatu()
    jeżeli komunikat mowi ze to tura tego klienta to break i wykonuje swoja ture
  poza tym tam gdzie pisales komentarze #wyslac komunikat w tych miejscach jest funkcja sendMsg ktora 
    wysyla na serwer a stamtad do wszystkich
    WAŻNE -> serwer wysyła komunikaty do wszystkich, nawet do tego od ktorego dostal
      na ten moment klient podczas swojego ruchu po prostu nie slucha
        i nie wiem co sie stanie jak potem odpali funkcje od odbierania stringow, mozliwe ze walna mu sie tam 3 na raz albo
          gorzej - exception na serwerze bo nie odbiera, mozna wstawic puste recv na kliencie zeby temu zapobiec jak cos
    
    
nie wiem dlaczego sie nie wlacza poprawnie, 
pewnie nie rozczytalem kodu dokladnie i nie umiem ustawic parametrow po prostu

[komunikat]
potrzebne jest przekazywanie tego czy ta tura bedzie nalezala do klienta, 
kolor klienta w stringu na ostatnim miejscu czy cos
