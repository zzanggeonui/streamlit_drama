import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

def run_ml_app() :
    df = pd.read_csv('data/realeditdrama.csv', thousands = ',')    
    genre_list = pd.read_csv('data/genre_sum.csv').head(10)
    
    select_rank = st.sidebar.selectbox('항목별 랭킹', ['전체','장르별','태그별','배우별'])
    status = st.radio('드라마랭킹 top100',['인기순','평점순','리뷰순'])
    if select_rank =='전체' :
        
        if status == '인기순' :
            st.dataframe(df.loc[:,['drama_name','Popularity']].sort_values('Popularity').head(100))
            
        elif status == '평점순' :
            st.dataframe(df.loc[:,['drama_name','score']].sort_values('score',ascending=False).head(100) )
        elif status == '리뷰순' :
            st.dataframe(df.loc[:,['drama_name','scored by']].sort_values('scored by',ascending=False ).head(100))
        elif status == '조회순' :
            st.dataframe(df.loc[:,['drama_name','Watchers']].sort_values('Watchers',ascending=False).head(100) )

    if select_rank =='장르별' :
        genre_all = pd.read_csv('data/genre_list.csv')
        genre_list = genre_all['genre'].tolist()
        genre_sum = pd.read_csv('data/genre_sum.csv')

        fig = px.pie(genre_sum.head(10), 'genre','sum',title='장르별 차트')
        st.plotly_chart(fig)

        app = []
        for x in genre_list :
            ac = df[df['Genres'].str.contains(str(x),na=False)]
            f = ac['score'].mean()
            app.append(f)

        genre_score = pd.DataFrame(data=app)
        genre_score = genre_score.rename(columns={0:'score'})
        genre_sl = genre_all.join(genre_score)
        ## 장르별 평균 평점 (중복데이터 포함)


        ap = []
        for x in genre_list :
            ac = df[df['Genres'].str.contains(str(x),na=False)]
            f = ac['Popularity'].mean()
            ap.append(f)

        genre_popul = pd.DataFrame(data=ap)
        genre_scpo = genre_sl.join(genre_popul)
        genre_scpo = genre_scpo.rename(columns={0:'popul'})
        ## popul여기

        appp = []
        for x in genre_list :
            ac = df[df['Genres'].str.contains(str(x),na=False)]
            f = ac['scored by'].mean()
            appp.append(f)

        genre_review = pd.DataFrame(data=appp)
        genre_scpore = genre_scpo.join(genre_review)
        genre_scpore = genre_scpore.rename(columns={0:'review'})
        
        ## 인덱스 설정및 중복값 제거
        genre_scpore = genre_scpore.set_index('0')
        genre_scpore = genre_scpore.drop_duplicates()
        

        st.subheader('화제를 모으는 작품이 많은 장르순입니다')
        st.dataframe(genre_scpore.loc[:,['popul']].sort_values('popul'))

            
        st.subheader('평가가 좋은 작품이 많은 장르입니다')
        st.dataframe(genre_scpore.loc[:,['score']].sort_values('score',ascending=False))
            

        st.subheader('리뷰가 많이 달리는 작품 장르입니다')
        st.dataframe(genre_scpore.loc[:,['review']].sort_values('review',ascending=False))
            
        
    



