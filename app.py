# Movie Data Dashboard - Python 3.12 Compatible
# Run: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Movie Dashboard", layout="wide")
st.title("Movie Data Dashboard")

# Load or generate data
@st.cache_data
def load_data():
    """Load movie data from CSV or generate sample data"""
    try:
        df = pd.read_csv('movies.csv')
    except:
        # Generate sample data
        np.random.seed(42)
        n = 500
        genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance']
        
        df = pd.DataFrame({
            'title': [f'Movie_{i}' for i in range(n)],
            'year': np.random.randint(1980, 2024, n),
            'genre': [np.random.choice(genres) for _ in range(n)],
            'rating': np.random.uniform(3, 9.5, n).round(1),
            'gross': np.random.uniform(10, 1500, n).round(0).astype(int)
        })
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Year range slider
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider("Year", year_min, year_max, (max(2000, year_min), year_max))

# Rating slider
rating_min = st.sidebar.slider("Min Rating", 3.0, 9.5, 6.0, 0.5)

# Genre multiselect
all_genres = sorted(df['genre'].unique().tolist())
default_genres = all_genres[:3] if len(all_genres) >= 3 else all_genres
genre_filter = st.sidebar.multiselect("Genre", all_genres, default=default_genres)

# Filter data
filtered = df[
    (df['year'].between(year_range[0], year_range[1])) &
    (df['rating'] >= rating_min) &
    (df['genre'].isin(genre_filter))
]

# Handle empty filtered data
if len(filtered) == 0:
    st.warning("No movies match the selected filters. Please adjust your filters.")
    filtered = df

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Movies", len(filtered))
col2.metric("Avg Rating", f"{filtered['rating'].mean():.2f}")
col3.metric("Avg Box Office", f"${filtered['gross'].mean():.0f}M")
col4.metric("Top Rating", f"{filtered['rating'].max():.1f}")

# Tabs
tab1, tab2, tab3 = st.tabs(["Rating Analysis", "Recommendations", "Search"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.histogram(
            filtered, x='rating', nbins=20, 
            title='Rating Distribution',
            color_discrete_sequence=['steelblue']
        )
        fig1.update_layout(xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        genre_avg = filtered.groupby('genre')['rating'].mean().reset_index()
        fig2 = px.bar(
            genre_avg, x='genre', y='rating', 
            title='Average Rating by Genre',
            color='rating', 
            color_continuous_scale='Viridis'
        )
        fig2.update_layout(xaxis_title="Genre", yaxis_title="Average Rating")
        st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.scatter(
        filtered, x='rating', y='gross', color='genre', 
        title='Rating vs Box Office', 
        hover_data=['title', 'year'],
        labels={'gross': 'Box Office ($M)', 'rating': 'Rating'}
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Top Rated Recommendations")
    top_movies = filtered.nlargest(10, 'rating')
    
    if len(top_movies) > 0:
        for i, row in top_movies.iterrows():
            st.write(f"**{row['title']}** - {row['rating']}/10 ({int(row['year'])}) | Box Office: ${int(row['gross'])}M | Genre: {row['genre']}")
    else:
        st.info("No recommendations available with current filters")

with tab3:
    search = st.text_input("Search Movies", placeholder="Enter movie title...")
    
    if search:
        results = filtered[filtered['title'].str.contains(search, case=False, na=False)]
        
        if len(results) > 0:
            st.success(f"Found {len(results)} movie(s)")
            for i, row in results.iterrows():
                st.write(f"**{row['title']}** ({int(row['year'])}) - Rating: {row['rating']}/10")
        else:
            st.info("No movies found. Try a different search term.")

# Footer
st.divider()
st.caption("Data source: Sample movie dataset | 500+ movies analyzed | Built with Python 3.12")

# Optional: Display raw data toggle
with st.expander("View Raw Data"):
    st.dataframe(filtered, use_container_width=True)