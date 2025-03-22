import requests
import os
from concurrent.futures import ThreadPoolExecutor
#from googletrans import Translator
from deep_translator import GoogleTranslator

# Fazer um programa que pede nome do filme e ano de release, enviar um request pra Omdb API pra pegar a sinopse E
# os reviews no Tmdb API em paralelo, e retornar os dados. pra domingo dia 30


#OMDB
def fetch_omdb_data(filme, ano, traduzir):
    omdb_key = ""
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_key}&t={filme}&y={ano}"
    response = requests.get(omdb_url)

    if response.status_code == 200:
        data = response.json()
        imdb_rating = data["Ratings"][0]["Value"]
        sinopse = data["Plot"]

        if traduzir:
            sinopse_pt = GoogleTranslator(source='auto', target='pt').translate(sinopse)
            return f"\nNota IMDB: {imdb_rating}\nSinopse: {sinopse_pt}"
        else:
            return f"\nNota IMDB: {imdb_rating}\nSinopse: {sinopse}"
    
    else:
        return {"error": "Falha ao obter dados do OMDB"}

#TMDB
def fetch_tmdb_reviews(filme, ano, traduzir):
    tmdb_header = { 
        "accept": "application/json", 
        "authorization": f"Bearer "
        }
    tmdb_url = f"https://api.themoviedb.org/3/search/movie?query={filme}&primary_release_year={ano}"
    response1 = requests.get(tmdb_url, headers=tmdb_header)

    if response1.status_code == 200:
        movie_id = response1.json()["results"][0]["id"]
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US" #em português tem menos reviews
        response2 = requests.get(reviews_url, headers=tmdb_header)

        if response2.status_code == 200:
            results = response2.json()["total_results"]
            data = response2.json()["results"]
            
            if results > 0:
                if results >= 1:
                    conteudo1 = data[0]['content']
                    if conteudo1.count('.') > 5: #reduz o tamanho da review
                        conteudo1 = '.'.join(conteudo1.split('.')[:5]) + '.'

                    if traduzir:
                        review1_pt = GoogleTranslator(source='auto', target='pt').translate(conteudo1)
                        review1 = f"\nReview 1 - Autor: {data[0]['author']} \n{review1_pt}"
                    else:
                        review1 = f"\nReview 1 - Autor: {data[0]['author']} \n{conteudo1}"

                    if results >= 2:
                        conteudo2 = data[1]['content']
                        if conteudo2.count('.') > 5:
                            conteudo2 = '.'.join(conteudo2.split('.')[:5]) + '.'

                        if traduzir:
                            review2_pt = GoogleTranslator(source='auto', target='pt').translate(conteudo2)
                            review2 = f"\n\nReview 2 - Autor: {data[1]['author']} \n{review2_pt}"
                        else:
                            review2 = f"\n\nReview 2 - Autor: {data[1]['author']} \n{conteudo2}"

                        if results >= 3:
                            conteudo3 = data[2]['content']
                            if conteudo3.count('.') > 5:
                                conteudo3 = '.'.join(conteudo3.split('.')[:5]) + '.'

                            if traduzir:
                                review3_pt = GoogleTranslator(source='auto', target='pt').translate(conteudo3)
                                review3 = f"\n\nReview 3 - Autor: {data[2]['author']} \n{review3_pt}"
                            else:
                                review3 = f"\n\nReview 3 - Autor: {data[2]['author']} \n{conteudo3}"

                            return review1 + review2 + review3
                        
                        else:
                            return review1 + review2

                    else:
                        return review1

            else:
                return "Nenhum review encontrado"
        
        else:
            return {"error": "Falha ao obter reviews do TMDB"}
        
    else:
        return {"error": "Falha ao obter ID do filme"}


# main():
#solicita o nome do filme e o ano de lançamento
os.system('cls')
filme = input("Digite o Nome do Filme (em inglês): ")
ano = input("Digite o Ano de Lançamento: ")

if input("\nDeseja traduzir os resultados para português? (s/n): ").lower() == 's':
    traduzir = True
else:
    traduzir = False

#faz as requests em paralelo
with ThreadPoolExecutor() as executor:
    omdb_future = executor.submit(fetch_omdb_data, filme, ano, traduzir)
    tmdb_future = executor.submit(fetch_tmdb_reviews, filme, ano, traduzir)

    omdb_data = omdb_future.result()
    tmdb_reviews = tmdb_future.result()

#resultado
os.system('cls')
print("Filme:", filme, "/ Lançamento:", ano)
print("\nOMDB:", omdb_data)
print("\nTMDB:", tmdb_reviews)
input("\nPressione Enter para sair...")
