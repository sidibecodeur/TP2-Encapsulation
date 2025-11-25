class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        self._titulaire = titulaire
        self.__solde = solde_initial
        self._operations = []  # Historique des opérations
        self._enregistrer_operation("Création du compte", solde_initial)
    
    def _enregistrer_operation(self, type_operation, montant):
        """Enregistre une opération dans l'historique"""
        self._operations.append({
            'type': type_operation,
            'montant': montant,
            'solde_apres': self.__solde,
            'timestamp': "simulé"  # En pratique, utiliser datetime.now()
        })
    
    def deposer(self, montant):
        if montant > 0:
            ancien_solde = self.__solde
            self.__solde += montant
            self._enregistrer_operation("Dépôt", montant)
            print(f"Dépôt de {montant} € effectué. Ancien solde: {ancien_solde} €, Nouveau solde: {self.__solde} €")
        else:
            print("Montant invalide. Le montant doit être positif.")

    def retirer(self, montant):
        if montant > 0 and montant <= self.__solde:
            ancien_solde = self.__solde
            self.__solde -= montant
            self._enregistrer_operation("Retrait", montant)
            print(f"Retrait de {montant} € effectué. Ancien solde: {ancien_solde} €, Nouveau solde: {self.__solde} €")
        else:
            print("Fonds insuffisants ou montant invalide.")

    @property
    def solde(self):
        return self.__solde
    
    @property
    def titulaire(self):
        return self._titulaire
    
    @property
    def operations(self):
        return self._operations.copy()  # Retourne une copie pour protéger l'original

    def __str__(self):
        return f"Titulaire : {self._titulaire}, Solde : {self.solde} €"
    
    def afficher_historique(self):
        """Affiche l'historique des opérations"""
        print(f"\nHistorique des opérations pour {self._titulaire}:")
        for op in self._operations:
            print(f"  - {op['type']}: {op['montant']} € (Solde: {op['solde_apres']} €)")


class CompteEpargne(CompteBancaire):
    def __init__(self, titulaire, solde_initial=0, taux_annuel=0.02):
        super().__init__(titulaire, solde_initial)
        self._taux_annuel = taux_annuel
    
    @property
    def taux_annuel(self):
        return self._taux_annuel
    
    def calculer_interet(self, periode_mois=12):
        """Calcule les intérêts pour une période donnée (en mois)"""
        interet = self.solde * self._taux_annuel * (periode_mois / 12)
        print(f"Intérêts calculés sur {periode_mois} mois: {interet:.2f} €")
        return interet
    
    def appliquer_interet(self, periode_mois=12):
        """Applique les intérêts au solde du compte"""
        interet = self.calculer_interet(periode_mois)
        if interet > 0:
            self.deposer(interet)
            self._enregistrer_operation("Intérêts", interet)
        return interet
    
    def __str__(self):
        return f"Compte Épargne - Titulaire : {self.titulaire}, Solde : {self.solde} €, Taux: {self.taux_annuel*100}%"


# Protection supplémentaire avec __setattr__
class CompteBancaireSecurise(CompteBancaire):
    def __setattr__(self, name, value):
        if name == 'solde' or name == '_CompteBancaire__solde':
            raise AttributeError(f"Modification directe de '{name}' interdite. Utilisez deposer() et retirer().")
        super().__setattr__(name, value)


if __name__ == "__main__":
    print("=== TEST COMPTE BANCAIRE DE BASE ===")
    compte = CompteBancaire("Ali", 1000)
    compte.deposer(200)
    compte.retirer(150)
    print(compte)
    print("Solde accessible (lecture) :", compte.solde)
    
    # Tentative de modification directe
    try:
        compte.solde = 500  # Ne fonctionnera pas
    except AttributeError as e:
        print(f"Erreur attendue: {e}")
    
    compte.afficher_historique()
    
    print("\n=== TEST COMPTE ÉPARGNE ===")
    compte_epargne = CompteEpargne("Sophie", 5000, 0.03)
    print(compte_epargne)
    compte_epargne.appliquer_interet(6)  # Intérêts sur 6 mois
    print(f"Solde après intérêts: {compte_epargne.solde} €")
    
    print("\n=== TEST COMPTE SÉCURISÉ ===")
    compte_securise = CompteBancaireSecurise("Jean", 2000)
    try:
        compte_securise.solde = 3000  # Devrait échouer
    except AttributeError as e:
        print(f"Erreur de sécurité: {e}")