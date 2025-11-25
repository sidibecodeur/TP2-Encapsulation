import uuid
from datetime import datetime

class CompteBancaire:
    def __init__(self, solde_initial=0.0):
        self.__solde = solde_initial
        self.__id = str(uuid.uuid4())[:8]  # Identifiant unique court
        self.__operations = []  # Historique des opérations
        self._enregistrer_operation("Création du compte", solde_initial)
    
    def _enregistrer_operation(self, type_operation, montant):
        """Enregistre une opération dans l'historique avec horodatage"""
        operation = {
            'type': type_operation,
            'montant': montant,
            'solde_apres': self.__solde,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.__operations.append(operation)
    
    def deposer(self, montant):
        if montant > 0:
            self.__solde += montant
            self._enregistrer_operation("Dépôt", montant)
            return True
        return False

    def retirer(self, montant):
        if 0 < montant <= self.__solde:
            self.__solde -= montant
            self._enregistrer_operation("Retrait", montant)
            return True
        return False

    def get_solde(self):
        return self.__solde
    
    def get_id(self):
        return self.__id
    
    def get_operations(self):
        """Retourne une copie de l'historique des opérations"""
        return self.__operations.copy()
    
    def generer_releve(self):
        """Génère un relevé détaillé des opérations"""
        releve = f"=== RELEVÉ DU COMPTE {self.__id} ===\n"
        releve += f"Solde actuel: {self.__solde:.2f}€\n"
        releve += "Opérations:\n"
        
        for op in self.__operations:
            releve += f"  [{op['timestamp']}] {op['type']}: {op['montant']:>8.2f}€ (Solde: {op['solde_apres']:>8.2f}€)\n"
        
        return releve
    
    def __str__(self):
        return f"Compte {self.__id} - Solde: {self.__solde:.2f}€"


class Client:
    def __init__(self, nom):
        self.nom = nom
        self.comptes = []  # Liste pour gérer plusieurs comptes
    
    def ajouter_compte(self, solde_initial=0.0):
        """Ajoute un nouveau compte au client"""
        nouveau_compte = CompteBancaire(solde_initial)
        self.comptes.append(nouveau_compte)
        return nouveau_compte
    
    def get_compte_par_id(self, compte_id):
        """Retourne un compte spécifique par son ID"""
        for compte in self.comptes:
            if compte.get_id() == compte_id:
                return compte
        return None
    
    def afficher(self):
        """Affiche les informations du client et tous ses comptes"""
        print(f"\n=== CLIENT : {self.nom} ===")
        if not self.comptes:
            print("Aucun compte associé")
            return
        
        for i, compte in enumerate(self.comptes, 1):
            print(f"Compte {i}: {compte}")
    
    def afficher_solde_total(self):
        """Affiche le solde total de tous les comptes"""
        total = sum(compte.get_solde() for compte in self.comptes)
        print(f"Solde total de {self.nom}: {total:.2f}€")
        return total
    
    def generer_releve_complet(self):
        """Génère un relevé pour tous les comptes du client"""
        print(f"\n=== RELEVÉ COMPLET - {self.nom} ===")
        for compte in self.comptes:
            print(compte.generer_releve())
            print("-" * 50)


# Exemple d'utilisation détaillé
if __name__ == "__main__":
    print("=== SYSTÈME BANCAIRE - COMPOSITION ===")
    
    # Création d'un client avec plusieurs comptes
    client = Client("Yassir")
    
    # Ajout de plusieurs comptes
    compte_courant = client.ajouter_compte(1000)
    compte_epargne = client.ajouter_compte(500)
    
    print("✓ Comptes créés avec succès")
    
    # Opérations sur le compte courant
    compte_courant.deposer(300)
    compte_courant.retirer(50)
    compte_courant.deposer(150)
    
    # Opérations sur le compte épargne
    compte_epargne.deposer(200)
    compte_epargne.retirer(100)
    
    print("✓ Opérations bancaires effectuées")
    
    # Affichage des informations
    client.afficher()
    client.afficher_solde_total()
    
    # Génération des relevés
    client.generer_releve_complet()
    
    # Test avec un compte spécifique
    print("\n=== TEST ACCÈS COMPTE SPÉCIFIQUE ===")
    compte_id = compte_courant.get_id()
    compte_trouve = client.get_compte_par_id(compte_id)
    
    if compte_trouve:
        print(f"Compte trouvé: {compte_trouve}")
        print(f"Dernières opérations:")
        operations = compte_trouve.get_operations()
        for op in operations[-3:]:  # 3 dernières opérations
            print(f"  - {op['type']}: {op['montant']}€")
    
    # Test avec un client sans compte
    print("\n=== TEST CLIENT SANS COMPTE ===")
    client_sans_compte = Client("Marie")
    client_sans_compte.afficher()