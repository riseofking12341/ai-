
import streamlit as st
import openai
from GoogleNews import GoogleNews

st.set_page_config(page_title="Smart Nyhetsanalys", page_icon="🧠")
st.title("🧠 Smart Nyhetsanalys för Företag")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def fetch_news(company):
    googlenews = GoogleNews(lang='sv')
    googlenews.search(company)
    return googlenews.results()[:3]

def analyze_news(news, company):
    text = f"{news['title']}. {news['desc']}"
    prompt = f"""
    Här är en nyhet kopplad till {company}:

    {text}

    🔍 Vad kan detta innebära för {company}?

    Svara med:
    - Sammanfattning av nyheten
    - Sannolik påverkan på aktien (liten/medel/stor)
    - Risk för nedgång (1–10)
    - Sannolikhet för uppgång (1–10)
    - Kort förklaring till båda
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

company = st.text_input("Skriv in ett företagsnamn", value="Astor Scandinavian Group")

if company:
    st.write(f"🔎 Letar efter nyheter för: **{company}**")
    news_list = fetch_news(company)

    for news in news_list:
        st.subheader(news["title"])
        st.caption(news["date"])
        st.markdown(f"[Länk till nyhet]({news['link']})")
        with st.spinner("Analyserar med GPT..."):
            analysis = analyze_news(news, company)
        st.markdown(analysis)
        st.divider()
