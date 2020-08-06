import math
import random
import streamlit as st




class resistance:
    def __init__(self):

        # basic ship parameters
        st.sidebar.header('Basic Ship Parameters')
        self.LOW = st.sidebar.slider('length of water line, LOW',50.0, 500.0, (120.0)) #length of waterline
        #self.LBP = st.sidebar.slider('length between perpendicular',0.0, 500.0, (40.0)) #length between perpendiculars
        self.B = st.sidebar.slider('breadth / breadth moulded, B',5.0, 90.0, (10.0))   #breadth
        self.T = st.sidebar.slider('draught, T',0.0, 50.0, (12.0))   #draught
        self.Vel = st.sidebar.slider('velocity of ship in m/s, V',1.0, 50.0, (20.0))
        self.Lcb = st.sidebar.slider('longitudanal center of buyoncy, Lcb',-10.0,10.0, (5.0))

        self.disp_vol = st.sidebar.slider('volume displacement, Vol_disp',10000.0, 100000.0, (50000.0))


        """
        self.Am = st.sidebar.slider('midship sectional area',0.0, 500.0, (120.0))  #midship section area
        self.Wpa = st.sidebar.slider('water plane area',0.0, 500.0, (120.0)) #water plane area
        """
        
        #some other area parameters
        st.sidebar.header('Some Other Parameters')
        self.Abt = st.sidebar.slider('transverse sectional area of bulb, Abt',1.0, 50.0, (25.0))  #the  transverse   sectional  area  of  the  bulb at  the  position  where  the  still-water surface inter-sects the  stem
        self.At = st.sidebar.slider('transverse area of transum, At',1.0, 50.0, (5.0))   #immersed part of the transverse area of the transom at zero speed
        self.Tf = st.sidebar.slider('draught forward, Tf',1.0, 20.0, (10.0))   # forward draught
        self.Hb = st.sidebar.slider('center of bulb area at FP, Hb',1.0, 20.0, (5.0))   # the  position  of  the   centre  of  transverse area Abt above  the  keel  line 
        
        
        #fluid property
        self.density = 1025
        self.nu = 0.00089

        # coefficients
        st.sidebar.header('Basic Ship Coefficients')
        self.Cb = st.sidebar.slider('block coefficient, Cb',0.0, 1.1, (0.69))
        self.Cm = st.sidebar.slider('coefficient of midship section, Cm',0.0, 1.1, (0.98))
        self.Cw = st.sidebar.slider('waterplane area coefficient, Cw',0.0, 1.1, (0.90))
        self.Cp = self.Cb/self.Cm
        

        # some other parameters
        self.Ks = 1   ## roughness value
        

    def form_factor(self,C_STERN):

        if self.T/self.LOW > 0.05:
            C12 =(self.T/self.LOW)**0.2228446
        elif 0.02 <= self.T/self.LOW <= 0.05:
            C12 = 48.20*(self.T/self.LOW - 0.02)**2.078 + 0.479948
        elif self.T/self.LOW < 0.02:
            C12 = 0.479948

        if C_STERN == "V-SHAPE":
            C13 = 1 + 0.003*(-10)
        elif C_STERN == "N-SHAPE":
            C13 = 1 + 0.003*(0)
        elif C_STERN == "U-SHAPE":
            C13 = 1 + 0.003*(10)
        
        """length of run
        Lr = self.LOW(1 - self.Cp + 0.06*self.Cp*self.Lcb/(4*self.Cp - 1))
        """

        Sapp = self.LOW*(2*self.T + self.B)*math.sqrt(self.Cm)*(0.453 + 0.4425*self.Cb - 0.2862*self.Cm - 0.003467*self.B/self.T + 0.3696*self.Cw) + 2.38*self.Abt/self.Cb 

        
        K1 = C13*(0.93 + C12*((self.B/(self.LOW*(1 - self.Cp + 0.06*self.Cp*self.Lcb/(4*self.Cp - 1))))**0.92497)*((0.95 - self.Cp)**-0.521448)*(1 - self.Cp + 0.0225*self.Lcb)**0.6906)
        
        ren = self.Vel*self.LOW*self.density/self.nu
        cf = 0.075/(math.log10(ren) - 2)**2

        
        return 0.5*self.density*Sapp*self.Vel*self.Vel*cf*K1        #here K1 is actually 1+K1

    """
    def appendage_resist(self, comp):
        
        one_plus_k2_eq = []
        if comp=='rudder_behind_skeg':
            one_plus_k2_eq.append(random.uniform(1.5,2.0))
        if comp=='rudder_behind_stern':
            one_plus_k2_eq.append(random.uniform(1.3,1.5))
        if comp=='twin_screw_balance_rudder':
            one_plus_k2.append(2.8)
        if comp=='shaft_brackets':
            one_plus_k2.append(3.0)
        if comp=='skeg':
            one_plus_k2.append(random.uniform(1.5,2.0))
        if comp=='strut_bossings':
            one_plus_k2.append(3.0)
        if comp=='hull_bossings':
            one_plus_k2.append(2.0)
        if comp=='shafts':
            one_plus_k2.append(random.uniform(2.0,4.0))
        if comp=='stabilizer_fins':
            one_plus_k2.append(2.8)
        if comp=='dome':
            one_plus_k2.append(2.7)
        if comp=='bilge_keels':
            one_plus_k2.append(1.4)
        
        /*
        REYNOLDSs number formula:
        ren = density of fluid x velocity of fluid x length / fluid viscoty
        or
        ren = velocity of fluid x length / v(nu)  where nu = fluid viscosity / density
        */
        ren = self.Vel*self.LOW*self.density/self.nu
        cf = 0.075/(math.log10(ren) - 2)^2

        return 0.5*self.density*(self.Vel)*(self.Vel)*Sapp*one_plus_k2_eq*Cf
    """

    def wave_resist(self):

        if self.B/self.LOW <= 0.11:
            C7 = 0.229577*(self.B/self.LOW)**0.33333
        elif 0.11 <self.B/self.LOW <0.25:
            C7 = self.B/self.LOW
        elif self.B/self.LOW>=0.25:
            C7 = 0.5 - 0.0625*self.LOW/self.B

        Lr = self.LOW*(1 - self.Cp + 0.06*self.Cp*self.Lcb/(4*self.Cp - 1))
        iE = 1 + 89*math.exp( (-(self.LOW/self.B)**0.80856)*((1 - self.Cw)**0.30484)*((1 - self.Cp - 0.0225*self.Lcb)**0.6367)*((Lr/self.B)**0.34574)*(100*self.disp_vol/(self.LOW)**3)**0.16302 )
        
        C1 = 2223105*(C7**(3.78613))*((self.T/self.B)**1.07961)*((90 - iE)**(-1.37565))
        
        C3 = (0.56*(self.Abt)**1.5)/(self.B*self.T*(0.31*math.sqrt(self.Abt) + self.Tf - self.Hb))
        
        C2 = math.exp(-1.89*math.sqrt(C3))
        
        C5 = 1 - 0.8*self.At/(self.B*self.T*self.Cm)
        

        if self.Cp < 0.80:
            c16 = 8.07981*self.Cp - 13.8673*self.Cp*self.Cp + 6.984388*self.Cp*self.Cp*self.Cp
        elif self.Cp >= 0.80:
            c16 = 1.73014 - 0.7067*self.Cp
        
        m1 = (0.0140407*self.LOW/self.T) - ((1.75254*self.disp_vol**0.33)/self.LOW) - (4.79323*self.B/self.LOW) - c16
        

        Fn = self.Vel/(math.sqrt(9.81*self.LOW))
        if (self.Vel**3)/self.disp_vol < 512:
            c15 = -1.69385
        elif (self.Vel**3)/self.disp_vol >1727:
            c15 = 0.0
        else:
            c15 = -1.69385 + (self.LOW/((self.disp_vol)**0.33))/2.36
        m2 = c15*self.Cp*self.Cp*math.exp(-0.1/(Fn*Fn))
        

        d = -0.9

        if self.LOW/self.B <12:
            lamb = 1.446*self.Cp - 0.03*self.LOW/self.B
        elif self.LOW/self.B >=12:
            lamb = 1.446*self.Cp - 0.36


        return C1*C2*C5*self.disp_vol*self.density*9.8*math.exp(m1*((Fn)**d) + m2*math.cos(lamb/(Fn)**2))

    
    
    def bulbous_bow_resist(self):


        Pb = 0.56*math.sqrt(self.Abt)/(self.Tf - 1.5*self.Hb)
        Fni = self.Vel/math.sqrt(9.81*(self.Tf - self.Hb - 0.25*math.sqrt(self.Abt) + 0.15*self.Vel*self.Vel))
        
        return 0.11*math.exp(-3/(Pb)**2)*(Fni**3)*(self.Abt**1.5)*self.density*9.81/(1 +Fni**2)

    
    
    def transom_pressure_resist(self):
        Fnt = (self.Vel)/(math.sqrt((2*9.81*self.At)/(self.B + self.B*self.Cw)))
        if Fnt < 5:
            c6 = 0.2*(1-0.2*Fnt)
        else :
            c6 = 0
        return 0.5*self.density*((self.Vel)**2)*(self.At)*c6
    
    
    
    
    def correlation_resist(self):
        if self.Tf/self.LOW <= 0.04:
            c4 = self.Tf/self.LOW
        else :
            c4 = 0.04

        C3 = (0.56*(self.Abt)**1.5)/(self.B*self.T*(0.31*math.sqrt(self.Abt) + self.Tf - self.Hb))
        C2 = math.exp(-1.89*math.sqrt(C3))
        
        if self.Ks < 150:
            Ca = 0.006*((self.LOW+100)**(-0.16)) - 0.00205 + 0.0003*(math.sqrt(self.LOW/7.5))*(self.Cb**4)*C2*(0.04-c4)

        else :
            Ca = 0.006*((self.LOW+100)**(-0.16)) - 0.00205 + 0.0003*(math.sqrt(self.LOW/7.5))*(self.Cb**4)*C2*(0.04-c4) + (0.105*((self.Ks)**0.33) - 0.005579)/self.LOW**0.33

        
        
        return 0.5*self.density*((self.Vel)**2)*Ca

    

app = resistance()

st.title("Resistance Calculation Using Holtrop & Mennen Method")

# Frictional Resistance 
st.header('Frictional Resistance, Rf')
st.write('Rf :',app.form_factor("U-SHAPE")/1000, 'KN')

# Wave Resistance
st.header('Wave Resistance, Rw')
st.write('Rw :', app.wave_resist()/1000, 'KN')

# Bulbous Bow Resistance
st.header('Bulbous Bow Resistance, Rb')
st.write('Rb :', app.bulbous_bow_resist()/1000, 'KN')

# Transom Pressure Resistance
st.header('Transom Pressure Resistance, Rtr')
st.write('Rtr :', app.transom_pressure_resist()/1000, 'KN')

# Model Ship Correlation Resistance
st.header('Model Ship Correlation Resistance, Ra')
st.write('Ra :', app.correlation_resist()/1000, 'KN')

total_resist = app.form_factor("U-SHAPE") + app.wave_resist() + app.bulbous_bow_resist() + app.transom_pressure_resist() + app.correlation_resist()
st.subheader('Total Resistance :')
total_resist/1000, 'KN'