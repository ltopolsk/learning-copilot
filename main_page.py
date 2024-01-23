import streamlit as st
from src.app.mongo import DBClient
from src.gpt.gptApi import gptManager
from src.app.auth import run_page
from src.app.misc import render_sidebar, render_pdf
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

def main(user_id, user_email):
    st.session_state.user_id=user_id
    db_client = DBClient(config=st.secrets["mongo"])
    gpt_manager = gptManager(**st.secrets["gpt_api"])
    st.session_state.db = db_client

    def disable():
        st.session_state.disabled = True

    def enable():
        st.session_state.disabled = False

    def upload_file():
        if not st.session_state.get('file_uploaded', False):
            enable()
        else:
            disable()

    if 'genNotes' not in st.session_state:
        st.session_state.disabled = True
    if 'genQuiz' not in st.session_state:
        st.session_state.disabled = True

    sidebar, body = st.columns([1, 8])

    render_sidebar(sidebar)

    body.markdown('<h1>Learning Copilot 📚</h1>', unsafe_allow_html=True)
    uploaded = body.file_uploader(label='Dodaj plik',on_change=upload_file, type=['pdf'])
    title = body.text_input('Wprowadź tytuł notatek/quizu')

    if title is not None and title != '':
        st.session_state.title = title

    save_result = body.checkbox('Zapisz quiz/notatki na później')
    col1, col2 = body.columns(2)
    clicked_notes = col1.button('Wygeneruj notatki', key='genNotes', disabled=st.session_state.disabled,use_container_width=True)
    clicked_quiz = col2.button('Wygeneruj quiz', key='genQuiz', disabled=st.session_state.disabled,use_container_width=True)

    if uploaded is not None:
        st.session_state.file_uploaded=True
    else:
        st.session_state.file_uploaded=False

    
    if clicked_notes:
        result_holder = st.empty()
        def progress(percent):
            with result_holder.container():
                st.progress(percent, f"Generowanie quizu {percent*100:.0f}%")
        md_content =gpt_manager.forward_read(uploaded, 'notes_markdown', callback=progress)
        st.session_state.file = render_pdf(md_content)
        if save_result:
            db_client.upload_notes(st.session_state.user_id, st.session_state.file, md_content, title)
        # with open('wyklad.md') as f:
        #     st.session_state.file = f.read()
        switch_page("notes")
    if clicked_quiz:
        result_holder = st.empty()
        def progress(percent):
            with result_holder.container():
                st.progress(percent, f"Generowanie quizu {percent*100:.0f}%")
    
        st.session_state.quiz = gpt_manager.forward_read(uploaded, 'quiz', callback=progress)
        # st.session_state.quiz = {'question': ['Co to jest korpus w kontekście przetwarzania języka naturalnego (NLP)? ', 'Co to są kolokacje w kontekście przetwarzania języka naturalnego (NLP)? ', 'Jaką rolę pełnią korpusy w przetwarzaniu języka naturalnego (NLP)? ', 'Dlaczego korpusy i kolokacje są ważne w przetwarzaniu języka naturalnego? ', 'Czym jest korpus w kontekście lingwistyki? ', 'Do czego korpusy językowe są wykorzystywane we współczesnej leksykografii? ', 'Z czego składa się Korpus Języka Polskiego PWN? ', 'Co jest dostępne bezpłatnie w sieciowej wersji Korpusu Języka Polskiego PWN? ', 'Co to jest korpus w kontekście językoznawstwa? ', 'Co oznacza, że korpus jest "zbilansowany"?', 'Czym różni się korpus jednojęzykowy od wielojęzycznego? ', 'Czym oznacza że korpus jest "anotowany"? ', 'Co to znaczy, że korpus jest "statyczny"?', 'Co to jest korpus w kontekście lingwistyki?', 'Co to jest Brown Corpus?', 'Gdzie można szukać korpusów tekstowych?', 'Czym jest Penn TreeBank?', 'Co to jest Enron Email Archive?'], 'answers': [['Kluczowe słowa wykorzystywane w kodowaniu ', 'Zbiór dokumentów tekstowych użytych do przeprowadzenia analizy ', 'Typ danych, które są przetwarzane przez algorytm NLP '], ['Połączenie kilku zdań w jeden blok tekstu ', 'Słowa, które często występują razem ', 'Sposób organizacji danych w korpusie '], ['Służą do generowania losowych zdań ', 'Są używane do tworzenia modeli języka przy użyciu danych ', 'Ograniczają ilość danych, które program NLP może przetworzyć '], ['Pomagają programowi NLP zrozumieć kontekst języka naturalnego ', 'Kolokacje pomagają programowi NLP generować bardziej naturalnie brzmiący tekst ', 'Korpusy zapewniają zasób danych, na których program NLP może się uczyć '], ['Zestaw reguł językowych ', 'Zbiór tekstów służący badaniom lingwistycznym ', 'Baza danych językowych '], ['Do tworzenia nowych słów ', 'Do określania częstości występowania form wyrazowych, konstrukcji składniowych, kontekstów ', 'Do tworzenia nowych języków '], ['Z bazy danych językowych ', 'Z fragmentów 386 różnych książek, 977 numerów 185 różnych gazet i czasopism, 84 nagranych rozmów, 207 stron internetowych oraz kilkuset ulotek reklamowych ', 'Z 40 milionów słów '], ['Pełna wersja korpusu ', 'Wersja demonstracyjna wielkości ponad 7,5 miliona słów ', 'Możliwość pobrania korpusu '], ['Zbiór zdań ', 'Zbiór tekstów reprezentatywnych dla języka, zapisanych w formie elektronicznej ', 'Zbiór słów w danym języku '], ['Zawiera teksty o różnej tematyce ', 'Zawiera teksty tylko o jednej tematyce ', 'Zawiera teksty, które są napisane w kilku językach '], ['Jednojęzykowy zawiera teksty tylko w jednym języku, a wielojęzyczny zawiera teksty w kilku językach ', 'Jednojęzykowy zawiera teksty tylko o jednym temacie, a wielojęzyczny zawiera teksty o kilku tematach ', 'Jednojęzykowy zawiera teksty napisane przez jednego autora, a wielojęzyczny zawiera teksty napisane przez różnych autorów'], ['Zawiera metadane, takie jak POS tags lub informacje o rozbiorze zdania ', 'Zawiera opisy zdjeć ', 'Zawiera notki na temat treści tekstu '], ['Nie jest aktualizowany ', 'Zawiera tylko statystyki ', 'Zawiera teksty tylko z jednego okresu '], ['Konkretna książka analizowana przez lingwistów', 'Zbiór tekstów używanych do analizy i badania języka ', 'Zestaw zasad gramatycznych języka'], ['Duży zbiór danych używany do badania języka angielskiego', 'Zbiór danych używany do badania języka polskiego', 'Korpus danych używany do badań nad klasyfikacją wiadomości e-mail'], ['The Corpora List ', 'Project Gutenberg', 'Penn TreeBank'], ['Korpus niestety niedostępny bezpłatnie', 'Korpus do badań nad klasyfikacją wiadomości e-mail', 'Repozytorium darmowych korpusów tekstowych o różnych kategoriach tematycznych'], ['Zbiór e-maili firmy Enron', 'Korpus do badań nad klasyfikacją wiadomości e-mail', 'Korpus niestety niedostępny bezpłatnie ']], 'correct': ['Zbiór dokumentów tekstowych użytych do przeprowadzenia analizy ', 'Słowa, które często występują razem. ', 'Są używane do tworzenia modeli języka przy użyciu danych ', '', 'Zbiór tekstów służący badaniom lingwistycznym ', 'Do określania częstości występowania form wyrazowych, konstrukcji składniowych, kontekstów ', 'Z fragmentów 386 różnych książek, 977 numerów 185 różnych gazet i czasopism, 84 nagranych rozmów, 207 stron internetowych oraz kilkuset ulotek reklamowych ', '', 'Zbiór tekstów reprezentatywnych dla języka, zapisanych w formie elektronicznej ', 'Zawiera teksty o różnej tematyce ', 'Jednojęzykowy zawiera teksty tylko w jednym języku, a wielojęzyczny zawiera teksty w kilku językach ', 'Zawiera metadane, takie jak POS tags lub informacje o rozbiorze zdania ', 'Zawiera teksty tylko z jednego okresu', 'Zbiór tekstów używanych do analizy i badania języka ', 'Duży zbiór danych używany do badania języka angielskiego', 'Wszystkie powyższe ', 'Korpus niestety niedostępny bezpłatnie ', 'Korpus do badań nad klasyfikacją wiadomości e-mail']}
        if save_result:
            db_client.upload_quiz(st.session_state.user_id, st.session_state.quiz, title)
        switch_page("quiz")


if __name__ == '__main__':
    run_page(main)

