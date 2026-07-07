# -*- coding: utf-8 -*-
"""
약물 용량 계산 - 공통 데이터 & 로직 모듈
데스크탑(CustomTkinter) 앱과 웹(Streamlit) 앱이 공통으로 이 모듈을 사용합니다.

※ 교육용(고등학교 수업량 유연화 탐구활동) 참고자료입니다.
   실제 임상 투약 결정에는 사용할 수 없습니다.
"""

DRUGS = [
    dict(name="아세트아미노펜", eng="Acetaminophen", category="수용성", use="해열진통제",
         adult_min=500, adult_max=650, unit="mg (1회)",
         ped_status="가능", ped_mgkg_min=10, ped_mgkg_max=15,
         renal=False, narrow_ti=False,
         elderly_note="간기능이 저하된 경우 총 용량을 감량해야 합니다.",
         remark="과량 복용 시 간독성 위험이 있습니다.", source="약학정보원"),
    dict(name="이부프로펜", eng="Ibuprofen", category="지용성", use="NSAID(해열진통소염제)",
         adult_min=200, adult_max=400, unit="mg (1회)",
         ped_status="가능", ped_mgkg_min=5, ped_mgkg_max=10,
         renal=False, narrow_ti=False,
         elderly_note="신장기능이 저하된 노인은 신중하게 투여해야 합니다.",
         remark="위장장애·신독성에 주의해야 합니다.", source="약학정보원"),
    dict(name="아스피린", eng="Aspirin", category="수용성", use="해열진통/항혈소판제",
         adult_min=500, adult_max=500, unit="mg (1회, 해열진통 기준)",
         ped_status="금기", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="저용량 장기복용 시 출혈 위험을 모니터링해야 합니다.",
         remark="소아·청소년의 바이러스 감염 시 라이증후군 위험으로 금기입니다.", source="약학정보원"),
    dict(name="아목시실린", eng="Amoxicillin", category="수용성", use="페니실린계 항생제",
         adult_min=250, adult_max=500, unit="mg (1회, 1일 3회)",
         ped_status="가능", ped_mgkg_min=20, ped_mgkg_max=40,
         renal=True, narrow_ti=False,
         elderly_note="신장기능에 따라 용량 조절이 필요합니다.",
         remark="1일 총량(mg/kg/day)을 3회로 나눠 복용합니다.", source="e약은요"),
    dict(name="세팔렉신", eng="Cephalexin", category="수용성", use="세팔로스포린계 항생제",
         adult_min=250, adult_max=500, unit="mg (1회, 1일 4회)",
         ped_status="가능", ped_mgkg_min=25, ped_mgkg_max=50,
         renal=True, narrow_ti=False,
         elderly_note="신장기능 저하 시 투여 간격을 늘려야 합니다.",
         remark="1일 총량(mg/kg/day)을 4회로 나눠 복용합니다.", source="e약은요"),
    dict(name="아지스로마이신", eng="Azithromycin", category="지용성", use="마크로라이드계 항생제",
         adult_min=250, adult_max=500, unit="mg (1일 1회)",
         ped_status="가능", ped_mgkg_min=10, ped_mgkg_max=10,
         renal=False, narrow_ti=False,
         elderly_note="간기능이 저하된 경우 신중하게 투여해야 합니다.",
         remark="조직 침투력이 높은 항생제입니다.", source="약학정보원"),
    dict(name="세프트리악손", eng="Ceftriaxone", category="수용성", use="세팔로스포린계 항생제(주사)",
         adult_min=1000, adult_max=2000, unit="mg (1일 1회)",
         ped_status="가능", ped_mgkg_min=50, ped_mgkg_max=75,
         renal=True, narrow_ti=False,
         elderly_note="신장과 간에서 함께 배설되어 조정 폭이 상대적으로 작습니다.",
         remark="1일 총량(mg/kg/day) 기준입니다.", source="약학정보원"),
    dict(name="겐타마이신", eng="Gentamicin", category="수용성", use="아미노글리코사이드계 항생제",
         adult_min=None, adult_max=None, unit="체중당 정밀계산 필요",
         ped_status="전문의 판단", ped_mgkg_min=3, ped_mgkg_max=5,
         renal=True, narrow_ti=True,
         elderly_note="신독성·이독성 위험이 커서 혈중농도 모니터링이 필수입니다.",
         remark="1일 총량(mg/kg/day) 기준이며 TDM이 필요합니다.", source="대한약전"),
    dict(name="반코마이신", eng="Vancomycin", category="수용성", use="글리코펩타이드계 항생제",
         adult_min=None, adult_max=None, unit="체중당 정밀계산 필요",
         ped_status="전문의 판단", ped_mgkg_min=10, ped_mgkg_max=15,
         renal=True, narrow_ti=True,
         elderly_note="신장기능에 따라 투여 간격 조정과 TDM이 필수입니다.",
         remark="8~12시간마다 투여하는 1회 용량 기준입니다.", source="대한약전"),
    dict(name="암로디핀", eng="Amlodipine", category="지용성", use="고혈압약(칼슘채널차단제)",
         adult_min=5, adult_max=10, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="저용량(2.5mg)부터 시작하는 것을 권장합니다.",
         remark="기립성 저혈압에 주의해야 합니다.", source="약학정보원"),
    dict(name="로자르탄", eng="Losartan", category="지용성", use="고혈압약(ARB)",
         adult_min=50, adult_max=100, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="신장기능이 저하된 경우 저용량으로 시작해야 합니다.",
         remark="고칼륨혈증을 모니터링해야 합니다.", source="약학정보원"),
    dict(name="에날라프릴", eng="Enalapril", category="수용성", use="고혈압약(ACE억제제)",
         adult_min=5, adult_max=20, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=0.08, ped_mgkg_max=0.08,
         renal=True, narrow_ti=False,
         elderly_note="신장기능이 저하된 경우 용량을 감소시켜야 합니다.",
         remark="마른기침 부작용이 흔합니다.", source="약학정보원"),
    dict(name="메토프롤롤", eng="Metoprolol", category="지용성", use="베타차단제",
         adult_min=50, adult_max=100, unit="mg (1일 1~2회)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="서맥이나 심부전 악화 여부를 모니터링해야 합니다.",
         remark="갑작스러운 중단은 금지해야 합니다.", source="약학정보원"),
    dict(name="푸로세미드", eng="Furosemide", category="수용성", use="고리형 이뇨제",
         adult_min=20, adult_max=40, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=1, ped_mgkg_max=2,
         renal=True, narrow_ti=False,
         elderly_note="전해질(칼륨)과 탈수 상태를 모니터링해야 합니다.",
         remark="전해질 불균형에 주의해야 합니다.", source="약학정보원"),
    dict(name="디곡신", eng="Digoxin", category="수용성", use="강심배당체(부정맥/심부전)",
         adult_min=0.125, adult_max=0.25, unit="mg (1일 1회)",
         ped_status="전문의 판단(정밀계산)", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=True, narrow_ti=True,
         elderly_note="신장기능이 저하된 경우 축적 위험이 매우 높습니다.",
         remark="혈중농도 검사(TDM)를 병행해야 합니다.", source="대한약전"),
    dict(name="와파린", eng="Warfarin", category="지용성", use="항응고제",
         adult_min=None, adult_max=None, unit="개인별 적정용량 상이(1~10mg)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=True,
         elderly_note="간기능과 병용약물에 따라 용량이 크게 달라져 INR 모니터링이 필요합니다.",
         remark="비타민K 섭취량에 영향을 받습니다.", source="대한약전"),
    dict(name="메트포르민", eng="Metformin", category="수용성", use="제2형 당뇨병약",
         adult_min=500, adult_max=2000, unit="mg (1일 총량)",
         ped_status="사용 안함", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=True, narrow_ti=False,
         elderly_note="신장기능이 저하된 경우 유산산증 위험으로 감량하거나 금기해야 합니다.",
         remark="조영제 검사 전후 중단이 필요합니다.", source="약학정보원"),
    dict(name="인슐린(속효성)", eng="Insulin", category="수용성", use="당뇨병 주사제",
         adult_min=None, adult_max=None, unit="환자별 개별화(단위/kg)",
         ped_status="가능(1형 당뇨 필수)", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=True,
         elderly_note="저혈당 위험이 높아 세심한 모니터링이 필요합니다.",
         remark="저혈당 증상 교육이 필요합니다.", source="대한당뇨병학회"),
    dict(name="레보티록신", eng="Levothyroxine", category="지용성", use="갑상선호르몬제",
         adult_min=None, adult_max=None, unit="체중당 개별화(1.6mcg/kg)",
         ped_status="가능(선천성갑상선저하증)", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=True,
         elderly_note="저용량부터 시작하며 심장 부담을 고려해야 합니다.",
         remark="공복 복용이 원칙입니다.", source="약학정보원"),
    dict(name="프레드니솔론", eng="Prednisolone", category="지용성", use="부신피질호르몬제(스테로이드)",
         adult_min=5, adult_max=60, unit="mg (질환별 상이)",
         ped_status="가능", ped_mgkg_min=0.5, ped_mgkg_max=2,
         renal=False, narrow_ti=False,
         elderly_note="장기 복용 시 골다공증·혈당 상승을 모니터링해야 합니다.",
         remark="급격한 중단은 금지해야 합니다.", source="약학정보원"),
    dict(name="오메프라졸", eng="Omeprazole", category="지용성", use="위산분비억제제(PPI)",
         adult_min=20, adult_max=40, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=1, ped_mgkg_max=1,
         renal=False, narrow_ti=False,
         elderly_note="장기간 사용 시 골절 위험 등을 고려해야 합니다.",
         remark="", source="약학정보원"),
    dict(name="파모티딘", eng="Famotidine", category="수용성", use="위산분비억제제(H2차단제)",
         adult_min=20, adult_max=20, unit="mg (1일 2회)",
         ped_status="가능", ped_mgkg_min=0.5, ped_mgkg_max=0.5,
         renal=True, narrow_ti=False,
         elderly_note="신장기능이 저하된 경우 용량을 감소시켜야 합니다.",
         remark="", source="약학정보원"),
    dict(name="세티리진", eng="Cetirizine", category="수용성", use="항히스타민제(2세대)",
         adult_min=10, adult_max=10, unit="mg (1일 1회)",
         ped_status="연령별 용량 참고", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=True, narrow_ti=False,
         elderly_note="신장기능이 저하된 경우 감량을 고려해야 합니다.",
         remark="소아는 연령별 지정 용량을 따라야 합니다.", source="약학정보원"),
    dict(name="로라타딘", eng="Loratadine", category="지용성", use="항히스타민제(2세대)",
         adult_min=10, adult_max=10, unit="mg (1일 1회)",
         ped_status="연령별 용량 참고", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="간기능이 저하된 경우 감량을 고려해야 합니다.",
         remark="소아는 연령별 지정 용량을 따라야 합니다.", source="약학정보원"),
    dict(name="디펜히드라민", eng="Diphenhydramine", category="지용성", use="항히스타민제(1세대)",
         adult_min=25, adult_max=50, unit="mg (1회)",
         ped_status="가능", ped_mgkg_min=5, ped_mgkg_max=5,
         renal=False, narrow_ti=False,
         elderly_note="항콜린 부작용으로 인지기능 저하·낙상 위험이 커서 사용 자제가 권고됩니다.",
         remark="노인 부적절 약물(PIM) 목록에 포함됩니다.", source="약학정보원"),
    dict(name="아토르바스타틴", eng="Atorvastatin", category="지용성", use="고지혈증약(스타틴)",
         adult_min=10, adult_max=40, unit="mg (1일 1회)",
         ped_status="사용 안함", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="간기능과 근육통(횡문근융해) 여부를 모니터링해야 합니다.",
         remark="", source="약학정보원"),
    dict(name="심바스타틴", eng="Simvastatin", category="지용성", use="고지혈증약(스타틴)",
         adult_min=10, adult_max=40, unit="mg (1일 1회)",
         ped_status="사용 안함", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="병용 약물에 따른 근육 부작용 상호작용에 주의해야 합니다.",
         remark="자몽주스와 상호작용이 있습니다.", source="약학정보원"),
    dict(name="설트랄린", eng="Sertraline", category="지용성", use="항우울제(SSRI)",
         adult_min=50, adult_max=100, unit="mg (1일 1회)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="저용량부터 시작하며 낙상·저나트륨혈증을 모니터링해야 합니다.",
         remark="급격한 중단은 금지해야 합니다.", source="약학정보원"),
    dict(name="디아제팜", eng="Diazepam", category="지용성", use="항불안제/신경안정제",
         adult_min=2, adult_max=10, unit="mg (1일 총량)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="반감기가 길어 축적·낙상 위험이 커서 사용 자제가 권고됩니다.",
         remark="노인 부적절 약물(PIM) 목록에 포함됩니다.", source="대한노인병학회"),
    dict(name="로라제팜", eng="Lorazepam", category="수용성", use="항불안제/신경안정제",
         adult_min=1, adult_max=4, unit="mg (1일 총량)",
         ped_status="전문의 판단", ped_mgkg_min=None, ped_mgkg_max=None,
         renal=False, narrow_ti=False,
         elderly_note="산화대사를 거치지 않아 노인에게 상대적으로 선호됩니다.",
         remark="디아제팜보다 노인에게 상대적으로 안전합니다.", source="대한노인병학회"),
]

DISCLAIMER = ("본 결과는 고등학교 탐구활동을 위한 교육용 계산 예시이며, "
              "실제 처방·투약 결정에는 사용할 수 없습니다. "
              "정확한 용량은 반드시 의료진과 상의하세요.")


def get_drug_names():
    return [d["name"] for d in DRUGS]


def get_drug(name):
    for d in DRUGS:
        if d["name"] == name:
            return d
    return None


def get_narrow_ti_drugs():
    return [d["name"] for d in DRUGS if d["narrow_ti"]]


def get_normal_ti_drugs():
    return [d["name"] for d in DRUGS if not d["narrow_ti"]]


def calc_crcl(age, weight, creatinine, sex="M"):
    """Cockcroft-Gault 공식으로 크레아티닌청소율(mL/min)을 추정합니다."""
    crcl = ((140 - age) * weight) / (72 * creatinine)
    if sex == "F":
        crcl *= 0.85
    return crcl


def _unit_label(unit_text):
    return unit_text.split("(")[0].strip()


def calculate(drug_name, age, weight, creatinine=None, sex="M"):
    """
    약물명/나이/체중/(선택)크레아티닌/성별을 받아 결과를 계산합니다.
    반환값: {"lines": [...], "warnings": [...], "need_creatinine": bool}
    """
    drug = get_drug(drug_name)
    if drug is None:
        return {"lines": ["약물 정보를 찾을 수 없습니다."], "warnings": [], "need_creatinine": False}

    lines = [f"[{drug['name']} ({drug['eng']})] · 분류: {drug['category']} · {drug['use']}"]
    warnings = []
    need_creatinine = False

    if age < 18:
        if drug["ped_status"] in ("금기", "사용 안함"):
            lines.append(f"이 약물은 소아에게 권장되지 않습니다. (소아 사용: {drug['ped_status']})")
        elif drug["ped_mgkg_min"] is not None:
            low = drug["ped_mgkg_min"] * weight
            high = drug["ped_mgkg_max"] * weight
            capped = False
            # 소아 체중이 많이 나가도 계산값이 성인 최대 용량(1회 기준)을 넘을 수 없음 (ceiling dose)
            if drug["adult_max"] is not None:
                if high > drug["adult_max"]:
                    high = drug["adult_max"]
                    capped = True
                if low > drug["adult_max"]:
                    low = drug["adult_max"]
            if abs(low - high) < 1e-9:
                lines.append(f"권장 용량(참고): 약 {low:.1f} mg")
            else:
                lines.append(f"권장 용량(참고): 약 {low:.1f} ~ {high:.1f} mg")
            lines.append(f"소아 사용: {drug['ped_status']}")
            if capped:
                lines.append(f"※ 체중 기준 계산값이 성인 최대 용량(약 {drug['adult_max']}{_unit_label(drug['unit'])})을 "
                              f"초과하여, 성인 최대 용량으로 제한(상한선 적용)했습니다.")
        else:
            lines.append(f"체중당 정밀 계산이 어려운 약물입니다. (소아 사용: {drug['ped_status']}) 전문의 상담이 필요합니다.")

    elif age >= 65:
        if drug["adult_min"] is None:
            lines.append("개인별 정밀 계산이 필요한 약물로, 전문의 상담이 필요합니다.")
        else:
            base = (drug["adult_min"] + drug["adult_max"]) / 2
            unit = _unit_label(drug["unit"])
            if drug["renal"]:
                if creatinine:
                    crcl = calc_crcl(age, weight, creatinine, sex)
                    ratio = max(0.25, min(1.0, crcl / 100))
                    adjusted = base * ratio
                    lines.append(f"추정 크레아티닌청소율(CrCl): 약 {crcl:.1f} mL/min")
                    lines.append(f"신장기능 반영 조정 용량(참고): 약 {adjusted:.2f} {unit}")
                else:
                    need_creatinine = True
                    empirical = base * 0.75
                    lines.append(f"경험적 감량 용량(참고, 크레아티닌 미입력): 약 {empirical:.2f} {unit}")
                    warnings.append("이 약물은 신장으로 배설되는 약물입니다. 신장기능에 이상이 있다면 "
                                     "혈청 크레아티닌 수치를 입력하면 훨씬 정확한 용량 조정이 가능합니다.")
            else:
                lines.append(f"표준 성인 용량(참고): {drug['adult_min']}~{drug['adult_max']} {unit}")
        lines.append(f"노인 주의사항: {drug['elderly_note']}")

    else:
        if drug["adult_min"] is None:
            lines.append(f"표준 용량: {drug['unit']} — 개인별 정밀 계산이 필요합니다.")
        else:
            lines.append(f"표준 성인 용량(참고): {drug['adult_min']}~{drug['adult_max']} {drug['unit']}")

    if drug["remark"]:
        lines.append(f"참고: {drug['remark']}")

    if drug["narrow_ti"]:
        warnings.append("⚠ 이 약물은 '좁은 치료역' 약물입니다. 계산값만으로 투여할 수 없고 "
                         "혈중농도 모니터링(TDM) 등 전문적 관리가 반드시 필요합니다.")

    return {"lines": lines, "warnings": warnings, "need_creatinine": need_creatinine}
