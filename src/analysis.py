# Movie Data Analysis - Python 3.12 Compatible
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(42)
n = 500

years = np.random.randint(1980, 2024, n)
ratings = np.random.uniform(3, 9.5, n).round(1)
gross = (ratings - 3) * 50 + np.random.normal(0, 100, n)
gross = np.clip(gross, 5, 2000).astype(int)

# Genres
genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance']
movie_genres = [np.random.choice(genres) for _ in range(n)]

# Create DataFrame
df = pd.DataFrame({
    'title': [f'Movie_{i}' for i in range(n)],
    'year': years,
    'genre': movie_genres,
    'rating': ratings,
    'gross': gross
})

print("Data Overview:")
print(df.head())
print(f"\nTotal Movies: {len(df)}")
print(f"Average Rating: {df['rating'].mean():.2f}")
print(f"Data types:\n{df.dtypes}")

# Analysis 1: Rating Distribution
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.hist(df['rating'], bins=20, color='steelblue', edgecolor='black')
plt.xlabel('Rating')
plt.ylabel('Number of Movies')
plt.title('Rating Distribution')

# Analysis 2: Average Rating by Genre
plt.subplot(1, 2, 2)
genre_rating = df.groupby('genre')['rating'].mean().sort_values()
plt.barh(genre_rating.index, genre_rating.values, color='coral')
plt.xlabel('Average Rating')
plt.title('Average Rating by Genre')

plt.tight_layout()
plt.show()

# Analysis 3: Rating vs Box Office
plt.figure(figsize=(8, 5))
plt.scatter(df['rating'], df['gross'], alpha=0.5, color='green')
plt.xlabel('Rating')
plt.ylabel('Box Office ($M)')
plt.title('Rating vs Box Office')
plt.show()

# Key Insights
print("\n" + "="*40)
print("Key Insights")
print("="*40)
print(f"1. Highest rated genre: {genre_rating.idxmax()} ({genre_rating.max():.2f})")
print(f"2. Lowest rated genre: {genre_rating.idxmin()} ({genre_rating.min():.2f})")
print(f"3. Rating-Box Office correlation: {df['rating'].corr(df['gross']):.2f}")
print(f"4. Highest rated movie: {df.loc[df['rating'].idxmax(), 'title']} ({df['rating'].max()}/10)")

# Save data for Streamlit
df.to_csv('movies.csv', index=False)
print("\nData saved to movies.csv")