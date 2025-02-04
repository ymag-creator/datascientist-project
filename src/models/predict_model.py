from xgboost.sklearn import XGBRegressor
import pandas as pd
import joblib
import os


class PredictModel:
    """Prédiciton des colonnes cibles par XGBoost"""

    def __init__(self):
        self.path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
        print("Répertoire courant PredictModel:", self.path)

        self.cols_cible_type = [
            "TurnoutTimeSeconds",
            "TravelTimeSeconds",
            "PumpSecondsOnSite",
        ]
        self.cols_Data = [
            ["CalYear", "HourOfCall", "Postcode_district", "Month", "DayOfWeek"],
            ["CalYear", "HourOfCall", "Postcode_district", "Month", "DayOfWeek"],
            ["CalYear", "PropertyType", "StopCode"],
        ]
        self.cols_cible = [
            [
                "TurnoutTimeSeconds_min",
                "TurnoutTimeSeconds_mean",
                "TurnoutTimeSeconds_max",
            ],
            [
                "TravelTimeSeconds_min",
                "TravelTimeSeconds_mean",
                "TravelTimeSeconds_max",
            ],
            [
                "PumpSecondsOnSite_min",
                "PumpSecondsOnSite_mean",
                "PumpSecondsOnSite_max",
            ],
        ]

    def create_dataframe(
        self,
        year,
        hour,
        property_type,
        postcode_district,
        stop_code,
        month,
        day_of_week,
    ):
        """Crée un dataframe de données brutes utilisable pour la prédiction
        Args:
            year (_type_): Année
            hour (_type_): Heure
            property_type (_type_): Type de propriété
            postcode_district (_type_): Post code district
            stop_code (_type_): Type d'incident
            month (_type_): mois
            day_of_week (_type_): Jour de la semaine

        Returns:
            _type_: Dataframe
        """
        data = [
            {
                "CalYear": min(2024, year),
                "HourOfCall": hour,
                "PropertyType": property_type,
                "Postcode_district": postcode_district,
                "StopCode": stop_code,
                "Month": month,
                "DayOfWeek": day_of_week,
            }
        ]
        df = pd.DataFrame(data)
        # Converti en text pour les encodeurs
        df.CalYear = df.CalYear.astype("str")
        df.HourOfCall = df.HourOfCall.astype("str")
        df.Month = df.Month.astype("str")
        df.DayOfWeek = df.DayOfWeek.astype("str")

        print(df.head(10))
        return df

    # Réduit les valeurs catégorielles à partir des valeurs calculées par Anova et
    # stockées sur disque, dans "PreProcessing Reduce categories"
    # Concerne 3 colonnes quiu avaient de nombreuses valeurs
    def reduceCategValues(self, df, col_cible_type):
        """Réduit les valeurs catégorielles, en remplaçant les valeurs non conservées par "OTHER" 

        Args:
            df (_type_): Dataframe
            col_cible_type (_type_): Type de colonne cible

        Returns:
            _type_: Le dataframe modifié
        """
        df_keep = pd.read_csv(
            os.path.join(self.path, f"keep {col_cible_type}.csv"), sep=";"
        )
        df_new = df.copy()

        # print(df_keep.head())
        replaces = {}
        # Pour chaque ligne des données à conserver/remplacer
        for keep_info in df_keep.itertuples():
            # Si ne conserve pas la valeur, l'ajoute dans le dictionnaire
            # par colonne
            if not (keep_info.Keep):
                # Si la colonne n'est pas dans le dictionnaire, l'ajoute et met un tableau vide
                if not (keep_info.Column in replaces):
                    print(keep_info.Column)
                    replaces[keep_info.Column] = []
                # Récupère le tableau pour la colonne
                val = replaces[keep_info.Column]
                # Ajoute la valeur catégorielle dans la liste des valeurs à ne pas conserver
                val.append(keep_info.Value)
                # Remet le tableau modifié en valeur de la colonne
                replaces[keep_info.Column] = val
        # Contrôle
        # print("replaces", replaces)
        # Pour chaque colonne, dans le DF, remplace les valeurs qui ne sont pas à conserver
        # par "OTHER"
        for col in replaces:
            # Pour la cible de Temps de déplacement, garde tout les Postcode_district
            # comme c'est la donnée de base du calcul
            if (col_cible_type == "TravelTimeSeconds") & (col == "Postcode_district"):
                # print("Ignore", col_cible_type, col)
                continue
            # print(col)
            # print("Avant remplacement", len(df_new[col].unique()), df_new[col].unique())
            # print("A remplacer", len(replaces[col]), replaces[col])
            # Effectue de le remplacement dans la colonne par OTHER pour les valeurs concernées
            df_new[col] = df_new[col].replace(to_replace=replaces[col], value="OTHER")
            # print("Après remplacement", len(df_new[col].unique()), df_new[col].unique())
            # print()
        return df_new

    def apply_encoder(self, df, col_cible_type):
        """Applique l'encodage des colonnes catégorielles

        Args:
            df (_type_): Dataframe
            col_cible_type (_type_): Type de colonne cible

        Returns:
            _type_: Le dataframe modifié
        """
        df_new = df.copy()
        # Encodage de l'année
        encoder = joblib.load(os.path.join(self.path, f"_ce_{col_cible_type}_OrdinalEncoder.pkl"))
        # Recrée un Dataframe, pour que les colonnes correspondent exactement à celles du Fit (nom et ordre)
        expected_columns = encoder.feature_names_in_
        missing_cols = set(expected_columns) - set(df_new.columns)
        # extra_cols = set(df_new.columns) - set(expected_columns)
        # print(expected_columns)
        # print(missing_cols)
        # print(extra_cols)
        # print(encoder.get_feature_names_out())
        # Ajoute les colonnes manquantes
        for col in missing_cols:
            df_new[col] = ""
        # Réorganiser les colonnes pour correspondre exactement à celles attendues
        df_new = df_new[list(expected_columns)]
        # print(df_new.head(10))
        # Applique l'encodage
        df_new = encoder.transform(df_new)

        # Encodage des colonnes catégorielles
        encoder = joblib.load(os.path.join(self.path, f"_ce_{col_cible_type}_BinaryEncoder.pkl"))
        expected_columns = encoder.feature_names_in_
        # print(expected_columns)
        # print(encoder.get_feature_names_out())
        # print(encoder.get_feature_names_out())
        # Applique l'encodage
        df_new = encoder.transform(df_new)
        # print(df_new.head(10))
        return df_new

    def predict(self, df):
        """Prédit les 9 colonnes cibles

        Args:
            df (_type_): Dataframe de données brutes

        Returns:
            _type_: Les prévisioons de temps de préparation, trajet, et sur site
        """
        # Prédit les colonnes cibles pour chaque type
        results = {}
        # Boucle sur les types de cibles
        for index, name in enumerate(self.cols_cible_type):
            # Applique la réduction des valeurs catégorielles
            X = self.reduceCategValues(df, name)
            # Applique l'encodage par cible
            X = self.apply_encoder(X, name)
            # Garde les colonnes nécessaires
            cols_to_keep = [
                col
                for col in X.columns
                if any(substring in col for substring in self.cols_Data[index])
            ]
            X = X[cols_to_keep]
            print(X.head(10))

            # Boucle sur les colonnes cibles
            for index_cible, col_cible in enumerate(self.cols_cible[index]):
                print(
                    "--------------------------------------------------------------------------------"
                )
                print("///////////////////////////", "cible", col_cible)
                # Charge le modèle
                xgb = joblib.load(os.path.join(self.path, f"_XGBoost_{col_cible}.pkl"))
                # Predit
                y_pred = xgb.predict(X)
                # Ajoute la valeur au tableau des résultats
                results[col_cible] = y_pred[0]
                print(results)
        return [results]
