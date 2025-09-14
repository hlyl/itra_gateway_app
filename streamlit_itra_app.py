# ITRA Gateway Questions - Streamlit App (Minimal Dependencies)
# Run with: uv run --with streamlit streamlit run itra_gateway_app.py

import streamlit as st
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="IT Risk Assessment - Gateway Questions",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@dataclass
class AssessmentPath:
    name: str
    enabled: bool
    question_count: int
    description: str


class ITRAGatewayApp:
    def __init__(self):
        self.phase_1_complete = False
        self.phase_2_complete = False
        self.phase_3_complete = False

    def main(self):
        # Header
        st.title("🛡️ IT Risk Assessment - Smart Gateway")
        st.markdown(
            "**Business-Friendly Risk Assessment** | Answer 8 key questions to determin your assessment scope"
        )

        # Progress tracking
        self.show_progress()

        # Initialize session state
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        if "assessment_start_time" not in st.session_state:
            st.session_state.assessment_start_time = datetime.now()

        # Main assessment flow
        col1, col2 = st.columns([2, 1])

        with col1:
            self.render_assessment_phases()

        with col2:
            self.render_sidebar_summary()

    def show_progress(self):
        phases_complete = 0
        answers = st.session_state.get("answers", {})

        # Phase 1 complete
        if answers.get("asset_type"):
            phases_complete += 1

        # Phase 2 complete
        phase_2_questions = ["B.2", "T.6", "B.3"]
        if all(q in answers for q in phase_2_questions):
            phases_complete += 1

        # Phase 3 complete
        phase_3_questions = ["S.1", "B.13", "D.1", "D.2"]
        if all(q in answers for q in phase_3_questions):
            phases_complete += 1

        progress = phases_complete / 3
        st.progress(progress)
        st.markdown(
            f"**Progress:** Phase {phases_complete + 1 if phases_complete < 3 else 3} of 3 | {int(progress * 100)}% Complete"
        )

    def render_assessment_phases(self):
        """Render the main assessment phases"""

        # Phase 1: Classification
        with st.container():
            st.header("📍 Phase 1: What Are We Assessing?")
            self.render_phase_1()

        # Phase 2: Major Risk Categories (only if Phase 1 complete)
        if st.session_state.get("answers", {}).get("asset_type"):
            st.divider()
            with st.container():
                st.header("🛡️ Phase 2: Major Risk Categories")
                self.render_phase_2()

            # Phase 3: Context & Scope (only if Phase 2 complete)
            phase_2_questions = ["B.2", "T.6", "B.3"]
            if all(q in st.session_state.get("answers", {}) for q in phase_2_questions):
                st.divider()
                with st.container():
                    st.header("📋 Phase 3: Context & Scope")
                    self.render_phase_3()

    def render_phase_1(self):
        """Phase 1: Asset Type Classification"""
        st.subheader("What type of technology solution are you assessing?")

        # Help text
        with st.expander("ℹ️ Help me understand the options"):
            st.markdown("""
            **Think about what you're primarily evaluating:**
            - **📱 Equipment/Device**: Physical things you can touch (computers, tablets, medical devices)
            - **🌐 IT Infrastructure**: Behind-the-scenes technology (servers, networks, cloud platforms)
            - **💻 Software Application**: Programs people log into and use for work
            - **🏥 Medical Software**: Anything used in healthcare or for patients
            """)

        asset_type = st.radio(
            "Select the type:",
            options=[
                "📱 Equipment/Device",
                "🌐 IT Infrastructure",
                "💻 Software Application",
                "🏥 Medical Software",
            ],
            key="asset_type_display",
            horizontal=True,
        )

        if asset_type:
            # Map display value to internal value
            asset_mapping = {
                "📱 Equipment/Device": "computerised_equipment",
                "🌐 IT Infrastructure": "it_infrastructure",
                "💻 Software Application": "it_system",
                "🏥 Medical Software": "health_software",
            }
            st.session_state.answers["asset_type"] = asset_mapping[asset_type]

            st.success(f"✅ Selected: {asset_type}")

    def render_phase_2(self):
        """Phase 2: Major Risk Categories"""

        # Question B.2: Regulatory Compliance
        st.subheader(
            "Does this solution handle regulated pharmaceutical data or processes?"
        )

        with st.expander("ℹ️ What does 'regulated pharmaceutical' mean?"):
            st.markdown("""
            **GxP refers to pharmaceutical regulations (like FDA requirements).**
            
            **Choose YES if this involves:**
            - Drug development, testing, or manufacturing
            - Clinical trials or patient studies  
            - Quality control or compliance reporting
            - Regulatory submissions or documentation
            
            **Choose NO if this is for:**
            - General business (HR, finance, marketing, general IT)
            - Non-pharmaceutical operations
            
            **When in doubt for pharma companies: Choose YES**
            """)

        b2_answer = st.radio(
            "Regulatory compliance:",
            options=[
                "✅ Yes - Handles regulated pharmaceutical activities",
                "❌ No - General business use only",
            ],
            key="B.2_display",
        )

        if b2_answer:
            st.session_state.answers["B.2"] = "Yes" if "Yes" in b2_answer else "No"

        # Question T.6: AI Technology
        st.subheader(
            "Does this solution use artificial intelligence, machine learning, or smart automation?"
        )

        with st.expander("ℹ️ How do I know if it uses AI?"):
            st.markdown("""
            **Choose YES if it:**
            - Makes decisions or recommendations automatically
            - Learns patterns from data
            - Predicts outcomes or trends
            - Adapts its behavior over time
            - Uses chatbots or voice recognition
            
            **Examples:** Recommendation engines, predictive analytics, automated decision systems, image recognition
            
            **Choose NO if it:**
            - Just follows fixed rules or workflows
            - Only stores and displays data
            - Requires human decisions for everything
            """)

        t6_answer = st.radio(
            "AI Technology:",
            options=[
                "🤖 Yes - Uses AI, machine learning, or smart automation",
                "📊 No - Follows fixed rules, no intelligent decisions",
            ],
            key="T.6_display",
        )

        if t6_answer:
            st.session_state.answers["T.6"] = "Yes" if "Yes" in t6_answer else "No"

        # Question B.3: Patient Safety
        st.subheader(
            "Could this solution directly or indirectly affect patient health or safety?"
        )

        with st.expander("ℹ️ How could it affect patient safety?"):
            st.markdown("""
            **Consider the chain of impact - even indirect effects count:**
            
            **Choose YES if:**
            - Used in hospitals, clinics, or medical facilities
            - Handles patient data or medical records
            - Affects medical decisions or treatment
            - Manages medical supplies or equipment
            - Could impact patient care if it failed
            
            **Examples:** Lab systems, patient scheduling, medical device control, pharmacy systems
            
            **When in doubt for healthcare environments: Choose YES**
            """)

        b3_answer = st.radio(
            "Patient Safety:",
            options=[
                "🏥 Yes - Could affect patient health or safety",
                "🏢 No - No patient impact",
            ],
            key="B.3_display",
        )

        if b3_answer:
            st.session_state.answers["B.3"] = "Yes" if "Yes" in b3_answer else "No"

    def render_phase_3(self):
        """Phase 3: Context & Scope"""

        # Question S.1: Network Connectivity
        st.subheader("How is this solution connected to networks?")

        with st.expander("ℹ️ Understanding network connectivity"):
            st.markdown("""
            **Think about how people access this system:**
            - Can employees use it from home?
            - Does it connect to the internet?
            - Can external partners access it?
            - Is it completely isolated?
            """)

        s1_answer = st.radio(
            "Network Access:",
            options=[
                "🔌 Not Connected - Standalone system",
                "🏢 Internal Only - Company network only",
                "🌐 Multiple Networks - Company + external access",
                "☁️ Cloud-Based - Internet/cloud hosted",
            ],
            key="S.1_display",
        )

        if s1_answer:
            s1_mapping = {
                "🔌 Not Connected - Standalone system": "Not Connected",
                "🏢 Internal Only - Company network only": "1",
                "🌐 Multiple Networks - Company + external access": "2",
                "☁️ Cloud-Based - Internet/cloud hosted": "2",
            }
            st.session_state.answers["S.1"] = s1_mapping[s1_answer]

        # Question B.13: Business Impact
        st.subheader(
            "If this solution was completely unavailable, what would be the business impact?"
        )

        with st.expander("ℹ️ Assessing business impact"):
            st.markdown("""
            **Consider these questions:**
            - Would customers be affected?
            - Would we miss regulatory deadlines?  
            - Would revenue be lost?
            - Would safety be compromised?
            - Could we use alternatives or manual processes?
            """)

        b13_answer = st.radio(
            "Business Impact:",
            options=[
                "🟢 Low - Minor inconvenience, work continues",
                "🟡 Medium - Significant delays, but business continues",
                "🔴 High - Major disruption, customer/safety/regulatory impact",
            ],
            key="B.13_display",
        )

        if b13_answer:
            b13_mapping = {
                "🟢 Low - Minor inconvenience, work continues": "Low",
                "🟡 Medium - Significant delays, but business continues": "Medium",
                "🔴 High - Major disruption, customer/safety/regulatory impact": "High",
            }
            st.session_state.answers["B.13"] = b13_mapping[b13_answer]

        # Question D.1: Data Input
        st.subheader("Do people enter important regulated data into this solution?")

        with st.expander("ℹ️ What counts as regulated data entry?"):
            st.markdown("""
            **Examples of regulated data entry:**
            - Lab results and test data
            - Clinical trial information
            - Manufacturing records
            - Quality control measurements
            - Batch records and lot numbers
            
            **Choose NO if:**
            - Data comes from other systems automatically
            - People only enter general business data
            - It's not pharmaceutical/medical data
            """)

        d1_answer = st.radio(
            "Data Entry:",
            options=[
                "📝 Yes - People manually enter regulated data",
                "🤖 No - Automatic data or not regulated data",
            ],
            key="D.1_display",
        )

        if d1_answer:
            st.session_state.answers["D.1"] = "Yes" if "Yes" in d1_answer else "No"

        # Question D.2: Data Processing
        st.subheader(
            "Does this solution automatically calculate, transform, or analyze regulated data?"
        )

        with st.expander("ℹ️ What is automatic data processing?"):
            st.markdown("""
            **Examples of automatic processing:**
            - Calculating drug dosages or concentrations
            - Generating compliance reports
            - Statistical analysis of test results  
            - Converting data between formats
            - Performing quality calculations
            
            **Choose NO if it:**
            - Just stores or displays data
            - Requires humans to do all calculations
            - Only handles non-regulated data
            """)

        d2_answer = st.radio(
            "Data Processing:",
            options=[
                "⚙️ Yes - Automatically processes regulated data",
                "📂 No - Just stores/displays data",
            ],
            key="D.2_display",
        )

        if d2_answer:
            st.session_state.answers["D.2"] = "Yes" if "Yes" in d2_answer else "No"

    def render_sidebar_summary(self):
        """Render the sidebar with assessment summary"""
        st.subheader("📊 Assessment Summary")

        answers = st.session_state.get("answers", {})

        if not answers:
            st.info("👆 Start by selecting your asset type")
            return

        # Show current answers
        st.markdown("**Your Answers:**")
        for key, value in answers.items():
            display_value = self.format_answer_for_display(key, value)
            st.markdown(f"• **{self.get_question_label(key)}**: {display_value}")

        # Calculate enabled paths
        if len(answers) >= 4:  # At least through Phase 2
            st.divider()
            st.subheader("🎯 Assessment Scope")

            enabled_paths = self.calculate_assessment_paths(answers)
            total_questions = sum(
                path.question_count for path in enabled_paths if path.enabled
            )

            # Create metrics using simple layout
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Questions", f"{total_questions}")
            with col2:
                enabled_count = sum(1 for path in enabled_paths if path.enabled)
                st.metric("Assessment Areas", f"{enabled_count}")

            # Estimate time
            min_time = int(total_questions * 0.5)
            max_time = int(total_questions * 1.0)
            st.metric("Estimated Time", f"{min_time}-{max_time} min")

            st.markdown("**Enabled Assessment Areas:**")
            for path in enabled_paths:
                if path.enabled:
                    st.success(f"✅ {path.name} ({path.question_count} questions)")
                else:
                    st.info(f"⏭️ {path.name} (skipped)")

        # Show next steps
        if len(answers) == 8:  # All gateway questions answered
            st.divider()
            st.success("🎉 Gateway Assessment Complete!")

            if st.button("📋 Generate Full Assessment", type="primary"):
                self.show_full_assessment_preview()

        # Quick reference
        st.divider()
        with st.expander("🤔 Quick Reference"):
            st.markdown("""
            **When in Doubt:**
            - **Regulation**: If pharma-related → Yes
            - **Patient Safety**: If any patient connection → Yes  
            - **AI**: If it does anything "smart" → Yes
            - **Impact**: If you'd panic if it failed → High
            - **Connectivity**: If remote access → Multiple Networks
            """)

    def format_answer_for_display(self, key: str, value: str) -> str:
        """Format answers for display"""
        display_mapping = {
            "asset_type": {
                "computerised_equipment": "📱 Equipment/Device",
                "it_infrastructure": "🌐 IT Infrastructure",
                "it_system": "💻 Software Application",
                "health_software": "🏥 Medical Software",
            },
            "B.2": {"Yes": "✅ Regulated", "No": "❌ General Business"},
            "T.6": {"Yes": "🤖 Uses AI", "No": "📊 No AI"},
            "B.3": {"Yes": "🏥 Patient Safety", "No": "🏢 No Patient Impact"},
            "S.1": {
                "Not Connected": "🔌 Not Connected",
                "1": "🏢 Internal Only",
                "2": "🌐 Multiple Networks",
            },
            "B.13": {
                "Low": "🟢 Low Impact",
                "Medium": "🟡 Medium Impact",
                "High": "🔴 High Impact",
            },
            "D.1": {"Yes": "📝 Manual Data Entry", "No": "🤖 Automatic Data"},
            "D.2": {"Yes": "⚙️ Processes Data", "No": "📂 Stores Only"},
        }

        return display_mapping.get(key, {}).get(value, value)

    def get_question_label(self, key: str) -> str:
        """Get display label for question"""
        labels = {
            "asset_type": "Asset Type",
            "B.2": "Regulatory Compliance",
            "T.6": "AI Technology",
            "B.3": "Patient Safety",
            "S.1": "Network Access",
            "B.13": "Business Impact",
            "D.1": "Data Entry",
            "D.2": "Data Processing",
        }
        return labels.get(key, key)

    def calculate_assessment_paths(
        self, answers: Dict[str, str]
    ) -> List[AssessmentPath]:
        """Calculate which assessment paths are enabled"""
        paths = []

        # GxP Compliance Path
        gxp_enabled = answers.get("B.2") == "Yes"
        paths.append(
            AssessmentPath(
                name="GxP Compliance Assessment",
                enabled=gxp_enabled,
                question_count=12 if gxp_enabled else 0,
                description="Full pharmaceutical compliance assessment",
            )
        )

        # Alternative Compliance Path
        alt_enabled = answers.get("B.2") == "No"
        paths.append(
            AssessmentPath(
                name="Alternative Compliance (GDP/GLP/GCP)",
                enabled=alt_enabled,
                question_count=3 if alt_enabled else 0,
                description="Non-GxP regulatory pathways",
            )
        )

        # AI Assessment Path
        ai_enabled = answers.get("T.6") == "Yes"
        paths.append(
            AssessmentPath(
                name="AI Risk Assessment",
                enabled=ai_enabled,
                question_count=8 if ai_enabled else 0,
                description="Artificial intelligence specific risks",
            )
        )

        # Patient Safety Path
        patient_enabled = answers.get("B.3") == "Yes"
        paths.append(
            AssessmentPath(
                name="Patient Safety Assessment",
                enabled=patient_enabled,
                question_count=2 if patient_enabled else 0,
                description="Patient health and safety impact",
            )
        )

        # Network Security Path
        network_enabled = answers.get("S.1") not in ["Not Connected", None]
        paths.append(
            AssessmentPath(
                name="Network Security Assessment",
                enabled=network_enabled,
                question_count=4 if network_enabled else 2,
                description="Network connectivity and security risks",
            )
        )

        # Business Criticality Path
        timing_enabled = answers.get("B.13") in ["Medium", "High"]
        paths.append(
            AssessmentPath(
                name="Detailed Timing Analysis",
                enabled=timing_enabled,
                question_count=2 if timing_enabled else 0,
                description="Availability and recovery requirements",
            )
        )

        # Data Integrity Paths
        data_input_enabled = answers.get("D.1") == "Yes"
        data_processing_enabled = answers.get("D.2") == "Yes"
        data_questions = 0
        if data_input_enabled:
            data_questions += 2
        if data_processing_enabled:
            data_questions += 1

        paths.append(
            AssessmentPath(
                name="Data Integrity Controls",
                enabled=data_input_enabled or data_processing_enabled,
                question_count=data_questions,
                description="Data input and processing validation",
            )
        )

        # Base assessments (always enabled)
        asset_type = answers.get("asset_type", "")
        base_counts = {
            "computerised_equipment": 28,
            "it_infrastructure": 22,
            "it_system": 30,
            "health_software": 28,
        }
        base_count = base_counts.get(asset_type, 25)

        paths.append(
            AssessmentPath(
                name="Base Risk Assessment",
                enabled=True,
                question_count=base_count,
                description="Core risk questions for all assets",
            )
        )

        return paths

    def show_full_assessment_preview(self):
        """Show preview of the full assessment"""
        st.subheader("📋 Full Assessment Preview")

        answers = st.session_state.get("answers", {})
        enabled_paths = self.calculate_assessment_paths(answers)

        # Summary metrics
        col1, col2, col3 = st.columns(3)

        total_questions = sum(
            path.question_count for path in enabled_paths if path.enabled
        )
        enabled_count = sum(1 for path in enabled_paths if path.enabled)
        min_time = total_questions * 0.5
        max_time = total_questions * 1.0

        col1.metric("Total Questions", total_questions)
        col2.metric("Assessment Areas", enabled_count)
        col3.metric("Estimated Time", f"{int(min_time)}-{int(max_time)} min")

        # Detailed breakdown
        st.markdown("**Assessment Breakdown:**")
        for path in enabled_paths:
            if path.enabled and path.question_count > 0:
                st.markdown(
                    f"• **{path.name}**: {path.question_count} questions - {path.description}"
                )

        # Export options
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📤 Export Configuration"):
                self.export_configuration(answers, enabled_paths, total_questions)

        with col2:
            st.info(
                "💡 Ready to proceed with the full detailed assessment based on these answers."
            )

    def export_configuration(
        self,
        answers: Dict[str, str],
        enabled_paths: List[AssessmentPath],
        total_questions: int,
    ):
        """Export the assessment configuration"""
        start_time = st.session_state.get("assessment_start_time", datetime.now())

        config = {
            "assessment_metadata": {
                "timestamp": datetime.now().isoformat(),
                "start_time": start_time.isoformat(),
                "duration_minutes": (datetime.now() - start_time).total_seconds() / 60,
                "total_gateway_questions": len(answers),
                "estimated_total_questions": total_questions,
            },
            "gateway_answers": answers,
            "assessment_scope": [
                {
                    "name": path.name,
                    "enabled": path.enabled,
                    "question_count": path.question_count,
                    "description": path.description,
                }
                for path in enabled_paths
            ],
            "summary": {
                "enabled_paths": sum(1 for path in enabled_paths if path.enabled),
                "total_questions": total_questions,
                "estimated_time_minutes": f"{int(total_questions * 0.5)}-{int(total_questions * 1.0)}",
            },
        }

        # Create JSON string
        json_string = json.dumps(config, indent=2)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"itra_assessment_config_{timestamp}.json"

        st.download_button(
            label="📥 Download Configuration JSON",
            data=json_string,
            file_name=filename,
            mime="application/json",
            help="Download the assessment configuration for integration with other systems",
        )

        # Show preview
        with st.expander("👁️ Preview Configuration"):
            st.code(json_string, language="json")


def main():
    app = ITRAGatewayApp()
    app.main()


if __name__ == "__main__":
    main()
