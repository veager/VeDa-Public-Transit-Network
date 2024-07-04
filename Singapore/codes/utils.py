import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx

import scipy
from scipy import sparse



class processing_route():
    def __init__(self, data, sta_loc, line_col, node_col, seq_col, space='l_space'):
        '''
        
        
        Parameters
        ----------
        data (pandas.DataFrame): 
            the data store the line route information
            Note: 'line_col' colume is to indicate the directed line, 
            'line_col' value of the same line for different direction must be different
        
        sta_loc (pandas.DataFrame): 
            the station location
            index : station id
            two columns : 'lng' (i.e., X), 'lat' (i.e., Y) : 
        
        line_col (str): 
            the column name in 'data' indicating the tranport line
        
        node_col (str): 
            the column name in 'data' indicating the node (station) id 
        
        seq_col (str): 
            the column name in 'data' indicating the sequence number of nodes in a line
        
        space (str in {'l_space', 'p_space'}):
            
        '''
        
        self.data     = data
        self.sta_loc  = sta_loc
        
        self.line_col = line_col  # the column indicate the directed line
        self.node_col = node_col  # the column indicate the transport station (node id) 
        self.seq_col  = seq_col   # the column indicate the sequence number of nodes (node id) in a line ()
        
        self.space    = space
    # --------------------------------------------------------------
    def route_to_segment(self):
        '''
        extract route (edge)
        '''
        line_node = {}
        
        route_segment = []
    
        for line_name, line_route in self.data.groupby(self.line_col):

            # sort values by station sequence number ('seq_col')
            line_route = line_route.sort_values(by=self.seq_col).reset_index(drop=True)
            
            line_node[line_name] = '|'.join(list(map(str, line_route[self.node_col].to_list())))
            
            if self.space == 'l_space':
                
                for ix in range(line_route.shape[0] - 1):
                    
                    route_segment.append({
                        'start_node' : line_route[self.node_col][ix],
                        'end_node'   : line_route[self.node_col][ix+1],
                        'line_name'  : line_name })
            
            elif self.space == 'p_space':
                
                for ix in range(line_route.shape[0] - 1):
                    for jx in range(ix+1, line_route.shape[0]):
                    
                        route_segment.append({
                            'start_node' : line_route[self.node_col][ix],
                            'end_node'   : line_route[self.node_col][jx],
                            'line_name'  : line_name })

        route_segment = pd.DataFrame(route_segment)
        
        self.line_node = pd.Series(line_node)
        self.line_node.index.rename('line_name', inplace=True)
        # print(self.line_node)
        
        return route_segment
    # --------------------------------------------------------------
    def route_to_shp(self, route_seg=True):
        '''
        Parameters:
        -----------
        route_seg (bool) : 
            whether aggregate the route segment by same line
        '''
        from shapely.geometry import LineString, Point
        
        route = self.route_to_segment()
        
        route = route.merge(self.sta_loc, 
                            left_on = 'start_node', right_index=True, how='left', 
                            suffixes = (None, '_start_node'),
                            validate = 'many_to_one')
        route = route.rename({'lng':'lng_start', 'lat':'lat_start'}, axis='columns')
        
        route = route.merge(self.sta_loc, 
                            left_on='end_node', right_index=True, how='left',
                            suffixes=(None, '_end_node'),
                            validate = 'many_to_one')
        route = route.rename({'lng':'lng_end', 'lat':'lat_end'}, axis='columns')
        
        
        def point2line(series):
            line = LineString([(series['lng_start'], series['lat_start']), 
                               (series['lng_end'], series['lat_end'])])
            return line
        
        route = gpd.GeoDataFrame(route[['start_node', 'end_node', 'line_name']],
                                 geometry = route[['lng_start', 'lat_start', 'lng_end', 'lat_end']].apply(point2line, axis=1)
                                )
                
        if not route_seg:
            route = route[['line_name', 'geometry']].dissolve('line_name') 
            route = route.merge(pd.DataFrame(self.line_node, columns=['node_list']), 
                                left_index=True, right_index=True, how='left')
            
        return route
    # --------------------------------------------------------------
    def route_to_multi_matrix(self):
        '''
        extract the multi adjacency matrices for each lin
        '''
        
        # self.data[seq_col] = self.data[seq_col].astype(int)

        # Node list
        # len(node_list) equals the shape of adjacency matrix
        node_list = self.data[self.node_col].unique().tolist()
        node_list.sort()

        # Line list
        # len(node_list) equals the number of adjacency matrix
        line_list = []

        adj_matric_all = {}

        for line_name, line_route in self.data.groupby(by=self.line_col):

            line_list.append(line_name)

            line_route = line_route.sort_values(by=self.seq_col).reset_index(drop=True)

            # set the last entry of the diagonal 
            adj_indicator = [0]
            row_indicator = [len(node_list)-1]
            col_indicator = [len(node_list)-1]
            
            if self.space == 'p_space':

                for i in range(line_route.shape[0]-1):
                    for j in range(i+1, line_route.shape[0]):

                        start_node = line_route[self.node_col][i]
                        end_node   = line_route[self.node_col][j]
                        
                        row_indicator.append(node_list.index(start_node))
                        col_indicator.append(node_list.index(end_node))
                        adj_indicator.append(1)
            # -------------------------------------------
            elif self.space == 'l_space':

                for i in range(line_route.shape[0]-1):
                    start_node = line_route[self.node_col][i]
                    end_node   = line_route[self.node_col][i+1]

                    row_indicator.append(node_list.index(start_node))
                    col_indicator.append(node_list.index(end_node))
                    adj_indicator.append(1)
            # -------------------------------------------

            adj_matrix = scipy.sparse.csr_matrix((adj_indicator, (row_indicator, col_indicator)))

            adj_matric_all[line_name] = adj_matrix

        return adj_matric_all, node_list
    # --------------------------------------------------------------
# ==============================================================================================================