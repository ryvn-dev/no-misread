# no-misread

一支 linter 加一個 Claude skill，管你跟 AI 之間來回的兩種文字：你寫給它的
prompt，和它寫回來給你的稿。prompt 檢查歧義，因為模型沒辦法反問你是什麼意思；
稿子檢查機器腔，因為讀的人一眼就認得出來。

<img src="assets/demo.svg" alt="終端機輸出：一段沒有禁用字、沒有破折號的文字仍然沒過，因為每一句都落在前一句的兩個字之內" width="760">

[English](README.md)

## 它檢查什麼

**任何文字都查**
- 隱形字元：零寬空格、word joiner、BOM、軟連字號。鍵盤打不出來，複製貼上
  也甩不掉，還會弄壞 `grep`。`--strip` 全部清掉，一個字都不動。
- 機器排版：破折號、彎引號、單字元刪節號。
- 被寫爛的詞、開場鋪陳、收尾總結、「不是 X，是 Y」句型、把動作推給抽象名詞、
  只喊重要卻不講是什麼。

**給人讀的稿子**：查句長節奏。上面那張圖就是重點：那段文字每一份字表都會放行，
但句長是 12、14、14、13、12。人寫出來是 4、31、9。`--check` 回報離散度
（`stdev_words`）和句長擠在中間的比例（`band_share`），兩個都不合格才判定，
所以刻意寫短的段落不會被冤枉。

**給 AI 讀的 prompt**：反過來查。模型會讀錯的縮寫、讀者問不到答案的
`may` / `might` / `could`、超過 25 字的句子。這種文字句子平、齊反而是對的，
節奏檢查會自動關掉。

模式不用你選。它讀完文字自己判斷，並把理由印出來：

```console
$ python3 nomisread.py --check my-prompt.md
  "direction": "going out to a machine",
  "direction_why": "detected: 26 句裡有 12 句以祈使句開頭"
```

判錯了就用 `--type prose` 或 `--type technical` 蓋過去。

<!-- no-misread: off -->
**中文另有一套規則**，看到中文自動切換：中文裡混半形標點（最明顯的破綻）、
翻譯腔句型、被寫爛的詞（「賦能」「顆粒度」「值得注意的是」），節奏改成算字數。
這份中文 README 的第一版被它抓出 87 個問題，現在這版是 0。
<!-- no-misread: on -->

## 安裝

```bash
npx skills add ryvn-dev/no-misread --skill no-misread --agent claude-code
```

或直接 clone：

```bash
git clone https://github.com/ryvn-dev/no-misread ~/.claude/skills/no-misread
```

Plugin：把這個 repo 加成 marketplace，安裝 `no-misread`。System prompt：
貼 `prompts/system-prompt.md`，約 250 字。Output style：
`output-styles/no-misread.md`。只想用 linter 本體：`lint/nomisread.py`
單檔、純標準庫，不用裝任何東西。

## 用法

```bash
SKILL=~/.claude/skills/no-misread

python3 "$SKILL/lint/nomisread.py" --strip draft.md > clean.md
python3 "$SKILL/lint/nomisread.py" --check clean.md
python3 "$SKILL/lint/nomisread.py" --learn 舊文章.md 筆記.md   # 校準
python3 "$SKILL/lint/nomisread.py" --self-test
```

或者直接跟 Claude 講：「把這段改得像人寫的」、「把這個 prompt 改到模型不會
誤讀」。

`--check` 有問題就 exit 1，可以接進 CI 當關卡。這個 repo 每次 push 都拿它
檢查自己的文件。

## 校準

`--learn` 量的是你自己寫的、沒經過模型的文字：你真實的句長分布，還有哪些
「被寫爛的詞」其實是你本來就在用的。之後的檢查就拿你的基準比，不用通用門檻。
你在自己四千字裡用了六次 `leverage`，它就不再抓，理由記在檔案裡。

它拒絕從模型產出學習，包括它自己剛改寫完的稿子。profile 放在
`~/.no-misread/voice.json`，跟著人走；repo 裡放 `./profile/voice.json`
就是團隊統一語氣，那份優先。

## 成績與限制

拿兩個模型、六種情境實測：每百字的問題數從 2.74 降到 1.34。給人讀的八格全部
改善；小模型上有兩格技術文字反而變差，細節和前提都在
[evals/results/RESULTS.md](evals/results/RESULTS.md)，第一條就先講明：
linter 量的是「有沒有照規則做」，不是文章好不好。

節奏檢查騙得過：每段塞一句三個字的短句，燈就綠了，文章卻更難看。沒有東西擋
得住這件事。那個數字是症狀回報，不是目標。

零分代表 regex 看得到的都乾淨，不代表這是人寫的。它也不對抗 AI 偵測器；該
揭露你用了 AI 的場合，就去揭露。

不要對原始碼跑 `--strip`：字串裡的彎引號被拉直，字串就變了。

## 授權

[MIT](LICENSE) © 2026 ryvn-dev。隨便用、隨便 fork、拿去賣都行，留著聲明就好。
它要是在你稿子裡抓到了什麼，給個星，下一個人才找得到它。
