import numpy as np
import pandas as pd

class ArAr_Naumenko_Dezes_Test:
    def __init__(self,sample_name = 'TEST',
        Calibration = 'BayesCal'):
        # Gradient of isochron (Naumenko-Dèzes et al. (2018)
        self.grad = 1.878
        # Gradient uncertainty of isochron (Naumenko-Dèzes et al. (2018)
        self.grad_err = 0.012
        # Select calibration (read in from author)
        self.Calibration = Calibration
        # User defined name
        self.sample_name = sample_name

        if self.Calibration == 'BayesCal':
            # Bayesian Decay Calibraiton Values
            self.lam_Ca = 4.9252e-10
            self.lam_Ca_err = 0.0054e-10
            self.lam_Ar = 5.70404e-11
            self.lam_Ar_err = 0.0053e-11
            
        if self.Calibration == 'Renne2011':
            # Bayesian Decay Calibraiton Values
            self.lam_Ca = 4.9548e-10
            self.lam_Ca_err = 0.0134e-10
            self.lam_Ar = 5.757e-11
            self.lam_Ar_err = 0.016e-11
            
        if self.Calibration =='Min2000':
            self.lam_Ca = 4.884e-10
            self.lam_Ca_err = 0.099e-10 / 2
            self.lam_Ar = 0.580e-10
            self.lam_Ar_err = 0.014e-10 /2
            
        if self.Calibration == 'SJ':
            self.lam_Ca = 4.962e-10
            self.lam_Ca_err = (0.05/28.27) * self.lam_Ca
            self.lam_Ar = 0.581e-10
            self.lam_Ar_err = (0.02/3.26) * self.lam_Ar
        


    def Age_Calculation_w_branching_ratio(self):
        """
        KCa age
        t = (1/lam_tot) ln(1 + (1/BCa) * m)
        m - gradient from 40K/44Ca vs. 40Ca/44Ca Isochron
        """
    
        age = []
        branching_ratio = []
        # Monte Carlo
        n = 100000
        for i in range(n):
            lam_Ar_mc = np.random.normal(self.lam_Ar, self.lam_Ar_err)
            lam_Ca_mc = np.random.normal(self.lam_Ca, self.lam_Ca_err)
            m = np.random.normal(self.grad, self.grad_err)
            
            lam_tot = lam_Ar_mc + lam_Ca_mc
            
            B_Ca = lam_Ca_mc/lam_tot
        
            age_mc = (1/lam_tot) * np.log(1 + (1/B_Ca)*m)
            
            age.append(age_mc)
            branching_ratio.append(B_Ca)
            
        return np.array(age), np.array(branching_ratio)
        
        
        
    def Covariances_and_Means(self):
        ages, branching_ratios = self.Age_Calculation_w_branching_ratio()
        
        age_mean = ages.mean(axis = 0)/1e6
        br_mean = branching_ratios.mean(axis = 0)
        
        # Get Ages and Branching ratio for ellipse plot
        means = np.array([br_mean, age_mean])
        
        cov = np.cov(branching_ratios, ages/1e6)
        
        return means, cov
