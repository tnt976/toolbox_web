# Flask Web App

一个简单但功能完整的 Flask Web 应用示例，展示 Python Web 开发的基础架构和最佳实践。

## 功能特性

- 响应式主页，带有英雄区域和功能展示卡片
- 关于页面，介绍项目和技术栈
- 交互式演示页面，展示 API 调用功能
- 现代化的 UI 设计

## 技术栈

- **后端**: Flask 3.0
- **模板引擎**: Jinja2
- **前端**: HTML5, CSS3, Vanilla JavaScript
- **样式**: 自定义 CSS，无额外依赖

## 安装和运行

### 1. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 项目结构

```
/workspace/
├── app.py                 # Flask 应用主文件
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── static/               # 静态资源
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── main.js       # JavaScript 逻辑
└── templates/            # HTML 模板
    ├── base.html         # 基础模板
    ├── index.html        # 主页
    ├── about.html        # 关于页
    └── demo.html         # 演示页
```

## 路由说明

| 路由 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 主页 |
| `/about` | GET | 关于页面 |
| `/demo` | GET | 交互演示页面 |
| `/api/greet` | POST | API 端点，处理演示数据 |

## 开发说明

- 应用在调试模式下运行（`debug=True`），修改代码后会自动重载
- 所有静态文件位于 `static` 目录
- 模板文件位于 `templates` 目录，使用 Jinja2 模板引擎
