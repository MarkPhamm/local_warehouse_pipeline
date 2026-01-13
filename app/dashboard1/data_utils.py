"""
Data Utilities Module - Common data transformation patterns.
This module centralizes data aggregation, filtering, and transformation logic
to avoid repetitive pandas operations across pages.
"""


class DataTransformations:
    """
    Collection of reusable data transformation methods.
    All methods return transformed DataFrames ready for visualization.
    """

    @staticmethod
    def aggregate_by_groups(df, group_cols, agg_dict):
        """
        Generic groupby aggregation with reset index.

        Args:
            df (DataFrame): Source data
            group_cols (str or list): Column(s) to group by
            agg_dict (dict): Aggregation specification {col: func}

        Returns:
            DataFrame: Aggregated data
        """
        return df.groupby(group_cols).agg(agg_dict).reset_index()

    @staticmethod
    def value_counts_df(df, column, top_n=None, column_names=None):
        """
        Converts value_counts to DataFrame with optional filtering and renaming.
        Commonly used for categorical data summaries.

        Args:
            df (DataFrame): Source data
            column (str): Column to count
            top_n (int): Limit to top N values
            column_names (list): Custom column names for result

        Returns:
            DataFrame: Value counts as DataFrame
        """
        result = df[column].value_counts()

        if top_n:
            result = result.head(top_n)

        result = result.reset_index()

        # Apply custom column names or use defaults
        if column_names:
            result.columns = column_names
        else:
            result.columns = [column.title(), "Count"]

        return result

    @staticmethod
    def resample_timeseries(df, date_column, freq="M", agg="size"):
        """
        Resamples time series data to specified frequency.
        Used for trend analysis in Executive Summary.

        Args:
            df (DataFrame): Source data
            date_column (str): Date column name
            freq (str): Pandas resample frequency ('M', 'W', 'D')
            agg (str): Aggregation method

        Returns:
            DataFrame: Resampled time series
        """
        return df.set_index(date_column).resample(freq).size().reset_index(name="count")

    @staticmethod
    def filter_top_n_groups(df, group_column, n=5):
        """
        Filters DataFrame to include only top N groups by count.
        Used in Product Issues for treemap filtering.

        Args:
            df (DataFrame): Source data
            group_column (str): Column to group and filter by
            n (int): Number of top groups to keep

        Returns:
            DataFrame: Filtered data
        """
        top_groups = df.groupby(group_column).size().nlargest(n).index
        return df[df[group_column].isin(top_groups)]

    @staticmethod
    def calculate_company_stats(df):
        """
        Calculates company performance statistics.
        Specific to Company Performance page requirements.

        Args:
            df (DataFrame): Raw complaint data with company and is_timely_response

        Returns:
            DataFrame: Company stats with Total_Complaints and Timely_Rate
        """
        stats = (
            df.groupby("company")
            .agg(Total_Complaints=("product", "count"), Timely_Rate=("is_timely_response", "mean"))
            .reset_index()
        )

        # Filter out companies with zero complaints (edge case)
        stats = stats[stats["Total_Complaints"] > 0]

        # Convert rate to percentage
        stats["Timely_Rate"] = stats["Timely_Rate"] * 100

        return stats

    @staticmethod
    def prepare_treemap_data(
        df, filter_option, product_col="product", sub_product_col="sub_product"
    ):
        """
        Prepares hierarchical data for treemap based on filter selection.

        Args:
            df (DataFrame): Source data
            filter_option (str): Filter choice ('All Products', 'Top 5 Products', 'Top 3 Products')
            product_col (str): Product column name
            sub_product_col (str): Sub-product column name

        Returns:
            DataFrame: Aggregated data ready for treemap
        """
        # Determine number of top products based on filter
        if filter_option == "Top 5 Products":
            n = 5
        elif filter_option == "Top 3 Products":
            n = 3
        else:
            n = None  # All products

        # Filter to top N products if specified
        if n:
            df = DataTransformations.filter_top_n_groups(df, product_col, n)

        # Aggregate by product and sub-product
        treemap_data = df.groupby([product_col, sub_product_col]).size().reset_index(name="count")

        return treemap_data
