import base64
import webbrowser
import time
import seaborn as sns

import streamlit as st
import pandas as pd
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# install
from fuzzywuzzy import fuzz
import subprocess

# 方法
# from  ChatFree.py import process_data

st.set_page_config(page_title="文创助手", page_icon="💬")

# Load data
data = pd.read_csv('static/data/filled_data.csv')

# 设置阈值
threshold = 70



if st.button('退出'):
    url = 'http://127.0.0.1:5000/mycollectp.html'
    webbrowser.open_new_tab(url)


# Image on the left

st.image('static/image/cy_L.png', use_column_width=True, width=800)
st.markdown("---")

st.markdown('''
           ### 文创助手
        ''')
st.markdown("---")


st.markdown('''
           ##### 请您填写以下内容，文创助手为您推算产品价格
        ''')
# Description on the right
st.markdown("---")


# 相似度匹配，大于百分之七十放入相似数组中
def find_similar_products(input_title, data, threshold):
    similar_products = []

    # 遍历数据集，找到与输入商品名称部分匹配的产品
    for idx, row in data.iterrows():
        ratio = fuzz.partial_ratio(input_title, row['title'])
        if ratio >= threshold:
            similar_products.append(row)

    return similar_products


# 加权平均价格，销量越高，权重越大
def calculate_weighted_average_price(similar_products):
    # 有相似产品
    if similar_products:
        total_price_times_deal_count = sum(product['price'] * product['deal_count'] for product in similar_products)
        total_deal_count = sum(product['deal_count'] for product in similar_products)

        if total_deal_count > 0:
            # 不等于0求加权平均价格
            weighted_average_price = total_price_times_deal_count / total_deal_count
            return weighted_average_price
        else:
            # 等于求平均价格
            average_price = sum(product['price'] for product in similar_products) / len(similar_products)
            return average_price
    # 没有相似产品
    else:
        # If there are no similar products, return None
        return None


def get_weighted_average_price_for_input_title(input_title, data, threshold):
    similar_products = find_similar_products(input_title, data, threshold)
    if similar_products:
        weighted_average_price = calculate_weighted_average_price(similar_products)
        return round(weighted_average_price, 2)
    else:
        return None


# 平均销量
def calculate_average_deal_count(similar_products):
    total_deal_count = sum(product['deal_count'] for product in similar_products)
    average_deal_count = total_deal_count / len(similar_products)
    return average_deal_count


def get_average_deal_count_for_input_title(input_title, data, threshold):
    similar_products = find_similar_products(input_title, data, threshold)
    if similar_products:
        average_deal_count = calculate_average_deal_count(similar_products)
        return round(average_deal_count, 0)
    else:
        return None


# Sidebar - Province selection
selected_province = st.selectbox('请选择省份', sorted(data['province'].unique()))
input_title = st.text_input('输入非遗商品名称来给出合适的定价:')
submitted = st.button('获得价格建议')
# 价格加权平均
if submitted:
    # similar_products = find_similar_products(input_title, data, threshold)
    # if similar_products:
    weighted_average_price = get_weighted_average_price_for_input_title(input_title, data, threshold)
    if weighted_average_price is not None:
        st.write(f" '{input_title}' 的建议价格为: {weighted_average_price}元")
    else:
        st.write("未在数据库中找到相似的产品，请尝试其他商品名称。")
# else:
#     st.write("未在数据库中找到相似的产品，请尝试其他商品名称。")


# 跳转语句
# submitted3 = st.button('询问暮词——销售策略建议')
# if submitted3:

#  # 调用 chat.py 中的函数并传递数据
# process_data(input_list)

# subprocess.Popen(['python', '非遗问答助手.py'])


# Filter data based on selected province
filtered_data = data[data['province'] == selected_province].sort_values(by='deal_count', ascending=False)

# st.markdown('<h1 style="color: black;">当前省份销售数据</h1>', unsafe_allow_html=True)


# 设置字体路径
font_path = 'static/font/汇文明朝体.otf'

# Display word cloud for selected province
wordcloud_text = ' '.join(filtered_data['title'])
wordcloud_selected_province = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(
    wordcloud_text)

# Display the title and image side by side

# Price distribution histogram
max_price = int(filtered_data['price'].max())  # Convert max price to integer
bins = range(0, max_price + 100, 100)  # Adjust bins

fig, ax = plt.subplots()
ax.hist(filtered_data['price'], bins=bins, color='orange', edgecolor='black')
ax.set_xlabel('Price')
ax.set_ylabel('Frequency')
ax.tick_params(axis='y', which='major', labelsize=8)  # Adjust y-axis tick label size


# Check if province and city names are the same
if selected_province not in filtered_data['city'].unique():
    # Sales quantity bar chart for each city
    city_sales_data = filtered_data.groupby(['province', 'city'])['deal_count'].sum().reset_index()

# Price statistics
price_stats = filtered_data['price'].describe()
price_df = pd.DataFrame({
    'Statistic': ['Max Price', 'Min Price', 'Mean Price'],
    'Value': [price_stats['max'], price_stats['min'], price_stats['mean']]
})

# Deal count statistics
deal_count_stats = filtered_data['deal_count'].describe()
deal_count_df = pd.DataFrame({
    'Statistic': ['Max Deal Count', 'Min Deal Count', 'Mean Deal Count'],
    'Value': [deal_count_stats['max'], deal_count_stats['min'], deal_count_stats['mean']]
})

# Display statistics side by side
