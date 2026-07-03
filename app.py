"""Streamlit Web UI for the Chain-of-Thought Reasoning Engine.

Provides a web interface for asking questions and viewing
the structured reasoning chain results.
"""

import asyncio
import logging
from typing import Optional

import streamlit as st

from src.llm_adapter import LLMAdapter
from src.orchestrator import Orchestrator
from src.framework_selector import list_frameworks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="My Thinker Buddy - Chain-of-Thought Engine",
    page_icon="🤔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .step-container {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E3A5F;
    }
    .step-header {
        color: #1E3A5F;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .step-description {
        color: #666;
        font-style: italic;
        margin-bottom: 1rem;
    }
    .step-content {
        line-height: 1.6;
    }
    .framework-badge {
        background-color: #1E3A5F;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #1E3A5F;
        color: white;
        font-weight: 600;
    }
    .info-box {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "base_url" not in st.session_state:
        st.session_state.base_url = "https://api.sumopod.com/v1"
    if "model" not in st.session_state:
        st.session_state.model = "gpt-4o-mini"
    if "result" not in st.session_state:
        st.session_state.result = None
    if "running" not in st.session_state:
        st.session_state.running = False


def render_header():
    """Render the main header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            '<div class="main-header">🤔 My Thinker Buddy</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sub-header">'
            "Chain-of-Thought Reasoning Engine - Multi-framework analysis"
            "</div>",
            unsafe_allow_html=True,
        )
    with col2:
        frameworks = list_frameworks()
        st.markdown(f"**Available Frameworks:** {len(frameworks)}")
        for fw in frameworks:
            st.markdown(f"- `{fw['key']}`: {fw['name']}")


def render_sidebar():
    """Render the sidebar configuration."""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        st.session_state.api_key = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.api_key,
            help="Your sumopod (OpenAI-compatible) API key",
        )

        st.session_state.base_url = st.text_input(
            "Base URL",
            value=st.session_state.base_url,
            help="API endpoint URL",
        )

        st.session_state.model = st.text_input(
            "Model",
            value=st.session_state.model,
            help="Model name (e.g., gpt-4o-mini, gpt-4o)",
        )

        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown(
            "- Leave framework empty for auto-detect\n"
            "- Or specify a framework key to override\n"
            "- Results show all reasoning steps"
        )

        st.markdown("---")
        st.markdown("### 📋 Frameworks")
        frameworks = list_frameworks()
        for fw in frameworks:
            with st.expander(fw["name"]):
                st.markdown(fw["description"])


async def run_analysis(
    question: str,
    framework_override: Optional[str],
    api_key: str,
    base_url: str,
    model: str,
) -> dict:
    """Run the analysis asynchronously."""
    llm = LLMAdapter(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )
    orchestrator = Orchestrator(llm_adapter=llm)

    preferred = framework_override if framework_override else None
    result = await orchestrator.analyze(
        question=question,
        preferred_framework=preferred,
        verbose=True,
    )
    return result


def render_result(result):
    """Render the analysis result."""
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    st.markdown(
        f'<div class="framework-badge">'
        f"Framework: {result.framework_name}"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"**Question:** {result.question}")
    st.markdown(f"**Description:** _{result.framework_description}_")
    st.markdown(f"**Steps Completed:** {len(result.steps)} / {result.total_steps}")
    st.markdown("")

    # Progress bar
    progress = len(result.steps) / max(result.total_steps, 1)
    st.progress(progress)
    st.markdown("")

    # Display each step
    for i, step in enumerate(result.steps):
        with st.container():
            st.markdown(
                f'<div class="step-container">',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="step-header">'
                f"Step {step.step_index + 1}: {step.step_name}"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="step-description">{step.step_description}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="step-content">{step.output}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # Summary
    st.markdown("---")
    st.markdown("### 📝 Summary")
    st.markdown(
        f"Completed **{len(result.steps)}** of **{result.total_steps}** "
        f"steps using the **{result.framework_name}** framework "
        f"to analyze: _{result.question}_"
    )

    # Download options
    st.markdown("### 💾 Export")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Download as Markdown",
            data=result.to_markdown(),
            file_name=f"analysis_{result.framework_key}.md",
            mime="text/markdown",
        )
    with col2:
        st.download_button(
            label="📋 Download as JSON",
            data=result.to_json(),
            file_name=f"analysis_{result.framework_key}.json",
            mime="application/json",
        )


def main():
    """Main application entry point."""
    init_session_state()
    render_sidebar()
    render_header()

    # Main input area
    st.markdown("---")
    st.markdown("## 🔍 Ask a Question")
    st.markdown(
        "Enter a question or problem to analyze using the best-fit framework."
    )

    question = st.text_area(
        "Your question:",
        placeholder=(
            "e.g., 'Why are customers churning in our SaaS product?' "
            "or 'What caused the production line shutdown?'"
        ),
        height=100,
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        framework_override = st.text_input(
            "Framework override (optional):",
            placeholder="Leave empty for auto-detect, or enter: fishbone, dmaic, etc.",
            help="Override the auto-detected framework",
        )
    with col2:
        run_button = st.button(
            "🚀 Analyze",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.running,
        )

    # Handle analysis
    if run_button and question:
        if not st.session_state.api_key:
            st.error(
                "Please enter your API key in the sidebar configuration."
            )
            return

        st.session_state.running = True
        with st.spinner("🧠 Running chain-of-thought analysis..."):
            try:
                result = asyncio.run(
                    run_analysis(
                        question=question,
                        framework_override=framework_override.strip()
                        if framework_override.strip()
                        else None,
                        api_key=st.session_state.api_key,
                        base_url=st.session_state.base_url,
                        model=st.session_state.model,
                    )
                )
                st.session_state.result = result
                st.success("✅ Analysis complete!")

            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                logger.exception("Analysis error")
            finally:
                st.session_state.running = False

    # Display previous results
    if st.session_state.result and not run_button:
        render_result(st.session_state.result)

    # Re-run detection
    if st.session_state.result and run_button:
        render_result(st.session_state.result)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        "My Thinker Buddy v1.0 | Powered by sumopod API"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()