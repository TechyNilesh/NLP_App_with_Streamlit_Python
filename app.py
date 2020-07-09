# Core Pkgs
import streamlit as st
import os
from PIL import Image


# NLP Pkgs
from textblob import TextBlob
import spacy
from gensim.summarization import summarize

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Function for Sumy Summarization
def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx, Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document, 3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

# Function to Analyse Tokens and Lemma


@st.cache
def text_analyzer(my_text):
	nlp = spacy.load('en')
	docx = nlp(my_text)
	# tokens = [ token.text for token in docx]
	allData = [('"Token":{},\n"Lemma":{}'.format(token.text, token.lemma_))
	            for token in docx]
	return allData

# Function For Extracting Entities


@st.cache
def entity_analyzer(my_text):
	nlp = spacy.load('en')
	docx = nlp(my_text)
	tokens = [token.text for token in docx]
	entities = [(entity.text, entity.label_)for entity in docx.ents]
	allData = ['"Token":{},\n"Entities":{}'.format(tokens, entities)]
	return allData


def main():
	""" NLP Based App with Streamlit """

	# Title
	#st.title("NLPiffy with Streamlit")

	html_temp = """
    <div style="background-color:#000a25;padding:1px">
    <h1 style="color:white;text-align:center;">NLPiffy with Streamlit</h1>
	<h3 style="color:white;text-align:center;">Natural Language Processing On the Go...!</h3>
    <p style="color:white;text-align:center;" >This is a Natural Language Processing(NLP) Based App useful for basic NLP task Tokenization,NER,Sentiment,Summarization.</p>
    </div> """
	
	st.markdown(html_temp,unsafe_allow_html=True)
	
	image = Image.open('nlp_h.jpg')
	
	st.image(image, use_column_width=True,format='PNG')

	# Tokenization
	if st.checkbox("Show Tokens and Lemma"):
		st.subheader("Tokenize Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Analyze"):
			nlp_result = text_analyzer(message)
			st.json(nlp_result)

	# Entity Extraction
	if st.checkbox("Show Named Entities"):
		st.subheader("Analyze Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Extract"):
			entity_result = entity_analyzer(message)
			st.json(entity_result)

	# Sentiment Analysis
	if st.checkbox("Show Sentiment Analysis"):
		st.subheader("Analyse Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		if st.button("Analyze"):
			blob = TextBlob(message)
			result_sentiment = blob.sentiment
			st.success(result_sentiment)

	# Summarization
	if st.checkbox("Show Text Summarization"):
		st.subheader("Summarize Your Text")

		message = st.text_area("Enter Text","Type Here ..")
		summary_options = st.selectbox("Choose Summarizer",['sumy','gensim'])
		if st.button("Summarize"):
			if summary_options == 'sumy':
				st.text("Using Sumy Summarizer ..")
				summary_result = sumy_summarizer(message)
			elif summary_options == 'gensim':
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)
			else:
				st.warning("Using Default Summarizer")
				st.text("Using Gensim Summarizer ..")
				summary_result = summarize(message)

		
			st.success(summary_result)

	html_temp1 = """
    <div style="background-color:#000a25">
    <p style="color:white;text-align:center;" >Designe & Developed By: <b>Nilesh Verma</b> </p>
    </div>
    """
	st.markdown(html_temp1,unsafe_allow_html=True)
	

if __name__ == '__main__':
	main()
