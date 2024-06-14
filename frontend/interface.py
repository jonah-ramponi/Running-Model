"""
Basic Streamlit interface, that I used to test out to see what the equation outputs look like

With more time I'd connect this to the API, I just used this for experimentation.
"""

import os
import argparse
import pandas as pd
import numpy as np

import streamlit as st
import altair as alt

ASSETS_PATH = "frontend/assets"
RUNNA_LOGO_PATH = os.path.join(ASSETS_PATH, "runna_logo.png")

st.set_page_config(
    page_title="Jonah's Runna Interface",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Plan Distance Visualization")
    parser.add_argument(
        "--target_mileage",
        type=int,
        default=30,
        help="The weekly mileage you aim to build up to (km).",
    )
    parser.add_argument(
        "--starting_mileage",
        type=int,
        default=15,
        help="Your starting weekly mileage (km).",
    )
    parser.add_argument(
        "-a",
        type=float,
        default=0.75,
        help="Parameter governing the shape of the curve (0 < a < 1).",
    )
    parser.add_argument(
        "-b",
        type=float,
        default=1.0,
        help="Parameter governing the shape of the curve (b > 0).",
    )
    parser.add_argument(
        "--n_value", type=int, default=12, help="Number of weeks in your training plan."
    )
    return parser.parse_args()


def visualize_plan(target_mileage, starting_mileage, a, b, n_value):
    with st.sidebar:
        st.markdown("#### Parameters")

        target_mileage = st.slider(
            "Select a value for your Target Mileage",
            0,
            120,
            30,
            help="The weekly mileage you aim to build up to (km).",
        )
        starting_mileage = st.slider(
            "Select a value for your Starting Mileage",
            0,
            120,
            15,
            help="Your starting weekly mileage (km).",
        )

        a = st.number_input(
            "Value for: a",
            min_value=0.01,
            max_value=1.0,
            value=0.75,
            step=0.01,
            help="Parameter governing the shape of the curve (0 < a < 1).",
        )
        b = st.number_input(
            "Value for: b",
            min_value=0.1,
            value=1.0,
            step=0.1,
            help="Parameter governing the shape of the curve (b > 0).",
        )

        n_value = st.slider(
            "Select the length of your Plan in weeks",
            1,
            24,
            12,
            help="Number of weeks in your training plan.",
        )

    n_values = np.arange(0, n_value)

    eq_1_mileage_by_week = target_mileage - (
        target_mileage - starting_mileage
    ) * np.power(a, n_values / b)

    eq_2_mileage_by_week = np.minimum(
        starting_mileage + (a * n_values) / b, target_mileage
    )

    chart_data = pd.DataFrame(
        {
            "Week": n_values,
            "Weekly Mileage (Eq 1)": eq_1_mileage_by_week,
            "Weekly Mileage (Eq 2)": eq_2_mileage_by_week,
        }
    ).set_index("Week")

    chart = (
        alt.Chart(chart_data.reset_index())
        .transform_fold(
            fold=["Weekly Mileage (Eq 1)", "Weekly Mileage (Eq 2)"],
            as_=["Equation", "Weekly Mileage"],
        )
        .mark_line()
        .encode(
            x=alt.X("Week:Q", title="Week Number"),
            y=alt.Y("Weekly Mileage:Q", title="Weekly Distance (km)"),
            color="Equation:N",
        )
    )
    TITLE_SIZING, LOGO_SIZING = st.columns((0.8, 0.2))

    with TITLE_SIZING:
        st.header("Plan Distance Visualisation")
        st.markdown(
            "To start with, I wanted to just be able to play around with the two models and compare them and see what type of plans they come up with! This quick interface allowed me to do that. With more time, I would integrate this interface with the API.\n\nI think in the future, it might be nice to build a playground like Desmos where you can play with parameters and test different model ideas out. See [Desmos](https://www.desmos.com/calculator). I also think it would make sense to visualize the week on week change in mileage (d/dn), but I didn't get round to doing this. I think it would be interesting to overlay cumulative mileage too."
        )
    with LOGO_SIZING:
        st.image(RUNNA_LOGO_PATH)

    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    args = parse_arguments()
    visualize_plan(
        args.target_mileage, args.starting_mileage, args.a, args.b, args.n_value
    )
