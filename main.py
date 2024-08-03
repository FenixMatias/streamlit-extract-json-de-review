import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """\
Para el siguiente texto, extraiga la siguiente \
información:

sentimiento: ¿Está satisfecho el cliente con el producto? 
Respuesta Positiva en caso afirmativo, Negativa en caso negativo \
no, Neutro si es cualquiera de ellos, o Desconocido si es desconocido.

días_entrega: Cuántos días tardó \
para que llegue el producto? Si este \
no se encuentra información, salida No hay información al respecto.

percepción_del_precio: ¿Cómo percibe el cliente el precio? 
Respuesta Caro si el cliente considera que el producto es caro, 
Barato si el cliente siente que el producto es barato,
no, Neutral si cualquiera de ellos, o Desconocido si es desconocido.

Formatee la salida como texto con viñetas con la opción \
siguientes claves:
- Sentimiento
- ¿Cuánto tardó en entregarse?
- ¿Cómo se percibió el precio?

Ejemplo de entrada:
Este vestido es increíble. Llegó en dos días, justo a tiempo para el regalo de aniversario de mi mujer. Es más barato que los otros vestidos que hay, pero creo que vale la pena por las características adicionales.

Ejemplo de salida:
- Sentimiento: Positivo
- ¿Cuánto tardó en entregarse? 2 días
- ¿Cómo se percibió el precio? Barato

text: {review}
"""

#Definición de variables PromptTemplate
prompt = PromptTemplate(
    input_variables=["review"],
    template=template,
)


#LLM y función de carga de llaves
def load_LLM(openai_api_key):
    """La lógica para cargar la cadena que desea utilizar debe ir aquí."""
    # Asegúrese de que su openai_api_key se establece como una variable de entorno
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    return llm


#Título y cabecera de la página
st.set_page_config(page_title="Extraer información clave de las reseñas de productos")
st.header("Extraer información clave de las reseñas de productos")


#Intro: instrucciones
col1, col2 = st.columns(2)

with col1:
    st.markdown("Extraer información clave de una reseña de producto.")
    st.markdown("""
        - Sentimiento
        - ¿Cuánto tardó en entregarse?
        - ¿Cómo se percibió su precio?
        """)

with col2:
    st.write("Contacte con [Matias Toro Labra](https://www.linkedin.com/in/luis-matias-toro-labra-b4074121b/) para construir sus proyectos de IA")


#Introducir la clave API de OpenAI
st.markdown("## Introduzca su clave API de OpenAI")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Entrada
st.markdown("## Introduzca la reseña del producto")

def get_review():
    review_text = st.text_area(label="Product Review", label_visibility='collapsed', placeholder="Your Product Review...", key="review_input")
    return review_text

review_input = get_review()

if len(review_input.split(" ")) > 700:
    st.write("Por favor, introduzca una reseña de producto más corta. La extensión máxima es de 700 palabras.")
    st.stop()

    
# Salida
st.markdown("### Datos clave extraídos:")

if review_input:
    if not openai_api_key:
        st.warning('Introduzca la clave de la API de OpenAI. \
            Instrucciones [aquí](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_review = prompt.format(
        review=review_input
    )

    key_data_extraction = llm(prompt_with_review)

    st.write(key_data_extraction)