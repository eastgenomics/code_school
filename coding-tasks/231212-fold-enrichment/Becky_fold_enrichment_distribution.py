import dxpy as dx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime


def get_002_cen_projects_in_period(first_date):
    """
    Gets all the 002 CEN projects between the period given
    Parameters
    ----------
    first_date : str
        e.g. '2023-07-18'
    Returns
    -------
    cen_projs_response : list
        list of dicts, each representing info about a proj found
    """
    # Search projs in the period starting with 002 and ending with CEN
    cen_projs_response = list(dx.find_projects(
        level='VIEW',
        created_after=first_date,
        name="002*CEN",
        name_mode="glob",
        describe={'fields': {'name': True}}
    ))

    return cen_projs_response


def get_hsmetrics_file(project_id, project_name):
    """
    Find the Picard HSMetrics .txt files from each run which is an
    output of MultiQC

    Parameters
    ----------
    project_id : str
        DX project ID
    project_name : str
        name of the DX project

    Returns
    -------
    hs_file_list : list
        list of dict objects, one per file
    """
    # Get objects from DNAnexus
    hsmetrics_file_response = list(
        dx.find_data_objects(
            project=project_id,
            name="multiqc_picard_HsMetrics.txt",
            classname='file',
            describe={
                'fields': {
                    'name': True,
                    'archivalState': True
                }
            }
        )
    )

    # Make into formatted dict so we can keep the project name for
    # plotting later
    hs_file_list = [
        {
            'project': x['project'],
            'project_name': project_name,
            'id': x['id'],
            'archive_state': x['describe']['archivalState']
        } for x in hsmetrics_file_response
    ]


    return hs_file_list


def read_to_df(file_dict):
    """
    Read the txt file into a pandas df

    Parameters
    ----------
    file_dict : dict
        dict of info about one file

    Returns
    -------
    metrics_df : pd.DataFrame
        pandas df with all the QC info about all samples in the run
    """
    proj_name = file_dict['project_name']
    run_name = proj_name.removeprefix('002_').removesuffix('_CEN')

    # Open the file with dx
    with dx.open_dxfile(file_dict['id'], mode='r') as dx_file:
        # Read TSV to pandas df
        metrics_df = pd.read_csv(dx_file, sep='\t')
        # Add run name as a column
        metrics_df['Run'] = run_name

    return metrics_df


def reformat_df(metrics_df):
    """
    Reformat df to add Run Date and date

    Parameters
    ----------
    metrics_df : pd.DataFrame
        pandas df with all QC metrics for all runs

    Returns
    -------
    metrics_df : pd.DataFrame
        pandas df with all QC metrics for all runs with extra columns
        and sorted by date
    """
    # Split out the run date and number e.g. '231204_240'
    # to plot this on X axis instead of whole run name
    metrics_df['Run Date'] = metrics_df['Run'].apply(
        lambda s: '_'.join(s.split('_')[0:6:2])
    )
    # Get just date column and order the runs by date
    metrics_df['date'] = metrics_df['Run'].apply(lambda s:s.split('_')[0])
    metrics_df.sort_values(by='date', inplace = True)

    return metrics_df


def plot_fold_enrichment(single_df):
    """
    Plot scatter graph with Plotly

    Parameters
    ----------
    single_df : pd.DataFrame
        dataframe of all samples with QC metrics
    """
    fig = px.scatter(
        single_df, x='Run Date', y='FOLD_ENRICHMENT', color='Run',
        custom_data=['Sample', 'Run'],
        trendline='ols',
        trendline_scope='overall'
    )

    # Update hover template to include Run name and sample name
    fig.update_traces(
        hovertemplate="<br>".join([
            "Run: %{customdata[1]}",
            "Sample: %{customdata[0]}",
            "Fold enrichment: %{y}<extra></extra>",
        ])
    )

    # Add single mean line across runs
    fig.add_trace(go.Scatter(
        x=single_df['Run Date'],
        y=[single_df['FOLD_ENRICHMENT'].mean()] * len(
            single_df['FOLD_ENRICHMENT']
        ),
        mode='lines',
        name='Mean',
        line=dict(dash='dot', width=2, color='black'),
        hovertemplate='Mean fold enrichment: %{y}'
    ))

    # Add titles
    fig.update_layout(
        xaxis_title='Run',
        yaxis_title="Fold enrichment",
        title="Fold enrichment distribution - all CEN runs since 2023-07-18",
        yaxis = dict(
            tickmode = 'linear',
            dtick = 100
        )
    )

    # Add hlines for current thresholds
    fig.add_hline(y=1750, line_color="orange", opacity=0.4)
    fig.add_hline(y=1800, line_color="red", opacity=0.4)
    fig.add_hline(y=1350, line_color="red", opacity=0.4)

    fig.update_xaxes(tickangle=60)

    # Remove the run colours from the legend
    for trace in fig['data']:
        if(trace['name'] not in ['Mean', 'Overall Trendline']):
            trace['showlegend'] = False

    fig.write_html("Becky_CEN_fold_enrichment_tick_100_plus_trendline.html")


def main():
    """
    Main function to get 002 projects and plot fold enrichment distribution
    """
    cen_002_projects = get_002_cen_projects_in_period('2023-07-18')
    print(
        datetime.now().replace(microsecond=0),
        f"Found {len(cen_002_projects)} CEN projects"
    )

    # Create big list of dicts for all hsmetrics files
    hs_files = []
    for proj in cen_002_projects:
        proj_id = proj['id']
        proj_name = proj['describe']['name']
        hs_file = get_hsmetrics_file(proj_id, proj_name)
        hs_files.extend(hs_file)
    print(
        datetime.now().replace(microsecond=0),
        f"Found {len(hs_files)} Picard HSMetrics files"
    )

    print(datetime.now().replace(microsecond=0), "Reading Picard HSMetrics files to a dataframe")
    # Read all hsmetrics for all runs to a single df
    list_of_dfs = []
    for file in hs_files:
        file_df = read_to_df(file)
        list_of_dfs.append(file_df)
    single_df = pd.concat(list_of_dfs)

    # Reformat df to add new columns
    formatted_df = reformat_df(single_df)

    print(datetime.now().replace(microsecond=0), "Plotting fold enrichment")
    plot_fold_enrichment(formatted_df)


if __name__ == '__main__':
    main()
