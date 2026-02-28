"""
Chart Factory Module - Creates consistent Plotly charts across the dashboard.
This module provides a centralized way to create charts with consistent styling,
eliminating code duplication and ensuring visual consistency.
"""

import plotly.express as px
from config import CHART_DIMENSIONS, COLOR_SCALES, COLORS, FONT_CONFIG


class ChartFactory:
    """
    Factory class for creating standardized Plotly charts.
    All methods return configured Plotly figure objects ready for display.
    """

    @staticmethod
    def get_base_layout(height=None, margin=None):
        """
        Returns base layout configuration applied to all charts.

        Args:
            height (int): Chart height in pixels
            margin (dict): Margin configuration {t, l, r, b}

        Returns:
            dict: Base layout configuration
        """
        if height is None:
            height = CHART_DIMENSIONS["default_height"]
        if margin is None:
            margin = CHART_DIMENSIONS["default_margin"]

        return dict(
            height=height,
            plot_bgcolor=COLORS["background"],
            paper_bgcolor=COLORS["background"],
            margin=margin,
            font=dict(
                family=FONT_CONFIG["family"], color=FONT_CONFIG["color"], size=FONT_CONFIG["size"]
            ),
        )

    @staticmethod
    def get_axis_config(show_grid=True, show_line=True, title=None):
        """
        Returns standardized axis configuration.

        Args:
            show_grid (bool): Whether to show grid lines
            show_line (bool): Whether to show axis line
            title (str): Axis title text

        Returns:
            dict: Axis configuration
        """
        config = {
            "showgrid": show_grid,
            "gridcolor": COLORS["grid"] if show_grid else None,
            "gridwidth": 1,
            "tickfont": dict(family=FONT_CONFIG["family"], color=COLORS["text_primary"], size=11),
            "title": title,
        }

        if show_line:
            config.update(
                {
                    "showline": True,
                    "linewidth": 2,
                    "linecolor": "rgba(255,255,255,0.12)",
                }
            )

        if title:
            config["title_font"] = dict(
                family=FONT_CONFIG["family"], color=COLORS["text_primary"], size=13
            )

        return config

    @staticmethod
    def get_colorbar_config(title="Volume", x=None):
        """
        Returns standardized colorbar configuration for heatmaps.

        Args:
            title (str): Colorbar title
            x (float): Horizontal position (0-1)

        Returns:
            dict: Colorbar configuration
        """
        config = dict(
            title=title,
            thickness=15,
            len=0.7,
            bgcolor="rgba(20, 25, 50, 0.8)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
            tickfont=dict(family=FONT_CONFIG["family"], size=10, color=COLORS["text_primary"]),
        )

        if x is not None:
            config["x"] = x

        return config

    @staticmethod
    def create_area_chart(df, x, y, line_color=None):
        """
        Creates an area chart for time series data.
        Used in Executive Summary for complaint volume trends.

        Args:
            df (DataFrame): Data source
            x (str): Column name for x-axis (typically date)
            y (str): Column name for y-axis (typically count)
            line_color (str): Line color (defaults to primary cyan)

        Returns:
            plotly.graph_objects.Figure: Configured area chart
        """
        if line_color is None:
            line_color = COLORS["primary"]

        fig = px.area(df, x=x, y=y, template="plotly_dark")

        # Style the area with gradient fill
        fig.update_traces(
            line_color=line_color,
            fillcolor="rgba(0, 174, 239, 0.1)",  # Very subtle fill
            line_width=3,
        )

        # Apply custom layout
        layout = ChartFactory.get_base_layout(height=400, margin=dict(t=20, l=0, r=0, b=0))
        layout.update(
            {
                "xaxis": {
                    **ChartFactory.get_axis_config(show_grid=False, show_line=False),
                    "title": None,
                },
                "yaxis": {
                    **ChartFactory.get_axis_config(show_grid=True, show_line=False),
                    "title": None,
                },
                "hovermode": "x unified",
            }
        )

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_donut_chart(df, values, names, hole=0.64, colors=None, center_text=None):
        """
        Creates a donut chart with consistent styling.
        Used for showing distribution of categorical data.

        Args:
            df (DataFrame): Data source
            values (str): Column name for slice sizes
            names (str): Column name for slice labels
            hole (float): Size of center hole (0-1)
            colors (list): Custom color sequence
            center_text (str): Text to display in center

        Returns:
            plotly.graph_objects.Figure: Configured donut chart
        """
        if colors is None:
            colors = COLOR_SCALES["blue_gradient"]

        fig = px.pie(df, values=values, names=names, hole=hole, color_discrete_sequence=colors)

        # Style traces with gaps between slices
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hoverinfo="label+percent+value",
            textfont=dict(color="white", weight="bold", size=16),
            marker=dict(
                line=dict(
                    color=COLORS["card_bg"],  # Matches card background
                    width=3.5,  # Creates visible gaps
                )
            ),
        )

        # Configure layout with horizontal legend
        layout = ChartFactory.get_base_layout(height=400)
        layout.update(
            {
                "showlegend": True,
                "legend": dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.1,
                    xanchor="center",
                    x=0.5,
                    font=dict(color=COLORS["text_primary"], size=11),
                ),
            }
        )

        # Add center annotation if text provided
        if center_text:
            layout["annotations"] = [
                dict(
                    text=center_text,
                    x=0.5,
                    y=0.5,
                    font_size=20,
                    showarrow=False,
                    font_color=COLORS["text_primary"],
                )
            ]

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_scatter_chart(
        df, x, y, size=None, color=None, hover_name=None, color_scale=None, labels=None, size_max=60
    ):
        """
        Creates a scatter plot for performance matrix visualization.
        Used in Company Performance page.

        Args:
            df (DataFrame): Data source
            x (str): Column for x-axis
            y (str): Column for y-axis
            size (str): Column for bubble size
            color (str): Column for color mapping
            hover_name (str): Column for hover label
            color_scale (list): Custom color scale
            labels (dict): Axis label mapping
            size_max (int): Maximum bubble size

        Returns:
            plotly.graph_objects.Figure: Configured scatter plot
        """
        if color_scale is None:
            color_scale = COLOR_SCALES["performance_gradient"]

        fig = px.scatter(
            df,
            x=x,
            y=y,
            hover_name=hover_name,
            size=size,
            color=color,
            color_continuous_scale=color_scale,
            labels=labels or {},
            size_max=size_max,
        )

        # Style markers with white borders
        fig.update_traces(
            marker=dict(line=dict(width=2, color="white"), opacity=0.85),
            hovertemplate="<b>%{hovertext}</b><br>Volume: %{x:,}<br>Timeliness: %{y:.1f}%<extra></extra>",
        )

        layout = ChartFactory.get_base_layout(margin=dict(t=30, l=20, r=20, b=20))
        layout.update(
            {
                "xaxis": ChartFactory.get_axis_config(title=labels.get(x) if labels else None),
                "yaxis": ChartFactory.get_axis_config(title=labels.get(y) if labels else None),
                "coloraxis_colorbar": ChartFactory.get_colorbar_config(title="Timeliness %"),
            }
        )

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_horizontal_bar(df, x, y, text=None, color=None):
        """
        Creates a horizontal bar chart for rankings and comparisons.

        Args:
            df (DataFrame): Data source
            x (str): Column for bar length
            y (str): Column for bar labels
            text (str): Column for text annotations
            color (str): Bar color

        Returns:
            plotly.graph_objects.Figure: Configured bar chart
        """
        if color is None:
            color = "rgba(56, 189, 248, 0.92)"

        fig = px.bar(df, x=x, y=y, orientation="h", text=text or x)

        # Style bars with borders and text
        fig.update_traces(
            marker=dict(
                color=color,
                line=dict(color="rgba(255,255,255,0.18)", width=1),
            ),
            texttemplate="%{x:,}",
            textposition="outside",
            textfont=dict(size=12, family=FONT_CONFIG["family"], color=COLORS["text_primary"]),
            hoverlabel=dict(
                bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color=COLORS["text_primary"], size=12)
            ),
            hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
        )

        layout = ChartFactory.get_base_layout(margin=dict(t=10, l=10, r=10, b=10))
        layout.update(
            {
                "xaxis": {
                    **ChartFactory.get_axis_config(show_line=False),
                    "zeroline": False,
                    "title": None,
                },
                "yaxis": {
                    "categoryorder": "total ascending",  # Sort bars by value
                    "tickfont": dict(color="rgba(230,237,247,0.92)", size=12),
                    "title": None,
                },
                "showlegend": False,
            }
        )

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_treemap(df, path, values, color, color_scale=None):
        """
        Creates a treemap for hierarchical data visualization.
        Used in Product Issues page to show product/sub-product hierarchy.

        Args:
            df (DataFrame): Data source
            path (list): Column names for hierarchy levels
            values (str): Column for tile sizes
            color (str): Column for color mapping
            color_scale (list): Custom color scale

        Returns:
            plotly.graph_objects.Figure: Configured treemap
        """
        if color_scale is None:
            color_scale = COLOR_SCALES["blue_monochrome"]

        fig = px.treemap(
            df,
            path=path,
            values=values,
            color=color,
            color_continuous_scale=color_scale,
        )

        # Style tiles with rounded corners and borders
        fig.update_traces(
            textinfo="label",
            texttemplate="<b>%{label}</b>",
            textfont=dict(
                family=FONT_CONFIG["family"],
                size=14,
                color="#F1F5F9",  # Always visible on dark tiles
            ),
            marker=dict(line=dict(color="rgba(255,255,255,0.15)", width=1.5), cornerradius=8),
            hoverlabel=dict(
                bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color=COLORS["text_primary"], size=13)
            ),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<extra></extra>",
        )

        layout = ChartFactory.get_base_layout(margin=dict(t=10, l=10, r=10, b=10))
        layout.update(
            {
                "coloraxis_colorbar": ChartFactory.get_colorbar_config(),
            }
        )

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def create_choropleth(df, locations, color, scope="usa", color_scale=None):
        """
        Creates a choropleth map for geographic data.
        Used in Geographic Trends page.

        Args:
            df (DataFrame): Data source
            locations (str): Column with state/region codes
            color (str): Column for color intensity
            scope (str): Geographic scope
            color_scale (list): Custom color scale

        Returns:
            plotly.graph_objects.Figure: Configured map
        """
        if color_scale is None:
            color_scale = COLOR_SCALES["heatmap_blue"]

        fig = px.choropleth(
            df,
            locations=locations,
            locationmode="USA-states",
            color=color,
            scope=scope,
            color_continuous_scale=color_scale,
            labels={color: "Volume"},
        )

        # Style map borders and hover
        fig.update_traces(
            marker_line_color="rgba(255,255,255,0.35)",
            marker_line_width=1.1,
            hoverlabel=dict(
                bgcolor="rgba(12, 18, 30, 0.95)", font=dict(color=COLORS["text_primary"], size=12)
            ),
            hovertemplate="<b>%{location}</b><br>Complaints: %{z:,}<extra></extra>",
        )

        # Configure map geography styling
        layout = ChartFactory.get_base_layout(margin=dict(t=0, l=0, r=0, b=0))
        layout.update(
            {
                "geo": dict(
                    bgcolor=COLORS["background"],
                    lakecolor="rgba(20, 70, 110, 0.35)",
                    landcolor="rgba(255,255,255,0.02)",
                    subunitcolor="rgba(255,255,255,0.16)",
                    countrycolor="rgba(255,255,255,0.16)",
                    showlakes=True,
                    showcountries=True,
                    projection_type="albers usa",
                ),
                "coloraxis_colorbar": {
                    **ChartFactory.get_colorbar_config(),
                    "x": 1.02,  # Position colorbar on right
                },
            }
        )

        fig.update_layout(**layout)
        return fig

    @staticmethod
    def add_reference_lines(
        fig, avg_x=None, avg_y=None, x_label="Avg Volume", y_label="Avg Timeliness"
    ):
        """
        Adds average reference lines to scatter plots.
        Used in Company Performance to show benchmarks.

        Args:
            fig (plotly.graph_objects.Figure): Figure to modify
            avg_x (float): X-axis average value
            avg_y (float): Y-axis average value
            x_label (str): Label for vertical line
            y_label (str): Label for horizontal line

        Returns:
            plotly.graph_objects.Figure: Modified figure
        """
        if avg_y is not None:
            fig.add_hline(
                y=avg_y,
                line_dash="dot",
                line_color="rgba(255,255,255,0.3)",
                line_width=2,
                annotation_text=y_label,
                annotation_position="right",
                annotation_font=dict(
                    family=FONT_CONFIG["family"], size=11, color=COLORS["text_primary"]
                ),
            )

        if avg_x is not None:
            fig.add_vline(
                x=avg_x,
                line_dash="dot",
                line_color="rgba(255,255,255,0.3)",
                line_width=2,
                annotation_text=x_label,
                annotation_font=dict(
                    family=FONT_CONFIG["family"], size=11, color=COLORS["text_primary"]
                ),
            )

        return fig
