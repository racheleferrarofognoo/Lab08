from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        lista_impianti = self._impianti
        count = 0
        consumo_totale_mensile = 0
        lista_consumi_per_impianto = []
        for impianto in lista_impianti:
            impianto_corrente = impianto.nome
            consumi = impianto.get_consumi()
            for consumo in consumi:
                if mese == consumo.data.month:
                    consumo_totale_mensile = consumo_totale_mensile + consumo.kwh
                    count += 1
                    #lista di tutti i kwh di consumi di uno dei due impianti per un certo mese
            media = consumo_totale_mensile / count
            lista_consumi_per_impianto.append((impianto_corrente, media))

        return lista_consumi_per_impianto


    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        #caso terminale
        if giorno > 8:
            self.__costo_ottimo = costo_corrente
            self.__sequenza_ottima = sequenza_parziale
            return

        #caso ricorsivo
        for id_impianto, consumi in consumi_settimana.items(): #???????????????
            costo_giornaliero = consumi[giorno-1]

            if ultimo_impianto is None or id_impianto != ultimo_impianto: #se cambio impianto o sono al primo
                costo_giornaliero += 5






    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        consumi_dict = {}
        for impianto in self._impianti:
            consumi = impianto.get_consumi()
            consumi_al_giorno = []
            for consumo in consumi:
                if mese == consumo.data.month and consumo.data.day < 7:
                    consumi_al_giorno.append(consumi.kwh)
            consumi_dict[impianto.id] = sorted(consumi_al_giorno)

        return consumi_dict


