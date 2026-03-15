import time
import webbrowser

from langchain.chains.llm import LLMChain
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_core.runnables import RunnableLambda
from operator import itemgetter
import base64
import streamlit as st
from zhipuai import ZhipuAI
from PIL import Image
import re

st.set_page_config(page_title="非遗探索", page_icon="💬")

client = ZhipuAI(api_key="baa1e0398bf908a20a363f992bf2283a.yes2lb7uYbjqc00C")  # 请填写您自己的APIKey

if st.button('退出'):
    url = 'http://127.0.0.1:5000/mycollectp.html'
    webbrowser.open_new_tab(url)


st.markdown('''
        ## 非遗探索之旅AI定制
    ''')

st.markdown('''
        ##### 古物不言，却独自承载着千百年来时光的尘埃;古物无声，却看遍了沧海桑田，潮涨潮落。沉默如古物，却不能成为我们忘却其价值甚至存在的理由。为此，了解非物质文化遗产，得其雅韵并使其再焕新机，可谓香草为萤，明亮夏夜。
    ''')

image = Image.open('static/image/b (10).jpg')

st.image(image,
         caption='',
         width=500
         )

st.slider("", 0, 100, (0, 100))

# “这是个性非遗的初步探索，决定了您的旅途的未来方向”替换为
st.markdown('''
           ##### 请您填写以下内容，AI将为您开启非遗探索之旅
        ''')


def get_personality(test_result):
    personalities = {
        range(5, 7): "创新匠人",
        range(7, 9): "传承领袖",
        range(9, 11): "学术研习者",
        range(11, 13): "艺术表现者",
        range(13, 15): "人文关怀者",
        range(15, 17): "探索冒险家",
        range(17, 19): "逻辑解析者",
        range(19, 20): "协调融合者",
        range(20, 21): "实效实践者"
    }
    for score_range, personality in personalities.items():
        if test_result in score_range:
            return personality
    return "未知"


def display_personality(personality):
    personalities_description = {
        "创新匠人": "富有创意，善于融合传统与现代元素，热衷于技艺革新。",
        "传承领袖": "组织力强，有领导魅力，致力于非遗文化的推广与传承。",
        "学术研习者": "热爱知识，深度探究非遗的历史渊源与文化内涵，擅长理论研究。",
        "艺术表现者": "情感丰富，擅长通过艺术形式表达对非遗的理解与感悟，追求美学体验。",
        "人文关怀者": "善良体贴，关注非遗与社区的关系，致力于非遗保护的社会效益。",
        "探索冒险家": "敢于尝试，乐于发掘非遗中的未知领域，热衷于非遗的跨界融合。",
        "逻辑解析者": "理性严谨，善于运用逻辑分析解读非遗现象，注重非遗项目的科学管理。",
        "协调融合者": "擅长沟通，能够协调各方关系，推动非遗项目顺利实施，注重团队协作。",
        "实效实践者": "务实高效，注重非遗项目的实际效果，擅长将非遗应用于日常生活。"
    }
    description = personalities_description.get(personality, "暂无描述")
    return description


def calculate_score(answers):
    score_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    total_score = sum(score_mapping[a] for a in answers)
    return total_score


test_questions = [
    {
        'question': '当面对一项非遗技艺时，你更倾向于：',
        'options': ['A：寻找新的表现手法和材料', 'B：组织展览或研讨会，让更多人了解',
                    'C：深入研究其历史背景和文化价值', 'D：将其融入自己的艺术创作中']
    },
    #
    {
        'question': '当在非遗保护工作中，你最关心的是：',
        'options': ['A：探索非遗与现代生活的结合点', 'B：系统梳理非遗资源，制定保护策略',
                    'C：通过非遗增进社区凝聚力', 'D：实现非遗项目的经济效益']
    },
    {
        'question': '当非遗项目面临困难时，你更可能：',
        'options': ['A：提出创新解决方案', 'B：协调各方资源，推动问题解决',
                    'C：分析问题根源，寻求科学应对', 'D：关注受影响的群体，提供支持']
    },
    {
        'question': '你的非遗兴趣主要源于：',
        'options': ['A：对传统技艺革新的热情', 'B：对文化遗产传承的责任感',
                    'C：对学术研究的热爱', 'D：对艺术表达的渴望']
    },

    {
        'question': '你认为非遗在现代社会的价值体现在：',
        'options': ['A：推动科技创新与跨界融合', 'B：作为文化软实力的重要组成部分',
                    'C：促进社会和谐与社区发展', 'D：实现经济价值与生活品质提升']
    }
]

reco = {
    "创新匠人": ['陶瓷艺术创新：如景德镇青花瓷创新设计、潮州手拉朱泥壶创新技艺',
                 '剪纸创新：如陕西剪纸与现代装饰艺术结合、立体剪纸创作',
                 '刺绣创新设计：如苏绣与现代服装设计融合、苗绣图案与时尚元素结合',
                 '木版年画创新制作：如杨柳青年画与当代审美结合的新作品',
                 '金属工艺创新研发：如景泰蓝工艺与现代家居饰品设计、银饰创新造型'],
    "传承领袖": ['传统节庆活动策划与组织：如端午龙舟赛、元宵灯会的创新举办',
                 '非遗传承人培训与管理：如组织非遗传承人研修班、传承体系构建',
                 '民间舞蹈团组建与演出：如组建汉唐舞团、推广民族民间舞蹈',
                 '口头传统与叙事史诗传播：如组织说书、评弹、史诗吟唱等公众活动'],
    # ...（其他人格类型的非遗项目推荐省略，按给定信息添加）
    "学术研习者": ['非遗文献整理与研究：如古籍修复与数字化、民间故事集编纂',
                   '非遗学术论文撰写：如发表关于非遗技艺、传承机制的研究成果',
                   '非遗历史档案编纂：如地方志中非遗项目整理、口述史记录',
                   '非遗知识讲座与研讨会：如举办专题讲座、参与国际学术会议'],
    "艺术表现者": ['传统戏曲表演：如京剧、越剧、川剧等剧目演绎与新编', '民间音乐演奏：如古琴独奏、民族管弦乐团音乐会',
                   '民间绘画与雕塑创作：如国画山水、人物画创作，石雕、木雕艺术品制作',
                   '传统服饰设计与展示：如旗袍改良设计、少数民族服饰走秀'],
    "人文关怀者": ['非遗教育进校园：如开设非遗课程、组织非遗手工课', '非遗与社区发展项目：如非遗工坊助力乡村产业振兴',
                   '非遗与公益慈善结合：如非遗义卖支持弱势群体、非遗公益广告制作',
                   '非遗与心理健康疗愈工作：如利用传统音乐疗法、陶艺疗法开展心理辅导'],
    "探索冒险家": ['非遗与科技融合创新：如VR/AR体验非遗技艺、3D打印在传统工艺中的应用',
                   '非遗与旅游线路开发：如非遗主题游、非遗体验式旅行',
                   '非遗与户外运动结合：如传统射箭与现代射箭比赛、风筝制作与放飞活动',
                   '非遗与国际文化交流：如参加国际非遗节、组织跨国非遗交流项目'],
    "逻辑解析者": ['非遗资源调查与评估：如地方非遗资源普查、濒危项目评估',
                   '非遗保护规划制定：如编制非遗保护五年规划、专项保护方案',
                   '非遗数字化建设与管理：如建立非遗数据库、开发非遗APP',
                   '非遗知识产权保护：如申请非遗专利、商标，处理侵权纠纷'],
    "协调融合者": ['非遗项目多方合作洽谈：如政府、企业、非营利组织间的合作协商',
                   '非遗工作坊组织与协调：如统筹非遗技艺传习、培训活动',
                   '非遗展览策划与布展：如设计非遗主题展览、组织策展团队',
                   '非遗跨区域交流活动：如组织非遗艺术家互访、联合举办非遗展览'],
    "实效实践者": ['非遗手工艺品制作与销售：如开设非遗手作店、线上电商平台运营',
                   '非遗美食烹饪与推广：如开设非遗美食餐厅、推广地方特色菜系',
                   '非遗技艺生活化应用：如将传统印染技艺用于现代家居纺织品',
                   '非遗与乡村振兴结合：如利用非遗产业带动农村就业、提升乡村文化品位']
}

answers = []
for i, question in enumerate(test_questions, start=1):
    st.markdown(f"#### {i}. {question['question']}")
    answer = st.radio("", question['options'])
    answers.append(answer[0])

test_result = calculate_score(answers)

submit_button = st.button('揭晓您的非遗传承角色')
if submit_button:

    st.success("正在揭晓...")
    with st.spinner("揭秘中..."):
        time.sleep(2)  # 模拟计算过程，实际可删除此行
    st.success("非遗传承角色揭晓！")

    st.subheader("您在非遗传承领域的角色为：")
    personality = get_personality(test_result)
    st.info(personality)

    st.subheader("您的非遗传承特质：")
    description = display_personality(personality)
    st.info(description)

    st.subheader("为您量身定制的非遗项目推荐：")
    recommended_projects = reco.get(personality, [])
    project_list = []

    for project in recommended_projects:
        project_list.append(f"- {project}")

    st.markdown("\n".join(project_list))
    st.session_state.final_result = description



# 添加文本框
st.subheader("非遗项目")
text_input = st.text_area("请输入您想体验的非遗文化项目：", "")

# 组合获取到的值
message_content = ""
if text_input:
    message_content += "想要体验的非遗文化项目: " + text_input

# 创建提交按钮
if st.button('提交', key="submit_button_1"):
    with st.spinner("暮词正在思考，请您稍作等待..."):
        question = message_content

        if question is not None:
            description = st.session_state.final_result
            system_prompt = st.text_area(
                "系统提示词",
                '''现在你需要扮演一个非物质文化遗产领域的专家和非物质文化探索之旅的规划专家，用户告诉你感兴趣的非遗项目，你要为他安排非物质文化遗产探索之旅，尽可能详细。如果你不知道问题的答案，就告诉用户该问题超出了自己的知识范围。如果用户询问你其他领域的问题，你可以礼貌地回答不清楚，无需进一步提问。

                                  -示例1-
                                  问题：想要体验的非遗项目——扎染
                                  答案：# 扎染非物质文化遗产探索之旅
                                  扎染，作为一种古老的手工印染技艺，在中国多个地区有着深厚的历史文化底蕴。为了让您全面深入地了解和体验扎染文化，以下是为您精心安排的非物质文化遗产探索之旅。
                                  第一站：大理白族自治州 - 云南省
                                  探索重点：大理白族扎染的文化传承与现代发展
                                  活动安排：
                                - 参观大理璞真扎染有限公司，了解国家级非遗项目“大理白族扎染”的传承和保护过程。
                                - 体验扎染工艺，亲手制作属于自己的扎染作品。
                                - 走访周城村，这里是白族扎染的重要发源地，感受白族文化和扎染艺术的交融。
                                - 探访中国第一个白族扎染博物馆，深入了解扎染的历史和技艺。

                                第二站：自贡市 - 四川省
                                探索重点：自贡扎染技艺的历史与现状
                                活动安排：
                                - 参观自贡市的扎染工坊，了解自贡扎染技艺的独特之处。
                                - 学习自贡扎染的传统手法，体验绞、缝、扎等多种扎染手法。
                                - 了解自贡扎染面临的挑战和保护措施，参与保护和传承活动。

                                第三站：云南省博物馆 - 云南省昆明市
                                探索重点：云南地区扎染技艺的多样性
                                活动安排：
                                - 参观云南省博物馆中的非物质文化遗产展览，观赏不同民族的扎染作品。
                                - 参加博物馆举办的扎染文化讲座，与专家学者交流扎染的历史和文化价值。

                                第四站：文化体验工作坊 - 各地
                                探索重点：亲手制作扎染工艺品
                                活动安排：
                                - 在专业指导下，参与扎染工作坊，从设计图案到完成作品，体验扎染的全过程。
                                - 创作个性化的扎染纪念品，如围巾、衣物、家居装饰品等。

                                第五站：当地市集 - 大理、自贡等地
                                探索重点：扎染产品的市场与商业价值
                                活动安排：
                                - 走访当地的市集和手工艺品市场，观察和购买各种扎染产品。
                                - 与当地手工艺人交流，了解扎染产品的销售情况和市场需求。

                                第六站：学术研究机构 - 相关大学或研究所
                                探索重点：扎染技艺的学术研究与创新
                                活动安排：
                                - 参观相关研究机构，了解扎染技艺的最新研究成果。
                                - 参与学术交流，探讨扎染技艺的创新发展和传承策略。

                                旅行小贴士：
                                - 请提前了解各地区的气候和穿着要求，以便做好相应的准备。
                                - 考虑到手工体验活动，建议穿着舒适，避免穿戴珍贵饰品。
                                - 可以提前学习一些基础的扎染知识和技巧，以便更好地参与体验活动。
                                - 尊重当地的文化习俗和工艺传承人，积极参与但不要干扰他们的日常工作。

                                通过这次非物质文化遗产探索之旅，您将能够深入体验和理解扎染技艺的独特魅力，感受传统手工艺与现代生活的完美结合。希望您的旅行充满收获和乐趣！
                                  '''

            )

            response_3 = client.chat.completions.create(
                model="glm-4",  # 填写需要调用的模型名称
                messages=[
                    {"role": "system",
                     "content": system_prompt},
                    {"role": "user",
                     "content": f"你好，以下是为您定制的非遗文化之旅：{question}{description}"}
                ],
                stream=True,
            )
            output_text = ""
            for chunk in response_3:
                if hasattr(chunk, 'choices') and chunk.choices:
                    output_text += chunk.choices[0].delta.content
            st.write(output_text)

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #f67280;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #ff9999;
    }
    </style>
    """,
    unsafe_allow_html=True
)
