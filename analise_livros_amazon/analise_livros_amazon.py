import pandas as pd

#st.set_page_config(layout = "wide")

df_reviews = pd.read_csv(r"C:\Users\diogo\OneDrive\Área de Trabalho\GitHub\projetos\analise_livros_amazon\dataset\customer reviews.csv")
df_top100_books = pd.read_csv(r"C:\Users\diogo\OneDrive\Área de Trabalho\GitHub\projetos\analise_livros_amazon\dataset\Top-100 Trending Books.csv")


df_reviews
#df_reviews.info()
#df_reviews.memory_usage()

df_top100_books
#df_top100_books.info()
#df_top100_books.memory_usage()


# Avaliar quais são os autores com mais de um livro dentro dos top 100
df_books_per_author = df_top100_books[["author", "book title", "rating"]].groupby("author").agg(num_books=("book title", "count"),
                                                                         min_rating=("rating", "min"),
                                                                         max_rating=("rating", "max"),
                                                                         mean_rating=("rating", "mean"))

        # df_books_per_author.columns = df_books_per_author.columns.droplevel()
        # df_books_per_author = df_books_per_author[["count", "min", "max", "mean"]]
        # df_books_per_author = df_books_per_author.rename(columns = {"count": "num books", "min": "min rating", "max": "max rating", "mean": "mean rating"})

df_books_per_author.query("num_books > 1")
df_books_per_author

# Quais são os gêneros de livros e avaliar as suas notas
df_books_per_genre = df_top100_books[["genre", "Rank", "rating"]].groupby("genre").agg(count = ("Rank", "count"), mean_rating = ("rating", "mean")).sort_values("mean_rating", ascending = False)
df_books_per_genre["mean_rating"] = df_books_per_genre["mean_rating"].round(2)

df_books_per_genre.head(10)

        # Excluindo os gêneros que possuem apenas um livro, temos uma comparação melhor em relação a média das avaliações entre os gêneros
df_books_per_genre_multiple = df_books_per_genre.query("count > 1")
df_books_per_genre_multiple

# Dentre os top 100 quantos livros foram publicados por ano e a média das avaliações por ano
df_book_per_year = df_top100_books[["year of publication", "Rank", "rating"]].groupby("year of publication").agg(
                                                                                                                count = ("Rank", "count"),
                                                                                                                min_rating = ("rating", "min"),
                                                                                                                max_rating = ("rating", "max"),
                                                                                                                average_rating = ("rating", "mean"),).sort_values("average_rating", ascending = False)
df_book_per_year["average_rating"] = df_book_per_year["average_rating"].round(2)
df_book_per_year

        # Excluindo os anos que possuem apenas um livro, temos uma comparação melhor em relação a média das avaliações entre os anos

df_book_per_year_multiple = df_book_per_year.query("count > 1")
df_book_per_year_multiple

