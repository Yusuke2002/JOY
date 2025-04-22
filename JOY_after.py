import streamlit as st

def round_up(value, unit):
    return int((value + unit - 1) // unit) * unit

def weighted_split(weights, counts, total_amount, round_unit=100):
    total_weight = sum(w * c for w, c in zip(weights, counts))
    if total_weight == 0:
        return [0] * len(counts)

    base = total_amount / total_weight
    raw_amounts = [round_up(base * w, round_unit) for w in weights]
    return raw_amounts

# UI
st.title("🎓 割り勘アプリ")

total = st.number_input("💰 合計金額（円）", min_value=0, value=0)
n1num = st.number_input("47代の金額", min_value=0, value=0)
n1 = st.number_input("47代の人数", min_value=0, value=0)
n2 = st.number_input("46代の人数", min_value=0, value=0)
n3 = st.number_input("45代の人数", min_value=0, value=0)
n4 = st.number_input("44代の人数", min_value=0, value=0)
m1 = st.number_input("43代の人数", min_value=0, value=0)
m2 = st.number_input("42代の人数", min_value=0, value=0)

if st.button("💸 割り勘する"):
    fixed_total = n1 * n1num
    remaining = total - fixed_total

    if remaining < 0:
        st.error("⚠️ 合計金額が47代の固定金額より小さいです！")
    else:
        # 重みは上の代ほど大きくする（42代が一番重い）
        weights = [1, 2, 3, 4, 5]  # 46〜42代
        weights_2 = [2, 3, 4, 5, 6]
        people = [n2, n3, n4, m1, m2]
        labels = ["46代", "45代", "44代", "43代", "42代"]

        if sum(people) == 0:
            st.warning("⚠️ 47代以外に1人以上入れてください！")
        else:
            # 割り勘計算
            amounts = weighted_split(weights, people, remaining)
            amounts_2 = weighted_split(weights_2, people, remaining)
            st.subheader("🧮 割り勘結果")
            st.write(f"47代：1人あたり **{n1num} 円（固定）**")

            for label, amt, count in zip(labels, amounts, people):
                if count > 0:
                    st.write(f"{label}：1人あたり **{amt} 円**")

            total_collected = fixed_total + sum(a * c for a, c in zip(amounts, people))
            st.markdown("---")
            st.write("Aパターン")
            st.write(f"💰 実際の合計金額：**{total_collected} 円**")
            st.write(f"🧾 差額：**{total_collected - total} 円**")

            for label, amt, count in zip(labels, amounts_2, people):
                if count > 0:
                    st.write(f"{label}：1人あたり **{amt} 円**")

            total_collected = fixed_total + sum(a * c for a, c in zip(amounts_2, people))
            st.markdown("---")
            st.write("Bパターン")
            st.write(f"💰 実際の合計金額：**{total_collected} 円**")
            st.write(f"🧾 差額：**{total_collected - total} 円**")
