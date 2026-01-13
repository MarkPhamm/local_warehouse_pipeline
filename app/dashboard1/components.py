"""
UI Components Module - Reusable Streamlit components.
This module provides wrapper functions for common UI patterns,
ensuring consistency and reducing code duplication.
"""

import streamlit as st


class UIComponents:
    """
    Collection of reusable UI component builders.
    All methods handle HTML rendering and Streamlit widget creation.
    """

    @staticmethod
    def kpi_card(label, value, icon, tooltip="", color=None):
        """
        Renders a KPI card with icon and value.
        Used in Executive Summary page for key metrics.

        Args:
            label (str): KPI label text
            value (str): KPI value (can include HTML)
            icon (str): Emoji or icon character
            tooltip (str): Hover tooltip text
            color (str): Optional color override for value
        """
        # If value is already HTML with span, use as-is
        # Otherwise wrap in default styling
        if isinstance(value, str) and "<span" in value:
            value_html = value
        else:
            value_html = f"<span style='font-size:2.2rem'>{value}</span>"

        html = f"""
        <div class="kpi-card" title="{tooltip}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value_html}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def adaptive_text(text, threshold=19, small_size="1.5rem", large_size="2.2rem"):
        """
        Creates adaptive text sizing based on length.
        Longer text gets smaller font to fit in KPI cards.

        Args:
            text (str): Text to display
            threshold (int): Character count threshold for size change
            small_size (str): Font size for long text
            large_size (str): Font size for short text

        Returns:
            str: HTML span with appropriate font size
        """
        size = small_size if len(text) > threshold else large_size
        return f"<span style='font-size:{size}'>{text}</span>"

    @staticmethod
    def chart_container(title, content_func):
        """
        Wraps chart in styled container with title.
        Provides consistent spacing and visual grouping.

        Args:
            title (str): Chart title
            content_func (callable): Function that renders chart content
        """
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f"### {title}")
        content_func()
        st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def info_filter(label, options, key=None, default=None):
        """
        Creates an info box with radio button filter.
        Used in Product Issues for treemap filtering.

        Args:
            label (str): Info box label
            options (list): Radio button options
            key (str): Unique widget key
            default (int): Default selected index

        Returns:
            str: Selected option value
        """
        st.info(label)
        return st.radio(
            "View", options=options, label_visibility="collapsed", key=key, index=default or 0
        )

    @staticmethod
    def select_filter(label, options, key=None):
        """
        Creates an info box with selectbox.
        Used for dropdown filters with explanatory label.

        Args:
            label (str): Info box label
            options (list): Selectbox options
            key (str): Unique widget key

        Returns:
            str: Selected option value
        """
        st.info(label)
        return st.selectbox("Select", options=options, label_visibility="collapsed", key=key)

    @staticmethod
    def render_kpi_row(kpi_data):
        """
        Renders a row of KPI cards using columns.
        Simplifies layout code in pages.

        Args:
            kpi_data (list): List of dicts with keys: label, value, icon, tooltip
        """
        cols = st.columns(len(kpi_data))

        for col, kpi in zip(cols, kpi_data):
            with col:
                UIComponents.kpi_card(
                    label=kpi["label"],
                    value=kpi["value"],
                    icon=kpi["icon"],
                    tooltip=kpi.get("tooltip", ""),
                )
