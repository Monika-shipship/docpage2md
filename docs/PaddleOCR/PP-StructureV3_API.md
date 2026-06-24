---
title: "AI Studio-帮助文档"
source: "https://ai.baidu.com/ai-doc/AISTUDIO/Fmfz6oh2e"
author:
published:
created: 2026-06-24
description: "百度AI Studio是面向AI学习者的一站式开发实训平台. 本平台集合了AI课程, 深度学习样例工程, 各领域的经典数据集, 云端的超强运算及存储资源, 以及比赛和社区. 你可以学习AI课程，提升技能，平台提供视频、项目、文档一体化课程，为你打造沉浸式学习体验。你可以探索项目，交流分享，平台提供精彩的实战项目、高质量数据集，更有免费GPU计算资源和在线实训环境。你可以参加比赛，用实力证明自己。"
tags:
  - "clippings"
---
## PP-StructureV3 服务化部署调用示例及 API 介绍：

> [PaddleOCR 开源项目 GitHub 地址](https://github.com/PaddlePaddle/PaddleOCR/tree/release/3.3) ，本服务 **基于该开源项目的 PP-StructureV3 模型构建** 。
>
> **版本说明** ：PaddleOCR 官网当前对应的 **PaddleX 版本为 3.3.12** ， **PaddlePaddle 版本为 3.2.1** 。

## 1\. PP-StructureV3 产线介绍

PP-StructureV3是一套高效、全面的文档解析解决方案，能够从各类文档图像和PDF文件中提取结构化信息。通过结合光学字符识别（OCR）、图像处理和深度学习等前沿技术，PP-StructureV3能够识别并提取文档中的文本块、标题、段落、图片、表格、公式、图表等多种元素，将复杂的文档内容转化为机器可读的数据格式（如Markdown、JSON），极大提升了文档数据处理的效率和准确性。

PP-StructureV3产线主要包括以下模块：

- **预处理模块** ：包括文档图像方向分类和文本图像矫正，为后续处理提供高质量的输入。
- **版面区域检测模块** ：通过版面区域检测，精准定位并区分文档中的不同功能区域。
- **OCR识别模块** ：采用PP-OCRv5模型，高效识别文本检测区域中的文本内容。
- **文档元素识别模块（可选）** ：支持表格识别、公式识别、图表解析和印章识别，能够从多种复杂文档中提取丰富的结构化语义信息。
- **阅读顺序模块** ：实现多栏文档的阅读顺序恢复和版面结构还原，使结果更加贴合原始文档的逻辑结构。

PP-StructureV3在多种文档类型下均表现优异，尤其在复杂结构和多栏布局的文档处理中具有明显优势。下图展示了PP-StructureV3文档解析产线的整体流程：

![](https://paddle-model-ecology.bj.bcebos.com/paddlex/demo_image/algorithm_ppstructurev3.png)

## 2\. API 配额规则及错误码说明

请查看 [文档](https://ai.baidu.com/ai-doc/AISTUDIO/Xmjclapam)

## 3.服务调用示例（python）

```python
# Please make sure the requests library is installed
# pip install requests
import base64
import os
import requests

# API_URL 及 TOKEN 请访问 [PaddleOCR 官网](https://aistudio.baidu.com/paddleocr/task) 在 API 调用示例中获取。
API_URL = "<your url>"
TOKEN = "<access token>"

file_path = "<local file path>"

with open(file_path, "rb") as file:
    file_bytes = file.read()
    file_data = base64.b64encode(file_bytes).decode("ascii")

headers = {
    "Authorization": f"token {TOKEN}",
    "Content-Type": "application/json"
}

required_payload = {
    "file": file_data,
    "fileType": <file type>,  # For PDF documents, set \`fileType\` to 0; for images, set \`fileType\` to 1
}

optional_payload = {
    "useDocOrientationClassify": False,
    "useDocUnwarping": False,
    "useTextlineOrientation": False,
    "useChartRecognition": False,
}

payload = {**required_payload, **optional_payload}

response = requests.post(API_URL, json=payload, headers=headers)
print(response.status_code)
assert response.status_code == 200
result = response.json()["result"]

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for i, res in enumerate(result["layoutParsingResults"]):
    md_filename = os.path.join(output_dir, f"doc_{i}.md")
    with open(md_filename, "w", encoding="utf-8") as md_file:
        md_file.write(res["markdown"]["text"])
    print(f"Markdown document saved at {md_filename}")
    for img_path, img in res["markdown"]["images"].items():
        full_img_path = os.path.join(output_dir, img_path)
        os.makedirs(os.path.dirname(full_img_path), exist_ok=True)
        img_bytes = requests.get(img).content
        with open(full_img_path, "wb") as img_file:
            img_file.write(img_bytes)
        print(f"Image saved to: {full_img_path}")
    for img_name, img in res["outputImages"].items():
        img_response = requests.get(img)
        if img_response.status_code == 200:
            # Save image to local
            filename = os.path.join(output_dir, f"{img_name}_{i}.jpg")
            with open(filename, "wb") as f:
                f.write(img_response.content)
            print(f"Image saved to: {filename}")
        else:
            print(f"Failed to download image, status code: {img_response.status_code}")
```

对于服务提供的主要操作：

- HTTP请求方法为POST。
- 请求体和响应体均为JSON数据（JSON对象）。
- 当请求处理成功时，响应状态码为 `200` ，响应体的属性如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| `logId` | `string` | 请求的UUID。 |
| `errorCode` | `integer` | 错误码。固定为 `0` 。 |
| `errorMsg` | `string` | 错误说明。固定为 `"Success"` 。 |
| `result` | `object` | 操作结果。 |

- 当请求处理未成功时，响应体的属性如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| `logId` | `string` | 请求的UUID。 |
| `errorCode` | `integer` | 错误码。与响应状态码相同。 |
| `errorMsg` | `string` | 错误说明。 |

服务提供的主要操作如下：

- **`infer`**

进行文档解析。

`POST /layout-parsing`

## 4\. 请求参数说明

| 名称 | 参数 | 类型 | 含义 | 是否必填 |
| --- | --- | --- | --- | --- |
| `输入文件` | `file` | `string` | 服务器可访问的图像文件或PDF文件的URL，或上述类型文件内容的Base64编码结果。默认对于超过10页的PDF文件，只有前10页的内容会被处理。   要解除页数限制，请在产线配置文件中添加以下配置： ```html Serving:   extra:     max_num_input_imgs: null ``` | 是 |
| `文件类型` | `fileType` | `integer` ｜ `null` | 文件类型。 `0` 表示PDF文件， `1` 表示图像文件。若请求体无此属性，则将根据URL推断文件类型。 | 否 |
| `图片方向矫正` | `useDocOrientationClassify` | `boolean` \| `null` | 是否在推理时使用文档方向分类模块，开启后，可以自动识别并矫正 0°、90°、180°、270°的图片，默认初始化为 `False` 。 | 否 |
| `图片扭曲矫正` | `useDocUnwarping` | `boolean` \| `null` | 是否在推理时使用文本图像矫正模块，开启后，可以自动矫正扭曲图片，例如褶皱、倾斜等情况，默认初始化为 `False` 。 | 否 |
| `文本行方向矫正` | `useTextlineOrientation` | `boolean` \| `null` | 是否在推理时使用文本行方向分类模块，开启后，可以自动识别和矫正 0° 和 180° 的文本行，默认初始化为 `False` 。 | 否 |
| `印章识别` | `useSealRecognition` | `boolean` \| `null` | 是否在推理时使用印章文本识别子产线，开启后，可以识别文档中的印章内容，默认初始化为 `False` 。 | 否 |
| `表格识别` | `useTableRecognition` | `boolean` \| `null` | 是否在推理时使用表格识别子产线，开启后，可以将文档中的表格转换为HTML或Markdown的结构化格式；若不开启，表格会保留为图片形式，默认初始化为 `True` 。 | 否 |
| `公式识别` | `useFormulaRecognition` | `boolean` \| `null` | 是否在推理时使用公式识别子产线，开启后，可以将数学公式转换为LaTeX代码；若不开启，公式会按普通文本识别，默认初始化为 `True` 。 | 否 |
| `图表转表格` | `useChartRecognition` | `boolean` \| `null` | 是否在推理时使用图表解析模块，开启后，可以自动解析文档中的图表（如柱状图、饼图等）并转换为表格形式，方便查看和编辑数据，默认初始化为 `False` 。 | 否 |
| `复杂版面处理` | `useRegionDetection` | `boolean` \| `null` | 是否在推理时使用文档区域检测模块，开启后，可以更好地识别报纸、杂志等排版复杂的文档内容，提高识别准确性，默认初始化为 `True` 。 | 否 |
| `版面区域过滤强度` | `layoutThreshold` | `number` \| `object` \| `null` | 版面模型得分阈值。 `0-1` 之间的任意浮点数。如果不设置，将使用产线初始化的该参数值，默认初始化为 `0.5` 。 | 否 |
| `NMS后处理` | `layoutNms` | `boolean` \| `null` | 开启后，会自动移除重复或高度重叠的区域框 | 否 |
| `扩张系数` | `layoutUnclipRatio` | `number` \| `array` \| `object` \| `null` | 版面区域检测模型检测框的扩张系数。 任意大于 `0` 浮点数。如果不设置，将使用产线初始化的该参数值，默认初始化为 `1.0` 。 | 否 |
| `版面区域检测的重叠框过滤方式` | `layoutMergeBboxesMode` | `string` \| `object` \| `null` | - **large** ，设置为large时，表示在模型输出的检测框中，对于互相重叠包含的检测框，只保留外部最大的框，删除重叠的内部框； - **small** ，设置为small，表示在模型输出的检测框中，对于互相重叠包含的检测框，只保留内部被包含的小框，删除重叠的外部框； - **union** ，不进行框的过滤处理，内外框都保留； 如果不设置，将使用产线初始化的该参数值，默认初始化为 `large` 。 | 否 |
| `文本检测图像边长限制` | `textDetLimitSideLen` | `integer` \| `null` | 文本检测的图像边长限制。 大于 `0` 的任意整数。如果不设置，将使用产线初始化的该参数值，默认初始化为 `736` 。 | 否 |
| `文本检测图像边长限制类型` | `textDetLimitType` | `string` \| `null` | 文本检测的边长度限制类型。支持 `min` 和 `max` ， `min` 表示保证图像最短边不小于 `textDetLimitSideLen` ， `max` 表示保证图像最长边不大于 `textDetLimitSideLen` 。如果不设置，将使用产线初始化的该参数值，默认初始化为 `min` 。 | 否 |
| `文本检测像素阈值` | `textDetThresh` | `number` \| `null` | 文本检测像素阈值，输出的概率图中，得分大于该阈值的像素点才会被认为是文字像素点。 大于 `0` 的任意浮点数。如果不设置，将使用产线初始化的该参数值（默认为 `0.3` ）。 | 否 |
| `文本检测框阈值` | `textDetBoxThresh` | `number` \| `null` | 文本检测框阈值，检测结果边框内，所有像素点的平均得分大于该阈值时，该结果会被认为是文字区域。 大于 `0` 的任意浮点数。如果不设置，将使用产线初始化的该参数值（默认为 `0.6` ）。 | 否 |
| `扩张系数` | `textDetUnclipRatio` | `number` \| `null` | 文本检测扩张系数，使用该方法对文字区域进行扩张，该值越大，扩张的面积越大。大于 `0` 的任意浮点数。如果不设置，将使用产线初始化的该参数值（默认为 `1.5` ）。 | 否 |
| `文本识别阈值` | `textRecScoreThresh` | `number` \| `null` | 文本识别阈值，得分大于该阈值的文本结果会被保留。 大于 `0` 的任意浮点数。如果不设置，将使用产线初始化的该参数值（默认为 `0.0` ，即不设阈值）。 | 否 |
| `印章检测图像边长限制` | `sealDetLimitSideLen` | `integer` \| `null` | 印章文本检测的图像边长限制。 大于 `0` 的任意整数。如果不设置，将使用产线初始化的该参数值，默认初始化为 `736` 。 | 否 |
| `印章检测图像边长限制类型` | `sealDetLimitType` | `string` \| `null` | 印章文本检测的图像边长限制类型。支持 `min` 和 `max` ， `min` 表示保证图像最短边不小于 `sealDetLimitSideLen` 表示保证图像最长边不大于 `sealDetLimitSideLen` 。如果不设置，将使用产线初始化的该参数值，默认初始化为 `min` 。 | 否 |
| `印章检测文本检测像素阈值` | `sealDetThresh` | `number` \| `null` | 检测像素阈值。输出的概率图中，得分大于该阈值的像素点才会被认为是文字像素点。 大于 `0` 的任意浮点数 。如果不设置，将默认使用产线初始化的该参数值 `0.2` 。 | 否 |
| `印章文本检测框阈值` | `sealDetBoxThresh` | `number` \| `null` | 检测框阈值，检测结果边框内，所有像素点的平均得分大于该阈值时，该结果会被认为是文字区域。 大于 `0` 的任意浮点数 。如果不设置，将默认使用产线初始化的该参数值 `0.6` 。 | 否 |
| `印章检测扩张系数` | `sealDetUnclipRatio` | `number` \| `null` | 印章文本检测扩张系数，使用该方法对文字区域进行扩张，该值越大，扩张的面积越大。 大于 `0` 的任意浮点数 。如果不设置，将默认使用产线初始化的该参数值 `0.5` 。 | 否 |
| `印章文本识别阈值` | `sealRecScoreThresh` | `number` \| `null` | 印章文本识别阈值，得分大于该阈值的文本结果会被保留。 大于 `0` 的任意浮点数 。如果不设置，将默认使用产线初始化的该参数值 `0.0` 。即不设阈值。 | 否 |
| `有线表转HTML` | `useWiredTableCellsTransToHtml` | `boolean` | 是否启用有线表单元格检测结果直转HTML，启用则直接基于有线表单元格检测结果的几何关系构建HTML。 | 否 |
| `无线表转HTML` | `useWirelessTableCellsTransToHtml` | `boolean` | 是否启用无线表单元格检测结果直转HTML，启用则直接基于无线表单元格检测结果的几何关系构建HTML。 | 否 |
| `表格方向矫正` | `useTableOrientationClassify` | `boolean` | 是否启用表格使用表格方向分类，启用时当图像中的表格存在90°、180°、270°旋转时，能够将方向校正并正确完成表格识别。 | 否 |
| `单元格识别模式` | `useOcrResultsWithTableCells` | `boolean` | 是否启用单元格切分OCR，启用时会基于单元格预测结果对OCR检测结果进行切分和重识别，避免出现文字缺失情况。 | 否 |
| `有线表格端到端预测` | `useE2eWiredTableRecModel` | `boolean` | 是否启用有线表端到端表格识别模式，启用则不使用单元格检测模型，只使用表格结构识别模型。 | 否 |
| `无线表格端到端预测` | `useE2eWirelessTableRecModel` | `boolean` | 是否启用无线表端到端表格识别模式，启用则不使用单元格检测模型，只使用表格结构识别模型。 | 否 |
| `可视化` | `visualize` | `boolean` \| `null` | 支持返回可视化结果图及处理过程中的中间图像。开启此功能后，将增加结果返回时间。 - 传入 `true` ：返回图像。 - 传入 `false` ：不返回图像。 - 若请求体中未提供该参数或传入 `null` ：遵循产线配置文件 `Serving.visualize` 的设置。    例如，在产线配置文件中添加如下字段：   ```html Serving:   visualize: False ``` 将默认不返回图像，通过请求体中的 `visualize` 参数可以覆盖默认行为。如果请求体和配置文件中均未设置（或请求体传入 `null` 、配置文件中未设置），则默认返回图像。 | 否 |

- 请求处理成功时，响应体的 `result` 具有如下属性：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| `layoutParsingResults` | `array` | 文档解析结果。数组长度为1（对于图像输入）或实际处理的文档页数（对于PDF输入）。对于PDF输入，数组中的每个元素依次表示PDF文件中实际处理的每一页的结果。 |
| `dataInfo` | `object` | 输入数据信息。 |

`layoutParsingResults` 中的每个元素为一个 `object` ，具有如下属性：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| `prunedResult` | `object` | 产线对象的 `predict` 方法生成结果的 JSON 表示中 `res` 字段的简化版本，其中去除了 `input_path` 和 `page_index` 字段。 |
| `markdown` | `object` | Markdown结果。 |
| `outputImages` | `object` \| `null` | 参见产线预测结果的 `img` 属性说明。图像为JPEG格式，使用Base64编码。 |
| `inputImage` | `string` \| `null` | 输入图像。图像为JPEG格式，使用Base64编码。 |

`markdown` 为一个 `object` ，具有如下属性：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| `text` | `string` | Markdown文本。 |
| `images` | `object` | Markdown图片相对路径和Base64编码图像的键值对。 |
| `isStart` | `boolean` | 当前页面第一个元素是否为段开始。 |
| `isEnd` | `boolean` | 当前页面最后一个元素是否为段结束。 |

对于返回的数据结构及字段说明，请查阅 [文档](https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PP-StructureV3.html) 。

**注** ：如果在使用过程中遇到问题，欢迎随时在 [issue](https://github.com/PaddlePaddle/PaddleOCR/issues) 区提交反馈。