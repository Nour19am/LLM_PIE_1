import streamlit as st
import yfinance as yf
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from openai import OpenAI
from yahoo_fin import stock_info


api_key = st.text_input("Enter your NVIDIA API key", type="password")
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  #api_key = "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"
  api_key=api_key
)

st.title("Agent financier")



# Initialiser le modèle NVIDIA
if "nvidia_model" not in st.session_state:
    st.session_state["nvidia_model"] = "nvidia/nemotron-4-340b-instruct"

# Initialiser l'historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = []


def get_stock_news(ticker):
    """
    Récupère les actualités liées à une action.
    """
    try:
        news = stock_info.get_news(ticker)
        st.write(f"Actualités pour {ticker} :")
        for item in news[:5]:  # Limiter à 5 nouvelles
            st.markdown(f"- [{item['title']}]({item['link']}) - {item['provider']}")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des nouvelles : {e}")



# Fonction pour récupérer les données financières
def fetch_financial_data(stock_ticker, period="1y"):
    """
    Récupère les données historiques d'une action à partir de Yahoo Finance.
    """
    try:
        stock = yf.Ticker(stock_ticker)
        historical_data = stock.history(period=period)
        return historical_data
    except Exception as e:
        return f"Erreur lors de la récupération des données : {e}"

# Afficher l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Traitement des entrées utilisateur
if prompt := st.chat_input("Posez une question ou demandez des données financières..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Vérifier si la question nécessite des données financières
    # Utilisation


    if "données historiques" in prompt.lower() or "prix" in prompt.lower():
        try:
            # Extraction de la commande (ticker et période)
            # Ex : "Donne-moi les données historiques de AAPL sur 6 mois"
            tokens = prompt.split()
            ticker = tokens[tokens.index("de") + 1]
            period = "6mo" if "6 mois" in prompt else "1y"  # Par défaut, 1 an

            # Appel à la fonction de récupération des données
            financial_data = fetch_financial_data(ticker, period)

            with st.chat_message("assistant"):
                if isinstance(financial_data, str):  # En cas d'erreur
                    st.markdown(financial_data)
                else:
                    st.markdown(f"Voici les données historiques pour **{ticker}** sur la période **{period}** :")
                    st.dataframe(financial_data.tail(10))  # Afficher les 10 dernières entrées

            st.session_state.messages.append({"role": "assistant", "content": "Données financières affichées."})

        except Exception as e:
            with st.chat_message("assistant"):
                st.markdown(f"Je n'ai pas pu traiter votre demande : {e}")

                
            st.session_state.messages.append({"role": "assistant", "content": f"Erreur : {e}"})

    else:  # Si ce n'est pas une demande de données financières
        
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["nvidia_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
