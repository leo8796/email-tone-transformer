# Development Notes

这个文档是我做第一个 AI project：Email Tone Transformer 时的开发复盘。

它不是正式 README，而是我自己以后复习用的。  
重点不是解释每个 function 怎么写，而是记录开发过程中真实遇到的坑、当时为什么卡住、背后的本质是什么。

代码具体怎么实现，以后看 repo 就能想起来；这里主要写那些以后只看代码不一定能想起来的开发问题。

---

## 1. 这个项目真正练的是什么

这个项目表面上是一个邮件语气改写工具：

```text
输入一封 email
选择一个 tone
调用 Gemini
输出改写后的 email 和 key changes
```

但它真正练的是一个最小 LLM app 的完整开发流程：

```text
用户输入
→ 程序构造 prompt
→ 调用 LLM API
→ 拿到模型输出
→ 程序处理输出
→ 展示结果
```

这和直接在 Gemini / ChatGPT 网页里问问题不一样。

网页里是：

```text
人直接和 AI 聊天
```

这个项目是：

```text
Python 程序调用 AI
```

所以这个项目的重点不是“邮件改写”这个功能本身，而是理解：

```text
怎么让自己的软件稳定地调用 LLM
怎么管理 API key
怎么处理依赖环境
怎么处理模型不稳定输出
怎么把项目包装成 GitHub repo
```

这是 LLM Engineering 的基础。

---

## 2. Mac 上 `python` 和 `python3` 的问题

一开始我运行：

```bash
python app.py
```

结果报错：

```text
zsh: command not found: python
```

当时容易误以为是 Python 没装好，或者项目坏了。

后来理解了：很多 Mac 默认没有 `python` 这个命令。  
Mac 上更常见的是：

```bash
python3
```

所以：

```bash
python app.py
```

可能找不到命令，而：

```bash
python3 app.py
```

可能可以运行。

但是这还不是最稳的方式，因为电脑里可能有多个 Python：

```text
macOS 系统自带 Python
自己安装的 Python
Cursor 创建的项目虚拟环境 Python
其他项目的 Python 环境
```

所以就算 `python3 app.py` 能跑，也不一定用的是我当前项目的虚拟环境。

最后更稳的运行方式是：

```bash
./.venv/bin/python app.py
```

这句话明确指定：

```text
用当前项目 .venv 里面的 Python 来运行 app.py
```

这样不会混到系统 Python 或其他 Python。

---

## 3. 为什么要用 `.venv`

我当时的理解是：

```text
我们创建了一个虚拟环境
然后在虚拟环境的 Python 里面下载 requirements
然后在虚拟环境里面跑 app.py
```

这个理解是对的。

`.venv` 的本质是：

```text
给当前项目创建一个独立的 Python 环境
```

为什么需要它？

因为不同项目可能需要不同的包、不同版本的包。如果全部装到全局 Python 里，时间久了容易混乱。

更重要的是，这次我遇到的实际问题就是：

```text
包可能安装在 A Python 环境里
但运行 app.py 时用的是 B Python 环境
```

这就会导致：

```text
我明明感觉已经安装过包
但运行时还是报 No module named ...
```

所以以后做 Python 项目时，要尽量养成这个习惯：

```text
一个项目一个 .venv
依赖装进这个 .venv
运行也用这个 .venv 里的 Python
```

最稳的命令：

```bash
./.venv/bin/python app.py
```

安装依赖也用同一个 Python：

```bash
./.venv/bin/python -m pip install -U google-genai python-dotenv
```

这可以保证：

```text
安装包的 Python
和
运行项目的 Python
是同一个环境
```

---

## 4. `pip: command not found` 的本质

一开始我运行：

```bash
pip install -U google-genai python-dotenv
```

结果报错：

```text
zsh: command not found: pip
```

这个不是项目代码错了，也不是包不存在，而是终端找不到一个叫 `pip` 的全局命令。

更稳的思路不是直接用 `pip`，而是让某个明确的 Python 去调用它自己的 pip：

```bash
python3 -m pip install -U google-genai python-dotenv
```

更稳的是：

```bash
./.venv/bin/python -m pip install -U google-genai python-dotenv
```

这句话的意思是：

```text
用当前项目 .venv 里的 Python
调用它对应的 pip
把包安装进当前项目环境
```

所以以后如果 `pip` 不行，不要慌，可以用：

```bash
python3 -m pip ...
```

如果项目有虚拟环境，优先用：

```bash
./.venv/bin/python -m pip ...
```

---

## 5. `No module named 'dotenv'` 的本质

运行项目时遇到过：

```text
ModuleNotFoundError: No module named 'dotenv'
```

一开始容易以为是 `.env` 文件错了，或者 `.env` 没创建好。

但真正原因是：

```text
当前运行 app.py 的 Python 环境里没有安装 python-dotenv 这个包
```

代码里写的是：

```python
from dotenv import load_dotenv
```

但是安装包的名字是：

```bash
python-dotenv
```

这里有一个容易混的点：

```text
安装包名：python-dotenv
代码 import 名：dotenv
```

所以看到：

```text
No module named 'dotenv'
```

要想到：

```text
当前 Python 环境缺少 python-dotenv
```

解决方法：

```bash
./.venv/bin/python -m pip install -U python-dotenv
```

这次我们也顺便安装 Gemini SDK：

```bash
./.venv/bin/python -m pip install -U python-dotenv google-genai
```

重点还是：要装进当前项目正在使用的 `.venv`。

---

## 6. `google-genai` 是什么，为什么要装

这个项目要调用 Gemini API，所以需要 Google 的 Python SDK：

```text
google-genai
```

代码里用：

```python
from google import genai
```

然后创建 Gemini client。

SDK 的作用是：

```text
Google 已经帮我封装好了和 Gemini API 通信的细节
我不用自己手写底层 HTTP 请求
```

如果没有 SDK，我可能要自己处理：

```text
API endpoint
headers
request body
authentication
response parsing
```

这样对第一个项目来说太复杂。

所以使用 SDK 的本质是：

```text
用官方工具包简化 API 调用
把注意力放在项目逻辑和 LLM workflow 上
```

---

## 7. `.gitignore` 为什么必须认真检查

`.gitignore` 里写：

```gitignore
.env
__pycache__/
.venv/
.DS_Store
```

这里最重要的是：

```text
.env
.venv/
```

`.env` 不能上传，因为里面有 API key。

`.venv/` 不上传，因为：

```text
它很大
它是本地环境
别人可以通过 requirements.txt 重建
```

`__pycache__/` 是 Python 自动生成的缓存。  
`.DS_Store` 是 macOS 自动生成的文件。  
这些都不应该上传。

上传 GitHub 前一定要跑：

```bash
git status
```

重点看有没有：

```text
.env
.venv/
```

如果 `.env` 出现在 `git status` 里，说明 `.gitignore` 没生效，必须先停下来修。  
不能带着 `.env` commit。

---

## 8. `requirements.txt` 的作用

`requirements.txt` 是项目依赖清单。

这个项目需要：

```txt
google-genai
python-dotenv
```

所以别人拿到项目后，可以运行：

```bash
pip install -r requirements.txt
```

或者：

```bash
python3 -m pip install -r requirements.txt
```

如果使用项目虚拟环境，也可以：

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

它的本质是：

```text
让别人知道这个项目需要哪些 Python 包
让项目可以在别的电脑上复现
```

所以：

```text
.venv 不上传
requirements.txt 上传
```

别人不需要我的 `.venv`，只需要依赖清单。

---

## 9. Cursor 里文件没保存的问题

开发过程中有一次运行结果不符合预期，后来发现 Cursor tab 上有小白点。

小白点表示：

```text
文件有改动但还没保存
```

如果文件没保存，Terminal 运行的还是旧版本。

解决方法：

```text
Command + S
```

以后运行项目之前，先确认主要文件都保存了：

```text
app.py
prompts.py
llm_client.py
.env
README.md
DEVELOPMENT_NOTES.md
```

这是一个很普通但很容易忽略的开发问题。

---

## 10. 为什么 prompt 里要强调 JSON，以及为什么要 JSON 输出

一开始我觉得：

```text
在 prompt 里面跟 Gemini 说清楚不就行了吗？
```

是的，prompt 里说清楚很重要。

但后来理解了：  
LLM 默认是聊天助手，不是普通函数。

如果只说：

```text
Rewrite this email in a friendly tone.
```

它可能会返回：

```text
Sure, here is a friendlier version:
...
```

这对人类看没问题，但对程序处理不稳定。

普通文本适合人看，比如：

```text
Rewritten Email:
Dear Professor...

Key Changes:
- ...
```

但程序很难稳定知道：

```text
哪部分是 rewritten email
哪部分是 key changes
```

JSON 更适合程序处理，比如：

```json
{
  "rewritten_email": "Dear Professor...",
  "tone": "friendly",
  "key_changes": [
    "Changed the greeting.",
    "Made the request more polite."
  ]
}
```

Python 可以直接访问：

```python
result["rewritten_email"]
result["key_changes"]
```

所以 prompt 里加了更严格的要求：

```text
Return only valid JSON.
Do not include markdown.
Do not include Markdown code block markers.
Do not include any explanation outside the JSON object.
```

这些要求的目的不是让邮件写得更好，而是：

```text
让 Gemini 输出更像程序可以处理的数据
减少它自由发挥
```

这就是 LLM app 和普通聊天的区别。

---

## 11. 为什么 prompt 说清楚了还要处理输出，以及 clean data 的意义

我当时问过：

```text
那在 prompt 里面跟他说清楚不行吗？
非要写这么复杂吗？
```

答案是：

```text
prompt 能解决大部分问题，但不能保证 100%
```

LLM 不是普通函数。普通函数你让它返回 dict，它基本就返回 dict。  
但 LLM 有时候会加解释、加 markdown、加代码块，或者返回的格式和我要求的不完全一样。

比如我希望它返回纯 JSON：

```json
{
  "rewritten_email": "...",
  "tone": "friendly",
  "key_changes": ["..."]
}
```

但模型有时可能不会只返回纯 JSON。它可能会在 JSON 外面包一层 Markdown 代码块。

也就是说，模型可能在开头多加：

```text
三个反引号 + json
```

在结尾多加：

```text
三个反引号
```

这对人类看没问题，因为这是 Markdown 代码块。  
但对 Python 的 `json.loads()` 来说不行，因为它只能解析纯 JSON。

对程序来说，这些多出来的 Markdown 标记就是“脏数据”。

所以这里的 clean data，本质就是：

```text
把模型返回的、不完全干净的文本
清理成程序可以继续处理的格式
```

在这个项目里，clean data 主要做的是：

```text
1. 去掉前后空格
2. 去掉开头的 Markdown JSON 代码块标记
3. 去掉开头的普通 Markdown 代码块标记
4. 去掉结尾的 Markdown 代码块标记
5. 得到尽可能接近纯 JSON 的文本
```

具体实现是这个函数：

```python
def clean_json_text(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    return text
```

这个函数的逻辑是：

```text
第一步：text.strip()
去掉模型返回内容前后的空格和换行。

第二步：如果开头是 Markdown JSON 代码块标记
就把这个标记去掉。

第三步：如果开头是普通 Markdown 代码块标记
也把它去掉。

第四步：如果结尾有 Markdown 代码块结束标记
也把它去掉。

最后返回清理后的文本。
```

举个例子，如果模型返回的内容本质上是：

```text
开头：Markdown JSON 代码块标记
中间：真正的 JSON
结尾：Markdown 代码块结束标记
```

清理后就只剩：

```text
真正的 JSON
```

然后程序再把清理后的文本交给：

```python
json.loads(raw_text)
```

这样 Python 才更有机会把它解析成 dictionary。

所以 `clean_json_text()` 的意义不是为了炫技，而是为了处理 LLM 输出里常见的小问题。

可以理解成：

```text
prompt = 事前约束模型
clean data = 事后清理模型输出
```

在真实 LLM app 里，这个思路很常见。

因为模型输出经常是“差一点就能用”：

```text
内容是对的
但格式多了一点东西
程序直接解析会失败
```

所以程序需要做一层清理。

这和普通数据处理里的 data cleaning 很像：

```text
用户输入可能有空格
CSV 可能有脏数据
网页抓取内容可能有 HTML 标签
LLM 输出可能有 markdown 包装
```

本质都是：

```text
真实世界的数据不会永远完美
程序要先清理，再处理
```

这个项目里的 clean data 只是最简单的一种：清理 LLM 返回文本里的 Markdown 包装。

以后做 RAG、Agent、爬虫、数据分析时，也会遇到类似问题：

```text
拿到的数据不是完全标准格式
要先清洗
再解析
再进入下一步逻辑
```

所以这一点很重要：

```text
LLM output 不能完全相信
要 prompt 约束 + 输出清理 + fallback 兜底
```

---

## 12. `prompts.py` 和 `llm_client.py` 的职责区别

这次很重要的理解是：

```text
prompts.py = 提前要求模型怎么回答
llm_client.py = 收到回答后检查、清理、解析
```

类比：

```text
prompts.py：
我提前告诉别人：请只交表格，不要写废话。

llm_client.py：
别人交来以后，我检查一下表格外面有没有套文件夹，有的话先拆掉。
```

所以这两个不是重复。

它们分别解决两个阶段的问题：

```text
prompt 阶段：尽量让模型按要求输出
response 阶段：模型输出不完美时做兜底
```

---

## 13. `json.loads()` 的限制

`json.loads()` 可以把 JSON 字符串变成 Python dictionary。

它能接受这种纯 JSON：

```json
{
  "rewritten_email": "Dear Professor...",
  "tone": "friendly",
  "key_changes": ["Made the request more polite."]
}
```

但它不能接受这种前面带解释的话：

```text
Sure, here is the JSON:
{
  ...
}
```

也不能接受在 JSON 外面包 Markdown 代码块的内容。

比如模型如果在开头加了：

```text
三个反引号 + json
```

然后在结尾加了：

```text
三个反引号
```

那对 `json.loads()` 来说就不是纯 JSON。

所以如果要用 `json.loads()`，就要确保输入尽量是纯 JSON。

这也是为什么 prompt 要强调格式，`llm_client.py` 也要做兜底。

---

## 14. 为什么要有 fallback

如果模型返回了无效 JSON，程序不能直接崩。

我原本希望模型返回的是纯 JSON，比如：

```json
{
  "rewritten_email": "Dear Professor...",
  "tone": "friendly",
  "key_changes": ["Made the request more polite."]
}
```

但模型有时可能返回普通文字，或者在 JSON 外面加 Markdown 包装。

比如它可能先说一句：

```text
Sure, here is the JSON:
```

然后再给 JSON。

或者它可能在 JSON 外面加代码块标记：

```text
开头多了：三个反引号 + json
结尾多了：三个反引号
```

这些内容对人类看没问题，但对 `json.loads()` 来说不是纯 JSON，所以会解析失败。

如果程序只写：

```python
return json.loads(raw_text)
```

那一旦模型输出不标准，整个程序就会报错中断。

所以需要 fallback。

fallback 的逻辑是：

```text
如果 JSON 解析成功
→ 返回 parsed dictionary

如果 JSON 解析失败
→ 不让程序崩
→ 把模型原始输出作为 rewritten_email 显示
→ 在 key_changes 里提示模型没有返回 valid JSON
```

这个设计的本质是：

```text
用户体验不能因为模型格式不完美就完全中断
```

也就是说，即使模型没有完全按 JSON 返回，用户至少还能看到模型给出的改写结果。

第一个项目里，这样的 fallback 已经够用了。

更正式的项目以后可以继续升级成：

```text
1. 如果 JSON 解析失败，自动让模型重试一次
2. 使用更严格的 schema 检查字段
3. 使用 Gemini structured output
4. 检查 rewritten_email / tone / key_changes 是否都存在
5. 如果字段缺失，给出更清楚的错误信息
```

这就是从 demo 项目走向更稳定 AI app 的方向。

---

## 15. 这次实际踩坑总结

这次主要踩了两大类坑。

第一类是 Python 环境问题：

```text
python 找不到
pip 找不到
包安装了但运行时找不到
dotenv 找不到
```

解决核心：

```text
明确使用 .venv
用 ./.venv/bin/python 运行
用 ./.venv/bin/python -m pip 安装
```

第二类是 LLM 输出问题：

```text
模型不一定严格返回 JSON
模型可能加 markdown
模型可能返回普通文本
```

解决核心：

```text
prompt 里更明确限制格式
llm_client.py 里做清理
JSON 解析失败时 fallback
```

---

## 16. 以后做类似项目的标准流程

以后再做小型 Python LLM project，可以按这个流程：

```text
1. 建项目文件夹
2. 创建 .venv
3. 写 requirements.txt
4. 写 .env.example
5. 写 .gitignore，确保 .env 和 .venv 被忽略
6. 写最小可运行代码
7. 用 ./.venv/bin/python app.py 跑通
8. 保存 example input / output
9. 写 README
10. 写 DEVELOPMENT_NOTES
11. git status 检查 secret 没被追踪
12. commit + push GitHub
```

---

## 17. 后续升级方向

这个项目现在是一个 terminal-based V1，已经完成了最小闭环。后续如果要升级，可以按优先级逐步做。

### 方向 1：加 Gradio UI

现在项目只能在 Terminal 里运行。  
下一步可以加一个简单的 Gradio web UI，让用户在网页里输入 email、选择 tone、点击按钮得到结果。

这样项目会更像一个真正能展示的 AI app。

可以新增：

```text
app_gradio.py
```

保留原来的 `app.py`，这样：

```text
app.py = terminal 版本
app_gradio.py = web UI 版本
```

### 方向 2：增加更多 tone

现在只有：

```text
professional
polite
concise
friendly
```

之后可以增加：

```text
apologetic
confident
academic
casual
persuasive
shorter
more natural
```

这能让项目功能更完整。

### 方向 3：增加 before / after 对比

现在输出主要是 rewritten email 和 key changes。

之后可以显示：

```text
Original Email
Rewritten Email
Key Changes
```

这样用户更容易看出模型到底改了什么。

### 方向 4：提高 JSON / structured output 稳定性

现在主要靠 prompt + cleanup + fallback。

以后可以继续升级为：

```text
更严格的 schema
response validation
retry when invalid JSON
Gemini structured output
```

这样项目会更接近生产级 AI app。

### 方向 5：支持多个模型 provider

现在只支持 Gemini。

以后可以抽象出 provider 层，支持：

```text
Gemini
OpenAI
Claude
local Ollama model
```

这样可以练习多模型切换，也更接近真实 LLM 工程项目。

### 方向 6：增加测试和错误处理

后续可以加：

```text
tests/
```

测试内容包括：

```text
tone 选择是否正确
prompt 是否包含 email 和 tone
API key 缺失时是否给出清楚错误
模型返回 invalid JSON 时 fallback 是否正常
```

这会让项目更像正式工程项目。

### 方向 7：部署

如果加了 Gradio UI，可以继续部署到：

```text
Hugging Face Spaces
Render
Railway
Vercel + backend
```

这样项目可以变成一个可访问的在线 demo。

---