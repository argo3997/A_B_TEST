"""
프로젝트 폴더 구조 자동 생성 스크립트
=====================================

사용법:
    python setup_project.py

이 스크립트를 실행하면 A/B 테스트 프로젝트에 필요한
모든 폴더 구조가 자동으로 생성됩니다.
"""

import os
import shutil

# 프로젝트 루트 폴더명
PROJECT_NAME = "AB_Test_Checkout_UI"

# 생성할 폴더 구조
FOLDERS = [
    "data/raw",
    "data/processed",
    "notebooks",
    "scripts",
    "outputs/figures",
    "outputs/reports",
    "tableau",
    "docs"
]

# 파일 이동 매핑 (원본 파일명 -> 목적지)
FILE_MAPPING = {
    # raw 데이터
    "kr_customers.csv": "data/raw/kr_customers.csv",
    "kr_orders.csv": "data/raw/kr_orders.csv",
    "kr_products.csv": "data/raw/kr_products.csv",
    "kr_order_items.csv": "data/raw/kr_order_items.csv",
    "kr_payments.csv": "data/raw/kr_payments.csv",
    
    # processed 데이터
    "ab_test_checkout_ui.csv": "data/processed/ab_test_checkout_ui.csv",
    
    # 노트북
    "AB_Test_Analysis.ipynb": "notebooks/AB_Test_Analysis.ipynb",
    
    # 스크립트
    "generate_kr_ecommerce.py": "scripts/01_generate_base_data.py",
    "generate_ab_test.py": "scripts/02_generate_ab_test_data.py",
    "ab_test_analysis.py": "scripts/03_analysis.py",
    
    # 문서
    "AB_Test_Strategy_1pager.md": "docs/AB_Test_Strategy_1pager.md",
    "README.md": "README.md",
    "requirements.txt": "requirements.txt"
}


def create_project_structure():
    """프로젝트 폴더 구조 생성"""
    
    print("="*50)
    print(f"🚀 프로젝트 구조 생성: {PROJECT_NAME}")
    print("="*50)
    
    # 프로젝트 루트 폴더 생성
    if not os.path.exists(PROJECT_NAME):
        os.makedirs(PROJECT_NAME)
        print(f"✅ 프로젝트 폴더 생성: {PROJECT_NAME}/")
    else:
        print(f"📁 프로젝트 폴더 존재: {PROJECT_NAME}/")
    
    # 하위 폴더 생성
    print("\n📂 폴더 구조 생성 중...")
    for folder in FOLDERS:
        folder_path = os.path.join(PROJECT_NAME, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"  ✅ {folder}/")
        else:
            print(f"  📁 {folder}/ (이미 존재)")
    
    # 파일 이동
    print("\n📄 파일 배치 중...")
    for src_file, dest_path in FILE_MAPPING.items():
        if os.path.exists(src_file):
            dest_full_path = os.path.join(PROJECT_NAME, dest_path)
            shutil.copy2(src_file, dest_full_path)
            print(f"  ✅ {src_file} -> {dest_path}")
        else:
            print(f"  ⚠️ {src_file} (파일 없음 - 나중에 수동 배치)")
    
    # .gitignore 생성
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# 데이터 파일 (용량이 크면 주석 해제)
# data/raw/*.csv
# data/processed/*.csv

# 출력물
outputs/figures/*.png
outputs/reports/*.csv
"""
    
    gitignore_path = os.path.join(PROJECT_NAME, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    print(f"\n✅ .gitignore 생성")
    
    print("\n" + "="*50)
    print("🎉 프로젝트 구조 생성 완료!")
    print("="*50)
    print(f"""
다음 단계:
1. cd {PROJECT_NAME}
2. pip install -r requirements.txt
3. jupyter notebook notebooks/AB_Test_Analysis.ipynb
""")


def print_tree():
    """폴더 구조 트리 출력"""
    
    print(f"""
📁 {PROJECT_NAME}/
│
├── 📁 data/
│   ├── 📁 raw/
│   │   ├── kr_customers.csv
│   │   ├── kr_orders.csv
│   │   ├── kr_products.csv
│   │   ├── kr_order_items.csv
│   │   └── kr_payments.csv
│   │
│   └── 📁 processed/
│       └── ab_test_checkout_ui.csv
│
├── 📁 notebooks/
│   └── AB_Test_Analysis.ipynb
│
├── 📁 scripts/
│   ├── 01_generate_base_data.py
│   ├── 02_generate_ab_test_data.py
│   └── 03_analysis.py
│
├── 📁 outputs/
│   ├── 📁 figures/
│   │   └── (시각화 이미지)
│   │
│   └── 📁 reports/
│       └── (분석 결과 CSV)
│
├── 📁 tableau/
│   └── (태블로 대시보드)
│
├── 📁 docs/
│   └── AB_Test_Strategy_1pager.md
│
├── .gitignore
├── requirements.txt
└── README.md
""")


if __name__ == "__main__":
    print_tree()
    
    response = input("\n이 구조로 프로젝트를 생성하시겠습니까? (y/n): ")
    if response.lower() == 'y':
        create_project_structure()
    else:
        print("취소되었습니다.")
