import os
import re

def generate_nav():
    # 1. 扫描当前目录下的所有 app 文件
    # Scan for files matching pattern app_*.html
    files = [f for f in os.listdir('.') if f.startswith('app_') and f.endswith('.html')]
    
    apps = []
    print(f"Found {len(files)} app files. Parsing metadata...")

    for f in files:
        # 解析文件名: app_001_name.html -> id: 1
        # Regex to extract ID from filename
        match = re.match(r'app_(\d+)_(.+)\.html', f)
        if match:
            app_id = int(match.group(1))
            
            # 读取文件内容获取 <title>
            # Read file content to extract <title> tag
            title = f
            try:
                with open(f, 'r', encoding='utf-8') as html_file:
                    content = html_file.read()
                    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                    if title_match:
                        title = title_match.group(1)
            except Exception as e:
                print(f"Error reading {f}: {e}")
            
            apps.append({
                'id': app_id,
                'filename': f,
                'title': title
            })
    
    # 2. 按 ID 排序
    # Sort apps by ID
    apps.sort(key=lambda x: x['id'])
    
    # 3. 生成 HTML 内容
    total = len(apps)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>1000小程序计划 - 网页版</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans SC', sans-serif; }}
        .app-card {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            background-color: white;
            border-radius: 0.75rem;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            border: 1px solid #f1f5f9;
            transition: all 0.2s;
            font-size: 0.875rem;
            color: #475569;
            text-decoration: none;
            font-weight: 500;
            position: relative;
            overflow: hidden;
        }}
        .app-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-color: #6366f1;
            color: #4f46e5;
            z-index: 10;
        }}
        .badge-new {{
            position: absolute; top: 0; right: 0;
            background-color: #ef4444; width: 8px; height: 8px; border-radius: 50%;
            margin: 6px;
        }}
    </style>
</head>
<body class="bg-slate-50 min-h-screen">

    <header class="bg-indigo-600 text-white shadow-lg sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                1000小程序计划
            </h1>
            <div class="text-sm bg-indigo-700 px-4 py-1.5 rounded-full flex items-center gap-2 shadow-inner">
                当前进度: <span class="font-bold text-yellow-300 text-lg font-mono">{total}</span> / 1000
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        
        <!-- Search Filter -->
        <div class="max-w-md mx-auto mb-8 relative">
            <input type="text" id="search" placeholder="搜索小程序 (Search)..." class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm transition" onkeyup="filterApps()">
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4" id="app-grid">
"""

    # 4. 生成卡片 HTML
    for app in apps:
        app_id = app['id']
        title = app['title']
        filename = app['filename']
        
        # 样式逻辑
        classes = "app-card"
        indicator = ""
        
        # 里程碑 (每50个)
        if app_id % 50 == 0:
            classes += " bg-yellow-50 border-yellow-200 text-yellow-800 font-bold ring-2 ring-yellow-200"
            title += " 🏆"
        # 最新生成的 5 个 (高亮显示)
        elif app_id > total - 5:
            classes += " bg-indigo-50 border-indigo-200 text-indigo-700 font-bold"
            indicator = '<div class="badge-new"></div>'
        
        display_id = f"{app_id:03d}"
        
        html += f'''            <a href="./{filename}" class="{classes}" data-search="{title.lower()} {app_id}">
                {indicator}
                <span class="opacity-40 mr-3 text-xs font-mono font-normal select-none">{display_id}</span>
                <span class="truncate">{title}</span>
            </a>
'''

    # Footer & Script
    html += """
        </div>
    </main>

    <footer class="text-center py-10 text-slate-400 text-sm">
        <p>&copy; 2026 1000小程序计划 | Hosted on GitHub Pages</p>
        <p class="text-xs mt-2 opacity-60">Last updated via Python Script</p>
    </footer>

    <script>
        function filterApps() {
            const input = document.getElementById('search').value.toLowerCase();
            const cards = document.querySelectorAll('.app-card');
            
            cards.forEach(card => {
                const text = card.getAttribute('data-search');
                if (text.includes(input)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>

</body>
</html>
"""

    # 5. 写入文件
    try:
        # 写入 index.html (供 GitHub Pages 默认访问)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Successfully generated index.html with {total} apps!")

        # 写入 navigation.html (供旧的小程序返回链接访问，内容与 index.html 完全一致)
        with open('navigation.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Successfully generated navigation.html (Compatibility Mode)!")
                
    except Exception as e:
        print(f"❌ Error writing file: {e}")

if __name__ == "__main__":
    generate_nav()