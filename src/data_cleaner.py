import pandas as pd
import numpy as np
import re
import sqlite3
from datetime import datetime
import logging
import unicodedata

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCleaner:
    """
    Classe pour nettoyer et agréger les données du projet de classification
    """
    
    def __init__(self):
        self.cleaning_rules = {
            'remove_duplicates': True,
            'remove_empty_products': True,
            'normalize_categories': True,
            'fix_prices': True,
            'validate_dates': True
        }
    
    def clean_product_names(self, df):
        """
        Nettoie les noms de produits
        """
        logger.info("🧹 Nettoyage des noms de produits...")
        
        if 'Produit' in df.columns:
            # Supprimer les lignes avec produits vides
            initial_count = len(df)
            df = df.dropna(subset=['Produit'])
            df = df[df['Produit'].str.strip() != '']
            
            # Normaliser les noms
            df['Produit'] = df['Produit'].str.lower()
            df['Produit'] = df['Produit'].str.strip()
            
            # Supprimer les quantités (ex: 1KG, 500ML, 4X125G)
            df['Produit'] = df['Produit'].apply(lambda x: re.sub(r'\b\d+[Xx]?\d*[a-z]+\b', '', x))
            
            # Supprimer les caractères spéciaux excessifs
            df['Produit'] = df['Produit'].apply(lambda x: re.sub(r'[^\w\s\-\.]', ' ', x))
            df['Produit'] = df['Produit'].apply(lambda x: re.sub(r'\s+', ' ', x))
            
            # Garder uniquement les caractères latins
            df['Produit'] = df['Produit'].apply(self.garder_caracteres_latin)
            
            # Supprimer les doublons
            df = df.drop_duplicates(subset=['Produit'])
            
            logger.info(f"✅ Produits nettoyés: {initial_count} → {len(df)}")
        
        return df
    
    def garder_caracteres_latin(self, texte):
        """
        Garde uniquement les caractères latins (et tout le reste sauf les lettres non latines)
        """
        if pd.isnull(texte):  # Si la valeur est NaN
            return texte
        texte = str(texte)
        resultat = ''
        for char in texte:
            if char.isalpha():
                nom = unicodedata.name(char, '')
                if 'LATIN' in nom:
                    resultat += char  # Lettre latine OK
                # Sinon, on supprime
            else:
                resultat += char  # On garde chiffres, ponctuation, espaces, symboles
        return resultat
    
    def normalize_categories(self, df):
        """
        Normalise les catégories de produits
        """
        logger.info("📂 Normalisation des catégories...")
        
        if 'Categories_OFF' in df.columns:
            # Mapping des catégories similaires
            category_mapping = {
                'fruits & legumes': 'Fruits & Légumes',
                'fruits et legumes': 'Fruits & Légumes',
                'fruits': 'Fruits & Légumes',
                'legumes': 'Fruits & Légumes',
                'viande': 'Viandes & Charcuterie',
                'viandes': 'Viandes & Charcuterie',
                'charcuterie': 'Viandes & Charcuterie',
                'poisson': 'Poisson & Fruits de mer',
                'fruits de mer': 'Poisson & Fruits de mer',
                'laitier': 'Produits laitiers',
                'laitiers': 'Produits laitiers',
                'yaourt': 'Produits laitiers',
                'fromage': 'Produits laitiers',
                'boisson': 'Boissons',
                'boissons': 'Boissons',
                'soda': 'Boissons',
                'epicerie': 'Épicerie salée',
                'epicerie salee': 'Épicerie salée',
                'sucre': 'Épicerie sucrée',
                'sucree': 'Épicerie sucrée',
                'chocolat': 'Épicerie sucrée',
                'hygiene': 'Hygiène',
                'entretien': 'Entretien / Ménage',
                'menage': 'Entretien / Ménage'
            }
            
            # Supprimer le préfixe "en:" (comme dans nettoyage.py)
            df['Categories_OFF'] = df['Categories_OFF'].str.removeprefix('en:')
            
            # Appliquer le mapping
            df['Categories_OFF'] = df['Categories_OFF'].str.lower()
            df['Categories_OFF'] = df['Categories_OFF'].map(category_mapping).fillna(df['Categories_OFF'])
            
            # Capitaliser correctement
            df['Categories_OFF'] = df['Categories_OFF'].str.title()
            
            logger.info(f"✅ Catégories normalisées: {df['Categories_OFF'].nunique()} catégories uniques")
        
        return df
    
    def fix_prices(self, df):
        """
        Corrige et valide les prix
        """
        logger.info("💰 Correction des prix...")
        
        price_columns = ['Prix', 'prix_total', 'budget']
        
        for col in price_columns:
            if col in df.columns:
                # Convertir en numérique
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Supprimer les prix négatifs ou trop élevés (>10000€)
                df = df[(df[col].isna()) | ((df[col] >= 0) & (df[col] <= 10000))]
                
                # Arrondir à 2 décimales
                df[col] = df[col].round(2)
                
                logger.info(f"✅ Prix corrigés pour {col}")
        
        return df
    
    def validate_dates(self, df):
        """
        Valide et corrige les dates
        """
        logger.info("📅 Validation des dates...")
        
        date_columns = ['date_achat', 'date_enregistrement', 'collected_at']
        
        for col in date_columns:
            if col in df.columns:
                # Convertir en datetime
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
                # Supprimer les dates futures ou trop anciennes (>10 ans)
                current_date = pd.Timestamp.now()
                df = df[(df[col].isna()) | 
                       ((df[col] <= current_date) & 
                        (df[col] >= current_date - pd.DateOffset(years=10)))]
                
                logger.info(f"✅ Dates validées pour {col}")
        
        return df
    
    def remove_corrupted_entries(self, df):
        """
        Supprime les entrées corrompues
        """
        logger.info("🚫 Suppression des entrées corrompues...")
        
        initial_count = len(df)
        
        # Supprimer les lignes avec trop de valeurs manquantes (>50%)
        threshold = len(df.columns) * 0.5
        df = df.dropna(thresh=threshold)
        
        # Supprimer les lignes avec des valeurs aberrantes
        if 'Prix' in df.columns:
            # Prix négatifs ou trop élevés
            df = df[(df['Prix'].isna()) | ((df['Prix'] >= 0) & (df['Prix'] <= 10000))]
        
        if 'Produit' in df.columns:
            # Produits avec des noms trop courts ou trop longs
            df = df[df['Produit'].str.len() >= 2]
            df = df[df['Produit'].str.len() <= 200]
        
        logger.info(f"✅ Entrées corrompues supprimées: {initial_count} → {len(df)}")
        
        return df
    
    def aggregate_data_sources(self, csv_files, output_file="data/aggregated_data.csv"):
        """
        Agrège les données de plusieurs sources
        """
        logger.info("🔄 Agrégation des données de plusieurs sources...")
        
        all_data = []
        
        for file in csv_files:
            try:
                df = pd.read_csv(file, sep=';')
                df['source'] = file
                all_data.append(df)
                logger.info(f"✅ Fichier chargé: {file} ({len(df)} lignes)")
            except Exception as e:
                logger.error(f"❌ Erreur lors du chargement de {file}: {e}")
        
        if all_data:
            # Concaténer tous les DataFrames
            aggregated_df = pd.concat(all_data, ignore_index=True)
            
            # Nettoyer les données agrégées
            aggregated_df = self.clean_all_data(aggregated_df)
            
            # Sauvegarder
            aggregated_df.to_csv(output_file, index=False, sep=';')
            logger.info(f" Données agrégées sauvegardées: {output_file} ({len(aggregated_df)} lignes)")
            
            return aggregated_df
        
        return None
    
    def clean_all_data(self, df):
        """
        Applique tous les nettoyages sur un DataFrame
        """
        logger.info("Application du pipeline de nettoyage complet...")
        
        initial_count = len(df)
        
        # 1. Supprimer les entrées corrompues
        df = self.remove_corrupted_entries(df)
        
        # 2. Nettoyer les noms de produits
        df = self.clean_product_names(df)
        
        # 3. Normaliser les catégories
        df = self.normalize_categories(df)
        
        # 4. Corriger les prix
        df = self.fix_prices(df)
        
        # 5. Valider les dates
        df = self.validate_dates(df)
        
        # 6. Supprimer les doublons finaux
        df = df.drop_duplicates()
        
        logger.info(f"🎉 Nettoyage terminé: {initial_count} → {len(df)} lignes")
        
        return df
    
    def generate_cleaning_report(self, df_before, df_after):
        """
        Génère un rapport de nettoyage
        """
        report = {
            'lignes_avant': len(df_before),
            'lignes_apres': len(df_after),
            'lignes_supprimees': len(df_before) - len(df_after),
            'taux_reduction': round((len(df_before) - len(df_after)) / len(df_before) * 100, 2),
            'categories_uniques': df_after['Categories_OFF'].nunique() if 'Categories_OFF' in df_after.columns else 0,
            'produits_uniques': df_after['Produit'].nunique() if 'Produit' in df_after.columns else 0
        }
        
        logger.info("📊 Rapport de nettoyage:")
        for key, value in report.items():
            logger.info(f"  {key}: {value}")
        
        return report

if __name__ == "__main__":
    cleaner = DataCleaner()
    
    # Exemple d'utilisation
    print("🧹 Test du pipeline de nettoyage")
    print("=" * 40)
    
    # Charger des données d'exemple
    try:
        df = pd.read_csv("data/tickets_categorie_final.csv", sep=';')
        print(f"📂 Données chargées: {len(df)} lignes")
        
        # Nettoyer
        df_clean = cleaner.clean_all_data(df)
        
        # Rapport
        cleaner.generate_cleaning_report(df, df_clean)
        
    except FileNotFoundError:
        print("❌ Fichier de données non trouvé. Créez d'abord des données d'exemple.") 