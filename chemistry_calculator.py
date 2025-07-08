def get_float_input(prompt, allow_zero=False, allow_negative=False):
    """Helper function to get a valid float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if not allow_zero and value == 0:
                print("오류: 값은 0이 될 수 없습니다.")
            elif not allow_negative and value < 0:
                print("오류: 값은 음수가 될 수 없습니다.")
            else:
                return value
        except ValueError:
            print("오류: 유효한 숫자를 입력해주세요.")

def get_previous_study_info():
    """Gets information about the reagent used in the previous study."""
    print("\n--- 선행 연구 정보 입력 ---")
    m_a = get_float_input("선행 연구 시약의 몰 농도 (M_A)를 입력하세요: ", allow_zero=False)
    g_a = get_float_input("선행 연구에서 사용한 시약의 질량 (g_A)을 입력하세요: ", allow_zero=False)
    mw_a = get_float_input("선행 연구 시약의 분자량 (MW_A, g/mol)을 입력하세요: ", allow_zero=False)

    while True:
        p_a_input = input("선행 연구 시약의 순도 (P_A, %, 기본값 100)? [Enter로 기본값 사용]: ")
        if not p_a_input:
            p_a = 100.0
            break
        try:
            p_a = float(p_a_input)
            if not (0 < p_a <= 100):
                print("오류: 순도는 0보다 크고 100보다 작거나 같아야 합니다.")
            else:
                break
        except ValueError:
            print("오류: 유효한 숫자를 입력해주세요.")

    return {"m_a": m_a, "g_a": g_a, "mw_a": mw_a, "p_a": p_a}

def get_my_reagent_info(default_mw):
    """Gets information about the reagent the user has."""
    print("\n--- 보유 시약 정보 입력 ---")
    # M_B: 내가 가진 시약이 이미 용액 상태일 때 그 용액의 몰 농도
    m_b = get_float_input("보유 시약 용액의 몰 농도 (M_B)를 입력하세요: ", allow_zero=False)

    mw_b_input = input(f"보유 시약의 분자량 (MW_B, g/mol, 기본값: 선행 연구와 동일한 {default_mw} g/mol)? [Enter로 기본값 사용]: ")
    if not mw_b_input:
        mw_b = default_mw
    else:
        while True:
            try:
                mw_b = float(mw_b_input)
                if mw_b <= 0:
                    print("오류: 분자량은 0보다 커야 합니다.")
                    mw_b_input = input(f"보유 시약의 분자량 (MW_B, g/mol, 기본값: 선행 연구와 동일한 {default_mw} g/mol)? [Enter로 기본값 사용]: ")
                else:
                    break
            except ValueError:
                print("오류: 유효한 숫자를 입력해주세요.")
                mw_b_input = input(f"보유 시약의 분자량 (MW_B, g/mol, 기본값: 선행 연구와 동일한 {default_mw} g/mol)? [Enter로 기본값 사용]: ")

    # P_B: M_B가 이미 순도를 고려한 농도라면 이 값은 100%가 되어야 함.
    # 만약 M_B가 시약병 라벨의 농도이고, 그 시약의 순도가 P_B% 라면, 실제 계산 시 M_B_actual = M_B * (P_B/100)를 사용해야 함.
    # 현재 계획에서는 M_B를 이미 최종적인, 실제 사용할 수 있는 용액의 농도로 가정.
    # 사용자가 혼동하지 않도록 일단 순도 P_B는 입력받지 않거나, 100%로 고정하는 것을 고려.
    # 여기서는 M_B가 최종 농도라고 명시하고 P_B는 생략.
    print("참고: 입력하신 보유 시약 몰 농도(M_B)는 실제 사용 가능한 최종 용액의 농도로 간주합니다.")

    return {"m_b": m_b, "mw_b": mw_b}

if __name__ == '__main__':
    # 테스트를 위한 임시 실행
    # prev_info = get_previous_study_info()
    # print("\n선행 연구 정보:", prev_info)

    # my_reagent_info = get_my_reagent_info(default_mw=prev_info["mw_a"])
    # print("보유 시약 정보:", my_reagent_info)

def main():
    print("="*50)
    print("선행 연구 기반 시약 필요량 계산기")
    print("="*50)
    print("선행 연구에서 사용된 시약의 양을 기준으로,")
    print("현재 보유 중인 다른 농도의 시약 용액을 얼마나 사용해야 하는지 계산합니다.")

    try:
        # 1. 사용자 입력 받기
        prev_info = get_previous_study_info()
        # 선행 연구 시약의 분자량을 보유 시약 분자량의 기본값으로 전달
        my_reagent_info = get_my_reagent_info(default_mw=prev_info["mw_a"])

        # 입력값 추출
        g_a = prev_info["g_a"]
        mw_a = prev_info["mw_a"]
        p_a = prev_info["p_a"]
        m_a_input = prev_info["m_a"] # 결과 표시에 사용될 수 있음

        m_b = my_reagent_info["m_b"]
        mw_b = my_reagent_info["mw_b"]

        # 2. 계산 수행
        # 선행 연구에서 사용된 용질의 몰 수 계산
        moles_a_calculated = calculate_moles_from_previous_study(g_a, mw_a, p_a)

        # 해당 몰 수만큼의 용질을 얻기 위해 필요한 내 시약 용액의 부피 계산
        volume_b_needed = calculate_required_volume_of_my_reagent(moles_a_calculated, m_b)

        # 그 부피에 해당하는 용질의 질량 계산
        mass_b_solute_needed = calculate_mass_of_solute_in_my_reagent_volume(moles_a_calculated, mw_b)

        # 3. 결과 표시
        display_results(
            moles_a_calc=moles_a_calculated,
            volume_b_needed=volume_b_needed,
            mass_b_solute_calc=mass_b_solute_needed,
            m_a_input=m_a_input, # 선행연구에서 입력받은 M_A 값
            g_a_input=g_a,
            p_a_input=p_a,
            mw_a_input=mw_a,
            m_b_input=m_b,
            mw_b_input=mw_b
        )

    except ValueError as ve:
        print(f"\n입력 오류: {ve}")
    except ZeroDivisionError:
        print("\n계산 오류: 0으로 나누는 연산이 발생했습니다. 입력값을 확인해주세요.")
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}")

if __name__ == '__main__':
    main()

# --- 계산 함수 ---
def calculate_moles_from_previous_study(g_a, mw_a, p_a):
    """Calculates the moles of solute used in the previous study."""
    actual_mass_a = g_a * (p_a / 100.0)
    moles_a = actual_mass_a / mw_a
    return moles_a

def calculate_required_volume_of_my_reagent(moles_a, m_b):
    """
    Calculates the required volume of the user's reagent solution (M_B)
    to get the equivalent moles of solute (moles_a).
    """
    if m_b == 0: # Should be caught by input validation, but as a safeguard
        raise ValueError("보유 시약의 몰 농도(M_B)는 0이 될 수 없습니다.")
    volume_b = moles_a / m_b
    return volume_b

def calculate_mass_of_solute_in_my_reagent_volume(moles_a, mw_b):
    """
    Calculates the mass of the solute in the determined volume of the user's reagent.
    This is essentially moles_a * mw_b.
    """
    mass_b_solute = moles_a * mw_b
    return mass_b_solute

# --- 결과 표시 함수 ---
def display_results(moles_a_calc, volume_b_needed, mass_b_solute_calc,
                    m_a_input, g_a_input, p_a_input, mw_a_input,
                    m_b_input, mw_b_input):
    """Displays the calculation results to the user."""
    print("\n--- 계산 결과 ---")
    print(f"선행 연구 정보:")
    print(f"  - 사용된 시약의 명시된 질량 (g_A): {g_a_input} g")
    print(f"  - 시약의 분자량 (MW_A): {mw_a_input} g/mol")
    print(f"  - 시약의 순도 (P_A): {p_a_input}%")
    # M_A는 직접 사용되진 않았지만, 참고용으로 보여줄 수 있음.
    # print(f"  - (참고) 선행 연구 시약 용액의 몰 농도 (M_A): {m_a_input} M")
    print(f"  => 계산된 순수 용질의 몰 수 (mol_A): {moles_a_calc:.6f} mol")

    print(f"\n보유 시약 정보:")
    print(f"  - 보유 시약 용액의 몰 농도 (M_B): {m_b_input} M")
    print(f"  - 보유 시약의 분자량 (MW_B): {mw_b_input} g/mol")

    print(f"\n계산된 필요량:")
    print(f"선행 연구와 동일한 {moles_a_calc:.6f} mol의 용질을 얻기 위해서는,")
    print(f"귀하가 보유한 {m_b_input} M 농도의 시약 용액을 【{volume_b_needed:.6f} L】 만큼 사용해야 합니다.")
    print(f"이 부피({volume_b_needed:.6f} L)의 용액에는 해당하는 용질이 【{mass_b_solute_calc:.4f} g】 포함되어 있습니다.")

    if mw_a_input != mw_b_input:
        print("\n주의: 선행 연구 시약과 보유 시약의 분자량이 다릅니다.")
        print("계산은 입력된 각 분자량을 기준으로 수행되었습니다.")

    print("\n참고: 이 계산은 사용자가 입력한 '보유 시약 용액의 몰 농도(M_B)'가")
    print("정확하며, 바로 사용할 수 있는 상태의 용액 농도임을 가정합니다.")
