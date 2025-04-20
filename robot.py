from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatSparkLLM
from langchain_core.messages import HumanMessage


st.set_page_config(page_title="问答机器人")

# 设置首行内容
st.title('问答机器人')

# 设置左边的sidebar内容
with st.sidebar:
    # 设置输入openai_key和接口访问地址的两个输入框
    openai_key = st.text_input('OpenAI API Key', )
    openai_base_url = st.text_input('OpenAI BASE URL',)



def generate_response(input_text, open_ai_key, openai_base_url):
    #这个地方的id，key等自己去官网申请，这个时免费的，我的这个部分我就写的意思一下了
    app_id = '07'
    api_key = 'YzQ1'
    api_secret = 'af'
    spark_llm = ChatSparkLLM(
        spark_app_id=app_id, spark_api_key=api_key, spark_api_secret=api_secret
    )

    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=open_ai_key,
        base_url=openai_base_url
    )

    # 构造一个模板template和一个prompt，从这里你可以看到提示词工程(prompt  engineering)的重要性
    template = """
    你是一个大毛创造的机器人，你只回答用户关于美食方面的问题。
    你回答用户提示时使用的语言，尽量形象，可以适当给用户科普一下美食的来源等！
    如果用户的问题中没有出现地名或者没有出现如下词语则可以判定为与美食无关：‘吃饭、美食、可口、好吃的、口感、味道’

    案例：
    1. 用户问题：今天天气如何？ 你的回答：抱歉，我只负责回答和美食相关的问题。
    2. 用户问题：你是谁？你的回答：我是大毛的问答机器人，我只负责回答和美食有关的问题。
    3. 用户问题：今天股市表现如何？你的回答：抱歉我只负责回答和美食的问题

    以下是用户的问题：
    {question}
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # 构造一个输出解析器和链
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    response = chain.invoke({"question": input_text})
    st.info(response)


