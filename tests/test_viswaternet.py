#!/usr/bin/env python

"""Tests for `viswaternet` package."""

import unittest
import viswaternet
import os
import matplotlib.pyplot as plt
import numpy as np

model = viswaternet.VisWNModel("tests/net1.inp")

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
        
        interval_results, interval_names = viswaternet.network.bin_parameter(self,dummy_data,self.model['node_names'],3)
        self.assertListEqual(interval_names,['1.000 - 3.000', '3.000 - 5.000', '5.000 - 7.000'],"Intervals are not being named properly.")
        
        dummy_data=[1,2,3,5,6,10]
        interval_results, interval_names = viswaternet.network.bin_parameter(self,dummy_data,self.model['node_names'],2,legend_sig_figs=0)
        self.assertListEqual(interval_names,['1 - 6','6 - 10'],"Interval names are not following sig-fig adjustments correctly.")
        
    def test_interval_dict_structure(self):
        """Tests that the dictionary produced by bin_parameter() is correct using trival case."""
        self.model = {}
        self.model['node_names'] = ['E1','E2','E3','E4','E5','E6']
        dummy_data=[1,2,3,5,6,7]
        # =============================================================================
        # Correct dict structure should be a nested dict with two layers, including
        # the interval name, the node names in that interval and then the index number
        # in the model['node_names] list.
        #
        # Nodes with values on the edge between two intervals should always be placed in
        # the interval with that value as the minimum.
        # =============================================================================
        correct_dict={'1.000 - 3.000': {'E1':0,'E2':1},
                      '3.000 - 5.000': {'E3':2},
                      '5.000 - 7.000': {'E4':3,'E5':4,'E6':5}}
        
        interval_results, interval_names = viswaternet.network.bin_parameter(self,dummy_data,self.model['node_names'],3)
        self.assertDictEqual(correct_dict,interval_results,"bin_parameter is not producing correct dictionary structure.")
        
class TestPlottingFunctions(unittest.TestCase):
    """Tests if plotting functions produce a plot."""
    
    def test_discrete_nodes_plotting(self):
        fig,ax=plt.subplots()
        model.plot_discrete_nodes(ax,parameter='elevation',savefig=True)
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_discrete_nodes() is not generating plot.")
        os.remove('net1.png')
        
    def test_discrete_link_plotting(self):
        fig,ax=plt.subplots()
        model.plot_discrete_links(ax,parameter='length',savefig=True)
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_discrete_links() is not generating plot.")
        os.remove('net1.png')
        
    def test_continuous_nodes_plotting(self):
        fig,ax=plt.subplots()
        model.plot_continuous_nodes(ax,parameter='elevation',savefig=True)
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_continuous_nodes() is not generating plot.")
        os.remove('net1.png')
    
    def test_continuous_links_plotting(self):
        fig,ax=plt.subplots()
        model.plot_continuous_links(ax,parameter='length',savefig=True)
        
        self.assertTrue(os.path.isfile('net1.png'),"plot_continuous_links() is not generating plot.")
        os.remove('net1.png')
    
    def test_unique_plotting(self):
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='demand_patterns',save_name='DemandPatterns_',savefig=True)
        
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='diameter',save_name='Diameter_',savefig=True)
        
        elements=['10','11','12']
        data=[10,6,15]
        fig,ax=plt.subplots()
        model.plot_unique_data(ax,parameter='custom_data',data_type='continuous',parameter_type ='node',custom_data_values=[elements,data],save_name='Custom_',savefig=True)
        
        self.assertTrue(os.path.isfile('DemandPatterns_net1.png'),"plot_unique_data() is not generating demand patterns plot.")
        self.assertTrue(os.path.isfile('Diameter_net1.png'),"plot_unique_data() is not generating diameter plot.")
        self.assertTrue(os.path.isfile('Custom_net1.png'),"plot_unique_data() is not generating custom values plot.")
        
        os.remove('DemandPatterns_net1.png')
        os.remove('Diameter_net1.png')
        os.remove('Custom_net1.png')
        
    def test_animate_plot(self):
        fig,ax=plt.subplots()
        
        model.animate_plot(ax=ax,function=model.plot_discrete_nodes,parameter='pressure',last_timestep=5,save_name='discrete')
        self.assertTrue(os.path.isfile('discrete.mp4'),"animate_plot() is not generating discrete plot gif file.")
        
        fig,ax=plt.subplots(figsize=(15,15))
        
        model.animate_plot(ax=ax,function=model.plot_continuous_nodes,parameter='pressure',last_timestep=5,save_name='continuous')
        self.assertTrue(os.path.isfile('continuous.mp4'),"animate_plot() is not generating continuous plot gif file.")
        
        os.remove('discrete.mp4')
        os.remove('continuous.mp4')

class TestNormalizeParameter(unittest.TestCase):
    """Tests parameter normalizing function"""
    
    def test_normalize_parameter(self):
        dummy_data=[0.0,50.0,100.0]
        test_normalized=[0,0.5,1]
        normalized_parameter = viswaternet.utils.normalize_parameter(dummy_data,0,1)
        self.assertListEqual(test_normalized,normalized_parameter,"Data is not being normalized correctly.")

class TestUnitConversion(unittest.TestCase):
    """Tests unit conversion function"""

    def test_unit_conversion(self):
        dummy_data=np.array([10.0,15.0,25.0]) #in meters
        correct_output=(dummy_data*3.28084).tolist()

        output = viswaternet.utils.unit_conversion(dummy_data,'length','ft')   
        self.assertListEqual(correct_output,output,"Data is not being converted to another unit correctly.")
        
class TestGetParameter(unittest.TestCase):
    
    def test_reservoir_tank_fetching(self):
        results, elements = model.get_parameter('node','pressure',5,tanks=True,reservoirs=True)
        self.assertAlmostEqual(results[0],91.91539,places=6,msg="Parameters are not in the correct order.")
        self.assertAlmostEqual(results[9],0,msg="Parameters are not in the correct order when reservoir data is collected.")
        self.assertAlmostEqual(results[10],40.014896,places=6,msg="Parameters are not in the correct order when tank data is collected.")
        
class TestInitalizeFunction(unittest.TestCase):
    
    def test_list_sizes(self):
        self.assertEqual(len(model.model['junc_names']),9,"Junctions are not being collected properly.")
        self.assertEqual(len(model.model['valve_names']),0,"Valves are not being collected properly.")
        self.assertEqual(len(model.model['tank_names']),1,"Tanks are not being collected properly.")
        self.assertEqual(len(model.model['reservoir_names']),1,"Reservoirs are not being collected properly.")
        self.assertEqual(len(model.model['G_pipe_name_list']),13,"Pipes are not being collected properly.")
        self.assertEqual(len(model.model['G_list_pumps_only']),1,"Pump pipes are not being collected properly.")
        self.assertEqual(len(model.model['G_list_valves_only']),0,"Pump pipes are not being collected properly.")
if __name__ == '__main__':
    unittest.main()    
    
    
    
    
