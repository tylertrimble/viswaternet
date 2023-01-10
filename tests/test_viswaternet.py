#!/usr/bin/env python

"""Tests for `viswaternet` package."""

import unittest
import viswaternet
import os
import matplotlib.pyplot as plt

model = viswaternet.VisWNModel("net1.inp")

class TestViswaternet(unittest.TestCase):
    """Tests for `viswaternet` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

class TestSaveFig(unittest.TestCase):
    """Tests for save_fig function."""
    
    def test_save_fig_naming(self):
        """Tests for file names outputted by save_fig function."""
        #Creates dummy model
        self.model = {}
        self.model['inp_file'] = 'dummynetwork.inp'
        
        fig,ax=plt.subplots()
        
        viswaternet.utils.save_fig(self)
        self.assertTrue(os.path.isfile('dummynetwork.png'), "save_fig() is not including network name to file name properly.")
        
        viswaternet.utils.save_fig(self,save_name="Test_")
        self.assertTrue(os.path.isfile('Test_dummynetwork.png'),"save_fig() is not applying user-defined string to file name correctly.")
        
        viswaternet.utils.save_fig(self,save_format='jpg')
        self.assertTrue(os.path.isfile('dummynetwork.jpg'),"save_fig() is not creating files with correct format.")
        
        os.remove('dummynetwork.png')
        os.remove('Test_dummynetwork.png')
        os.remove('dummynetwork.jpg')

class TestParameterBinning(unittest.TestCase):
    """Tests data binning."""
    
    def test_interval_naming(self):
        self.model = {}
        self.model['node_names'] = ['E1','E2','E3','E4','E5','E6']
        dummy_data=[1,2,3,5,6,7]
        
        interval_results, interval_names = viswaternet.network.bin_parameter(self,dummy_data,self.model['node_names'],4)
        self.assertListEqual(interval_names.tolist(),['1.000 - 3.000', '3.000 - 5.000', '5.000 - 7.000'],"Intervals are not being named properly.")
        
        dummy_data=[1,2,3,5,6,10]
        interval_results, interval_names = viswaternet.network.bin_parameter(self,dummy_data,self.model['node_names'],3,legend_sig_figs=0)
        self.assertListEqual(interval_names.tolist(),['1 - 6','6 - 10'],"Interval names are not following sig-fig adjustments correctly.")
        
    def test_interval_dict_structure(self):
        """"""
class TestPlottingFunctions(unittest.TestCase):
    """Tests if plotting functions produce a plot."""
    
    def test_discrete_nodes_plotting(self):
        fig,ax=plt.subplots()
        model.plot_discrete_nodes(ax,parameter='elevation')
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_discrete_nodes() is not generating plot.")
        os.remove('net1.png')
        
    def test_discrete_link_plotting(self):
        fig,ax=plt.subplots()
        model.plot_discrete_links(ax,parameter='length')
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_discrete_links() is not generating plot.")
        os.remove('net1.png')
        
    def test_continuous_nodes_plotting(self):
        fig,ax=plt.subplots()
        model.plot_continuous_nodes(ax,parameter='elevation')
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_continuous_nodes() is not generating plot.")
        os.remove('net1.png')
    
    def test_continuous_links_plotting(self):
        fig,ax=plt.subplots()
        model.plot_continuous_links(ax,parameter='length')
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_continuous_links() is not generating plot.")
        os.remove('net1.png')
    
    def test_unique_plotting(self):
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='demand_patterns',save_name='DemandPatterns_')
        
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='diameter',save_name='Diameter_')
        
        elements=['10','11','12']
        data=[10,6,15]
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='custom_data',data_type='continuous',parameter_type ='node',custom_data_values=[elements,data],save_name='Custom_')
        
        self.assertTrue(os.path.isfile('DemandPatterns_net1.png'),"plot_unique_data() is not generating demand patterns plot.")
        self.assertTrue(os.path.isfile('Diameter_net1.png'),"plot_unique_data() is not generating diameter plot.")
        self.assertTrue(os.path.isfile('Custom_net1.png'),"plot_unique_data() is not generating custom values plot.")
        
        os.remove('DemandPatterns_net1.png')
        os.remove('Diameter_net1.png')
        os.remove('Custom_net1.png')
        
    def test_animate_plot(self):
        fig,ax=plt.subplots()
        
        model.animate_plot(ax,function=model.plot_discrete_nodes,parameter='pressure',data_type='discrete',parameter_type='node',last_timestep=5,gif_save_name='discrete')
        self.assertTrue(os.path.isfile('discrete.gif'),"animate_plot() is not generating discrete plot gif file.")
        
        fig,ax=plt.subplots()
        
        model.animate_plot(ax,function=model.plot_continuous_nodes,parameter='pressure',data_type='continuous',parameter_type='node',last_timestep=5,gif_save_name='continuous')
        self.assertTrue(os.path.isfile('continuous.gif'),"animate_plot() is not generating continuous plot gif file.")
        
        # os.remove('discrete.gif')
        # os.remove('continuous.gif')
if __name__ == '__main__':
    unittest.main()    
    
    
    
    