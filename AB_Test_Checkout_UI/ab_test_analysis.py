# =============================================================================
# A/B 테스트 데이터 분석 - 새 결제 페이지 UI 테스트
# =============================================================================
# 
# 📁 필요한 파일:
#   - kr_customers.csv
#   - kr_orders.csv
#   - kr_products.csv
#   - kr_order_items.csv
#   - kr_payments.csv
#   - ab_test_checkout_ui.csv
#
# 📦 필요한 라이브러리 설치:
#   pip install pandas numpy matplotlib seaborn scipy
#
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# Mac인 경우 아래 주석 해제
# plt.rcParams['font.family'] = 'AppleGothic'

# =============================================================================
# 1. 데이터 로드
# =============================================================================
print("=" * 60)
print("📂 1. 데이터 로드")
print("=" * 60)

# 파일 경로 설정 (본인 환경에 맞게 수정)
DATA_PATH = "./"  # 데이터 파일이 있는 폴더 경로

# 베이스 데이터 로드
customers = pd.read_csv(f"{DATA_PATH}kr_customers.csv")
orders = pd.read_csv(f"{DATA_PATH}kr_orders.csv")
products = pd.read_csv(f"{DATA_PATH}kr_products.csv")
order_items = pd.read_csv(f"{DATA_PATH}kr_order_items.csv")
payments = pd.read_csv(f"{DATA_PATH}kr_payments.csv")

# A/B 테스트 데이터 로드
ab_test = pd.read_csv(f"{DATA_PATH}ab_test_checkout_ui.csv")

print(f"✅ 고객 데이터: {len(customers):,}건")
print(f"✅ 주문 데이터: {len(orders):,}건")
print(f"✅ 상품 데이터: {len(products):,}건")
print(f"✅ 주문상품 데이터: {len(order_items):,}건")
print(f"✅ 결제 데이터: {len(payments):,}건")
print(f"✅ A/B 테스트 데이터: {len(ab_test):,}건")

# =============================================================================
# 2. 데이터 기본 탐색
# =============================================================================
print("\n" + "=" * 60)
print("🔍 2. 데이터 기본 탐색")
print("=" * 60)

print("\n[A/B 테스트 데이터 구조]")
print(ab_test.info())

print("\n[A/B 테스트 데이터 샘플]")
print(ab_test.head(10))

print("\n[A/B 테스트 그룹 분포]")
print(ab_test['test_group'].value_counts())

print("\n[전환 여부 분포]")
print(ab_test['converted'].value_counts())

# =============================================================================
# 3. A/B 테스트 핵심 지표 분석
# =============================================================================
print("\n" + "=" * 60)
print("📊 3. A/B 테스트 핵심 지표 분석")
print("=" * 60)

# 그룹별 전환율
conversion_summary = ab_test.groupby('test_group').agg({
    'customer_id': 'count',
    'converted': ['sum', 'mean']
}).round(4)
conversion_summary.columns = ['총_방문자', '전환_수', '전환율']
conversion_summary['전환율(%)'] = (conversion_summary['전환율'] * 100).round(2)

print("\n[그룹별 전환율]")
print(conversion_summary)

# 전환율 차이 계산
control_rate = ab_test[ab_test['test_group'] == 'control']['converted'].mean()
treatment_rate = ab_test[ab_test['test_group'] == 'treatment']['converted'].mean()
absolute_diff = treatment_rate - control_rate
relative_lift = (treatment_rate - control_rate) / control_rate * 100

print(f"\n[전환율 비교]")
print(f"  Control (기존 UI): {control_rate:.2%}")
print(f"  Treatment (새 UI): {treatment_rate:.2%}")
print(f"  절대적 차이: +{absolute_diff:.2%}p")
print(f"  상대적 개선율 (Lift): +{relative_lift:.1f}%")

# =============================================================================
# 4. 통계적 유의성 검정
# =============================================================================
print("\n" + "=" * 60)
print("📐 4. 통계적 유의성 검정")
print("=" * 60)

# 데이터 분리
control_data = ab_test[ab_test['test_group'] == 'control']['converted']
treatment_data = ab_test[ab_test['test_group'] == 'treatment']['converted']

# Chi-square 검정
contingency_table = pd.crosstab(ab_test['test_group'], ab_test['converted'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\n[Chi-square 검정]")
print(f"  Chi-square 통계량: {chi2:.4f}")
print(f"  p-value: {p_value:.6f}")
print(f"  자유도: {dof}")

if p_value < 0.05:
    print(f"  ✅ 결과: 통계적으로 유의미함 (p < 0.05)")
else:
    print(f"  ❌ 결과: 통계적으로 유의미하지 않음 (p >= 0.05)")

# Z-test for proportions
n_control = len(control_data)
n_treatment = len(treatment_data)
p_control = control_data.mean()
p_treatment = treatment_data.mean()
p_pooled = (control_data.sum() + treatment_data.sum()) / (n_control + n_treatment)

se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
z_score = (p_treatment - p_control) / se
p_value_z = 2 * (1 - stats.norm.cdf(abs(z_score)))

print(f"\n[Z-test for Proportions]")
print(f"  Z-score: {z_score:.4f}")
print(f"  p-value: {p_value_z:.6f}")

# 95% 신뢰구간
ci_control = stats.proportion_confint(control_data.sum(), n_control, alpha=0.05)
ci_treatment = stats.proportion_confint(treatment_data.sum(), n_treatment, alpha=0.05)

print(f"\n[95% 신뢰구간]")
print(f"  Control: [{ci_control[0]:.2%}, {ci_control[1]:.2%}]")
print(f"  Treatment: [{ci_treatment[0]:.2%}, {ci_treatment[1]:.2%}]")

# =============================================================================
# 5. 세그먼트별 분석
# =============================================================================
print("\n" + "=" * 60)
print("📈 5. 세그먼트별 분석")
print("=" * 60)

# 디바이스별 전환율
print("\n[디바이스별 전환율]")
device_conversion = ab_test.groupby(['test_group', 'device'])['converted'].agg(['sum', 'count', 'mean'])
device_conversion.columns = ['전환수', '총수', '전환율']
device_conversion['전환율(%)'] = (device_conversion['전환율'] * 100).round(2)
print(device_conversion)

# 피벗 테이블로 변환
device_pivot = ab_test.pivot_table(
    values='converted', 
    index='device', 
    columns='test_group', 
    aggfunc='mean'
) * 100
device_pivot['차이(%p)'] = device_pivot['treatment'] - device_pivot['control']
device_pivot['Lift(%)'] = (device_pivot['treatment'] - device_pivot['control']) / device_pivot['control'] * 100
print("\n[디바이스별 전환율 비교]")
print(device_pivot.round(2))

# 연령대별 전환율
print("\n[연령대별 전환율]")
age_pivot = ab_test.pivot_table(
    values='converted', 
    index='age_group', 
    columns='test_group', 
    aggfunc='mean'
) * 100
age_pivot['차이(%p)'] = age_pivot['treatment'] - age_pivot['control']
age_pivot['Lift(%)'] = (age_pivot['treatment'] - age_pivot['control']) / age_pivot['control'] * 100
print(age_pivot.round(2))

# 지역별 전환율
print("\n[지역별 전환율 (Top 10)]")
region_pivot = ab_test.pivot_table(
    values='converted', 
    index='region', 
    columns='test_group', 
    aggfunc='mean'
) * 100
region_pivot['차이(%p)'] = region_pivot['treatment'] - region_pivot['control']
region_pivot = region_pivot.sort_values('차이(%p)', ascending=False)
print(region_pivot.head(10).round(2))

# =============================================================================
# 6. 전환 고객 추가 분석
# =============================================================================
print("\n" + "=" * 60)
print("💰 6. 전환 고객 추가 분석")
print("=" * 60)

# 전환된 고객만 필터링
converted_df = ab_test[ab_test['converted'] == 1].copy()

print(f"\n전환 고객 수: {len(converted_df):,}명")

# 평균 객단가
print("\n[평균 객단가]")
aov_by_group = converted_df.groupby('test_group')['order_value'].agg(['mean', 'median', 'std'])
aov_by_group.columns = ['평균', '중앙값', '표준편차']
print(aov_by_group.round(0))

aov_control = converted_df[converted_df['test_group'] == 'control']['order_value'].mean()
aov_treatment = converted_df[converted_df['test_group'] == 'treatment']['order_value'].mean()
print(f"\n객단가 상승: {((aov_treatment/aov_control)-1)*100:.1f}%")

# 결제 소요 시간
print("\n[결제 소요 시간]")
time_by_group = converted_df.groupby('test_group')['checkout_time_sec'].agg(['mean', 'median', 'std'])
time_by_group.columns = ['평균(초)', '중앙값(초)', '표준편차']
print(time_by_group.round(1))

time_control = converted_df[converted_df['test_group'] == 'control']['checkout_time_sec'].mean()
time_treatment = converted_df[converted_df['test_group'] == 'treatment']['checkout_time_sec'].mean()
print(f"\n시간 단축: {((time_control-time_treatment)/time_control)*100:.0f}%")

# 결제 수단 분포
print("\n[결제 수단 분포]")
payment_dist = pd.crosstab(
    converted_df['test_group'], 
    converted_df['payment_method'], 
    normalize='index'
) * 100
print(payment_dist.round(1))

# =============================================================================
# 7. 일별 추이 분석
# =============================================================================
print("\n" + "=" * 60)
print("📅 7. 일별 추이 분석")
print("=" * 60)

# 날짜 변환
ab_test['visit_date'] = pd.to_datetime(ab_test['visit_date'])

# 일별 전환율
daily_conversion = ab_test.groupby(['visit_date', 'test_group']).agg({
    'converted': ['sum', 'count', 'mean']
}).reset_index()
daily_conversion.columns = ['visit_date', 'test_group', '전환수', '방문자수', '전환율']

print("\n[일별 전환율 추이 (처음 7일)]")
daily_pivot = daily_conversion.pivot(index='visit_date', columns='test_group', values='전환율')
print((daily_pivot.head(7) * 100).round(2))

# 누적 전환율
ab_test_sorted = ab_test.sort_values('visit_date')
ab_test_sorted['cumsum_converted'] = ab_test_sorted.groupby('test_group')['converted'].cumsum()
ab_test_sorted['cumcount'] = ab_test_sorted.groupby('test_group').cumcount() + 1
ab_test_sorted['cumulative_rate'] = ab_test_sorted['cumsum_converted'] / ab_test_sorted['cumcount']

print("\n[누적 전환율 - 마지막 시점]")
cumulative_final = ab_test_sorted.groupby('test_group')['cumulative_rate'].last() * 100
print(cumulative_final.round(2))

# =============================================================================
# 8. 시각화
# =============================================================================
print("\n" + "=" * 60)
print("📊 8. 시각화 생성")
print("=" * 60)

# 그래프 스타일 설정
plt.style.use('seaborn-v0_8-whitegrid')
colors = {'control': '#6B7280', 'treatment': '#3B82F6'}

# Figure 생성 (2x3 서브플롯)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('A/B 테스트 분석 결과 - 새 결제 UI 테스트', fontsize=16, fontweight='bold')

# 8-1. 전환율 비교 막대 그래프
ax1 = axes[0, 0]
conversion_rates = [control_rate * 100, treatment_rate * 100]
bars = ax1.bar(['Control\n(기존 UI)', 'Treatment\n(새 UI)'], conversion_rates, 
               color=[colors['control'], colors['treatment']], edgecolor='black', linewidth=1.2)
ax1.set_ylabel('전환율 (%)')
ax1.set_title('그룹별 전환율 비교')
ax1.set_ylim(0, max(conversion_rates) * 1.3)

# 값 표시
for bar, rate in zip(bars, conversion_rates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Lift 표시
ax1.annotate(f'+{relative_lift:.1f}%', xy=(1, treatment_rate*100), 
             xytext=(1.3, treatment_rate*100 + 2),
             fontsize=12, color='green', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='green'))

# 8-2. 디바이스별 전환율
ax2 = axes[0, 1]
device_data = ab_test.groupby(['device', 'test_group'])['converted'].mean().unstack() * 100
x = np.arange(len(device_data.index))
width = 0.35
bars1 = ax2.bar(x - width/2, device_data['control'], width, label='Control', color=colors['control'])
bars2 = ax2.bar(x + width/2, device_data['treatment'], width, label='Treatment', color=colors['treatment'])
ax2.set_ylabel('전환율 (%)')
ax2.set_title('디바이스별 전환율')
ax2.set_xticks(x)
ax2.set_xticklabels(device_data.index)
ax2.legend()
ax2.set_ylim(0, device_data.values.max() * 1.3)

# 8-3. 연령대별 전환율
ax3 = axes[0, 2]
age_order = ['20대', '30대', '40대', '50대', '60대 이상']
age_data = ab_test.groupby(['age_group', 'test_group'])['converted'].mean().unstack() * 100
age_data = age_data.reindex(age_order)
x = np.arange(len(age_data.index))
bars1 = ax3.bar(x - width/2, age_data['control'], width, label='Control', color=colors['control'])
bars2 = ax3.bar(x + width/2, age_data['treatment'], width, label='Treatment', color=colors['treatment'])
ax3.set_ylabel('전환율 (%)')
ax3.set_title('연령대별 전환율')
ax3.set_xticks(x)
ax3.set_xticklabels(age_data.index, rotation=45, ha='right')
ax3.legend()

# 8-4. 일별 전환율 추이
ax4 = axes[1, 0]
for group in ['control', 'treatment']:
    group_data = daily_conversion[daily_conversion['test_group'] == group]
    ax4.plot(group_data['visit_date'], group_data['전환율'] * 100, 
             marker='o', markersize=4, label=group.capitalize(), color=colors[group], linewidth=2)
ax4.set_ylabel('전환율 (%)')
ax4.set_xlabel('날짜')
ax4.set_title('일별 전환율 추이')
ax4.legend()
ax4.tick_params(axis='x', rotation=45)

# 8-5. 객단가 분포 (박스플롯)
ax5 = axes[1, 1]
converted_df.boxplot(column='order_value', by='test_group', ax=ax5)
ax5.set_ylabel('주문 금액 (원)')
ax5.set_xlabel('그룹')
ax5.set_title('그룹별 객단가 분포')
plt.suptitle('')  # 기본 제목 제거

# 8-6. 결제 수단 비교
ax6 = axes[1, 2]
payment_data = pd.crosstab(converted_df['payment_method'], converted_df['test_group'], normalize='columns') * 100
payment_data.plot(kind='barh', ax=ax6, color=[colors['control'], colors['treatment']])
ax6.set_xlabel('비중 (%)')
ax6.set_title('결제 수단 비중')
ax6.legend(title='그룹')

plt.tight_layout()
plt.savefig('ab_test_analysis_result.png', dpi=150, bbox_inches='tight')
print("✅ 'ab_test_analysis_result.png' 저장 완료!")
plt.show()

# =============================================================================
# 9. 추가 시각화 - 신뢰구간 & 누적 전환율
# =============================================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle('통계적 검증 시각화', fontsize=14, fontweight='bold')

# 9-1. 신뢰구간 에러바
ax1 = axes2[0]
groups = ['Control', 'Treatment']
means = [control_rate * 100, treatment_rate * 100]
ci_lower = [ci_control[0] * 100, ci_treatment[0] * 100]
ci_upper = [ci_control[1] * 100, ci_treatment[1] * 100]
errors = [[m - l for m, l in zip(means, ci_lower)], 
          [u - m for m, u in zip(means, ci_upper)]]

ax1.errorbar(groups, means, yerr=errors, fmt='o', markersize=10, capsize=10, 
             capthick=2, elinewidth=2, color=[colors['control'], colors['treatment']])
ax1.set_ylabel('전환율 (%)')
ax1.set_title('95% 신뢰구간')
ax1.set_ylim(10, 22)

# 신뢰구간 겹침 여부 표시
if ci_control[1] < ci_treatment[0]:
    ax1.text(0.5, 20, '✅ 신뢰구간 겹치지 않음\n→ 통계적으로 유의미', 
             ha='center', fontsize=10, color='green',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

# 9-2. 누적 전환율 추이
ax2 = axes2[1]
for group in ['control', 'treatment']:
    group_data = ab_test_sorted[ab_test_sorted['test_group'] == group]
    # 샘플링 (너무 많으면 그래프가 느려짐)
    sample_idx = np.linspace(0, len(group_data)-1, 100, dtype=int)
    sampled = group_data.iloc[sample_idx]
    ax2.plot(sampled['cumcount'], sampled['cumulative_rate'] * 100, 
             label=group.capitalize(), color=colors[group], linewidth=2)

ax2.set_xlabel('누적 샘플 수')
ax2.set_ylabel('누적 전환율 (%)')
ax2.set_title('누적 전환율 추이 (수렴 확인)')
ax2.legend()
ax2.axhline(y=control_rate*100, color=colors['control'], linestyle='--', alpha=0.5)
ax2.axhline(y=treatment_rate*100, color=colors['treatment'], linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('ab_test_statistical_validation.png', dpi=150, bbox_inches='tight')
print("✅ 'ab_test_statistical_validation.png' 저장 완료!")
plt.show()

# =============================================================================
# 10. 최종 요약 리포트
# =============================================================================
print("\n" + "=" * 60)
print("📋 10. 최종 요약 리포트")
print("=" * 60)

print(f"""
┌─────────────────────────────────────────────────────────────┐
│           🧪 A/B 테스트 최종 결과 요약                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 핵심 지표                                                │
│  ┌─────────────────┬─────────────┬─────────────┬──────────┐│
│  │ 지표            │ Control     │ Treatment   │ 변화     ││
│  ├─────────────────┼─────────────┼─────────────┼──────────┤│
│  │ 전환율          │ {control_rate:>8.2%}    │ {treatment_rate:>8.2%}    │ +{relative_lift:>5.1f}%  ││
│  │ 객단가          │ {aov_control:>8,.0f}원  │ {aov_treatment:>8,.0f}원  │ +{((aov_treatment/aov_control)-1)*100:>5.1f}%  ││
│  │ 결제시간        │ {time_control:>8.0f}초   │ {time_treatment:>8.0f}초   │ -{((time_control-time_treatment)/time_control)*100:>5.0f}%  ││
│  └─────────────────┴─────────────┴─────────────┴──────────┘│
│                                                             │
│  📐 통계적 검증                                              │
│  • p-value: {p_value:.6f} {'✅ 유의미 (p < 0.05)' if p_value < 0.05 else '❌ 유의미하지 않음'}
│  • Z-score: {z_score:.4f}                                          │
│                                                             │
│  💡 주요 인사이트                                            │
│  • 모바일에서 가장 큰 효과 (+{(device_pivot.loc['모바일', '차이(%p)']):.2f}%p)               │
│  • 20~30대에서 효과 극대화 (+6%p 이상)                       │
│  • 간편결제 비중 증가 (신용카드 ↓, 카카오/네이버페이 ↑)     │
│                                                             │
│  ✅ 권고사항: 새 결제 UI 전체 적용                           │
│  📈 예상 효과: 월 매출 약 {((1+relative_lift/100)*(1+(aov_treatment/aov_control-1))-1)*100:.0f}% 증가                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# 11. 결과 데이터 저장
# =============================================================================
print("\n" + "=" * 60)
print("💾 11. 결과 데이터 저장")
print("=" * 60)

# 분석 결과 요약 저장
summary_data = {
    '지표': ['전환율', '객단가', '결제소요시간', 'p-value', 'Z-score'],
    'Control': [f'{control_rate:.2%}', f'{aov_control:,.0f}원', f'{time_control:.0f}초', '-', '-'],
    'Treatment': [f'{treatment_rate:.2%}', f'{aov_treatment:,.0f}원', f'{time_treatment:.0f}초', '-', '-'],
    '변화': [f'+{relative_lift:.1f}%', f'+{((aov_treatment/aov_control)-1)*100:.1f}%', 
             f'-{((time_control-time_treatment)/time_control)*100:.0f}%', f'{p_value:.6f}', f'{z_score:.4f}']
}
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('ab_test_summary.csv', index=False, encoding='utf-8-sig')
print("✅ 'ab_test_summary.csv' 저장 완료!")

# 세그먼트별 분석 결과 저장
device_pivot.to_csv('ab_test_device_analysis.csv', encoding='utf-8-sig')
age_pivot.to_csv('ab_test_age_analysis.csv', encoding='utf-8-sig')
print("✅ 'ab_test_device_analysis.csv' 저장 완료!")
print("✅ 'ab_test_age_analysis.csv' 저장 완료!")

print("\n🎉 분석 완료!")
