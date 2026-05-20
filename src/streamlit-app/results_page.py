import streamlit as st
import os, sys
_here = os.path.dirname(os.path.abspath(__file__))   # .../src/streamlit-app
_src  = os.path.abspath(os.path.join(_here, ".."))   # .../src
sys.path.insert(0, _src)
from models import LLMCandidateResponse

# ── Theme constants (mirrors config.toml) ────────────────────────────────────
TEXT        = "#1B2A4A"
TEXT_MUTED  = "#4A5E7A"   # lighter navy for secondary labels
PRIMARY     = "#1B2A4A"

# ── Semantic palette (status colours only) ───────────────────────────────────
GREEN_FG, GREEN_BG = "#1a7f4b", "#d4edda"
AMBER_FG, AMBER_BG = "#7a5200", "#fff3cd"
RED_FG,   RED_BG   = "#a32d2d", "#fde8e8"
BLUE_FG,  BLUE_BG  = "#0c5fa5", "#d0e8fb"

VERDICT_STYLES = {
    "Fast-Track": ("🟢", GREEN_FG, GREEN_BG),
    "Standard":   ("🔵", BLUE_FG,  BLUE_BG),
    "Borderline": ("🟡", AMBER_FG, AMBER_BG),
    "Reject":     ("🔴", RED_FG,   RED_BG),
}

HIRE_STYLES = {
    "Strong Hire":      (GREEN_FG, GREEN_BG),
    "Hire":             (GREEN_FG, GREEN_BG),
    "Conditional Hire": (AMBER_FG, AMBER_BG),
    "No Hire":          (RED_FG,   RED_BG),
}

SKILL_STYLES = {
    "Matched": ("✅", GREEN_FG, GREEN_BG),
    "Partial": ("⚠️",  AMBER_FG, AMBER_BG),
    "Missing": ("❌", RED_FG,   RED_BG),
}

TREND_ICON = {
    "Ascending": "📈",
    "Stable":    "➡️",
    "Declining": "📉",
    "Pivoting":  "🔄",
}

SENIORITY_CONF_COLOR = {
    "High":   (GREEN_FG, GREEN_BG),
    "Medium": (AMBER_FG, AMBER_BG),
    "Low":    (RED_FG,   RED_BG),
}

SIGNAL_COLORS = {
    "Strong":  (GREEN_FG, GREEN_BG),
    "Average": (AMBER_FG, AMBER_BG),
    "Weak":    (RED_FG,   RED_BG),
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _badge(label: str, color: str, bg: str) -> str:
    return (
        f'<span style="background:{bg};color:{color};padding:4px 14px;'
        f'border-radius:99px;font-size:16px;font-weight:700;">{label}</span>'
    )

def _section(title: str):
    st.markdown(f"### {title}")
    st.markdown("---")

def _pill_list(items: list[str], color: str, bg: str):
    pills = " ".join(
        f'<span style="background:{bg};color:{color};padding:3px 12px;'
        f'border-radius:99px;font-size:16px;margin:3px;display:inline-block;">{i}</span>'
        for i in items if i
    )
    st.markdown(pills, unsafe_allow_html=True)

def _kv(key: str, value: str):
    c1, c2 = st.columns([1, 1])
    c1.markdown(
        f"<span style='color:{TEXT_MUTED};font-size:17px;'>{key}</span>",
        unsafe_allow_html=True
    )
    c2.markdown(
        f"<span style='color:{TEXT};font-size:17px;font-weight:600;'>{value}</span>",
        unsafe_allow_html=True
    )


# ── Main render ───────────────────────────────────────────────────────────────

def render_results_page():
    raw = st.session_state.analysis_response
    u   = st.session_state.user_entries

    if raw is None:
        st.error("No analysis result found. Please go back and run the analysis.")
        if st.button("← Back"):
            st.session_state.page = 'main'
            st.rerun()
        return

    # ── Sanitize raw dict before Pydantic validation ─────────────────────────
    # The LLM occasionally returns malformed fields; coerce them to safe defaults
    # so validation never crashes the results page.
    if isinstance(raw, dict):
        # Fix breakdown items that came back as plain strings instead of dicts
        sc = raw.get("stack_compatibility", {})
        if isinstance(sc, dict):
            sc["breakdown"] = [
                item if isinstance(item, dict)
                else {"required_skill": str(item), "candidate_status": "Missing", "evidence": None}
                for item in sc.get("breakdown", [])
            ]
            raw["stack_compatibility"] = sc

        # Fix career_trajectory fields that came back as None when int is required
        ct = raw.get("career_trajectory", {})
        if isinstance(ct, dict):
            if ct.get("industry_match_score") is None:
                ct["industry_match_score"] = 0
            raw["career_trajectory"] = ct

        r: LLMCandidateResponse = LLMCandidateResponse(**raw)
    else:
        r: LLMCandidateResponse = raw

    # ── Back button ───────────────────────────────────────────────────────────
    if st.button("← Back to Analysis"):
        st.session_state.page = 'main'
        st.session_state.analysis_response = None
        st.session_state.user_entries = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    icon, v_color, v_bg = VERDICT_STYLES.get(r.screening_verdict, ("⚪", TEXT_MUTED, "#eee"))
    candidate_name = r.candidate_overview.name or "Candidate"

    col_name, col_verdict = st.columns([3, 1])
    with col_name:
        st.markdown(
            f"<h1 style='color:{TEXT};margin-bottom:6px;'>{candidate_name}</h1>"
            f"<p style='color:{TEXT_MUTED};font-size:18px;margin-top:0;'>{r.one_line_summary}</p>",
            unsafe_allow_html=True
        )
    with col_verdict:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:right;">{_badge(f"{icon}  {r.screening_verdict}", v_color, v_bg)}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Overview + Seniority & Communication ───────────────────────────
    col_ov, col_sen = st.columns(2)

    with col_ov:
        _section("👤 Candidate Overview")
        ov = r.candidate_overview
        info = {
            "Current Title":      ov.current_title or "—",
            "Experience":         f"{ov.total_years_experience} yrs" if ov.total_years_experience else "—",
            "Education":          ov.education or "—",
            "Location":           ov.location or "—",
            "CV Language":        ov.cv_language,
            "Open to Relocation": ov.open_to_relocation,
            "Work Preference":    ov.work_preference,
        }
        for k, v in info.items():
            _kv(k, v)

    with col_sen:
        _section("🎯 Seniority Assessment")
        sa = r.seniority_assessment
        cf_color, cf_bg = SENIORITY_CONF_COLOR.get(sa.confidence, (TEXT_MUTED, "#eee"))
        st.markdown(
            f"<span style='color:{TEXT};font-size:18px;font-weight:600;'>Level: {sa.level}</span>"
            f"&nbsp;&nbsp;{_badge(sa.confidence + ' confidence', cf_color, cf_bg)}",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(sa.justification)

        st.markdown("<br>", unsafe_allow_html=True)
        _section("💬 Communication Signal")
        cs = r.communication_signal
        sc, sb = SIGNAL_COLORS.get(cs.communication_signal, (TEXT_MUTED, "#eee"))
        st.markdown(
            f"{_badge(cs.communication_signal, sc, sb)}"
            f"&nbsp;&nbsp;<span style='color:{TEXT};font-size:17px;'>"
            f"CV Quality Score: <b>{cs.cv_quality_score}/100</b></span>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stack Compatibility ───────────────────────────────────────────────────
    _section("🛠️ Stack Compatibility")

    score = r.stack_compatibility.overall_compatibility_score
    score_color = GREEN_FG if score >= 70 else AMBER_FG if score >= 40 else RED_FG
    st.markdown(
        f"<span style='color:{TEXT};font-size:18px;'>Overall Compatibility Score: "
        f"<span style='font-size:26px;font-weight:700;color:{score_color};'>{score}/100</span></span>",
        unsafe_allow_html=True
    )
    st.progress(score / 100)
    st.markdown("<br>", unsafe_allow_html=True)

    for item in r.stack_compatibility.breakdown:
        icon_s, col_s, bg_s = SKILL_STYLES.get(item.candidate_status, ("•", TEXT_MUTED, "#eee"))
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 3])
            c1.markdown(
                f"<span style='color:{TEXT};font-size:17px;font-weight:600;'>{item.required_skill}</span>",
                unsafe_allow_html=True
            )
            c2.markdown(f"{_badge(f'{icon_s} {item.candidate_status}', col_s, bg_s)}", unsafe_allow_html=True)
            c3.markdown(
                f"<span style='color:{TEXT_MUTED};font-size:16px;'>{item.evidence or '—'}</span>",
                unsafe_allow_html=True
            )
        st.markdown(f"<hr style='margin:6px 0;border-color:#c8cdd6;'>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Career Trajectory + Compensation ───────────────────────────────
    col_ct, col_comp = st.columns(2)

    with col_ct:
        _section("📊 Career Trajectory")
        ct = r.career_trajectory
        trend_icon = TREND_ICON.get(ct.trend, "")
        avg = f"{round(ct.avg_tenure_months)} months/role" if ct.avg_tenure_months else "—"
        st.markdown(f"<span style='color:{TEXT};font-size:17px;'>**Trend:** {trend_icon} {ct.trend}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:{TEXT};font-size:17px;'>**Avg Tenure:** {avg}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:{TEXT};font-size:17px;'>**Job Hopper:** {'⚠️ Yes' if ct.job_hopper_flag else '✅ No'}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:{TEXT};font-size:17px;'>**Industry Match Score:** {ct.industry_match_score}/100</span>", unsafe_allow_html=True)
        if ct.industries_worked_in:
            st.markdown(f"<span style='color:{TEXT};font-size:17px;'>**Industries:**</span>", unsafe_allow_html=True)
            _pill_list(ct.industries_worked_in, BLUE_FG, BLUE_BG)

    with col_comp:
        _section("💰 Compensation Signal")
        comp = r.compensation_signal
        if comp.estimated_min or comp.estimated_max:
            lo = f"{comp.estimated_min:,.0f}" if comp.estimated_min else "?"
            hi = f"{comp.estimated_max:,.0f}" if comp.estimated_max else "?"
            st.markdown(
                f"<span style='color:{TEXT};font-size:17px;'>Estimated Range:<br>"
                f"<span style='font-size:22px;font-weight:700;color:{TEXT};'>{comp.currency} {lo} – {hi}</span></span>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<span style='color:{TEXT_MUTED};font-size:17px;'><i>Compensation data not available from CV.</i></span>",
                unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        if comp.likely_above_budget:
            st.warning("⚠️ Candidate is likely above budget.")
        else:
            st.success("✅ Candidate appears within budget range.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full Evaluation ───────────────────────────────────────────────────────
    _section("📋 Full Evaluation")
    ev = r.full_evaluation

    col_s, col_g = st.columns(2)
    with col_s:
        st.markdown(f"<span style='color:{TEXT};font-size:18px;font-weight:700;'>✅ Strengths</span>", unsafe_allow_html=True)
        for s in ev.strengths:
            st.markdown(f"- {s}")
    with col_g:
        st.markdown(f"<span style='color:{TEXT};font-size:18px;font-weight:700;'>⚠️ Gaps</span>", unsafe_allow_html=True)
        for g in ev.gaps:
            st.markdown(f"- {g}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_rf, col_na = st.columns(2)
    with col_rf:
        st.markdown(f"<span style='color:{TEXT};font-size:18px;font-weight:700;'>🚩 Red Flags</span>", unsafe_allow_html=True)
        if ev.red_flags:
            for rf in ev.red_flags:
                st.markdown(f"- {rf}")
        else:
            st.markdown("*None identified.*")
    with col_na:
        st.markdown(f"<span style='color:{TEXT};font-size:18px;font-weight:700;'>🏆 Notable Achievements</span>", unsafe_allow_html=True)
        if ev.notable_achievements:
            for na in ev.notable_achievements:
                st.markdown(f"- {na}")
        else:
            st.markdown("*None noted.*")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<span style='color:{TEXT};font-size:17px;'>🤝 <b>Cultural Fit Indicators:</b> {ev.cultural_fit_indicators}</span>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Hiring recommendation banner ──────────────────────────────────────────
    hr_color, hr_bg = HIRE_STYLES.get(ev.hiring_recommendation, (TEXT_MUTED, "#eee"))
    st.markdown(
        f'<div style="background:{hr_bg};border-left:6px solid {hr_color};'
        f'padding:20px 24px;border-radius:10px;margin-bottom:16px;">'
        f'<p style="margin:0 0 6px;font-size:14px;color:{TEXT_MUTED};font-weight:700;'
        f'text-transform:uppercase;letter-spacing:.07em;">Hiring Recommendation</p>'
        f'<p style="margin:0 0 10px;font-size:24px;font-weight:700;color:{hr_color};">{ev.hiring_recommendation}</p>'
        f'<p style="margin:0;font-size:17px;color:{TEXT};line-height:1.6;">{ev.recommendation_rationale}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f"<span style='color:{TEXT};font-size:18px;'>Final Fit Score: "
        f"<span style='font-size:28px;font-weight:700;color:{hr_color};'>{ev.final_fit_score}/100</span></span>",
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Recruiter Decision ────────────────────────────────────────────────────
    _section("📌 Recruiter Decision")

    col_a, col_s2, col_r = st.columns(3)
    with col_a:
        if st.button("✅  Approve", use_container_width=True, type="primary"):
            st.session_state['recruiter_decision'] = 'Approved'
    with col_s2:
        if st.button("⭐  Shortlist", use_container_width=True):
            st.session_state['recruiter_decision'] = 'Shortlisted'
    with col_r:
        if st.button("❌  Reject", use_container_width=True):
            st.session_state['recruiter_decision'] = 'Rejected'

    decision = st.session_state.get('recruiter_decision')
    if decision:
        decision_styles = {
            'Approved':    (GREEN_FG, GREEN_BG, "✅"),
            'Shortlisted': (BLUE_FG,  BLUE_BG,  "⭐"),
            'Rejected':    (RED_FG,   RED_BG,   "❌"),
        }
        dc, db, di = decision_styles[decision]
        st.markdown(
            f'<div style="background:{db};border-left:6px solid {dc};padding:16px 24px;'
            f'border-radius:10px;margin-top:14px;">'
            f'<span style="color:{dc};font-weight:700;font-size:18px;">'
            f'{di} {candidate_name} has been marked as <u>{decision}</u>.</span>'
            f'</div>',
            unsafe_allow_html=True
        )