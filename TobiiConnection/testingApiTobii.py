import asyncio
from g3pylib import TobiiG3

# Adresse IP locale en mode point d'accès
G3_ADDRESS = "192.168.75.51"

async def main():
    # Étape 1 : Connexion aux lunettes
    glasses = TobiiG3(G3_ADDRESS)
    await glasses.connect()
    print("✅ Connecté aux Tobii Pro Glasses 3")

    # Étape 2 : Démarrer l'enregistrement
    await glasses.api("recorder!start", method="POST", body=[])
    print("🎥 Enregistrement démarré")

    # Étape 3 : Définir un nom lisible pour l'enregistrement
    await glasses.api("recorder.visible-name", method="POST", body="Test_Enregistrement")
    
    # Étape 4 : Ajouter un événement personnalisé
    await asyncio.sleep(2)  # Simuler un délai
    await glasses.api("recorder!send-event", method="POST", body=[
        "evenement", {"note": "Début de tâche"}
    ])
    print("📝 Événement ajouté")

    # Attendre un peu pendant que l'enregistrement tourne
    await asyncio.sleep(10)

    # Étape 5 : Arrêter l'enregistrement
    await glasses.api("recorder!stop", method="POST", body=[])
    print("🛑 Enregistrement arrêté")

    # Déconnexion propre
    await glasses.disconnect()
    print("🔌 Déconnecté")

# Lancer le programme
if __name__ == "__main__":
    asyncio.run(main())
j