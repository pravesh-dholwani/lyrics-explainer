from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os




def get_link_for_lyrics(song_name, artist_name):
    search = DuckDuckGoSearchResults(verbose=True, output_format="list")
    # # search.invoke({"args": {"query":"Obama"}, "id": "1", "name": search.name, "type": "tool_call"})
    # # search.
    # song = "52 bars"
    # artist = "Karan Aujla"
    # language = ""
    response = search.run(f"give me the lyrics of {song_name} song by {artist_name}")

    print(type(response))
    source_links = []
    for r in response:
        source_links.append(r["link"])
    # source_link = response[0]["link"]
    return source_links

def get_docs_for_lyrics(source_links):
    docs = []
    for source_link in source_links:
        loader = WebBaseLoader(
        web_path = source_link)

        docs1 = loader.load()
        docs.extend(docs1)

    return docs

def get_lyrics_from_docs(song, docs):
    llm = ChatGroq(
        model = "llama3-70b-8192",
        verbose=True
    )

    prompt = PromptTemplate(
        input_variables=["docs", "song"],
        template='''Here is the context for the lyrics of a song named - {song}
                    extract the lyrics of the song and give me the lyrics line by line
                    {docs}
                    '''
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.invoke({'song': song, 'docs': docs})

    # print("Lyrics", response)

    return response["text"]



def explain_lyrics(song_name, artist_name, language, docs):
    llm = ChatGroq(
        model = "llama3-70b-8192",
        verbose=True
    )

    prompt = PromptTemplate(
        input_variables=['docs'],
        template='''
            You are a very knowledgable person in the indian punjabi music insustry and you explain the lyrics of the song to people and that is the only source of income for you.
            You always keep things simple and clear, and you also easily get the context of the songs and lyrics.
            You have to explain the whole song lyric by lyric, and dont miss even a single line, if you miss any line you will become homeless
            
        '''

    )

    prompt = PromptTemplate(
        input_variables=['docs'],
        template=f'''
        You are an expert in the {language} music industry, with a deep understanding of the cultural, emotional, and artistic elements that shape the music. Your only source of livelihood is explaining {language} song lyrics, line by line, to your audience in a way that resonates with their emotions and connects them to the artist's intent.

        Your goal is to analyze every single line without skipping any, offering clear and simple explanations that also capture the underlying context, feelings, and story of the song. You should:

        Understand and explain the emotional undertone of each lyric (joy, heartbreak, pride, nostalgia, etc.).
        Highlight cultural references, idioms, or metaphors that enhance the song's meaning.
        Provide insights into the artist's perspective, connecting the lyrics to their possible life experiences or themes in {language} music.
        Maintain a balance between detailed interpretation and simplicity, making the explanation easy to understand for everyone, regardless of their knowledge of {language} music.
        Remember, skipping even one line means losing your livelihood, so pay close attention to every detail of the song's lyrics. Ensure the explanations are heartfelt, accurate, and engaging to your audience.
        GIve the whole explaination in one response
        this is the lyrics of song''' + song_name +''' by '''+ artist_name +'''
        {docs}
        '''
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(docs)

    return response

def driver(song_name, artist_name, language):
    source_link = get_link_for_lyrics(song_name, artist_name)
    docs = get_docs_for_lyrics(source_link)
    # print("docs", docs)
    lyrics = get_lyrics_from_docs(song_name, docs)
    print(lyrics)
    explaination = explain_lyrics(song_name, artist_name, language, lyrics)

    return explaination

    
