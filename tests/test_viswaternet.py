#!/usr/bin/env python

"""Tests for `viswaternet` package."""


import unittest

import viswaternet

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
        import os
        import matplotlib.pyplot as plt
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
        
if __name__ == '__main__':
    unittest.main()    
    
    
    
    