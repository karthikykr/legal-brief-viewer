import json
import re

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

df = pd.read_csv("opinions_30.csv")


def extract_case_name(url):
    try:
        slug = re.search(r"/opinion/\d+/(.*?)/", url).group(1)
        words = slug.split("-")
        name = " ".join(words).title()
        name = name.replace(" V ", " Vs ")
        return name
    except:
        return "Unknown Case"


case_names = [extract_case_name(df.iloc[i, 1]) for i in range(len(df))]
idx = st.sidebar.selectbox(
    "Select Case", range(len(df)), format_func=lambda x: case_names[x]
)

row = df.iloc[idx]
original_text = row.iloc[0]
link = row.iloc[1]
brief = json.loads(row.iloc[2])

meta = brief["case_metadata"]
parties = brief["parties"]
keywords = brief["keywords"]
issues = brief["issues_analysis"]
decision = brief["court_decision"]
timeline = brief["case_timeline"]
history = brief["procedural_history"]
background = brief["background"]
citations = brief["citations"]

# ---------- STYLE ----------
st.markdown(
    """
<style>
.chip {
    display:inline-block;
    padding:6px 12px;
    margin:4px 6px 4px 0;
    background:#eef2ff;
    border-radius:20px;
    font-size:12px;
}
.meta-row {
    display:flex;
    gap:80px;
    margin-top:10px;
    font-size:14px;
}
.label {
    color:#6b7280;
    font-size:13px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(f"## ⚖️ {extract_case_name(link)}")
st.markdown(f"**{meta['civil_number']}**")
st.markdown(meta["court"])

c1, c2, c3 = st.columns(3)


def show(col, label, value):
    if value and str(value).lower() != "none":
        with col:
            st.markdown(f"<div class='label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"**{value}**")


show(c1, "Date Filed", meta.get("date_filed"))
show(c2, "Decision Date", meta.get("decision_date"))
show(c3, "Judge", meta.get("judge"))

if meta.get("disposition"):
    st.markdown("**Disposition**")
    st.write(meta["disposition"])

st.divider()

st.markdown("### Keywords")
chips = ""
for k in keywords:
    if k:
        chips += f"<span class='chip'>{k}</span>"
st.markdown(chips, unsafe_allow_html=True)

st.markdown("### Parties")

p1, p2 = st.columns(2)

with p1:
    st.markdown("**Plaintiffs**")
    chips = ""
    for x in parties["plaintiffs"]:
        chips += f"<span class='chip'>{x}</span>"
    st.markdown(chips, unsafe_allow_html=True)

with p2:
    st.markdown("**Defendants**")
    chips = ""
    for x in parties["defendants"]:
        chips += f"<span class='chip'>{x}</span>"
    st.markdown(chips, unsafe_allow_html=True)

tabs = st.tabs(
    [
        "Issues",
        "Decision",
        "Timeline",
        "Procedural History",
        "Background",
        "Citations",
        "Original Opinion",
    ]
)

with tabs[0]:
    for issue in issues:
        st.subheader(f"Issue {issue['issue_number']}")
        st.write("**Question**")
        st.write(issue["question"])
        st.write("**Holding**")
        st.write(issue["holding"])
        st.write("**Ratio**")
        st.write(issue["ratio"])
        st.divider()

with tabs[1]:
    st.write("**Holding**")
    st.write(decision["holding"])
    st.write("**Outcome**")
    st.write(decision["outcome"])
    st.write("**Reasoning**")
    for r in decision["reasoning"]:
        st.write(r)

with tabs[2]:
    for t in timeline:
        st.write(f"**{t['date']}** — {t['event']}")

with tabs[3]:
    for h in history:
        st.write(f"**{h['date']} | {h['court']}**")
        st.write(h["event"])

with tabs[4]:
    st.write(background["summary"])
    st.markdown("**Key Facts**")
    for f in background["key_facts"]:
        st.write("•", f)

with tabs[5]:
    for sec, items in citations.items():
        st.markdown(f"**{sec.replace('_', ' ').title()}**")
        for i in items:
            st.write("•", i)

with tabs[6]:
    st.markdown(f"[Open Source Link]({link})")
    st.text_area("", original_text, height=800)
