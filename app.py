
           


            st.plotly_chart(
                comparison_fig,
                width="stretch",
                key="dnv_pathway_cross_comparison",
                config={"displayModeBar": False, "responsive": True},
            )

        with insight_col:
            st.markdown(
                '<div class="scenario-section-label">Interpretation</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="scenario-side-insight">
                    <div class="scenario-side-insight-row">
                        <span>Outcome</span>
                        {selected_summary["outcome"]}
                    </div>
                    <div class="scenario-side-insight-row">
                        <span>Trade-off</span>
                        {selected_summary["tradeoff"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("More details", expanded=False):
            assumption_cols = st.columns(7, gap="small")
            assumptions = [
                ("Wind", f"{selected_details['wind_mult']:.1f}×"),
                ("Carbon", f"{selected_details['carbon_mult']:.1f}×"),
                ("Geopolitics", f"{selected_details['sanctions_val']:.2f}"),
                ("EU", selected_details["eu_policy_val"].capitalize()),
                ("Oil price", f"${selected_details['oil_p']}/bbl"),
                ("Grid", selected_details["grid_inv"].capitalize()),
                ("Data centres", f"{selected_details['datacentre_growth']:.1f}×"),
            ]

            for col, (label, value) in zip(assumption_cols, assumptions):
                with col:
                    st.metric(label, value)

            detail_metric = st.selectbox(
                "Additional chart",
                options=["GHG emissions", "Oil & gas exports", "Wind share"],
                key="dnv_pathway_detail_chart",
            )

            if detail_metric == "GHG emissions":
                detail_fig = plot_emissions(
                    selected_data,
                    show_uncertainty=False,
                    show_baseline=(selected_scenario != reference_name),
                )
            elif detail_metric == "Oil & gas exports":
                detail_fig = plot_export_composition(selected_data)
            else:
                detail_fig = plot_renewable_share(
                    selected_data,
                    show_baseline=(selected_scenario != reference_name),
                )

            detail_fig = compact_scenario_chart(detail_fig, height=270)
            st.plotly_chart(
                detail_fig,
                width="stretch",
                key="dnv_selected_pathway_detail",
                config={"displayModeBar": False, "responsive": True},
            )

