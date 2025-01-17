Lumo Pasos è un'applicazione per la gestione dell'illuminazione ambientale che consente di regolare luminosità e temperatura attraverso un interfaccia web consistente di due modalità, manuale e automatica.

# Funzionalità Principali

## 1. Modalità Manuale
La modalità manuale consente all'utente di impostare i parametri delle lampade a valori specifici:
- **Luminosità:** Regola l'intensità della luce.
- **Temperatura:** regola la tonalità (calda o fredda) della luce.

## 2. Modalità Automatica
La modalità automatica sfrutta una webcam installata sul controller delle luci per calibrarle in modo da ottenere i valori desiderati a livello ambientale, contrastando la luce naturale.
Ciò permette (in maniera più o meno approssimata a seconda della precisione della webcam e delle luci utilizzate) di mantenere un illuminazione costante a discapito dei fattori esterni.
- **Analisi ambientale:** La webcam cattura immagini per calcolare il colore medio dell'ambiente.
- **Adattamento dinamico:** La luce viene regolata automaticamente per approssimare l'illuminazione desiderata.

# Caratteristiche Tecniche

## Server Web Flask
- L'applicazione utilizza Flask per servire l'interfaccia web e gestire le richieste utente.
- Comunicazione in tempo reale tra client e server per l'applicazione delle modifiche.

## Analisi del Colore
- Calcolo dei valori medi di rosso, verde e blu (RGB) tramite OpenCV.
- Compensazione dell'illuminazione ambientale tramite formule che tengono in considerazione la natura del progetto: In alcuni casi risulta impossibile ottenere i risultati sperati
  (es. viene richiesta un illuminazione più scura di quella ambientale). In questo caso si effettua un approssimazione che punta al valore possibile più vicino a quello richiesto.
- L'analisi viene effettuata in tempo reale sul feedback della webcam e si autocorregge costantemente, confrontando i valori reali con quelli desiderati

## Interfaccia Utente
- **Modalità manuale:** Slider per personalizzare luminosità e temperatura.
- **Modalità automatica:** Regolazione automatica che approssima ai valori impostati negli input numerici, basata sui dati acquisiti dalla webcam.

# Istruzioni per l'Uso
Per avviare fare riferimento al Makefile (make server e make client) e modificare l'ip negli script all'indirizzo del broker MQTT. Docker non è ancora implementato.

## Modalità Manuale
- Attivare il controllo manuale e usare gli slider per regolare luminosità e temperatura ai valori desiderati per le lampade.

## Modalità Automatica
- Attivare il controllo automatico, impostare i valori desiderai a livello ambientale e lasciare che la webcam regoli i parametri.

# Tecnologie Utilizzate
- **Flask:** Framework per la gestione del server web.
- **HTML5, CSS3, Bootstrap:** Per un'interfaccia moderna e responsiva.
- **JavaScript:** Per l'interattività dell'interfaccia.
- **OpenCV:** Per l'elaborazione delle immagini catturate dalla webcam.
- **Paho MQTT:** Libreria per l'interfacciamento con broker MQTT per la comunicazione tra client e server.
- **Mosquitto:** Broker MQTT che abilita la comunicazione tra client e server.

# Autori
Lumo Pasos è stato sviluppato da:
- **Alessandro Dominici**
- **Jacopo Spitaleri**
- **Mactar Seck Ibrahima**
