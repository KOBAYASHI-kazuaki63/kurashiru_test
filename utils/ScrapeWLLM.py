import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI
from tqdm import tqdm

load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

OPENAI_API_KEY = os.getenv("PENAI_API_KEY")

output_format = """
    {"info": {
    keywordInfo: [xx],
    headInfo: {
      videoLink: "",
      captureLink: "",
      name: "xx",
      description:
        "xx",
      time: xx,
      cost: xx,
    },
    material: [
      {
        name: xx,
        volumn: xx,
      },
    ],
    procedure: ["aaa", "bbbb"],
    point: xx,
    review: {
      star: xx,
      reviewCount: xx,
      moreInfo: xx,
      userReview: [
        {
          userName: xx,
          userIcon: xx,
          capture: xx,
          date: xx,
          reviewStar: xx,
          reviewComment: xx
        },
      ],
    },
    frequenQuestions: [
      {
        questionContent: "xx",
        questionAnswer:
          "xx",
      },
    ],
    question: [
      {
        userIcon: "xx",
        questionUser: "xx",
        quesionContent: "xx",
        answer: "xx",
      },
    ],
    relative_receipt:[
    {
        relativeCookCapture:xx,
        relativeCookName:xx,
        relativeCookDescription:xx
    },
    ]
  },}
"""


class ScrapeWLLM:
    def __init__(self, list_url: list) -> None:
        self.list_url = list_url

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.session = requests.Session()
        retries = Retry(
            total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def scrape(self) -> list:
        l_result = []
        for url in tqdm(self.list_url, desc="Scraping URLs"):
            result = self.fetch_html(url)
            l_result.append(result)
        return l_result

    def fetch_html(self, url: str) -> dict:
        print(f"Fetching URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            return self.call_gemini(soup)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return [{"message": f"Error fetching the URL: {e}"}]

    def call_gemini(self, html_content: str) -> dict:
        prompt = """
        # 依頼
        下記のHTMLの中から.webmの動画URL（videoLink）、サムネイルURL(captureLink)、レシピタイトル(name)、説明文(description)、調理時間(time)、費用目安(cost)、材料名(material)、手順(procedure)、ポイント(point)、たべれぽ（review）、よくある質問(frequenQuestions)、質問(question)、このレシピに関連するレシピ（relative_receipt）を抽出してください。
        {html_content}

        # フォーマット
        {format}
""".format(
            html_content=html_content, format=output_format
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "HTMLの解析を、必ずフォーマットを守ってJSON形式で返却してください。",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            response_message = response.choices[0].message.content
            print(response_message)
            return json.loads(response_message)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return [{"message": "Invalid JSON response from Gemini"}]
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return [{"message": f"Error calling Gemini: {e}"}]
