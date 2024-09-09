import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def dataframe_manipulation(data):
    #initialising columns:
    data['reb_pct'] = data['oreb_pct'] + data['dreb_pct'] 
    init_columns = ['oreb_pct_chng_yoy', 'dreb_pct_chng_yoy', 'reb_pct_chng_yoy', 
                    'usg_pct_chng_yoy', 'ts_pct_chng_yoy', 'ast_pct_chng_yoy',
                    'oreb_pct_chng_tot', 'dreb_pct_chng_tot', 'reb_pct_chng_tot',
                    'usg_pct_chng_tot', 'ts_pct_chng_tot', 'ast_pct_chng_tot',
                    'season_number', 'gp_chng_yoy', 'gp_chng_tot', 'pts_chng_yoy',
                    'pts_chng_tot', 'reb_chng_yoy', 'reb_chng_tot', 'ast_chng_yoy',
                    'ast_chng_tot']
    data[init_columns] = 0
    visited_players = []
    for i in range(len(data)):
        p_name = data.iloc[i,1]
        #print(i)
        if p_name not in visited_players:
            visited_players.append(p_name)
            prev_ind = i
            init_ind = i
            for j in range(i+1,len(data)):
                #calculating values for the new columns
                if data.iloc[j,1] == p_name:
                    data.loc[j,'oreb_pct_chng_yoy'] = data.iloc[j,16] - data.iloc[prev_ind,16]  
                    data.loc[j,'dreb_pct_chng_yoy'] = data.iloc[j,17] - data.iloc[prev_ind,17]
                    data.loc[j,'reb_pct_chng_yoy'] = data.iloc[j,23] - data.iloc[prev_ind,23] 
                    data.loc[j,'usg_pct_chng_yoy'] = data.iloc[j,18] - data.iloc[prev_ind,18]
                    data.loc[j,'ts_pct_chng_yoy'] = data.iloc[j,19] - data.iloc[prev_ind,19]
                    data.loc[j,'ast_pct_chng_yoy'] = data.iloc[j,20] - data.iloc[prev_ind,20]
                    data.loc[j,'oreb_pct_chng_tot'] = data.iloc[j,16] - data.iloc[init_ind,16]  
                    data.loc[j,'dreb_pct_chng_tot'] = data.iloc[j,17] - data.iloc[init_ind,17]
                    data.loc[j,'reb_pct_chng_tot'] = data.iloc[j,23] - data.iloc[init_ind,23]
                    data.loc[j,'usg_pct_chng_tot'] = data.iloc[j,18] - data.iloc[init_ind,18]
                    data.loc[j,'ts_pct_chng_tot'] = data.iloc[j,19] - data.iloc[init_ind,19]
                    data.loc[j,'ast_pct_chng_tot'] = data.iloc[j,20] - data.iloc[init_ind,20]
                    data.loc[j,'season_number'] = data.loc[prev_ind,'season_number'] + 1
                    data.loc[j,'gp_chng_yoy'] = data.iloc[j,11] - data.iloc[prev_ind,11]
                    data.loc[j,'gp_chng_tot'] = data.iloc[j,11] - data.iloc[init_ind,11]
                    data.loc[j,'pts_chng_yoy'] = data.iloc[j,12] - data.iloc[prev_ind,12]
                    data.loc[j,'pts_chng_tot'] = data.iloc[j,12] - data.iloc[init_ind,12]
                    data.loc[j,'reb_chng_yoy'] = data.iloc[j,13] - data.iloc[prev_ind,13]
                    data.loc[j,'reb_chng_tot'] = data.iloc[j,13] - data.iloc[init_ind,13]
                    data.loc[j,'ast_chng_yoy'] = data.iloc[j,14] - data.iloc[prev_ind,14]
                    data.loc[j,'ast_chng_tot'] = data.iloc[j,14] - data.iloc[init_ind,14]
                    prev_ind = j
    return data


def grouped_lineplot(data, pos_list, l_age, u_age, fig):
    #creating a mask of the data based on the position requried
    data_pos = data.query("position in "+str(pos_list))
    init = 0
    #creating a lamda funciton which will act as a status flag for our legend function in the plotly graph
    legend_flag = lambda init : True if init == 0 else False
    for i in range(len(data_pos)):
        #creating another mask of the dataframe to get the age of the player when he started his career
        if data_pos[data_pos['player_name'] == data_pos.iloc[i,1]].iloc[0,3] > l_age and data_pos[data_pos['player_name'] == data_pos.iloc[i,1]].iloc[0,3] < u_age:
            #adding lines into the plot based on the performace metric
            fig.add_trace(go.Scatter(x=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['season_number'],
                                     y=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['reb_chng_tot'],
                                     connectgaps = True, legendgroup = 'rebound', name = 'Change in rebound',
                                     showlegend = legend_flag(init), 
                                     line=dict(color='royalblue', width=2),
                                    ))
            fig.add_trace(go.Scatter(x=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['season_number'],
                             y=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['pts_chng_tot'],
                             connectgaps = True, legendgroup = 'points', name = 'Change in points',
                             showlegend = legend_flag(init), 
                             line=dict(color='orange', width=2),
                            ))
            fig.add_trace(go.Scatter(x=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['season_number'],
                             y=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['ast_chng_tot'],
                             connectgaps = True, legendgroup = 'assists', name = 'Change in assists',
                             showlegend = legend_flag(init), 
                             line=dict(color='red', width=2),
                            ))
            fig.add_trace(go.Scatter(x=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['season_number'],
                     y=data_pos[data_pos['player_name'] == data_pos.iloc[i,1]]['gp_chng_tot'],
                     connectgaps = True, legendgroup = 'gp', name = 'Change in GP',
                     showlegend = legend_flag(init), 
                     line=dict(color='purple', width=2),
                    ))
            init += 1
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='Season wise change in stats for the position: '+ pos_list[0],
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    fig.update_layout(annotations=annotations)
    #fig.show()
    return fig