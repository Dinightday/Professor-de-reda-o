from langchain_google_genai import GoogleGenerativeAI
import streamlit as st
import os

try:
  api_key = st.secrets('GOOGLE_API_KEY')
except TypeError:
  api_key = os.getenv('GOOGLE_API_KEY')

st.set_page_config(layout='wide', page_title='Redação')

st.title('Professor de Redação')

c1, c2 = st.columns(2)

llm = GoogleGenerativeAI(model='gemini-2.5-flash',
temperature=0.2,
api_key=api_key)

with c1:
  tema = st.text_input('Coloque o tema:', width=400)
  st.markdown('---')
  colocar = st.text_area('Coloque a redação:', height=100)
  enviar = st.button('Enviar')
  prompt = f'''
Analise a redação enviada na caixa de texto sobre o tema: {tema}.

Restrições de Formato e Estrutura:
- Siga a estrutura dissertativa-argumentativa de 4 parágrafos (Introdução, D1, D2, Conclusão).
- Mantenha o tom objetivo e siga rigorosamente as regras.
- Não use negritos ou qualquer formatação especial.
- A resposta deve ser obrigatoriamente dividida em **três blocos** usando o separador //SEP//.

Formato de Saída OBRIGATÓRIO:
[BLOCO 1]//SEP//[BLOCO 2]//SEP//[BLOCO 3]

Detalhes dos Blocos:
1. BLOCO 1 (Nota IA): APENAS a porcentagem, com % no final.
2. BLOCO 2 (Nota Final): APENAS o número de 0 a 1000.
3. BLOCO 3 (Análise Completa): O restante da análise textual, incluindo:
    - Análise Estrutural: Avalie a adesão à fórmula de 4 parágrafos e o equilíbrio da argumentação.
    - Pontos Críticos: Aponte as falhas mais graves.
    - Dicas de Melhoria: Forneça sugestões objetivas.
    - Conectivos Sugeridos: Liste 3-5 conectivos adequados para o tema.

Conteúdo da Redação para Análise:
{colocar}
'''
  if enviar:
    with st.spinner('Carregando...'):
      response = llm.invoke(prompt)

      with c2:
        IA_nota = response.split('//SEP//')
        if len(IA_nota) == 3:
          IA = IA_nota[0].strip()
          nota_final = IA_nota[1].strip()
          analise = IA_nota[2].strip()

          st.metric(label='Porcentagem de IA', value=IA)
          st.metric(label='Nota', value=nota_final)
        st.subheader('Analise:', analise)
        st.write(analise)
